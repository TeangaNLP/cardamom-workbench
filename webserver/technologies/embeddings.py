# -*- coding: UTF-8 -*-

import os
import gensim
from typing import Literal

def get_models_by_iso(iso_code: str, MODEL_DIR = '/code/language_models/embeddings'):
    """
    Finds all embedding models for a particular language.
    :param iso_code: ISO 639-3 language code (str)
    :return: list of model names
    """
    lang = "_%s_" % iso_code
    lang_models = []
    for root, dirs, files in os.walk(MODEL_DIR):
        for file in files:
            if lang in file:
                lang_models.append(file)

    return lang_models


def choose_model(lang_models: list, choice: Literal['default', 'diachronic', 'related'] = 'default'):
    """
    :param lang_models: list of model names
    :param choice: which model to return
    :return: a model name (str)
    """
    filtered_models = []

    # filtering the list of model names
    if choice == 'default':
        if len(lang_models) == 1:
            filtered_models = lang_models
        else:
            filtered_models = [m for m in lang_models if "synchronic" in m]
    elif choice == 'diachronic':
        filtered_models = [m for m in lang_models if "diachronic" in m]
    elif choice == 'related':
        filtered_models = [m for m in lang_models if "related" in m]

    # checking if we have any results
    if len(filtered_models) == 0:
        print("No models found")
    else:
        return filtered_models[0]


def load_model(iso_code, compressed=True, binary=True, MODEL_DIR = '/code/language_models/embeddings'):
    """
    Loads a pretrained FastText model.
    :param iso_code: iso_code of a language (str)
    :param compressed: if the model is in compressed w2v format or not
    :param binary: if the model is compressed, is it in binary or text format
    :return: KeyedVectors object or FastTextKeyedVectors object
    """
    if iso_code is not None:
        lang_models = get_models_by_iso(iso_code)
        file = choose_model(lang_models)
        if compressed:
            return file, gensim.models.KeyedVectors.load_word2vec_format(os.path.join(MODEL_DIR, file), binary=binary)
        else:
            return file, gensim.models.FastText.load(os.path.join(MODEL_DIR, file))
    else:
        print("Language is required")


def find_similar(query: str, model, n=10):
    """
    Returns top n words most similar to a query.
    :param query: word (str)
    :param model: loaded embedding model (KeyedVectors or FastTextKeyedVectors object)
    :param n: number of words to return
    :return: a list of similar words
    """
    if isinstance(model, gensim.models.keyedvectors.KeyedVectors):
        try:
            return model.similar_by_word(query, topn=n)
            # return just words, without similarity scores
            # return [result[0] for result in output]
        except KeyError:
            print("""This word is unknown to the model. Make sure your query is lowercase. 
                   If it is a diachronic/multilingual model, don't forget to add a language 
                   code to your query, e.g. gaeilge_gle""")
    else:
        return model.wv.similar_by_word(query, topn=n)
        # return just words, without similarity scores
        # return [result[0] for result in output]
