import argparse
import pandas as pd
from Bot.pipeline import Pipeline
from Bot.Resolver import DefinitionsProvider
from Bot.Similarity import SimilarityMode


pd.options.mode.chained_assignment = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='Embeddings/models/cfa_spacy_mdl-investopedia_plus_cfa')
    parser.add_argument('--dataset', type=str, default='Data/qa_mock_exams/all_def_problems_cleaned.xml')
    parser.add_argument('--glossary', type=str, default='Data/material_handbook/glossary_manual.json')
    parser.add_argument('--similarity-mode', type=str, default=SimilarityMode.NORMAL)
    parser.add_argument('--provider-mode', type=str, default=DefinitionsProvider.GLOSS_ONLY,
                        help=("Enable to defined the behavior when fetching definitions."
                              "Either look only glossary ('gloss-only'), "
                              "only use DrQA ('drqa-only') "
                              "use DrQA as a fallback when no definitions are available ('drqa-fallback') "
                              "or use both definitions sources simultaneously"))
    args = parser.parse_args()
    pipeline = Pipeline(args)
    pipeline.process()
