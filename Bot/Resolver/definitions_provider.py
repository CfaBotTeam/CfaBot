class DefinitionSource:
    DRQA = 'drqa'
    GLOSS = 'glossary'
    QUESTION = 'question'
    CHOICE = 'choice'


class DefinitionsProvider:
    GLOSS_ONLY = 'gloss-only'
    DRQA_ONLY = 'drqa-only'
    DRQA_FALLBACK = 'drqa-fallback'
    BOTH = 'both'

    def __init__(self, glossary, drqa_def_finder, mode):
        self.glossary_ = glossary
        self.drqa_def_finder_ = drqa_def_finder
        self.mode_ = mode

    def is_in_glossary(self, loosly, keyword):
        if loosly:
            return self.glossary_.has_loosly_matching_keyword(keyword)
        return self.glossary_.has_matching_keyword(keyword)

    def get_glossary_definitions(self, loosly, keyword):
        if loosly:
            return self.glossary_.get_loose_definition(keyword)
        return self.glossary_.get_definitions(keyword)

    @staticmethod
    def wrap_with_source(definitions, source):
        if definitions is None:
            return None
        return list(map(lambda d: [d, source], definitions))

    def get_definitions(self, keyword, loosly=False):
        if self.mode_ == self.GLOSS_ONLY:
            defs = self.get_glossary_definitions(loosly, keyword)
            return self.wrap_with_source(defs, DefinitionSource.GLOSS)
        if self.mode_ == self.DRQA_ONLY:
            defs = self.drqa_def_finder_.find_definitions(keyword)
            return self.wrap_with_source(defs, DefinitionSource.DRQA)
        if self.mode_ == self.DRQA_FALLBACK:
            if self.is_in_glossary(loosly, keyword):
                defs = self.get_glossary_definitions(loosly, keyword)
                return self.wrap_with_source(defs, DefinitionSource.GLOSS)
            defs = self.drqa_def_finder_.find_definitions(keyword)
            return self.wrap_with_source(defs, DefinitionSource.DRQA)
        # Otherwise both mode
        gloss_defs = self.get_glossary_definitions(loosly, keyword)
        drqa_defs = self.drqa_def_finder_.find_definitions(keyword)
        drqa_defs = self.wrap_with_source(drqa_defs, DefinitionSource.DRQA)
        if gloss_defs is None:
            return drqa_defs
        gloss_defs = self.wrap_with_source(gloss_defs, DefinitionSource.GLOSS)
        return gloss_defs + drqa_defs
