from Bot.Classification.Features import GlossaryFeatures
from Bot.Classification.Features import LengthFeatures
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import VerbFeatures


class DefKeywordFilterFactory:
    def get_filters(self, df):
        filters = df[VerbFeatures.HAS_DEF_VERB]
        filters &= df[VerbFeatures.CENTRALITY] > 0.6
        filters &= df[LengthFeatures.Q_CH_LEN_RATIO] < 27.0
        filters &= df[GlossaryFeatures.ANY_CH_IN_GLOSS]
        filters &= ~df[NlpFeatures.HAS_NUMBER]
        filters &= ~df[NlpFeatures.HAS_NER]
        return filters
