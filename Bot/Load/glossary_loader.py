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
        key = self.get_loosly_matching_keyword(term)
        return key is not None

    def get_loosly_matching_keyword(self, term):
        keys = self.get_keys()
        for key in keys:
            if key in term:
                return key
        return None

    def get_definitions(self, term):
        keyword = self.get_matching_keyword(term)
        if keyword is None:
            return None
        defs = self.glossary_[keyword]
        if isinstance(defs, str):
            return [defs]
        return defs

    def get_loose_definition(self, term):
        keyword = self.get_loosly_matching_keyword(term)
        if keyword is None:
            return None
        defs = self.glossary_[keyword]
        if isinstance(defs, str):
            return [defs]
        return defs


class GlossaryLoader:
    FILEPATH = 'Data/material_handbook/glossary_manual.json'

    def load(self):
        return Glossary(json.load(open(self.FILEPATH, 'r')))
