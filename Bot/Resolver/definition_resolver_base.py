import numpy as np
from random import randint
from Bot.Utils import get_enum_name
from Bot.Classification import ProblemCategory


class DefinitionsComparison:
    def __init__(self, question_keyword, question_definitions, choices, choices_keywords, choices_definitions):
        self.question_keyword_ = question_keyword
        self.question_definitions_ = question_definitions
        self.choices_ = choices
        self.choices_keywords_ = choices_keywords
        self.choices_definitions_ = choices_definitions

    def has_question_definitions(self):
        return self.question_definitions_ is not None


class DefinitionResolverBase:
    def __init__(self, def_provider, scorer):
        self.def_provider_ = def_provider
        self.scorer_ = scorer

    def random_choice(self, problem):
        max = 2
        if 'choice_D' in problem:
            max = 3
        return randint(0, max)

    def add_result_info(self, problem, choices, max_index, comparison_results, predicted_answer, debug):
        filename = problem['filename']
        nb = problem['question_nb']
        debug[filename + '_' + nb] = {
            'question': problem['question'],
            'real_answer': problem['answer'],
            'random_answer': max_index == -1,
            'predicted_answer': predicted_answer,
            'choices': choices,
            'comparisons': comparison_results,
            'category': get_enum_name(ProblemCategory, problem['category']),
        }

    def get_choices(self, problem):
        keys = ['choice_A', 'choice_B', 'choice_C', 'choice_D']
        return [problem[key] for key in keys if key in problem and problem[key] is not np.NaN]

    def get_comparison(self, problem, choices):
        raise NotImplementedError("This method need to be overloaded")

    def get_result_from_index(self, problem, max_index):
        if max_index == -1:
            max_index = self.random_choice(problem)
        return chr(max_index + ord('A'))

    def perform_comparison(self, comparison, comparisons):
        max_score = 0
        max_index = -1
        c_comparisons = []
        for q_def, q_source in comparison.question_definitions_:
            q_comparisons = {'q_keyword': comparison.question_keyword_, 'q_def': q_def, 'source': q_source, 'c_comparisons': c_comparisons}
            comparisons.append(q_comparisons)
            for i_choice, choice in enumerate(comparison.choices_):
                c_keyword = comparison.choices_keywords_[i_choice]
                definitions = comparison.choices_definitions_[i_choice]
                if definitions is None:
                    continue
                c_def_comparisons = []
                c_comparisons.append(c_def_comparisons)
                for c_def, c_source in definitions:
                    score = self.scorer_.score(c_def, q_def)
                    c_def_comparisons.append({'c_keyword': c_keyword, 'c_def': c_def, 'source': c_source, 'score': score})
                    if score > max_score:
                        max_score = score
                        max_index = i_choice
        return max_score, max_index

    def find_prediction(self, problem, results):
        comparison_results = []
        choices = self.get_choices(problem)
        comparison = self.get_comparison(problem, choices)
        max_index = -1
        if comparison.has_question_definitions():
            max_score, max_index = self.perform_comparison(comparison, comparison_results)
        predicted_answer = self.get_result_from_index(problem, max_index)
        self.add_result_info(problem, choices, max_index, comparison_results, predicted_answer, results)
        return predicted_answer

    def resolve(self, problems, debug):
        return problems.apply(lambda x: self.find_prediction(x, debug), axis=1)
