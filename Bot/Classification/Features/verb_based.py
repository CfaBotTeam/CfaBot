from Bot.Classification.Features import FeaturesFactory
from Bot.Classification.Features import NlpFeatures


class VerbFeatures:
    HAS_DEF_VERB = 'has_def_verb'
    CENTRALITY = 'verb_centrality'


class VerbFeaturesFactory(FeaturesFactory):
    def __init__(self):
        self.features_ = [VerbFeatures.HAS_DEF_VERB, VerbFeatures.CENTRALITY]

    @staticmethod
    def get_verb_token(problem):
        tokens = problem[NlpFeatures.QUESTION_NLP]
        for i, token in enumerate(reversed(tokens)):
            if token.text == 'defined' or token.text == 'described':
                return len(tokens) - 1 - i, token
        return -1, None

    def has_def_verb(self, problem):
        _, token = self.get_verb_token(problem)
        return token is not None

    def get_verb_centrality(self, problem):
        verb_index, _ = self.get_verb_token(problem)
        nb_tokens = len(problem['question_nlp'])
        res = (verb_index + 1) / nb_tokens
        if nb_tokens % 2 == 1:
            res -= 1 / (2 * nb_tokens)
        return res

    def calc_features(self, problem):
        has_def_verb = self.has_def_verb(problem)
        verb_centrality = self.get_verb_centrality(problem)

        return has_def_verb, verb_centrality
