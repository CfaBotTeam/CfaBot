import argparse
import pandas as pd
from Bot.pipeline import Pipeline
from Bot.Resolver import DefinitionsProvider


pd.options.mode.chained_assignment = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--dataset', type=str, default='Data/qa_practice_exams_new/def_new_problems.xml')
    parser.add_argument('--dataset', type=str, default='Data/qa_mock_exams/def_problems.xml')
    # parser.add_argument('--glossary', type=str, default='Data/material_handbook/glossary_manual.json')
    parser.add_argument('--glossary', type=str, default='Data/material_handbook/glossary_merged.json')
    parser.add_argument('--provider-mode', type=str, default=DefinitionsProvider.GLOSS_ONLY,
                        help=("Enable to defined the behavior when fetching definitions."
                              "Either look only glossary ('gloss-only'), "
                              "or only use DrQA ('drqa-only') "  
                              "or use both definitions sources"))
    args = parser.parse_args()
    pipeline = Pipeline(args)
    pipeline.process()
