import json


class Glossary:
    def __init__(self, glossary):
        self.glossary_ = glossary

    def has_keyword(self, keyword):
        try:
            key = keyword.lower()
        except:
            return False
        return key in self.glossary_

    def get_keys(self):
        return self.glossary_.keys()

    def get_definitions(self, keyword):
        key = keyword.lower()
        return [self.glossary_[key]]


class GlossaryLoader:
    def load(self):
        path = 'Data/material_handbook/glossary.json'
        return Glossary(json.load(open(path)))
