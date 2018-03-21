from Bot.Load import ProblemsReader
from Bot.Classification import ProblemsClassifier
from Bot.Classification import ProblemCategory
from Bot.Load import GlossaryLoader
from Bot.Resolver import ResolverFactory
from Bot.Utils import get_enum_name


class Pipeline:
    def __init__(self):
        self.glossary_ = GlossaryLoader().load()
        self.problems_reader_ = ProblemsReader()
        self.classifier_ = ProblemsClassifier(self.glossary_)
        self.resolver_factory_ = ResolverFactory(self.glossary_)

    def resolve_category(self, category):
        print("Resolving category" + str(category))
        problems = self.classifier_.get_category(category)

        category_name = get_enum_name(ProblemCategory, category)
        print("Found {} problems matching the category ".format(len(problems)) + str(category_name))
        resolver = self.resolver_factory_.get_resolver(category)
        resolver.resolve(problems)
        correct_answers = problems[problems['prediction'] == problems['answer']]
        print("Correct answers = " + str(len(correct_answers) / len(problems)))

    def process(self):
        all_problems_df = self.problems_reader_.read_all_problems()
        print("Total number of problems = " + str(len(all_problems_df)))
        self.classifier_.fit(all_problems_df)
        self.resolve_category(ProblemCategory.DEF_KEYWORD)
