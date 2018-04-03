from Bot.Classification.Features import GlossaryFeatures
from Bot.Classification.Features import LengthFeatures
from Bot.Classification.Features import NlpFeatures


class DefKeywordFilerFactory:
    def get_filters(self, df):
        return df['category'] == self.category_

    def get_filters(self, df):
        filters = ~df['question'].str.contains(', CFA,')
        filters &= (df['question'].str.contains('described as') |
                    df['question'].str.contains('defined as'))
        filters &= df[LengthFeatures.Q_CH_LEN_RATIO] < 12.0
        filters &= df[GlossaryFeatures.ANY_CH_IN_GLOSS]
        filters &= ~df[NlpFeatures.HAS_DIGIT]
        filters &= ~df[NlpFeatures.HAS_PERSON]
        return filters
