import numpy as np
from Bot.Resolver import DefinitionResolverBase
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import SubjectFeatures
from Bot.Classification.Features import VerbFeaturesFactory


class KeywordDefResolverBase(DefinitionResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [[choice] for choice in choices]

    def get_question_definition(self, problem):
        subject = problem[SubjectFeatures.Q_SUBJECT]
        return self.glossary_.get_loose_definition(subject)


class KeywordDefResolver(KeywordDefResolverBase):
    def get_choices(self, problem):
        keys = ['choice_A', 'choice_B', 'choice_C', 'choice_D']
        return [problem[key] for key in keys if key in problem and problem[key] is not np.NaN]


class KeywordDefStartEndResolver(KeywordDefResolverBase):
    def get_right_of_verb(self, problem):
        tokens = problem[NlpFeatures.QUESTION_NLP]
        i_token, token = VerbFeaturesFactory.get_verb_token(problem)
        right = ''.join(map(lambda t: t.text_with_ws, tokens[i_token + 1:]))
        if right.endswith(':'):
            right = right[:len(right) - 1]
        return right.strip()

    def get_choices(self, problem):
        def_start = self.get_right_of_verb(problem)
        keys = ['choice_A', 'choice_B', 'choice_C', 'choice_D']
        return [def_start + ' ' + problem[key] for key in keys if key in problem and problem[key] is not np.NaN]
