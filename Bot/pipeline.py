import datetime
import json
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

    def resolve_category(self, category, results):
        category_name = get_enum_name(ProblemCategory, category)
        print("Resolving category " + str(category_name))
        problems = self.classifier_.get_category(category)

        print("Found {} problems matching the category ".format(len(problems)))
        resolver = self.resolver_factory_.get_resolver(category)
        results[category_name] = resolver.resolve(problems)
        correct_answers = problems[problems['prediction'] == problems['answer']]
        print("Correct answers = " + str(len(correct_answers) / len(problems)))

    def write_results(self, results):
        now = datetime.datetime.now().strftime("%m_%d_%H_%M")
        result_path = 'results_{}.json'.format(now)
        print('Writing results to {}'.format(result_path))
        with open(result_path, 'w') as f:
            f.write(json.dumps(results, indent=4))

    def process(self):
        results = {}
        all_problems_df = self.problems_reader_.read_all_problems()
        print("Total number of problems = " + str(len(all_problems_df)))
        self.classifier_.fit(all_problems_df)
        self.resolve_category(ProblemCategory.DEF_KEYWORD, results)
        self.write_results(results)
