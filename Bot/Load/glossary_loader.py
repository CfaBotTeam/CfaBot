import re
import json
from spacy.lang.en.stop_words import STOP_WORDS


class Glossary:
    def __init__(self, glossary):
        self.glossary_ = glossary

    def get_keys(self):
        return self.glossary_.keys()

    def is_roman(self, word):
        return re.match('^[IVXLC]+$', word) is not None

    def get_keyword(self, sentence):
        words = sentence.split(' ')
        words = [x.lower() for x in words if self.is_roman(x) or x.lower() not in STOP_WORDS]
        return ' '.join(words)

    def get_matching_keyword(self, term):
        keys = self.glossary_.keys()
        keyword = term
        if keyword in keys:
            return keyword
        keyword = self.get_keyword(term)
        if keyword in keys:
            return keyword
        return None

    def has_matching_keyword(self, term):
        return self.get_matching_keyword(term) is not None

    def has_loosly_matching_keyword(self, term):
        keys = self.get_keys()
        for key in keys:
            if key in term:
                return True
        return False

    def get_definitions(self, term):
        keyword = self.get_matching_keyword(term)
        if keyword is None:
            return None
        return [self.glossary_[keyword]]


class GlossaryLoader:
    def load(self):
        path = 'Data/material_handbook/glossary_manual.json'
        return Glossary(json.load(open(path)))
