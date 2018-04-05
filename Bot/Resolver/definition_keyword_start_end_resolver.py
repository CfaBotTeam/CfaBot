from Bot.Resolver import DefinitionKeywordResolverBase
from Bot.Classification.Features import SubjectFeatures


class DefinitionKeywordStartEndResolver(DefinitionKeywordResolverBase):
    def __init__(self, glossary, scorer):
        self.glossary_ = glossary
        self.scorer_ = scorer

    def get_choices(self, problem):
        return problem[SubjectFeatures.CHOICE_Q_TERMS]
