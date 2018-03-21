import json


class Glossary:
    def __init__(self, glossary):
        self.glossary_ =  glossary

    def has_keyword(self, keyword):
        return keyword in self.glossary_

    def get_keys(self):
        return self.glossary_.keys()

    def get_definitions(self, keyword):
        return [self.glossary_[keyword]]


class GlossaryLoader:
    def load(self):
        path = 'Data/material_handbook/glossary.json'
        return Glossary(json.load(open(path)))