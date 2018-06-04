import json
import spacy
from os import listdir
from os.path import isfile, join, dirname, basename
import Embeddings.models
from Embeddings.vizualiser.dto import Problem
from Embeddings.vizualiser.dto import ComparedToken
from Embeddings.vizualiser.dto import Comparison


class SimiliarityVizualiser:
    def __init__(self, results_directory):
        self.nlp_models_ = {}
        self.results_directory_ = results_directory

    def load_category(self, model, category, result):
        for question_id, problem in result[category].items():
            if not question_id in self.all_problems_:
                self.all_problems_[question_id] = Problem(question_id, model, category, problem)
            else:
                self.all_problems_[question_id].add_model(model, problem)

    def load_all_problems(self):
        categories = set()
        for f in listdir(self.results_directory_):
            full_path = join(self.results_directory_, f)
            if not isfile(full_path):
                continue
            result = json.load(open(full_path, 'r'))
            model = result['model']
            self.all_models_.append(model)
            for key in result:
                if key == 'overall' or key == 'model':
                    continue
                if not key in categories:
                    categories.add(key)
                self.load_category(model, key, result)
        return categories

    def load(self):
        self.all_problems_ = {}
        self.all_models_ = []
        self.all_categories_ = []
        categories = self.load_all_problems()
        for category in categories:
            self.all_categories_.append(category)
        self.all_models_.sort(key=len)
        self.all_categories_.sort()
        return self.all_models_, self.all_categories_

    def select_problems(self, model, category):
        selected_problems = []
        for problem in self.all_problems_.values():
            if problem.has_model(model) and problem.category_ == category:
                selected_problems.append(problem)
        return selected_problems

    def get_problem_by_id(self, id):
        if id in self.all_problems_:
            return self.all_problems_[id]
        return None

    def get_nlp(self, model_name):
        if model_name != 'en' and model_name != 'en_core_web_lg':
            model_name = join(dirname(Embeddings.models.__file__), basename(model_name))
        if model_name not in self.nlp_models_:
            self.nlp_models_[model_name] = spacy.load(model_name, disable=['tagger', 'parser', 'ner', 'textcat'])
        return self.nlp_models_[model_name]

    def get_similarity(self, token1, token2):
        try:
            return token1.similarity(token2)
        except:
            return 0.0

    def get_sentence_compared_tokens(self, sentence1_nlp, sentence2_nlp):
        sentence_compared_tokens = []
        for token1 in sentence1_nlp:
            token1_scores = []
            for token2 in sentence2_nlp:
                token1_scores.append(self.get_similarity(token1, token2))
            sentence_compared_tokens.append(ComparedToken(token1, token1_scores))
        return sentence_compared_tokens

    def get_comparison(self, problem_id, choice_index, comparison_index, model):
        problem = self.get_problem_by_id(problem_id)
        nlp = self.get_nlp(model)
        comparisons = problem.get_comparisons(model)
        if choice_index > len(comparisons) - 1 or comparison_index > len(comparisons[choice_index]) - 1:
            return Comparison([], [])
        sentences = comparisons[choice_index][comparison_index]
        sentence1_nlp = nlp(sentences[0])
        sentence2_nlp = nlp(sentences[1])
        sentence1_compared_tokens = self.get_sentence_compared_tokens(sentence1_nlp, sentence2_nlp)
        sentence2_compared_tokens = self.get_sentence_compared_tokens(sentence2_nlp, sentence1_nlp)
        return Comparison(sentence1_compared_tokens, sentence2_compared_tokens)
