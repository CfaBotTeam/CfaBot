from Bot.Classification.Filters import FilterFactoryBase
from Bot.Classification.Features import GlossaryFeatures
from Bot.Classification.Features import LengthFeatures
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import VerbFeatures
from Bot.Classification.Features import SubjectFeatures


class DefKeywordFilterFactoryBase(FilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[VerbFeatures.HAS_DEF_VERB]
        filters &= df[VerbFeatures.CENTRALITY] > 0.6
        filters &= df[LengthFeatures.Q_CH_LEN_RATIO] < 27.0
        filters &= ~df[NlpFeatures.HAS_NUMBER]
        filters &= ~df[NlpFeatures.HAS_NER]
        return filters


class DefKeywordFilterFactory(DefKeywordFilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[GlossaryFeatures.ANY_CH_IN_GLOSS]
        return filters


class DefKeywordStartEndFilterFactory(DefKeywordFilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[SubjectFeatures.CHOICE_Q_SUB_IN_GLOSS]
        return filters
