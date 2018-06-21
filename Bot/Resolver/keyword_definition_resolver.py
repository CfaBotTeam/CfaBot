from Bot.Resolver import DefinitionResolverBase
from Bot.Classification.Features import NlpFeatures
from Bot.Classification.Features import SubjectFeatures
from Bot.Classification.Features import VerbFeaturesFactory
from Bot.Resolver import DefinitionSource
from Bot.Resolver import DefinitionsComparison


class KeywordDefResolverBase(DefinitionResolverBase):
    def get_comparison(self, problem, choices):
        subject = problem[SubjectFeatures.Q_SUBJECT]
        q_keyword, q_defs = self.def_provider_.get_definitions(subject, loosly=True)
        choices_keywords_defs = self.get_choices_definitions(problem, choices)
        return DefinitionsComparison(q_keyword, q_defs, choices, choices_keywords_defs)

    def get_choices_definitions(self, problem, choices):
        raise NotImplementedError("This method need to be overloaded")


class KeywordDefResolver(KeywordDefResolverBase):
    def get_choices_definitions(self, problem, choices):
        return [['', [[choice, DefinitionSource.CHOICE]]] for choice in choices]


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
        return [['', [['%s %s' % (def_start, choice), DefinitionSource.CHOICE]]] for choice in choices]
