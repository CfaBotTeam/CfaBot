import re
from Bot.Classification.Features import FeaturesFactory


class NlpFeatures:
    QUESTION_NLP = 'question_nlp'
    HAS_NUMBER = 'nlp_has_number'
    HAS_NER = 'nlp_has_ner'


class NlpFeaturesFactory(FeaturesFactory):
    def __init__(self):
        self.features_ = [NlpFeatures.HAS_NUMBER, NlpFeatures.HAS_NER]

    def has_numbers(self, problem):
        for token in problem[NlpFeatures.QUESTION_NLP]:
            if re.match("^[0-9]+[.,]?[0-9]*$", str(token)) is not None:
                return True
        return False

    def get_entity_types(self, problem):
        ent_type_ids = set()
        ent_types = []
        for token in problem[NlpFeatures.QUESTION_NLP]:
            if token.ent_type != 0 and token.ent_type not in ent_type_ids:
                ent_type_ids.add(token.ent_type)
                ent_types.append(token.ent_type_)
        if len(ent_types) == 0:
            return None
        return ent_types

    def has_ner(self, ent_types):
        return ent_types is not None and ('PERSON' in ent_types or 'PERCENT' in ent_types)

    def calc_features(self, problem):
        has_numbers = self.has_numbers(problem)
        ent_types = self.get_entity_types(problem)
        has_ner = self.has_ner(ent_types)
        return has_numbers, has_ner
