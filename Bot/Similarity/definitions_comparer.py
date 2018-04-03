from Bot.Similarity import SimilarityScorer


class DefinitionsComparer:
    def __init__(self, nlp):
        self.scorer_ = SimilarityScorer(nlp)

    def compare(self, question, *defs_args):
        sim_max = 0
        i_max = 0
        for i, definitions in enumerate(defs_args):
            for definition in definitions:
                similarity = self.scorer_.score(question, definition)
                if similarity > sim_max:
                    sim_max = similarity
                    i_max = i
        return i_max