import argparse
import pandas as pd
from Bot.pipeline import Pipeline
from Bot.Resolver import DefinitionsProvider
from Bot.Similarity import SimilarityMode


pd.options.mode.chained_assignment = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='Data/qa_mock_exams/all_def_problems_cleaned.xml')
    parser.add_argument('--glossary', type=str, default='Data/material_handbook/glossary_manual2.json')
    parser.add_argument('--similarity-mode', type=str, default=SimilarityMode.WEIGHTED)
    parser.add_argument('--provider-mode', type=str, default=DefinitionsProvider.GLOSS_ONLY,
                        help=("Enable to defined the behavior when fetching definitions."
                              "Either look only glossary ('gloss-only'), "
                              "or only use DrQA ('drqa-only') "  
                              "or use both definitions sources"))
    args = parser.parse_args()
    pipeline = Pipeline(args)
    pipeline.process()
