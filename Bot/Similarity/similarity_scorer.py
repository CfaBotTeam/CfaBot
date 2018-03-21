import spacy


class SimilarityScorer:
    def __init__(self):
        self.nlp_ = spacy.load('en')

    def score(self, span1, span2):
        doc1 = self.nlp_(span1)
        doc2 = self.nlp_(span2)
        return doc1.similarity(doc2)
