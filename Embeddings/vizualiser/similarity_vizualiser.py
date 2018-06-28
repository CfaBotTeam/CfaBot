import json
import os
import os.path
import Embeddings.models
from Embeddings.vizualiser.dto import Problem
from Embeddings.vizualiser.dto import ComparedToken
from Embeddings.vizualiser.dto import NlpComparison
from Bot.Classification import ProblemsClassifier
from Bot.Classification import ProblemCategory
from Bot.Utils import get_enum_name
from Bot.Load import SpacyLoader
from Bot.Similarity import SimilarityScorer


class SimiliarityVizualiser:
    def __init__(self, results_directory):
        self.nlp_models_ = {}
        self.results_directory_ = results_directory
        self.spacy_loader_ = SpacyLoader()

    def load_category(self, fullname, model, category, result, dataset, provider, similarity_mode, glossary):
        for question_id, problem in result[category].items():
            if not question_id in self.all_problems_:
                self.all_problems_[question_id] = Problem(question_id, fullname, model, category, problem, dataset, provider, similarity_mode, glossary)
            else:
                self.all_problems_[question_id].add_file(fullname, model, problem, dataset, provider, similarity_mode, glossary)

    def load_all_problems(self):
        file_categories = set()
        for filename in os.listdir(self.results_directory_):
            full_path = os.path.join(self.results_directory_, filename)
            if not os.path.isfile(full_path) or not full_path.endswith('.json'):
                continue
            result = json.load(open(full_path, 'r'))
            model = os.path.basename(result['model'])
            dataset = result['dataset']
            glossary = os.path.basename(result['glossary'])
            provider_mode = result['provider_mode']
            similarity_mode = result['similarity_mode']
            file_without_ext = os.path.splitext(filename)[0]
            # fullname = "%s-%s-%s" % (file_without_ext, model, provider_mode)
            self.all_files_.append(file_without_ext)
            categories = set(map(lambda x: get_enum_name(ProblemCategory, x), ProblemsClassifier.HANDLED_CATEGORIES))
            for key in result:
                if not key in categories:
                    continue
                if not key in file_categories:
                    file_categories.add(key)
                self.load_category(file_without_ext, model, key, result, dataset, provider_mode, similarity_mode, glossary)
        return file_categories

    def load(self):
        self.all_problems_ = {}
        self.all_files_ = []
        self.all_categories_ = []
        categories = self.load_all_problems()
        for category in categories:
            self.all_categories_.append(category)
        self.all_files_.sort(key=len)
        self.all_categories_.sort()
        return self.all_files_, self.all_categories_

    def select_problems(self, filename, category):
        selected_problems = []
        for problem in self.all_problems_.values():
            if problem.has_file(filename) and problem.category_ == category:
                selected_problems.append(problem)
        return selected_problems

    def get_problem_by_id(self, id):
        if id in self.all_problems_:
            return self.all_problems_[id]
        return None

    def get_nlp(self, model_name, similarity_mode):
        if model_name != 'en' and model_name != 'en_core_web_lg':
            model_name = os.path.join(os.path.dirname(Embeddings.models.__file__), os.path.basename(model_name))
        if model_name not in self.nlp_models_:
            nlp = self.spacy_loader_.load_nlp(model_name, disable=['tagger', 'parser', 'ner', 'textcat'])
            self.nlp_models_[model_name] = [nlp, SimilarityScorer(nlp, similarity_mode)]
        return self.nlp_models_[model_name]

    def get_similarity(self, token1, token2, scorer):
        try:
            return token1.similarity(token2)
            # return scorer.score_tokens(token1, token2)
        except Exception as e:
            return 0.0

    def get_sentence_compared_tokens(self, sentence1_nlp, sentence2_nlp, scorer):
        sentence_compared_tokens = []
        for token1 in sentence1_nlp:
            token1_scores = []
            for token2 in sentence2_nlp:
                token1_scores.append(self.get_similarity(token1, token2, scorer))
            sentence_compared_tokens.append(ComparedToken(token1, token1_scores))
        return sentence_compared_tokens

    def get_comparison(self, problem_id, filename, choice_index, q_option_index, c_option_index):
        problem = self.get_problem_by_id(problem_id)
        comparisons = problem.get_comparisons(filename)
        if q_option_index > len(comparisons) - 1 or \
           choice_index > len(comparisons[q_option_index]) - 1 or \
           c_option_index > len(comparisons[q_option_index][choice_index]) - 1:
            return None
        return comparisons[q_option_index][choice_index][c_option_index]

    def get_nlp_comparison(self, comparison, model, similarity_mode):
        nlp, scorer = self.get_nlp(model, similarity_mode)
        if comparison is None:
            return NlpComparison([], [])
        q_sentence_nlp = nlp(comparison.q_definition_)
        c_sentence_nlp = nlp(comparison.c_definition_)
        q_sentence_compared_tokens = self.get_sentence_compared_tokens(q_sentence_nlp, c_sentence_nlp, scorer)
        c_sentence_compared_tokens = self.get_sentence_compared_tokens(c_sentence_nlp, q_sentence_nlp, scorer)
        return NlpComparison(q_sentence_compared_tokens, c_sentence_compared_tokens)
