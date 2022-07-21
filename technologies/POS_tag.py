from nltk import pos_tag


def cardamom_postag(string, tokens, provenance, matrix_language=None):

    # Identify languages currently supported by NLTK's POS-tagger.
    nltk_langs = {'en': 'eng', 'ru': 'rus'}
    cardamom_langs = {'ga': 'Irish', 'la': 'Latin', 'sga': 'Old Irish'}
    supported_langs = {**nltk_langs, **cardamom_langs}

    # Get tokens from string using their indices, add them to token dictionaries in list.
    tokens = [{**i, **{'token': string[i.get('start'):i.get('end')]}} for i in tokens
              if i.get('type') in ['auto', 'manual']]

    # Reduce list to only tokens with a language identified
    if matrix_language:
        tokens = [i if i.get('language') else {**i, **{'language': matrix_language}} for i in tokens]
    else:
        tokens = [{**i, **{'language': i.get('language')}} for i in tokens if i.get('language')]

    # Reduce list to only tokens with a supported language
    tokens = [i for i in tokens if i.get('language') in supported_langs]

    # POS-tag tokens and greate output list
    pos_list = [{'type': 'POS-tag', 'start': i.get('start'), 'end': i.get('end'),
                 'pos': pos_tag([i.get('token')], lang=supported_langs.get(i.get('language')))[0][1],
                 'provenance': provenance} for i in tokens]

    return pos_list


# if __name__ == "__main__":
#
#     from Tokeniser import cardamom_tokenise
#
#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."
#
#     toks_en = cardamom_tokenise(test_en, 1, 'en')
#
#     print(cardamom_postag(test_en, toks_en, 2, 'en'))
