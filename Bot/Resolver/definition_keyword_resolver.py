import numpy as np
from random import randint
from Bot.Utils import get_enum_name
from Bot.Classification import ProblemCategory


class DefinitionKeywordResolver:
    def __init__(self, glossary, scorer):
        self.glossary_ = glossary
        self.scorer_ = scorer

    def random_choice(self, problem):
        max = 2
        if 'choice_D' in problem:
            max = 3
        return randint(0, max)

    def add_debug_info(self, problem, max_index, choices_results, debug):
        filename = problem['filename']
        nb = problem['question_nb']
        debug[filename + '_' + nb] = {
            'question': problem['question'],
            'answer': problem['answer'],
            'max_index': max_index,
            'choices_results': choices_results,
            'category': get_enum_name(ProblemCategory, problem['category'])
        }

    def find_prediction(self, problem, debug):
        max_score = 0
        max_index = -1
        question = problem['question']
        choices_results = []
        for i_choice, choice_key in enumerate(['choice_A', 'choice_B', 'choice_C', 'choice_D']):
            choice = problem[choice_key]
            if choice is np.NaN:
                continue
            scores = {}
            choice_scores = {'choice': choice, 'scores': scores}
            choices_results.append(choice_scores)
            definitions = self.glossary_.get_definitions(choice)
            if definitions is None:
                continue
            for definition in definitions:
                score = self.scorer_.score(definition, question)
                scores[definition] = score
                if score > max_score:
                    max_score = score
                    max_index = i_choice

        self.add_debug_info(problem, max_index, choices_results, debug)

        if max_index == -1:
            max_index = self.random_choice(problem)
        res = chr(max_index + 65)

        return res

    def resolve(self, problems):
        debug = {}
        if len(problems) > 0:
            problems['prediction'] = problems.apply(lambda x: self.find_prediction(x, debug), axis=1)
        return debug
