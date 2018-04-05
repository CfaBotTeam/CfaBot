from Bot.Classification import ProblemCategory
from Bot.Resolver import DefinitionKeywordResolver
from Bot.Resolver import DefinitionKeywordStartEndResolver
from Bot.Similarity import SimilarityScorer


class ResolverFactory:
    def __init__(self, glossary, nlp):
        self.glossary_ = glossary
        self.sim_scorer_ = SimilarityScorer(nlp)

    def get_resolver(self, category):
        if category == ProblemCategory.DEF_KEYWORD:
            return DefinitionKeywordResolver(self.glossary_, self.sim_scorer_)
        if category == ProblemCategory.DEF_KEYWORD_START_END:
            return DefinitionKeywordStartEndResolver(self.glossary_, self.sim_scorer_)
        return None
