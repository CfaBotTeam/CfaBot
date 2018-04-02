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

    def get_definitions(self, sentence):
        keyword = sentence
        if keyword not in self.glossary_:
            keyword = self.get_keyword(sentence)
            if keyword not in self.glossary_:
                return None
        return [self.glossary_[keyword]]


class GlossaryLoader:
    def load(self):
        path = 'Data/material_handbook/glossary_manual.json'
        return Glossary(json.load(open(path)))
