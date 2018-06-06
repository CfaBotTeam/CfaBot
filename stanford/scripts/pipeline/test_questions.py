#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Run predictions using the full DrQA retriever-reader pipeline."""

import torch
import time
import json
import argparse
import logging

from drqa import pipeline
from drqa.retriever import utils
from drqa.selector import ChoiceSelector
from drqa.utils import CfaEncoder
import os
from datetime import datetime



logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)


parser = argparse.ArgumentParser()
parser.add_argument('dataset', type=str)
parser.add_argument('--out-dir', type=str, default='/tmp',
                    help=("Directory to write prediction file to "
                          "(<dataset>-<model>-pipeline.preds)"))
parser.add_argument('--reader-model', type=str, default=None,
                    help="Path to trained Document Reader model")
parser.add_argument('--retriever-model', type=str, default=None,
                    help="Path to Document Retriever model (tfidf)")
parser.add_argument('--doc-db', type=str, default=None,
                    help='Path to Document DB')
parser.add_argument('--embedding-file', type=str, default=None,
                    help=("Expand dictionary to use all pretrained "
                          "embeddings in this file"))
parser.add_argument('--candidate-file', type=str, default=None,
                    help=("List of candidates to restrict predictions to, "
                          "one candidate per line"))
parser.add_argument('--n-docs', type=int, default=5,
                    help="Number of docs to retrieve per query")
parser.add_argument('--top-n', type=int, default=1,
                    help="Number of predictions to make per query")
parser.add_argument('--tokenizer', type=str, default=None,
                    help=("String option specifying tokenizer type to use "
                          "(e.g. 'corenlp')"))
parser.add_argument('--no-cuda', action='store_true',
                    help="Use CPU only")
parser.add_argument('--gpu', type=int, default=-1,
                    help="Specify GPU device id to use")
parser.add_argument('--parallel', action='store_true',
                    help='Use data parallel (split across gpus)')
parser.add_argument('--num-workers', type=int, default=None,
                    help='Number of CPU processes (for tokenizing, etc)')
parser.add_argument('--batch-size', type=int, default=128,
                    help='Document paragraph batching size')
parser.add_argument('--predict-batch-size', type=int, default=1000,
                    help='Question batching size')
args = parser.parse_args()
t0 = time.time()

args.cuda = not args.no_cuda and torch.cuda.is_available()
if args.cuda:
    torch.cuda.set_device(args.gpu)
    logger.info('CUDA enabled (GPU %d)' % args.gpu)
else:
    logger.info('Running on CPU only.')

if args.candidate_file:
    logger.info('Loading candidates from %s' % args.candidate_file)
    candidates = set()
    with open(args.candidate_file) as f:
        for line in f:
            line = utils.normalize(line.strip()).lower()
            candidates.add(line)
    logger.info('Loaded %d candidates.' % len(candidates))
else:
    candidates = None

logger.info('Initializing pipeline...')
DrQA = pipeline.DrQA(
    reader_model=args.reader_model,
    fixed_candidates=candidates,
    embedding_file=args.embedding_file,
    tokenizer=args.tokenizer,
    batch_size=args.batch_size,
    cuda=args.cuda,
    data_parallel=args.parallel,
    ranker_config={'options': {'tfidf_path': args.retriever_model,
                               'strict': False}},
    db_config={'options': {'db_path': args.doc_db}},
    num_workers=args.num_workers,
)

reader = DrQA.reader
choice_selector = ChoiceSelector(reader.word_dict, reader.network.embedding, DrQA.processes)

# ------------------------------------------------------------------------------
# Read in dataset and make predictions
# ------------------------------------------------------------------------------


logger.info('Loading queries from %s' % args.dataset)
with open(args.dataset) as f:
    text = f.readline()
    data = json.loads(text)
    queries = data['queries']


answer2idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def try_match_spans_with_choices(spans, choices, answer):
    choice_index = {choice: i for i, choice in enumerate(choices)}
    answer_index = answer2idx[answer]
    most_similars = choice_selector.select_most_similar(spans, choices)
    selected_choice = most_similars[0]['choice']
    selected_choice_index = choice_index[selected_choice]
    is_correct = answer_index == selected_choice_index
    return most_similars, is_correct


nb_correct = 0

for i_batch in range(0, len(queries), args.predict_batch_size):
    batch = queries[i_batch: i_batch + args.predict_batch_size]
    batch_questions = [data['question'] for data in batch]
    predictions = DrQA.process_batch(
        batch_questions,
        n_docs=args.n_docs,
        top_n=args.top_n,
        return_context=True
    )

    for i_pred, prediction in enumerate(predictions):
        batch_question = batch[i_pred]
        preds = []
        for pred in prediction:
            preds.append({'span': pred['span'], 'context': pred['context']['text'],
                          'doc_id': pred['doc_id'], 'doc_sore': pred['doc_score'],
                          'span_score': pred['span_score']})
        batch_question['predictions'] = preds
        spans = list(map(lambda x: x['span'], preds))
        spans = [s for s in spans if s]
        if len(spans) == 0:
            batch_question['is_correct'] = False
            continue

        choices = batch_question['choices']
        if spans[0] == 'mark' and choices[0] == "loan to the futures trader.":
            whatever = 1
        answer = batch_question['answer']
        most_similars, is_correct = try_match_spans_with_choices(spans, choices, answer)
        batch_question['best_matches'] = most_similars
        batch_question['is_correct'] = is_correct
        if is_correct:
            nb_correct += 1

all_queries = {'queries': queries}

filename = os.path.basename(args.dataset)
basename = os.path.splitext(filename)[0]
now = datetime.now().strftime("%m_%d_%H_%M")
result_filename = now + '_' + basename + '_res.json'
logger.info('Writing results to %s' % result_filename)
with open(result_filename, 'w') as f:
    f.write(json.dumps(all_queries, indent=4, sort_keys=True, cls=CfaEncoder))

logger.info('Correct response: %.4f(%%)' % ((nb_correct / len(queries)) * 100))
logger.info('Total time: %.2f' % (time.time() - t0))
