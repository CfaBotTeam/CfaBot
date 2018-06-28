import numpy as np
from random import randint
from Bot.Utils import get_enum_name
from Bot.Classification import ProblemCategory


class DefinitionsComparison:
    def __init__(self, question_keyword, question_gloss_keyword, question_definitions, choices, choices_keywords_defs):
        self.question_keyword_ = question_keyword
        self.question_gloss_keyword_ = question_gloss_keyword
        self.question_definitions_ = question_definitions
        self.choices_ = choices
        self.choices_keywords_defs_ = choices_keywords_defs

    def has_question_definitions(self):
        return self.question_definitions_ is not None


class ChoiceDefinitions:
    def __init__(self, choice_keyword, choice_gloss_keyword, choice_definitions):
        self.keyword_ = choice_keyword
        self.gloss_keyword_ = choice_gloss_keyword
        self.definitions_ = choice_definitions


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
        for q_def, q_source in comparison.question_definitions_:
            c_comparisons = []
            q_comparisons = {'q_keyword': comparison.question_keyword_,
                             'q_gloss_keyword': comparison.question_gloss_keyword_,
                             'q_def': q_def,
                             'source': q_source,
                             'c_comparisons': c_comparisons}
            comparisons.append(q_comparisons)
            for i_choice, choice in enumerate(comparison.choices_):
                choice_definitions = comparison.choices_keywords_defs_[i_choice]
                if choice_definitions is None:
                    continue
                c_def_comparisons = []
                c_comparisons.append(c_def_comparisons)
                if choice_definitions.definitions_ is None:
                    continue
                for c_def, c_source in choice_definitions.definitions_:
                    score = self.scorer_.score(c_def, q_def)
                    c_def_comparisons.append({'c_keyword': choice_definitions.keyword_,
                                              'c_gloss_keyword': choice_definitions.gloss_keyword_,
                                              'c_def': c_def,
                                              'source': c_source,
                                              'score': score})
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
