from Bot.Classification.Features import FeaturesFactory


class NlpFeatures:
    QUESTION_NLP = 'question_nlp'
    HAS_DIGIT = 'nlp_has_digit'
    HAS_PERSON = 'nlp_has_person'


class NlpFeaturesFactory(FeaturesFactory):
    def __init__(self):
        self.features_ = [NlpFeatures.HAS_DIGIT, NlpFeatures.HAS_PERSON]

    def has_numbers(self, problem):
        for token in problem[NlpFeatures.QUESTION_NLP]:
            if token.is_digit:
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

    def has_person(self, ent_types):
        return ent_types is not None and 'PERSON' in ent_types

    def calc_features(self, problem):
        has_numbers = self.has_numbers(problem)
        ent_types = self.get_entity_types(problem)
        has_person = self.has_person(ent_types)

        return has_numbers, has_person