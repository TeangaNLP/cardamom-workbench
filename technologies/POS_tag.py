from nltk import pos_tag
from Train_Taggers import train_pos_tagger


def cardamom_postag(string, tokens, provenance, matrix_language=None):

    # Identify languages currently supported by NLTK's POS-tagger.
    nltk_langs = {'en': 'eng', 'ru': 'rus'}
    corp_langs = {'af': 'Afrikaans', 'akk': 'Akkadian', 'aqz': 'Akuntsu', 'sq': 'Albanian', 'am': 'Amharic',
                  'grc': 'Ancient Greek', 'hbo': 'Ancient Hebrew', 'apu': 'Apurina', 'ar': 'Arabic', 'hy': 'Armenian',
                  'aii': 'Assyrian', 'bm': 'Bambara', 'eu': 'Basque', 'bej': 'Beja', 'be': 'Belarusian',
                  'bn': 'Bengali', 'bho': 'Bhojpuri', 'br': 'Breton', 'bg': 'Bulgarian', 'bxr': 'Buryat',
                  'yue': 'Cantonese', 'ca': 'Catalan', 'ceb': 'Cebuano', 'zh': 'Chinese', 'ckt': 'Chukchi',
                  'lzh': 'Classical Chinese', 'cop': 'Coptic', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
                  'nl': 'Dutch', 'en': 'English', 'myv': 'Erzya', 'et': 'Estonian', 'fo': 'Faroese', 'fi': 'Finnish',
                  'fr': 'French', 'qfn': 'Frisian Dutch', 'gl': 'Galician', 'de': 'German', 'got': 'Gothic',
                  'el': 'Greek', 'gub': 'Guajajara', 'gn': 'Guarani', 'he': 'Hebrew', 'hi': 'Hindi',
                  'qhe': 'Hindi English', 'hit': 'Hittite', 'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian',
                  'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese', 'jv': 'Javanese', 'urb': 'Kaapor', 'xnr': 'Kangri',
                  'krl': 'Karelian', 'arr': 'Karo', 'kk': 'Kazakh', 'kfm': 'Khunsari', 'quc': 'Kiche',
                  'koi': 'Komi Permyak', 'kpv': 'Komi Zyrian', 'ko': 'Korean', 'kmr': 'Kurmanji', 'la': 'Latin',
                  'lv': 'Latvian', 'lij': 'Ligurian', 'lt': 'Lithuanian', 'olo': 'Livvi', 'nds': 'Low Saxon',
                  'jaa': 'Madi', 'mpu': 'Makurap', 'mt': 'Maltese', 'gv': 'Manx', 'mr': 'Marathi',
                  'gun': 'Mbya Guarani', 'mdf': 'Moksha', 'myu': 'Munduruku', 'pcm': 'Naija', 'nyq': 'Nayini',
                  'nap': 'Neapolitan', 'sme': 'North Sami', 'no': 'Norwegian', 'cu': 'Old Church Slavonic',
                  'orv': 'Old East Slavic', 'fro': 'Old French', 'sga': 'Old Irish', 'otk': 'Old Turkish',
                  'fa': 'Persian', 'pl': 'Polish', 'qpm': 'Pomak', 'pt': 'Portuguese', 'ro': 'Romanian',
                  'ru': 'Russian', 'sa': 'Sanskrit', 'gd': 'Scottish Gaelic', 'sr': 'Serbian', 'sms': 'Skolt Sami',
                  'sk': 'Slovak', 'sl': 'Slovenian', 'soj': 'Soi', 'ajp': 'South Levantine Arabic', 'es': 'Spanish',
                  'sv': 'Swedish', 'swl': 'Swedish Sign Language', 'gsw': 'Swiss German', 'tl': 'Tagalog',
                  'ta': 'Tamil', 'tt': 'Tatar', 'eme': 'Teko', 'te': 'Telugu', 'th': 'Thai', 'tpn': 'Tupinamba',
                  'tr': 'Turkish', 'qtd': 'Turkish German', 'uk': 'Ukrainian', 'xum': 'Umbrian', 'hsb': 'Upper Sorbian',
                  'ur': 'Urdu', 'ug': 'Uyghur', 'vi': 'Vietnamese', 'wbp': 'Warlpiri', 'cy': 'Welsh',
                  'hyw': 'Western Armenian', 'wo': 'Wolof', 'sjo': 'Xibe', 'sah': 'Yakut', 'yo': 'Yoruba',
                  'ess': 'Yupik'}
    supported_langs = sorted(list(set([i for i in {**corp_langs, **nltk_langs}])))

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

    # Collect a list of all languages used, and train taggers for each one that isn't already supported in NLTK
    tok_langs = sorted(list(set([i.get('language') for i in tokens if i.get('language') not in nltk_langs])))
    tagger_dict = {corp_langs.get(tok_lang): train_pos_tagger(corp_langs.get(tok_lang)) for tok_lang in tok_langs}

    # POS-tag tokens and create output list
    pos_list = [{'type': 'auto-POS', 'start': i.get('start'), 'end': i.get('end'),
                 'pos': pos_tag([i.get('token')], lang=nltk_langs.get(i.get('language')), tagset='universal')[0][1],
                 'provenance': provenance} if i.get('language') in nltk_langs else
                {'type': 'auto-POS', 'start': i.get('start'), 'end': i.get('end'),
                 'pos': tagger_dict.get(corp_langs.get(i.get('language'))).tag([i.get('token')])[0][1],
                 'provenance': provenance} for i in tokens]

    return pos_list


# if __name__ == "__main__":
#
#     from Tokeniser import cardamom_tokenise
#
#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."
#     toks_en = cardamom_tokenise(test_en, 1, 'en')
#
#     # print(cardamom_postag(test_en, toks_en, 2, 'en'))
#
#     # gael_tagger = train_pos_tagger("Irish")
#
#     test_ga = "Chonaic mé mo mhadra ag rith. Thit sé agus é á casadh."
#     toks_ga = cardamom_tokenise(test_ga, 3, 'ga')
#
#     print(cardamom_postag(test_ga, toks_ga, 4, 'ga'))
