from nltk.tokenize import word_tokenize


def cardamom_tokenise(string, text_language, reserved_toks=None):
    """Tokenises a string of text and returns a list containing data for each token in the in a dictionary:

       [{'token': 'str', 'start': int, 'end': int, 'reserved_token': bool,
       'text_language': 'str', 'token_language': 'str'}, ...]

       A list of reserved tokens which have been manually annotated can be supplied as an argument, these will be
       passed through without being affected."""

    # Identify languages currently supported by NLTK's tokeniser.
    nltk_langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french', 'german', 'greek', 'italian',
                  'norwegian', 'polish', 'portuguese', 'russian', 'slovene', 'spanish', 'swedish', 'turkish']

    # If reserved tokens are passed to the tokeniser, do not alter tokenisation between their indices.
    # Check to make sure reserved tokens are in order, do not overlap, and no duplicates exist.
    # Check to make sure reserved tokens contain the correct data.
    # Separate substrings which can be tokenised from reserved tokens which cannot be tokenised.
    if reserved_toks:
        # Check that reserved tokens are in the correct format, if not raise error with informative message.
        if not isinstance(reserved_toks, list):
            raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                               f"[{{'token': 'Hello', 'start': 0, 'end': 5, 'reserved_token': True, "
                               f"'text_language': 'english', 'token_language': 'english'}}, {{...}} ...].\n"
                               f"Instead, got {type(reserved_toks).__name__} class entry: {reserved_toks}.")
        for indset in reserved_toks:
            if not isinstance(indset, dict):
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'token': 'Hello', 'start': 0, 'end': 5, 'reserved_token': True, "
                                   f"'text_language': 'english', 'token_language': 'english'}}, {{...}} ...].\n"
                                   f"Problem found in '{type(indset).__name__}' class entry: {indset}.")
        stringlist = list()
        current_index = 0
        for indset in reserved_toks:
            # Check that there are no duplicate entries in reserved tokens, if there are raise error.
            if reserved_toks.count(indset) > 1:
                raise RuntimeError(f"Duplicate token found in reserved tokens' list: {indset}")
            # Check that reserved tokens contain the correct key-value pairs, if not raise error.
            checklist = ["token", "start", "end", "reserved_token", "text_language", "token_language"]
            if not all(data_type in checklist for data_type in indset):
                problem_keys = [key for key in indset if key not in checklist]
                if len(problem_keys) == 1:
                    problem_keys = f"'{problem_keys[0]}'"
                    plurality = ""
                else:
                    plurality = "s"
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'token': 'Hello', 'start': 0, 'end': 5, 'reserved_token': True, "
                                   f"'text_language': 'english', 'token_language': 'english'}}, {{...}} ...].\n"
                                   f"Problem found in key{plurality}: {problem_keys}.")
            if not all(data_type in indset for data_type in checklist):
                problem_keys = [key for key in checklist if key not in indset]
                if len(problem_keys) == 1:
                    problem_keys = f"'{problem_keys[0]}'"
                    plurality = ""
                else:
                    plurality = "s"
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'token': 'Hello', 'start': 0, 'end': 5, reserved_token': True, "
                                   f"'text_language': 'english', 'token_language': 'english'}}, {{...}} ...].\n"
                                   f"Key{plurality}, {problem_keys}, missing.")
            tok_form = indset.get("token")
            # Check that the value for the reserved token's form is a string.
            if not isinstance(tok_form, str):
                raise RuntimeError(f"Expected value 'str' for key, 'token'. Got {type(tok_form).__name__}\n{indset}")
            start = indset.get("start")
            end = indset.get("end")
            # Check that values of start and end indices for reserved tokens are integers. If not, raise error.
            if not all(isinstance(index, int) for index in [start, end]):
                if not isinstance(start, int):
                    raise RuntimeError(f"Expected value of class 'int' for key, 'start'. Got class "
                                       f"'{type(start).__name__}':\n{indset}")
                elif not isinstance(end, int):
                    raise RuntimeError(f"Expected value of class 'int' for key, 'end'. Got class "
                                       f"'{type(end).__name__}':\n{indset}")
            reserved = indset.get("reserved_token")
            # Check that all values for identifying reserved tokens are Boolean.
            if not isinstance(reserved, bool):
                raise RuntimeError(f"Expected of class 'bool' for key, 'reserved_token'. Got class "
                                   f"'{type(reserved).__name__}':\n{indset}")
            # Check that all tokens reserved tokens supplied are identified as reserved tokens.
            if not reserved:
                raise RuntimeError("Expected Boolean value True for key, 'reserved_token'. Got value False")
            # Check that reserved tokens are in order of occurrence and do not overlap in the string.
            # If they are out of order or overlap, raise an error.
            if start < current_index:
                raise RuntimeError(f"Reserved tokens overlap or are not in order of occurrence.\nStarting index "
                                   f"({start}) of token, {indset}, precedes end index of preceding token "
                                   f"({current_index}).")
            string_to_tok = string[current_index:start]
            reserved_token = string[start:end]
            # Raise an error if the reserved token does not match the text in the string between the provided indices.
            if tok_form != reserved_token:
                raise RuntimeError(f'Reserved token, "{tok_form}", did not match text in string, "{reserved_token}", '
                                   f'from index {start} to index {end}.')
            stringlist.extend([("^tokenise", string_to_tok), ("^reserved", indset)])
            current_index = end
        string_to_end = string[current_index:]
        stringlist.append(("^tokenise", string_to_end))
    # If no reserved tokens are passed to the tokeniser, tokenise the whole string.
    # Create a list containing only the one string and mark it for tokenisation.
    else:
        stringlist = [("^tokenise", string)]

    # Tokenise substrings which are tagged for tokenisation and add resulting tokens to the token list.
    # Add reserved tokens to the token list without changes.
    if text_language in nltk_langs:
        token_list = list()
        for substring in stringlist:
            tok_tag = substring[0]
            tok_string = substring[1]
            if tok_tag == "^tokenise":
                token_list.extend(word_tokenize(tok_string, text_language))
            elif tok_tag == "^reserved":
                token_list.append(tok_string)
    else:
        raise RuntimeError(f'Could not tokenise text. Check language, "{text_language}", is supported by tokeniser.')

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    for token in token_list:
        # For tokens which have just been tokenised above, create token data for them and add this to indexed list.
        if isinstance(token, str):
            tok_index = string[current_index:].find(token) + current_index
            tok_dict = {"token": token, "start": tok_index, "end": tok_index + len(token),
                        "reserved_token": False, "text_language": text_language, "token_language": text_language}
        # For reserved tokens, make no changes to token data and add it to indexed list.
        elif isinstance(token, dict):
            tok_dict = token
        else:
            raise RuntimeError(f"Unexpected token variable/object type found, class {type(token)}: {token}")
        indexed_tokens.append(tok_dict)
        current_index = tok_dict.get("end")

    return indexed_tokens


# if __name__ == "__main__":
#
#     test_en = "This is some test text. It doesn't say very much. But, it is useful for the sake of testing!\nI " \
#               "hope it works because I don't want it to be a time-waste. Críoch."
#
#     test_de = "Das lange Zeit verarmte und daher von Auswanderung betroffene Irland hat sich inzwischen zu einer " \
#               "hochmodernen, in manchen Gegenden multikulturellen Industrie- und Dienstleistungsgesellschaft " \
#               "gewandelt. Es hat jährlich 10 Millionen ausländische Touristen (Stand 2017).\n\nLaut einer " \
#               "repräsentativen Umfrage des Worldwide Independent Network und der Gallup International Association, " \
#               "die zwischen 2011 und 2012 durchgeführt wurde, bezeichneten sich zehn Prozent der befragten Iren " \
#               "als „überzeugter Atheist“, 44 Prozent nannten sich „nicht-religiös“ und 47 Prozent gaben an, eine " \
#               "religiöse Person zu sein."
#
#     no_tok = [{"token": "very much", "start": 39, "end": 48, "reserved_token": True,
#                "text_language": "english", "token_language": "english"},
#               {"token": "time-waste", "start": 141, "end": 151, "reserved_token": True,
#                "text_language": "english", "token_language": "english"},
#               {"token": "Críoch", "start": 153, "end": 159, "reserved_token": True,
#                "text_language": "english", "token_language": "irish"}]
#
#     # print(cardamom_tokenise(test_en, "english"))
#     # print(cardamom_tokenise(test_de, "german"))
#     print(cardamom_tokenise(test_en, "english", reserved_toks=no_tok))
