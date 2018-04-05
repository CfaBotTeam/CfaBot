import numpy as np
from Bot.Resolver import DefinitionKeywordResolverBase


class DefinitionKeywordResolver(DefinitionKeywordResolverBase):
    def __init__(self, glossary, scorer):
        self.glossary_ = glossary
        self.scorer_ = scorer

    def get_choices(self, problem):
        keys = ['choice_A', 'choice_B', 'choice_C', 'choice_D']
        return [problem[key] for key in keys if key in problem and problem[key] is not np.NaN]