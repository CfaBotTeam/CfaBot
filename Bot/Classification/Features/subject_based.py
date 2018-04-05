import numpy as np
from spacy.symbols import nsubj, nsubjpass, det
from Bot.Classification.Features import FeaturesFactory
from Bot.Classification.Features import VerbFeaturesFactory


class SubjectFeatures:
    CHOICE_Q_TERMS = 'choice_q_terms'
    CHOICE_Q_SUB_IN_GLOSS = 'choice_q_sub_in_gloss'


class SubjectFeaturesFactory(FeaturesFactory):
    def __init__(self, glossary):
        self.glossary_ = glossary
        self.features_ = [SubjectFeatures.CHOICE_Q_TERMS, SubjectFeatures.CHOICE_Q_SUB_IN_GLOSS]

    def get_definition_subject(self, problem):
        _, verb_token = VerbFeaturesFactory.get_verb_token(problem)
        while verb_token is not None and verb_token != verb_token.head:
            verb_token = verb_token.head
        if verb_token is None:
            return ''
        for child in verb_token.children:
            if child.dep != nsubj and child.dep != nsubjpass:
                continue
            subtree = list(child.subtree)
            if subtree[0].dep == det:
                subtree = subtree[1:]
            return ''.join(map(lambda x: x.text_with_ws, subtree))
        return ''

    def extract_choice_query_keywords(self, problem):
        subject = self.get_definition_subject(problem)
        choice_a = (problem['choice_A'] + ' ' + subject).strip()
        choice_b = (problem['choice_B'] + ' ' + subject).strip()
        choice_c = (problem['choice_C'] + ' ' + subject).strip()
        if 'choice_D' not in problem or problem['choice_D'] is np.NaN:
            return choice_a, choice_b, choice_c
        choice_d = (problem['choice_D'] + ' ' + subject).strip()
        return choice_a, choice_b, choice_c, choice_d

    def any_keyword_in_glossary(self, keywords):
        for keyword in keywords:
            if self.glossary_.has_matching_keyword(keyword):
                return True
        return False

    def calc_features(self, problem):
        keywords = self.extract_choice_query_keywords(problem)
        any_keyword_in_gloss = self.any_keyword_in_glossary(keywords)
        return keywords, any_keyword_in_gloss
