import re
from spacy.lang.en.stop_words import STOP_WORDS
from Levenshtein.StringMatcher import StringMatcher


class Glossary:
    def __init__(self, glossary, nlp):
        self.glossary_ = glossary
        self.nlp_ = nlp
        self.tokenized_keys_ = self.tokenize_keys()

        import os

        debug_filepath = 'debug_missing_terms.txt'
        if os.path.exists(debug_filepath):
            os.remove(debug_filepath)
        self.debug_file_ = open(debug_filepath, 'w')

    def get_keys(self):
        return self.glossary_.keys()

    def tokenize_text(self, text):
        tokens = self.nlp_(text, disable=["tagger", "parser", "ner", "textcat"])
        return [str(token) for token in tokens if str(token) not in STOP_WORDS]

    def tokenize_keys(self):
        result = {}
        for key in self.get_keys():
            result[key] = set(self.tokenize_text(key))
        return result

    def is_roman(self, word):
        return re.match('^[IVXLC]+$', word) is not None

    def get_keyword(self, sentence):
        words = sentence.split(' ')
        words = [x.lower() for x in words if self.is_roman(x) or x.lower() not in STOP_WORDS]
        return ' '.join(words)

    def get_matching_keyword(self, term):
        keys = self.glossary_.keys()
        keyword = term.lower()
        if keyword in keys:
            return keyword
        keyword = self.get_keyword(term)
        if keyword in keys:
            return keyword
        return None

    def has_matching_keyword(self, term):
        return self.get_matching_keyword(term) is not None

    def has_loosly_matching_keyword(self, term):
        key = self.get_loosly_matching_keyword(term)
        return key is not None

    def get_loosly_matching_keyword(self, term):
        splitted_terms = self.tokenize_text(term)
        max_nb_commun = 0
        most_common_keys = []
        for key, key_tokens in self.tokenized_keys_.items():
            nb_words_common = 0
            for potential_word in splitted_terms:
                if potential_word in key_tokens:
                    nb_words_common += 1
            if nb_words_common > max_nb_commun:
                max_nb_commun = nb_words_common
                most_common_keys = []
            if nb_words_common == max_nb_commun:
                most_common_keys.append(key)

        min_distance = 9999999
        result = None
        for key in most_common_keys:
            match = StringMatcher(seq1=key, seq2=term)
            distance = match.distance()
            if distance < min_distance:
                min_distance = distance
                result = key
        return result

    def get_definitions(self, term):
        keyword = self.get_matching_keyword(term)
        if keyword is None:
            self.debug_file_.write(term + "\n")
            return None, None
        defs = self.glossary_[keyword]
        if isinstance(defs, str):
            return keyword, [defs]
        return keyword, defs

    def get_loose_definition(self, term):
        keyword = self.get_loosly_matching_keyword(term)
        if keyword is None:
            self.debug_file_.write(term + "\n")
            return None, None
        defs = self.glossary_[keyword]
        if isinstance(defs, str):
            return keyword, [defs]
        return keyword, defs

