from Bot.Classification import ProblemCategory
from Bot.Features import LengthFeaturesFactory
from Bot.Features import GlossaryFeaturesFactory


class ProblemsClassifier:
    def __init__(self, glossary):
        self.glossary_ = glossary
        self.problems_ = None
        self.feature_factories_ = [LengthFeaturesFactory(), GlossaryFeaturesFactory(glossary)]
        self.filters_ = {ProblemCategory.DEF_KEYWORD: self.get_def_keyword_filters}

    def add_features(self, df):
        for factory in self.feature_factories_:
            factory.add_features(df)

    def get_default_filters(self, df):
        filters = ~df['question'].str.contains(', CFA,')
        filters &= df['question_choice_len_ratio'] < 12.0
        filters &= df['any_choice_in_glossary'] == True
        return filters

    def get_def_keyword_filters(self, df):
        filters = ~df['question'].str.contains(', CFA,')
        filters &= df['question_choice_len_ratio'] < 12.0
        filters &= df['any_choice_in_glossary'] == True
        sub_filter = df['question'].str.contains('described as')
        sub_filter |= df['question'].str.contains('defined as')
        filters &= sub_filter
        return filters

    def extract_category(self, df, filters_factory=None):
        if filters_factory is None:
            filters_factory = self.get_default_filters
        return df[filters_factory(df)]

    def fit(self, df):
        self.problems_ = df
        self.add_features(df)
        df['category'] = ProblemCategory.OTHER
        categories = [ProblemCategory.DEF_KEYWORD]
        for category in categories:
            filters = self.filters_[category]
            df.loc[filters, 'category'] = category

    def get_category(self, category):
        return self.problems_[self.problems_['category'] == category]
