import numpy as np
from Bot.Classification.Features import SubjectFeatures
from Bot.Resolver import DefinitionResolverBase


class DefinitionKeywordResolverBase(DefinitionResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [self.glossary_.get_definitions(choice) for choice in choices]

    def get_question_definition(self, problem):
        return problem['question']


class DefinitionKeywordResolver(DefinitionKeywordResolverBase):
    def get_choices(self, problem):
        keys = ['choice_A', 'choice_B', 'choice_C', 'choice_D']
        return [problem[key] for key in keys if key in problem and problem[key] is not np.NaN]


class DefinitionKeywordStartEndResolver(DefinitionKeywordResolverBase):
    def get_choices(self, problem):
        return problem[SubjectFeatures.CHOICE_Q_TERMS]
