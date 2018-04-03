class SimilarityScorer:
    def __init__(self, nlp):
        self.nlp_ = nlp

    def score(self, span1, span2):
        doc1 = self.nlp_(span1)
        doc2 = self.nlp_(span2)
        return doc1.similarity(doc2)
