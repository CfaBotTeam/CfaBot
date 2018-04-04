import re
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS
from Bot.Classification.Features import FeaturesFactory


class GlossaryFeatures:
    ANY_CH_IN_GLOSS = 'any_choice_in_glossary'


class GlossaryFeaturesFactory(FeaturesFactory):
    def __init__(self, glossary):
        self.glossary_ = glossary
        self.features_ = [GlossaryFeatures.ANY_CH_IN_GLOSS]

    def is_roman(self, word):
        return re.match('^[IVXLC]+$', word) is not None

    def get_keyword(self, term):
        words = term.split(' ')
        words = [x.lower() for x in words if self.is_roman(x) or x.lower() not in STOP_WORDS]
        return ' '.join(words)

    def is_in_glossary(self, term):
        if term is np.NaN:
            return False
        return self.glossary_.has_matching_keyword(term)

    def calc_features(self, problem):
        a_in_gloss = self.is_in_glossary(problem['choice_A'])
        b_in_gloss = self.is_in_glossary(problem['choice_B'])
        c_in_gloss = self.is_in_glossary(problem['choice_C'])
        d_in_gloss = 'choice_D' in problem and self.is_in_glossary(problem['choice_D'])
        any_in_gloss = a_in_gloss or b_in_gloss or c_in_gloss or d_in_gloss
        return any_in_gloss
