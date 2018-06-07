import argparse
from Bot.pipeline import Pipeline
from Bot.Resolver import DefinitionsProvider


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='Data/qa_mock_exams/all_problems.xml')
    parser.add_argument('--provider-mode', type=str, default=DefinitionsProvider.GLOSS_ONLY,
                        help=("Enable to defined the behavior when fetching definitions."
                              "Either look only glossary ('gloss-only'), "
                              "or only use DrQA ('drqa-only') "  
                              "or use both definitions sources"))
    args = parser.parse_args()
    pipeline = Pipeline(args)
    pipeline.process()
