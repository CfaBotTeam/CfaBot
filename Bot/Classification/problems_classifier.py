from Bot.Classification import ProblemCategory
from Bot.Features import LengthFeaturesFactory
from Bot.Features import GlossaryFeaturesFactory


class CategoryFilterFactory:
    def __init__(self, category):
        self.category_ = category

    def get_filters(self, df):
        return df['category'] == self.category_


class ProblemsClassifier:
    def __init__(self, glossary):
        self.glossary_ = glossary
        self.problems_ = None
        self.feature_factories_ = [LengthFeaturesFactory(), GlossaryFeaturesFactory(glossary)]
        self.filters_factories = {ProblemCategory.DEF_KEYWORD: CategoryFilterFactory(ProblemCategory.DEF_KEYWORD)}

    def add_features(self, df):
        for factory in self.feature_factories_:
            factory.add_features(df)

    def get_def_keyword_filters(self, df):
        filters = ~df['question'].str.contains(', CFA,')
        filters &= df['question_choice_len_ratio'] < 12.0
        filters &= df['any_choice_in_glossary'] == True
        sub_filter = df['question'].str.contains('described as')
        sub_filter |= df['question'].str.contains('defined as')
        filters &= sub_filter
        return filters

    def fit(self, df):
        self.problems_ = df
        self.add_features(df)
        df['predicted_category'] = ProblemCategory.OTHER
        categories = [ProblemCategory.DEF_KEYWORD]
        for category in categories:
            filters_factory = self.filters_factories[category]
            filters = filters_factory.get_filters(df)
            df.loc[filters, 'predicted_category'] = category

    def get_category(self, category):
        return self.problems_[self.problems_['predicted_category'] == category]
