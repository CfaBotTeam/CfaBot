from Bot.Classification.Filters import FilterFactoryBase
from Bot.Classification.Features import LengthFeatures
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import VerbFeatures
from Bot.Classification.Features import SubjectFeatures


class KeywordDefFilterFactoryBase(FilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[VerbFeatures.HAS_DEF_VERB]
        filters &= ~df[NlpFeatures.HAS_NUMBER]
        filters &= ~df[NlpFeatures.HAS_NER]
        filters &= df[SubjectFeatures.Q_SUB_IN_GLOSS]
        return filters


class KeywordDefFilterFactory(KeywordDefFilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[LengthFeatures.Q_CH_LEN_RATIO] < 2
        return filters


class KeywordDefStartEndFilterFactory(KeywordDefFilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df[VerbFeatures.CENTRALITY] < 0.6
        return filters
