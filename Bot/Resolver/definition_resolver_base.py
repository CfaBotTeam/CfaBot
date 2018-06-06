from random import randint
from Bot.Utils import get_enum_name
from Bot.Classification import ProblemCategory


class DefinitionResolverBase:
    WITH_COMPARISON = False

    def __init__(self, def_provider, scorer):
        self.def_provider_ = def_provider
        self.scorer_ = scorer

    def random_choice(self, problem):
        max = 2
        if 'choice_D' in problem:
            max = 3
        return randint(0, max)

    def add_result_info(self, problem, max_index, choices_results, predicted_answer, debug):
        filename = problem['filename']
        nb = problem['question_nb']
        debug[filename + '_' + nb] = {
            'question': problem['question'],
            'real_answer': problem['answer'],
            'random_answer': max_index == -1,
            'predicted_answer': predicted_answer,
            'choices_results': choices_results,
            'category': get_enum_name(ProblemCategory, problem['category']),
        }

    def get_choices(self, problem):
        raise NotImplementedError("This method need to be overloaded")

    def get_choices_definitions(self, problem, choices):
        raise NotImplementedError("This method need to be overloaded")

    def get_question_definition(self, problem):
        raise NotImplementedError("This method need to be overloaded")

    def get_result_from_index(self, problem, max_index):
        if max_index == -1:
            max_index = self.random_choice(problem)
        return chr(max_index + ord('A'))

    def find_prediction(self, problem, results):
        max_score = 0
        max_index = -1
        choices_results = []
        question_to_compare = self.get_question_definition(problem)
        choices = self.get_choices(problem)
        choices_definitions = self.get_choices_definitions(problem, choices)
        for i_choice, choice in enumerate(choices):
            scores = {}
            comparisons = []
            choice_scores = {'choice': choice, 'scores': scores}
            if self.WITH_COMPARISON:
                choice_scores['comparisons'] = comparisons
            choices_results.append(choice_scores)
            definitions = choices_definitions[i_choice]
            if definitions is None:
                continue
            for definition in definitions:
                score = self.scorer_.score(definition, question_to_compare)
                comparisons.append((definition, question_to_compare))
                scores[definition] = score
                if score > max_score:
                    max_score = score
                    max_index = i_choice
        predicted_answer = self.get_result_from_index(problem, max_index)
        self.add_result_info(problem, max_index, choices_results, predicted_answer, results)
        return predicted_answer

    def resolve(self, problems, debug):
        return problems.apply(lambda x: self.find_prediction(x, debug), axis=1)
