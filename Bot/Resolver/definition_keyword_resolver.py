from Bot.Classification.Features import SubjectFeatures
from Bot.Resolver import DefinitionResolverBase
from Bot.Resolver import DefinitionSource
from Bot.Resolver import DefinitionsComparison
from Bot.Resolver import ChoiceDefinitions


class DefinitionKeywordResolverBase(DefinitionResolverBase):
    def get_comparison(self, problem, choices):
        q_defs = [[problem['question'], DefinitionSource.QUESTION]]
        choices_keyword_defs = self.get_choices_definitions(problem, choices)
        return DefinitionsComparison('', '', q_defs, choices, choices_keyword_defs)

    def get_choices_definitions(self, problem, choices):
        raise NotImplementedError("This method need to be overloaded")


class DefinitionKeywordResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        result = []
        for choice in choices:
            gloss_keyword, gloss_defs = self.def_provider_.get_definitions(choice, loosly=False)
            result.append(ChoiceDefinitions(choice, gloss_keyword, gloss_defs))
        return result


class DefinitionKeywordStartEndResolver(DefinitionKeywordResolverBase):
    def get_choices_definitions(self, problem, choices):
        result = []
        for choice in problem[SubjectFeatures.CHOICE_Q_TERMS]:
            gloss_keyword, gloss_defs = self.def_provider_.get_definitions(choice, loosly=False)
            result.append(ChoiceDefinitions(choice, gloss_keyword, gloss_defs))
        return result
