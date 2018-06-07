from Bot.Classification.Features import SubjectFeatures
from Bot.Resolver import DefinitionResolverBase
from Bot.Resolver import DefinitionSource


class DefinitionKeywordResolverBase(DefinitionResolverBase):
    def get_question_definitions(self, problem):
        return [[problem['question'], DefinitionSource.QUESTION]]


class DefinitionKeywordResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [self.def_provider_.get_definitions(choice, loosly=False) for choice in choices]


class DefinitionKeywordStartEndResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        choices = problem[SubjectFeatures.CHOICE_Q_TERMS]
        return [self.def_provider_.get_definitions(choice, loosly=False) for choice in choices]
