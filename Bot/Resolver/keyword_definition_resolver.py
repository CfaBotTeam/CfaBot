from Bot.Resolver import DefinitionResolverBase
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import SubjectFeatures
from Bot.Classification.Features import VerbFeaturesFactory
from Bot.Resolver import DefinitionSource


class KeywordDefResolverBase(DefinitionResolverBase):
    def get_question_definitions(self, problem):
        subject = problem[SubjectFeatures.Q_SUBJECT]
        return self.def_provider_.get_definitions(subject, loosly=True)


class KeywordDefResolver(KeywordDefResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [[[choice, DefinitionSource.CHOICE]] for choice in choices]


class KeywordDefStartEndResolver(KeywordDefResolverBase):
    def get_right_of_verb(self, problem):
        tokens = problem[NlpFeatures.QUESTION_NLP]
        i_token, token = VerbFeaturesFactory.get_verb_token(problem)
        right = ''.join(map(lambda t: t.text_with_ws, tokens[i_token + 1:]))
        if right.endswith(':'):
            right = right[:len(right) - 1]
        return right.strip()

    def get_choices_definitions(self, problem, choices):
        def_start = self.get_right_of_verb(problem)
        return [[['%s %s' % (def_start, choice), DefinitionSource.CHOICE]] for choice in choices]
