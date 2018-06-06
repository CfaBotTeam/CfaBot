class DefinitionsProvider:
    def __init__(self, glossary, drqa_def_finder):
        self.glossary_ = glossary
        self.drqa_def_finder_ = drqa_def_finder

    def is_in_glossary(self, loosly, keyword):
        if loosly:
            return self.glossary_.has_loosly_matching_keyword(keyword)
        return self.glossary_.has_matching_keyword(keyword)

    def get_glossary_definitions(self, loosly, keyword):
        if loosly:
            return self.glossary_.get_loose_definition(keyword)
        return self.glossary_.get_definitions(keyword)

    def get_definitions(self, keyword, loosly=False):
        if self.is_in_glossary(loosly, keyword):
            return self.get_glossary_definitions(loosly, keyword)
        return self.drqa_def_finder_.find_definitions(keyword)
