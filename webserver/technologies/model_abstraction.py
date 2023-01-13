# from model import TokenModel, POSInstanceModel
from Tokeniser import tokenise
from POS_tag import pos_tag


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
