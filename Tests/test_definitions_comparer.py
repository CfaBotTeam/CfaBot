import unittest
from Bot.Similarity.definitions_comparer import DefinitionsComparer


class TestDefinitionsComparer(unittest.TestCase):
    def setUp(self):
        self.comparer_ = DefinitionsComparer()

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
        max_type = self.comparer_.compare(question, type1_defs, type2_defs)
        self.assertEqual(max_type, 1)


if __name__ == '__main__':
    unittest.main()
