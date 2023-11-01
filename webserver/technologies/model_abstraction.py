import sys
import os
cur_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_file_dir)
from model import TokenModel, POSInstanceModel, RelatedWordModel
from Tokeniser import tokenise
from POS_tag import pos_tag
from embeddings import *


def cardamom_tokenise(string, iso_code=None, reserved_toks=None, uploaded_file_id=None):

    token_models = tokenise(string, iso_code, reserved_toks, uploaded_file_id)

    token_models = [TokenModel(
        reserved_token=tok_mod.get("reserved_token"), start_index=tok_mod.get("start_index"),
        end_index=tok_mod.get("end_index"), token_language_id=tok_mod.get("token_language_id"),
        type_=tok_mod.get("type_"), uploaded_file_id=tok_mod.get("uploaded_file_id")
    ) for tok_mod in token_models]

    return token_models


def cardamom_postag(string, tokens, matrix_language=None):

    pos_models = pos_tag(string, tokens, matrix_language)

    pos_models = [POSInstanceModel(
        token_id=pos_model.get("token_id"), tag=pos_model.get("tag"), type_=pos_model.get("type_")
    ) for pos_model in pos_models]

    return pos_models


def cardamom_find_similar_words(string, iso_code=None):

    model_name, model = load_model(iso_code)
    related_words = find_similar(string, model)
    related_words = [RelatedWordModel(
        query=string, query_language=iso_code, model_name=model_name,
        word=related_word_tpl[0], similarity_score=related_word_tpl[1]
    ) for related_word_tpl in related_words]

    return related_words
