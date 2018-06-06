#!/bin/bash

python scripts/pipeline/interactive.py --retriever-mode data/cfa/new_documents-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz --doc-db data/cfa/new_documents.db --reader-model data/reader/multitask.mdl
