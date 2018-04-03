from Bot.Classification.Features import FeaturesFactory
from Bot.Classification.Features import NlpFeatures


class VerbFeatures:
    HAS_DEF_VERB = 'has_def_verb'
    CENTRALITY = 'verb_centrality'


class VerbFeaturesFactory(FeaturesFactory):
    def __init__(self):
        self.features_ = [VerbFeatures.HAS_DEF_VERB, VerbFeatures.CENTRALITY]

    def has_def_verb(self, problem):
        question = problem['question']
        return 'defined' in question or 'described' in question

    def get_verb_centrality(self, problem):
        index = -1
        for i, token in enumerate(problem[NlpFeatures.QUESTION_NLP]):
            t = str(token)
            if t == 'defined' or t == 'described':
                index = i
                break
        if index == -1:
            return -1
        nb_tokens = len(problem['question_nlp'])
        res = (index + 1) / nb_tokens
        if nb_tokens % 2 == 1:
            res -= 1 / (2 * nb_tokens)
        return res

    def calc_features(self, problem):
        has_def_verb = self.has_def_verb(problem)
        verb_centrality = self.get_verb_centrality(problem)

        return has_def_verb, verb_centrality
