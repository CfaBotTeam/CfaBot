import numpy as np
from Bot.Classification.Features import FeaturesFactory


class LengthFeatures:
    AVG_Q_LEN = 'average_question_len'
    Q_CH_LEN_RATIO = 'question_choice_len_ratio'


class LengthFeaturesFactory(FeaturesFactory):
    def __init__(self):
        self.features_ = [LengthFeatures.AVG_Q_LEN, LengthFeatures.Q_CH_LEN_RATIO]

    def calc_average_q_len(self, problem):
        res = len(problem['choice_A']) + \
              len(problem['choice_B']) + \
              len(problem['choice_C'])
        if problem['choice_D'] is np.NaN:
            return res / 3
        res += len(problem['choice_D'])
        return res / 4

    def calc_features(self, problem):
        avg_q_len = self.calc_average_q_len(problem)
        ratio = len(problem['question']) / avg_q_len
        return avg_q_len, ratio
