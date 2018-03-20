import unittest
from Core.Similarity.definitions_comparer import DefinitionsComparer


class TestDefinitionsComparer(unittest.TestCase):
    def setUp(self):
        self.scorer_ = Defi()

    def test_stat_test_errors(self):
        type1_defs = ['the false rejection of the null hypothesis',
                      'rejects the null hypothesis when it is true',
                      'a type of error that occurs when a null hypothesis is rejected although it is true',
                      'the rejection of the null hypothesis when it is actually true',
                      'rejecting a true null',
                      'Rejecting the null when it is actually true',
                      'the rejection of the null hypothesis when it is actually true',
                      "rejecting the null hypothesis when it's true"]
        type2_defs = ['not rejecting the null hypothesis when it is false',
                       'describes the error that occurs when one accepts a null hypothesis that is actually false',
                       'confirms an idea that should have been rejected',
                       'a false null hypothesis will be accepted by a statistical test',
                       'not rejecting the null when it is false',
                       'the failure to reject the null hypothesis when it is actually false',
                       'the probability of failing to reject a false null',
                       'failing to reject the null hypothesis when it is false',
                       'the failure to reject the null hypothesis when it is actually false']
        question = 'A hypothesis test fails to reject a false null hypothesis. This result is best described as a:'
        self.scorer_.score()

    def test_choice_selector2(self):
        spans = ["a shortage"]
        choices = ["loan to the futures trader.",
                   "requirement set by federal regulators.",
                   "down payment from the futures trader."]
        most_similars = self.selector_.select_most_similar(spans, choices)
        self.assertEqual(most_similars[0]['choice'], 'loan to the futures trader.')
        self.assertEqual(most_similars[0]['similarity'], -0.1051579974591732)
        self.assertEqual(most_similars[1]['choice'], 'down payment from the futures trader.')
        self.assertEqual(most_similars[1]['similarity'], -0.1051579974591732)
        self.assertEqual(most_similars[2]['choice'], 'requirement set by federal regulators.')
        self.assertEqual(most_similars[2]['similarity'], -0.06476668361574411)


if __name__ == '__main__':
    unittest.main()
