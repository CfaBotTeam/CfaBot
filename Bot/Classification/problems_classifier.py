from Bot.Classification import ProblemCategory
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import NlpFeaturesFactory
from Bot.Classification.Features import GlossaryFeaturesFactory
from Bot.Classification.Features import LengthFeaturesFactory
from Bot.Classification.Filters import DefKeywordFilterFactory
from Bot.Classification.Features import VerbFeaturesFactory


class ProblemsClassifier:
    def __init__(self, glossary, nlp):
        self.nlp_ = nlp
        self.problems_ = None
        self.glossary_ = glossary
        self.feature_factories_ = [VerbFeaturesFactory(),
                                   LengthFeaturesFactory(),
                                   GlossaryFeaturesFactory(glossary),
                                   NlpFeaturesFactory()]
        self.filters_factories_ = {ProblemCategory.DEF_KEYWORD: DefKeywordFilterFactory()}

    def add_features(self):
        for factory in self.feature_factories_:
            factory.add_features(self.problems_)

    def add_nlp(self):
        self.problems_[NlpFeatures.QUESTION_NLP] = self.problems_['question'].apply(self.nlp_)

    def fit(self, df):
        self.problems_ = df
        self.add_nlp()
        self.add_features()
        df['predicted_category'] = ProblemCategory.OTHER
        categories = [ProblemCategory.DEF_KEYWORD]
        for category in categories:
            filters_factory = self.filters_factories_[category]
            filters = filters_factory.get_filters(df)
            df.loc[filters, 'predicted_category'] = category

    def get_category(self, category):
        return self.problems_[self.problems_['predicted_category'] == category]
