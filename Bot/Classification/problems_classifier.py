from Bot.Classification import ProblemCategory
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import NlpFeaturesFactory
from Bot.Classification.Features import GlossaryFeaturesFactory
from Bot.Classification.Features import LengthFeaturesFactory
from Bot.Classification.Features import VerbFeaturesFactory
from Bot.Classification.Features import SubjectFeaturesFactory
from Bot.Classification.Filters import DefKeywordFilterFactory
from Bot.Classification.Filters import DefKeywordStartEndFilterFactory
from Bot.Classification.Filters import ScenarioFilterFactory
from Bot.Classification.Filters import KeywordDefFilterFactory
from Bot.Classification.Filters import KeywordDefStartEndFilterFactory


class ProblemsClassifier:
    def __init__(self, glossary, nlp):
        self.nlp_ = nlp
        self.problems_ = None
        self.glossary_ = glossary
        self.feature_factories_ = [
            VerbFeaturesFactory(),
            LengthFeaturesFactory(),
            GlossaryFeaturesFactory(glossary),
            NlpFeaturesFactory(),
            SubjectFeaturesFactory(glossary)
        ]
        self.filters_factories_ = {
            ProblemCategory.SCENARIO: ScenarioFilterFactory(),
            ProblemCategory.DEF_KEYWORD: DefKeywordFilterFactory(),
            ProblemCategory.DEF_KEYWORD_START_END: DefKeywordStartEndFilterFactory(),
            ProblemCategory.KEYWORD_DEF: KeywordDefFilterFactory(),
            ProblemCategory.KEYWORD_DEF_START_END: KeywordDefStartEndFilterFactory(),
        }

    def add_features(self):
        for factory in self.feature_factories_:
            factory.add_features(self.problems_)

    def add_nlp(self):
        self.problems_[NlpFeatures.QUESTION_NLP] = self.problems_['question'].apply(self.nlp_)

    def fit(self, df):
        self.problems_ = df
        print("Analysing questions with spacy")
        self.add_nlp()
        print("Adding features")
        self.add_features()
        df['predicted_category'] = ProblemCategory.UNLABELED
        categories = self.filters_factories_.keys()
        for category in categories:
            filters_factory = self.filters_factories_[category]
            filters = filters_factory.get_filters(df)
            df.loc[filters, 'predicted_category'] = category

    def get_category_filter(self, category):
        return self.problems_['predicted_category'] == category
