# -*- coding: UTF-8 -*-

import os
import gensim

MODEL_DIR = '../language_models/embeddings'


def get_models_by_iso(iso):
    """
    Finds all embedding models for a particular language.
    :param iso: ISO 639-3 language code (str)
    :return: list of model names
    """
    lang = "_%s_" % iso
    lang_models = []
    for root, dirs, files in os.walk(MODEL_DIR):
        for file in files:
            if lang in file:
                lang_models.append(file)
    return lang_models


def load_model(file, compressed=True, binary=True):
    """
    Loads a pretrained FastText model.
    :param file: model file name (str) selected by a user from a list
    of models for a given language
    :param compressed: if the model is in compressed w2v format or not
    :param binary: if the model is compressed, is it in binary or text format
    :return: KeyedVectors object or FastTextKeyedVectors object
    """
    if compressed:
        return gensim.models.KeyedVectors.load_word2vec_format(os.path.join(MODEL_DIR, file), binary=binary)
    else:
        return gensim.models.FastText.load(os.path.join(MODEL_DIR, file))


def find_similar(query, model, n=10):
    """
    Returns top n words most similar to a query.
    :param query: word (str)
    :param model: loaded embedding model (KeyedVectors or FastTextKeyedVectors object)
    :param n: number of words to return
    :return: a list of tuples
    """
    if isinstance(model, gensim.models.keyedvectors.KeyedVectors):
        try:
            return model.similar_by_word(query, topn=n)
        except KeyError:
            return """This word is unknown to the model. Make sure your query is lowercase. 
                   If it is a diachronic/multilingual model, don't forget to add a language 
                   code to your query, e.g. gaeilge_gle"""
    else:
        return model.wv.similar_by_word(query, topn=n)
