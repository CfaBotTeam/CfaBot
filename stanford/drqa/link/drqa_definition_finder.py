from stanford.drqa.pipeline import DrQA


class DrqaDefinitionFinder:
    def __init__(self):
        self.reader_model_ = "stanford/data/reader/multitask.mdl"
        self.candidates_ = None
        self.embedding_file_ = None
        self.tokenizer_ = "simple"
        self.batch_size_ = 128
        self.cuda_ = False
        self.parallel_ = False
        self.ranker_config_ = {
            'options': {
                'tfidf_path': 'stanford/data/cfa/documents-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
                'strict': False
            }
        }
        self.db_config_ = {'options': {'db_path': 'stanford/data/cfa/documents.db'}}
        self.num_workers_ = 4
        self.predict_batch_size_ = 1000
        self.top_n_ = 5
        self.n_docs_ = 5
        print('Loading DrQA')
        # self.drqa_ = DrQA(
        #     reader_model=self.reader_model_,
        #     fixed_candidates=self.candidates_,
        #     embedding_file=self.embedding_file_,
        #     tokenizer=self.tokenizer_,
        #     batch_size=self.batch_size_,
        #     cuda=self.cuda_,
        #     data_parallel=self.parallel_,
        #     ranker_config=self.ranker_config_,
        #     db_config=self.db_config_,
        #     num_workers=self.num_workers_,
        # )

    def find_definitions(self, keyword):
        question = "What is a %s?" % keyword
        predictions = self.drqa_.process_batch(
            [question],
            n_docs=self.n_docs_,
            top_n=self.top_n_,
            return_context=True
        )
        return [x['span'] for x in predictions[0]]
