import datetime
import json
from Bot.Load import SpacyLoader
from Bot.Load import ProblemsReader
from Bot.Classification import ProblemsClassifier
from Bot.Classification import ProblemCategory
from Bot.Resolver import ResolverFactory
from Bot.Glossary import Glossary
from Bot.Utils import get_enum_name
from Bot.Resolver import DefinitionsProvider
from stanford.drqa.link import DrqaDefinitionFinder


class Pipeline:
    def __init__(self, args):
        self.args_ = args
        self.model_name_ = args.model
        self.nlp_ = SpacyLoader().load_nlp(self.model_name_)
        glossary = self.load_glossary(args.glossary)
        def_finder = DrqaDefinitionFinder()
        def_provider = DefinitionsProvider(glossary, def_finder, args.provider_mode)
        self.problems_reader_ = ProblemsReader(args.dataset)
        self.classifier_ = ProblemsClassifier(glossary, self.nlp_)
        self.resolver_factory_ = ResolverFactory(def_provider, self.nlp_, args.similarity_mode)

    def load_glossary(self, filepath):
        return Glossary(json.load(open(filepath, 'r')), self.nlp_)

    def add_category_results(self, category_name, results, category_problems):
        nb_correct = 0
        nb_total = len(category_problems)
        percentage = 0
        if len(category_problems) > 0:
            nb_correct = len(category_problems[category_problems['prediction'] == category_problems['answer']])
            percentage = (nb_correct / nb_total) * 100
        results['overall']['nb_total'] += nb_total
        results['overall']['nb_correct'] += nb_correct
        results['overall'][category_name] = {
            'percentage': percentage,
            'nb_correct': nb_correct,
            'nb_total': nb_total
        }
        print("Correct answers = %0.3f%%, (%d out of %d)" % (percentage, nb_correct, nb_total))

    def resolve_category_internal(self, category, category_problems, category_filter, category_results):
        resolver = self.resolver_factory_.get_resolver(category)
        res = resolver.resolve(category_problems, category_results)
        category_problems.loc[category_filter, 'prediction'] = res

    def resolve_category(self, category, df, results):
        category_name = get_enum_name(ProblemCategory, category)
        print("Resolving category " + str(category_name))
        category_filter = self.classifier_.get_category_filter(category)
        category_problems = df.loc[category_filter]

        print("Found {} problems matching the category ".format(len(category_problems)))
        category_results = {}
        if len(category_problems) > 0:
            self.resolve_category_internal(category, category_problems, category_filter, category_results)

        results[category_name] = category_results
        self.add_category_results(category_name, results, category_problems)

    def write_results(self, results, success_rate):
        results['overall']['success_rate'] = success_rate
        now = datetime.datetime.now().strftime("%m_%d_%H_%M")
        result_path = 'Results/results_{}.json'.format(now)
        print('Writing results to {}'.format(result_path))
        with open(result_path, 'w') as f:
            f.write(json.dumps(results, indent=4))

    def process(self):
        print("Definitions provider mode => %s" % self.args_.provider_mode)
        results = {
            'model': self.model_name_,
            'dataset': self.args_.dataset,
            'glossary': self.args_.glossary,
            'provider_mode': self.args_.provider_mode,
            'similarity_mode': self.args_.similarity_mode,
            'overall': {'nb_total': 0, 'nb_correct': 0},
        }
        all_problems_df = self.problems_reader_.read_all_problems()

        total_nb_questions = len(all_problems_df)
        print("Total number of questions = %d" % total_nb_questions)
        self.classifier_.fit(all_problems_df)

        for category in ProblemsClassifier.HANDLED_CATEGORIES:
            self.resolve_category(category, all_problems_df, results)
            print()

        nb_questions_answered = results['overall']['nb_total']
        nb_correct_answers = results['overall']['nb_correct']
        success_rate = (nb_correct_answers / nb_questions_answered) * 100
        print("%d questions answered out of %d" % (nb_questions_answered, total_nb_questions))
        print("%d correctly answered (success rate: %f)" % (nb_correct_answers, success_rate))
        self.write_results(results, success_rate)
