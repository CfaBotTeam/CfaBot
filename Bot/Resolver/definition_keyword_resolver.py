from Bot.Classification.Features import SubjectFeatures
from Bot.Resolver import DefinitionResolverBase
from Bot.Resolver import DefinitionSource
from Bot.Resolver import DefinitionsComparison


class DefinitionKeywordResolverBase(DefinitionResolverBase):
    def get_comparison(self, problem, choices):
        q_defs = [[problem['question'], DefinitionSource.QUESTION]]
        choices_definitions = self.get_choices_definitions(problem, choices)
        return DefinitionsComparison(q_defs, choices, choices_definitions)

    def get_choices_definitions(self, problem, choices):
        raise NotImplementedError("This method need to be overloaded")


class DefinitionKeywordResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [self.def_provider_.get_definitions(choice, loosly=False) for choice in choices]


class DefinitionKeywordStartEndResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        choices = problem[SubjectFeatures.CHOICE_Q_TERMS]
        return [self.def_provider_.get_definitions(choice, loosly=False) for choice in choices]
