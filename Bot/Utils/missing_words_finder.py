class MissingWordsFinder:
    def __init__(self, nlp):
        self.nlp_ = nlp

    def add_sentence_missing_words(self, sentence, missing_words):
        for token in self.nlp_(sentence, disable=['tagger', 'parser', 'ner', 'textcat']):
            word = token.string.strip()
            if not self.nlp_.vocab.has_vector(word) and word not in missing_words:
                missing_words.add(word)

    def add_problem_missing_words(self, problem, missing_words):
        self.add_sentence_missing_words(problem['question'], missing_words)
        self.add_sentence_missing_words('choice_A', missing_words)
        self.add_sentence_missing_words('choice_B', missing_words)
        self.add_sentence_missing_words('choice_C', missing_words)
        if 'choice_D' in problem:
            self.add_sentence_missing_words('choice_D', missing_words)

    def get_missing_words(self, all_problems_df):
        missing_words = set()
        all_problems_df.apply(lambda x: self.add_problem_missing_words(x, missing_words), axis=1)
        return missing_words
