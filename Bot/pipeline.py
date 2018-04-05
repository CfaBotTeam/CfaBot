import datetime
import json
import spacy
from Bot.Load import ProblemsReader
from Bot.Classification import ProblemsClassifier
from Bot.Classification import ProblemCategory
from Bot.Load import GlossaryLoader
from Bot.Resolver import ResolverFactory
from Bot.Utils import get_enum_name


class Pipeline:
    def __init__(self):
        self.nlp_ = spacy.load('en', disable=['tagger', 'textcat'])
        self.glossary_ = GlossaryLoader().load()
        self.problems_reader_ = ProblemsReader()
        self.classifier_ = ProblemsClassifier(self.glossary_, self.nlp_)
        self.resolver_factory_ = ResolverFactory(self.glossary_, self.nlp_)

    def resolve_category(self, category, df, results):
        category_name = get_enum_name(ProblemCategory, category)
        print("Resolving category " + str(category_name))
        category_filter = self.classifier_.get_category_filter(category)
        category_problems = df.loc[category_filter]

        print("Found {} problems matching the category ".format(len(category_problems)))
        resolver = self.resolver_factory_.get_resolver(category)
        category_results = {}
        res = resolver.resolve(category_problems, category_results)
        category_problems.loc[category_filter, 'prediction'] = res
        results[category_name] = category_results
        correct_answers = category_problems[category_problems['prediction'] == category_problems['answer']]
        print("Correct answers = " + str(len(correct_answers) / len(category_problems)))

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

        categories = [ProblemCategory.DEF_KEYWORD, ProblemCategory.DEF_KEYWORD_START_END]
        for category in categories:
            self.resolve_category(category, all_problems_df, results)
            print()

        self.write_results(results)
