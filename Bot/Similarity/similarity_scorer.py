import numpy as np
import os.path
import Embeddings.data


class SimilarityMode:
    NORMAL = 'normal'
    WEIGHTED = 'weighted'


class SimilarityScorer:
    def __init__(self, nlp, mode):
        self.nlp_ = nlp
        self.mode_ = mode
        if mode == SimilarityMode.WEIGHTED:
            self.vector_weights_ = self.get_vector_weights()

    def get_vector_weights(self):
        data_dir = os.path.dirname(Embeddings.data.__file__)
        words_count = {}
        with open(os.path.join(data_dir, 'words_count.tsv'), 'r') as f:
            for line in f:
                splitted = line.split('\t')
                words_count[splitted[0]] = float(splitted[1])
        vector_weights = {}
        for word, count in words_count.items():
            vector_weights[word] = 1 / count
        return vector_weights

    def get_token_vector(self, token):
        word = str(token).lower()
        weight = self.vector_weights_[word] if self.mode_ == SimilarityMode.WEIGHTED else 1.0
        return weight * token.vector

    def compute_vector(self, doc):
        if self.mode_ == SimilarityMode.WEIGHTED:
            tokens = list(filter(lambda token: str(token).lower() in self.vector_weights_, doc))
        else:
            tokens = list(doc)
        tokens_length = len(tokens)
        if tokens_length == 0:
            return [0.0] * doc.vocab.vectors_length
        result = np.zeros((doc.vocab.vectors_length,), dtype='f')
        for token in tokens:
            result += self.get_token_vector(token)
        return result / tokens_length

    def score(self, span1, span2):
        doc1 = self.nlp_(span1)
        doc2 = self.nlp_(span2)

        # doc1.user_hooks['vector'] = self.compute_vector
        # doc2.user_hooks['vector'] = self.compute_vector

        return doc1.similarity(doc2)

    # def score(self, span1, span2):
    #     doc1 = self.nlp_(span1)
    #     doc2 = self.nlp_(span2)
    #
    #     doc1.user_hooks['vector'] = self.compute_vector
    #     doc2.user_hooks['vector'] = self.compute_vector
    #
    #     score = 0.0
    #     # nb_scores = 0
    #     for token1 in doc1:
    #         interaction_scores = []
    #         max_interaction_score = 0.0
    #         for token2 in doc2:
    #             try:
    #                 interaction_score = token1.similarity(token2)
    #                 interaction_scores.append(interaction_score)
    #             except:
    #                 continue
    #         for max in sorted(interaction_scores, reverse=True)[:2]:
    #             score += max
    #         # nb_scores += 1
    #
    #     return score / (len(doc1) * 2)

    def score_tokens(self, token1, token2):
        # word1 = str(token1).lower()
        # word2 = str(token2).lower()
        # doc1 = self.nlp_(word1)
        # doc2 = self.nlp_(word2)
        #
        # doc1.user_hooks['vector'] = self.compute_vector
        # doc2.user_hooks['vector'] = self.compute_vector
        #
        return token1.similarity(token2)
        # word1 = str(token1).lower()
        # weight = self.vector_weights_[word] if self.mode_ == SimilarityMode.WEIGHTED else 1.0
