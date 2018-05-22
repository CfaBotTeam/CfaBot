import tensorflow as tf
import word2vec_optimized
import os
import spacy


lib = tf.load_op_library(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'word2vec_ops.so'))


class ModelDumper:
    def __init__(self, model_path, dump_path):
        self.model_path_ = model_path
        self.dump_path_ = dump_path

    def dump(self):
        with tf.Graph().as_default(), tf.Session() as session:
            opts = word2vec_optimized.Options()
            model = word2vec_optimized.Word2Vec(opts, session)
            model.saver.restore(session, self.model_path_)
            embeddings = session.run(model._w_in)
            nlp = spacy.load("en_core_web_sm", vectors=False)
            for w_idx, word in enumerate(opts.vocab_words):
                if w_idx == 0:
                    nlp.vocab.reset_vectors(shape=embeddings.shape)
                vector = embeddings[w_idx, :]
                nlp.vocab.set_vector(word.decode('utf-8'), vector)
        nlp.to_disk('cfa_spacy_mdl')


if __name__ == "__main__":
    dumper = ModelDumper("models/model.ckpt-2263444", "model_result.vec")
    dumper.dump()
