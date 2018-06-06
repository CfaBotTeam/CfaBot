#!/bin/bash

python scripts/pipeline/test_questions.py --n-docs 5 --top-n 5 --num-workers 4 --tokenizer simple --retriever-model data/cfa/documents-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz --doc-db data/cfa/documents.db --reader-model data/reader/multitask.mdl data/datasets/cfa_definition_questions.json
