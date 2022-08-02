from nltk.tokenize import word_tokenize


def cardamom_tokenise(string, provenance=None, iso_code=None, reserved_toks=None):
    """Tokenises a string of text and returns a list containing data for each token dictionaries:

       [{'type': 'auto', 'start_index': int, 'end_index': int, 'provenance': int}, ...]"""

    # Identify languages for which we have corpora.
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

    # Identify languages currently supported by NLTK's tokeniser.
    nltk_langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french',
                  'german', 'greek', 'italian', 'norwegian', 'polish', 'portuguese', 'russian',
                  'slovene', 'spanish', 'swedish', 'turkish']

    # If reserved tokens are passed to the tokeniser, do not alter tokenisation between their indices.
    # Check to make sure reserved tokens are in order, do not overlap, and no duplicates exist.
    # Check to make sure reserved tokens contain the correct data.
    # Separate substrings which can be tokenised from reserved tokens which cannot be tokenised.
    if reserved_toks:
        # Check that reserved tokens are in the correct format (a list of dictionaries),
        # if not raise error with informative message.
        if not isinstance(reserved_toks, list):
            raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                               f"[{{'type': 'auto', 'start_index': 0, 'end_index': 5, 'text_language': 'en',"
                               f"'token_language': 'en', 'provenance': 1}}, {{...}}, ...]\n"
                               f"Instead, got {type(reserved_toks).__name__} class entry:\n{reserved_toks}.")
        for indset in reserved_toks:
            if not isinstance(indset, dict):
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'type': 'auto', 'start_index': 0, 'end_index': 5, 'text_language': 'en',"
                                   f"'token_language': 'en', 'provenance': 1}}, {{...}}, ...]\n"
                                   f"Problem found in '{type(indset).__name__}' class entry: {indset}.")
        stringlist = list()
        current_index = 0
        for indset in reserved_toks:
            # Check that there are no duplicate entries in reserved tokens, if there are raise error.
            if reserved_toks.count(indset) > 1:
                raise RuntimeError(f"Duplicate token found in reserved tokens' list: {indset}")
            # Check that reserved tokens contain the correct key-value pairs, if not raise error.
            checklist = ["type", "start_index", "end_index", "provenance"]
            if not all(data_type in checklist for data_type in indset):
                problem_keys = [key for key in indset if key not in checklist]
                if len(problem_keys) == 1:
                    problem_keys = f"'{problem_keys[0]}'"
                    plurality = ""
                else:
                    plurality = "s"
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\n"
                                   f"Each dict should contain the keys: {checklist}\n"
                                   f"Problem found in key{plurality}: {problem_keys}.")
            if not all(data_type in indset for data_type in checklist):
                problem_keys = [key for key in checklist if key not in indset]
                if len(problem_keys) == 1:
                    problem_keys = f"'{problem_keys[0]}'"
                    plurality = ""
                else:
                    plurality = "s"
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\n"
                                   f"Each dict should contain the keys: {checklist}\n"
                                   f"Key{plurality}, {problem_keys}, missing.")
            tok_type = indset.get("type")
            # Check that the value for the reserved token's form is a string.
            if not isinstance(tok_type, str):
                raise RuntimeError(f"Expected value of type 'str' for key, 'type'. "
                                   f"Got value of type '{type(tok_type).__name__}':\n{indset}")
            elif tok_type != "manual":
                raise RuntimeError(f"Expected value 'manual' for key, 'type'. "
                                   f"Got value '{tok_type}':\n{indset}")
            start_index = indset.get("start_index")
            end_index = indset.get("end_index")
            # Check that values of start_index and end_index indices for reserved tokens are integers. If not, raise error.
            if not all(isinstance(index, int) for index in [start_index, end_index]):
                if not isinstance(start_index, int):
                    raise RuntimeError(f"Expected value of class 'int' for key, 'start_index'. Got class "
                                       f"'{type(start_index).__name__}':\n{indset}")
                elif not isinstance(end_index, int):
                    raise RuntimeError(f"Expected value of class 'int' for key, 'end_index'. Got class "
                                       f"'{type(end_index).__name__}':\n{indset}")
            # Check that reserved tokens are in order of occurrence and do not overlap in the string.
            # If they are out of order or overlap, raise an error.
            if start_index < current_index:
                raise RuntimeError(f"Reserved tokens overlap or are not in order of occurrence.\nStarting index "
                                   f"({start_index}) of token, {indset}, precedes end_index index of preceding token "
                                   f"({current_index}).")
            string_to_tok = string[current_index:start_index]
            stringlist.extend([("^tokenise", string_to_tok), ("^reserved", indset)])
            current_index = end_index
        string_to_end = string[current_index:]
        stringlist.append(("^tokenise", string_to_end))
    # If no reserved tokens are passed to the tokeniser, tokenise the whole string.
    # Create a list containing only the one string and mark it for tokenisation.
    else:
        stringlist = [("^tokenise", string)]

    # Tokenise substrings which are tagged for tokenisation using the primary language of the document if supplied.
    # Add resulting tokens to the token list.
    # Add reserved tokens to the token list without changes.
    token_list = list()
    for substring in stringlist:
        tok_tag = substring[0]
        tok_string = substring[1]
        if tok_tag == "^tokenise":
            if iso_code:
                matrix_language = corp_langs.get(iso_code)
                matrix_language = matrix_language.lower()
                if matrix_language in nltk_langs:
                    token_list.extend(word_tokenize(tok_string, matrix_language))
                else:
                    token_list.extend(word_tokenize(tok_string))
            else:
                token_list.extend(word_tokenize(tok_string))
        elif tok_tag == "^reserved":
            token_list.append(tok_string)

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    for token in token_list:
        # For tokens which have just been tokenised above, create token data for them and add this to indexed list.
        if isinstance(token, str):
            tok_index = string[current_index:].find(token) + current_index
            tok_dict = {"type": "auto", "start_index": tok_index, "end_index": tok_index + len(token),
                        "provenance": provenance}
        # For reserved tokens, make no changes to token data and add it to indexed list.
        elif isinstance(token, dict):
            tok_dict = token
        else:
            raise RuntimeError(f"Unexpected token variable/object type found, class {type(token)}: {token}")
        indexed_tokens.append(tok_dict)
        current_index = tok_dict.get("end_index")

    return indexed_tokens


# if __name__ == "__main__":
#
#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."
#
#     test_de = "Das lange Zeit verarmte und daher von Auswanderung betroffene Irland " \
#               "hat sich inzwischen zu einer hochmodernen, in manchen Gegenden multikulturellen " \
#               "Industrie- und Dienstleistungsgesellschaft gewandelt. Es hat jährlich 10 " \
#               "Millionen ausländische Touristen (Stand 2017).\n\nLaut einer repräsentativen " \
#               "Umfrage des Worldwide Independent Network und der Gallup International " \
#               "Association, die zwischen 2011 und 2012 durchgeführt wurde, bezeichneten sich " \
#               "zehn Prozent der befragten Iren als „überzeugter Atheist“, 44 Prozent nannten " \
#               "sich „nicht-religiös“ und 47 Prozent gaben an, eine religiöse Person zu sein."
#
#     res_toks = [{"type": "manual", "start_index": 51, "end_index": 60, "provenance": 2},
#                 {"type": "manual", "start_index": 153, "end_index": 163, "provenance": 2},
#                 {"type": "manual", "start_index": 165, "end_index": 171, "provenance": 3}]
#
#     # print(cardamom_tokenise(test_de, 1, "de"))
#     # print(cardamom_tokenise(test_en, 1, "en"))
#     print(cardamom_tokenise(test_en, 1, "en", res_toks))
