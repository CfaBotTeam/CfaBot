import numpy as np

from Bot.Classification.Features import FeaturesFactory


class GlossaryFeatures:
    A_IN_GLOSS = 'choice_A_in_glossary'
    A_GLOSS_TERM = 'choice_A_glossary_term'
    B_IN_GLOSS = 'choice_B_in_glossary'
    B_GLOSS_TERM = 'choice_B_glossary_term'
    C_IN_GLOSS = 'choice_C_in_glossary'
    C_GLOSS_TERM = 'choice_C_glossary_term'
    D_IN_GLOSS = 'choice_D_in_glossary'
    D_GLOSS_TERM = 'choice_D_glossary_term'
    ANY_CH_IN_GLOSS = 'any_choice_in_glossary'


class GlossaryFeaturesFactory(FeaturesFactory):
    def __init__(self, glossary):
        self.glossary_ = glossary
        self.features_ = [GlossaryFeatures.A_IN_GLOSS, GlossaryFeatures.A_GLOSS_TERM,
                          GlossaryFeatures.B_IN_GLOSS, GlossaryFeatures.B_GLOSS_TERM,
                          GlossaryFeatures.C_IN_GLOSS, GlossaryFeatures.C_GLOSS_TERM,
                          GlossaryFeatures.D_IN_GLOSS, GlossaryFeatures.D_GLOSS_TERM,
                          GlossaryFeatures.ANY_CH_IN_GLOSS]

    def get_glossary_term(self, sentence):
        if sentence is np.NaN:
            return False
        for keyword in self.glossary_.get_keys():
            if keyword.lower() in sentence.lower():
                return keyword
        return ''

    def calc_features(self, problem):
        a_term = self.get_glossary_term(problem['choice_A'])
        a_in_gloss = a_term != ''
        b_term = self.get_glossary_term(problem['choice_B'])
        b_in_gloss = a_term != ''
        c_term = self.get_glossary_term(problem['choice_C'])
        c_in_gloss = a_term != ''
        d_term = self.get_glossary_term(problem['choice_D'])
        d_in_gloss = a_term != ''
        any_in_gloss = a_in_gloss or b_in_gloss or c_in_gloss or d_in_gloss
        return a_in_gloss, a_term, b_in_gloss, b_term, c_in_gloss, c_term, \
               d_in_gloss, d_term, any_in_gloss