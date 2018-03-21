from random import randint


class DefinitionKeywordResolver:
    def __init__(self, glossary, scorer):
        self.glossary_ = glossary
        self.scorer_ = scorer

    def random_choice(self, problem):
        max = 2
        if 'choice_D' in problem:
            max = 3
        return randint(0, max)

    def find_prediction(self, problem):
        nb_keywords = 0
        max_score = 0
        max_index = -1
        question = problem['question']
        for i_choice, choice_key in enumerate(['choice_A', 'choice_B', 'choice_C', 'choice_D']):
            choice = problem[choice_key]
            if not self.glossary_.has_keyword(choice):
                if (choice_key == 'choice_A' and problem["choice_A_in_glossary"]) or \
                   (choice_key == 'choice_B' and problem["choice_B_in_glossary"]) or \
                   (choice_key == 'choice_C' and problem["choice_C_in_glossary"]) or \
                   (choice_key == 'choice_D' and problem["choice_D_in_glossary"]):
                    continue
                continue
            print('keyword in glossary')
            definitions = self.glossary_.get_definitions(choice)
            for definition in definitions:
                score = self.scorer_.score(definition, question)
                if score > max_score:
                    max_score = score
                    max_index = i_choice
        if max_index == -1:
            max_index = self.random_choice(problem)

        return chr(max_index + 65)

    def resolve(self, problems):
        problems['prediction'] = problems.apply(self.find_prediction, axis=1)
