import tensorflow as tf
import word2vec_optimized
import os
import spacy


lib = tf.load_op_library(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'word2vec_ops.so'))


class ModelDumper:
    def __init__(self, model_path, tsv_path):
        self.model_path_ = model_path
        self.tsv_path_ = tsv_path

    def dump(self):
        with tf.Graph().as_default(), tf.Session() as session:
            opts = word2vec_optimized.Options()
            model = word2vec_optimized.Word2Vec(opts, session)
            model.saver.restore(session, self.model_path_)
            embeddings = session.run(model._w_in)
            nlp = spacy.load("en_core_web_sm", vectors=False)
            nlp.vocab.reset_vectors(shape=embeddings.shape)
            for w_idx, word in enumerate(opts.vocab_words):
                vector = embeddings[w_idx, :]
                nlp.vocab.set_vector(word.decode('utf-8'), vector)
        nlp.to_disk('models/cfa_spacy_mdl-investopedia_plus_cfa')

    def dump_metadata_viz_tsv(self):
        with tf.Graph().as_default(), tf.Session() as session, \
             open(self.tsv_path_, 'w') as f_tsv:
            opts = word2vec_optimized.Options()
            word2vec_optimized.Word2Vec(opts, session)
            f_tsv.write("Word\tFrequency\n")
            for w_idx, word in enumerate(opts.vocab_words):
                count = opts.vocab_counts[w_idx]
                f_tsv.write("%s\t%s\n" % (word.decode('utf-8'), count))


if __name__ == "__main__":
    dumper = ModelDumper("models/model.ckpt-2052219", "words_idx.tsv")
    # dumper.dump()
    dumper.dump()
