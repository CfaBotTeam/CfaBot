import unittest
from drqa import tokenizers
from drqa.selector import ChoiceSelector
from drqa.reader import DocReader
from drqa.pipeline.drqa import init_tokenizer


class TestChoiceSelector(unittest.TestCase):
    def setUp(self):
        reader_model = 'data/reader/multitask.mdl'
        reader = DocReader.load(reader_model, normalize=False)
        tok_class = tokenizers.get_class('simple')
        init_tokenizer(tok_class)
        self.selector_ = ChoiceSelector(reader.word_dict, reader.network.embedding)

    # def test_choice_selector(self):
    #     spans = ["By separately analyzing the security into a bond and the embedded option"]
    #     choices = ["Z-spread minus the option cost.",
    #                "Z-spread plus the cost of the option.",
    #                "value of the security's embedded option."]
    #     most_similars = self.selector_.select_most_similar(spans, choices)
    #     pass

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