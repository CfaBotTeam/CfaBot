# Author: Robert Guthrie

import torch
import torch.autograd as autograd
import torch.nn.functional as F
import numpy as np
from drqa.pipeline import tokenize_text
from multiprocessing import Pool


class ChoiceSelector:
    def __init__(self, word_dict, embedding, processes=None):
        self.word_dict_ = word_dict
        self.embedding_ = embedding
        self.processes_ = processes if processes is not None else Pool(processes=4)

    def tokenize(self, texts):
        result = self.processes_.map_async(tokenize_text, texts)
        return [res.words() for res in result.get()]

    def get_phrase_embedding(self, tokens):
        lookups = [self.word_dict_[w] for w in tokens]
        lookup_tensor = torch.LongTensor(lookups)
        return self.embedding_(autograd.Variable(lookup_tensor))

    def compute_similarity(self, span_emb, choice_emb):
        span_word_similarities = []
        for span_word_emb in span_emb:
            span_word_emb = span_word_emb.view(1, -1)
            min_span_choice_sim = float("inf")
            for choice_word_emb in choice_emb:
                choice_word_emb = choice_word_emb.view(1, -1)
                sim_tensor = F.cosine_similarity(span_word_emb, choice_word_emb)
                sim = sim_tensor.data[0]
                if sim < min_span_choice_sim:
                    min_span_choice_sim = sim
            span_word_similarities.append(min_span_choice_sim)
        return np.mean(span_word_similarities)

    def select_most_similar(self, spans, choices):
        spans_tokens = self.tokenize(spans)
        choices_tokens = self.tokenize(choices)
        span_embeddings = []
        choice_embeddings = []
        for i, span_tokens in enumerate(spans_tokens):
            span_emb = self.get_phrase_embedding(span_tokens)
            span_embeddings.append((span_emb, spans[i]))

        for i, choice_tokens in enumerate(choices_tokens):
            choice_emb = self.get_phrase_embedding(choice_tokens)
            choice_embeddings.append((choice_emb, choices[i]))

        results = []
        for (span_emb, span) in span_embeddings:
            for (choice_emb, choice) in choice_embeddings:
                similarity = self.compute_similarity(span_emb, choice_emb)
                results.append({'span': span, 'choice': choice, 'similarity': similarity})

        results.sort(key=lambda res: res['similarity'])
        return results[:3]
