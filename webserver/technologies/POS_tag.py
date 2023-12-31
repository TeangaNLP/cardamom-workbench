from UD_Parser import load_langsupport
from Train_Taggers import load_tagger


def pos_tag(string, tokens, matrix_language=None):

    # Identify languages currently supported by NLTK's POS-tagger.
    corp_langs = load_langsupport()
    supported_langs = sorted(list(set([i for i in corp_langs])))

    # Get tokens from string using their indices, add them to token dictionaries in list.
    tokens = [{**i, **{'token': string[i.get('start_index'):i.get('end_index')]}} for i in tokens
              if i.get('type_') in ['auto', 'manual']]

    unexpected_substrings = ["\\n", "\\\\", "\\\"", "\\'"]
    for retrieved_tok in tokens:
        from_text = retrieved_tok.get("token")
        if any(substring in from_text for substring in unexpected_substrings):
            found_substring = [i for i in unexpected_substrings if i in from_text]
            if len(found_substring) > 1:
                plurality = "s"
            else:
                plurality = ""
                found_substring = found_substring[0]
            raise RuntimeError(f"Cannot POS-tag text."
                               f"\n    Token \"{from_text}\", at index {retrieved_tok.get('start_index')}, "
                               f"contains unexpected substring{plurality}, \"{found_substring}\"."
                               f"\n    Ensure alignment of text with token indices: "
                               f"({retrieved_tok.get('start_index')} - {retrieved_tok.get('end_index')}).")

    # Reduce list to only tokens with a language identified
    if matrix_language:
        tokens = [i if i.get('token_language_id') else {**i, **{'token_language_id': matrix_language}} for i in tokens]
    else:
        tokens = [{**i, **{'token_language_id': i.get('token_language_id')}} for i in tokens
                  if i.get('token_language_id')]

    # Reduce list to only tokens with a supported language
    tokens = [i for i in tokens if i.get('token_language_id') in supported_langs]

    # Collect a list of all languages used, and load taggers for each one
    tok_langs = sorted(list(set([i.get('token_language_id') for i in tokens])))
    tagger_dict = {corp_langs.get(tok_lang): load_tagger(corp_langs.get(tok_lang)) for tok_lang in tok_langs}

    # POS-tag tokens and create output list
    pos_list = [{"token_id": i.get("id"),
                 "tag": tagger_dict.get(corp_langs.get(i.get('token_language_id'))).tag([i.get('token').lower()])[0][1],
                 "type_": "auto"} for i in tokens]

    return pos_list


# if __name__ == "__main__":
#
#     from Tokeniser import tokenise
#
#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."
#     toks_en = tokenise(test_en, 'en')
#     for tok_no, tok in enumerate(toks_en):
#         tok["id"] = tok_no
#
#     print(pos_tag(test_en, toks_en, 'en'))
#
#     test_ga = "Chonaic mé mo mhadra ag rith. Thit sé agus é á casadh."
#     toks_ga = tokenise(test_ga, 'ga')
#     for tok_no, tok in enumerate(toks_ga):
#         tok["id"] = tok_no
#
#     print(pos_tag(test_ga, toks_ga, 'ga'))
#
#     test_la = (
#         "NEQVEPORROQVISQVAMESTQVIDOLOREMIPSVMQVIADOLORSITAMETCONSECTETVRADIPISCIVELIT\n\n"
#         "NEQVE·PORRO·QVISQVAM·EST·QVI·DOLOREM·IPSVM·QVIA·DOLOR·SIT·AMET·CONSECTETVR·ADIPISCI·VELIT\n\n"
#         "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit"
#     )
#     toks_la = tokenise(test_la, 'la')
#     for tok_no, tok in enumerate(toks_la):
#         tok["id"] = tok_no
#
#     print([i.get("tag") for i in pos_tag(test_la, toks_la, 'la')])
