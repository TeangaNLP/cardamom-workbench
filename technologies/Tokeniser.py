from nltk.tokenize import word_tokenize
from datetime import date, datetime


def cardamom_tokenise(string, log_data, text_language=None, reserved_toks=None):
    """Tokenises a string of text and returns a list containing data for each token in the in a dictionary:

       [{'type': 'token', 'start': int, 'end': int, 'text_language': str, 'token_language': str, 'data': dict},
       ...]

       Each token will contain a 'data' key, which will allow the pass-through of log data from the workbench:

       {... 'data': {'user_id': int, 'time': str, 'date': str, 'reserved': bool}}

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
                               f"[{{'type': 'token', 'start': 0, 'end': 5, 'text_language': 'english',"
                               f"'token_language': 'english', 'data': {{'user_id': int, 'time': str, 'date': str, "
                               f"'reserved': bool}}}}, {{...}}, ...]\nInstead, got {type(reserved_toks).__name__} "
                               f"class entry:\n{reserved_toks}.")
        for indset in reserved_toks:
            if not isinstance(indset, dict):
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'type': 'token', 'start': 0, 'end': 5, 'text_language': 'english',"
                                   f"'token_language': 'english', 'data': {{'user_id': int, 'time': str, 'date': str, "
                                   f"'reserved': bool}}}}, {{...}}, ...]\nProblem found in '{type(indset).__name__}' "
                                   f"class entry: {indset}.")
        stringlist = list()
        current_index = 0
        for indset in reserved_toks:
            # Check that there are no duplicate entries in reserved tokens, if there are raise error.
            if reserved_toks.count(indset) > 1:
                raise RuntimeError(f"Duplicate token found in reserved tokens' list: {indset}")
            # Check that reserved tokens contain the correct key-value pairs, if not raise error.
            checklist = ["type", "start", "end", "text_language", "token_language", "data"]
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
            elif tok_type != "token":
                raise RuntimeError(f"Expected value 'token' for key, 'type'. "
                                   f"Got value '{tok_type}':\n{indset}")
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
            reserved = indset.get("data").get("reserved")
            # Check that all values for identifying reserved tokens are Boolean.
            if not isinstance(reserved, bool):
                raise RuntimeError(f"Expected of class 'bool' for key, 'reserved'. Got class "
                                   f"'{type(reserved).__name__}':\n{indset}")
            # Check that all tokens reserved tokens supplied are identified as reserved tokens.
            if not reserved:
                raise RuntimeError("Expected Boolean value True for key, 'reserved'. Got value False")
            # Check that reserved tokens are in order of occurrence and do not overlap in the string.
            # If they are out of order or overlap, raise an error.
            if start < current_index:
                raise RuntimeError(f"Reserved tokens overlap or are not in order of occurrence.\nStarting index "
                                   f"({start}) of token, {indset}, precedes end index of preceding token "
                                   f"({current_index}).")
            string_to_tok = string[current_index:start]
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
    token_list = list()
    for substring in stringlist:
        tok_tag = substring[0]
        tok_string = substring[1]
        if tok_tag == "^tokenise":
            if text_language:
                if text_language in nltk_langs:
                    token_list.extend(word_tokenize(tok_string, text_language))
                else:
                    raise RuntimeError(f'Could not tokenise text. '
                                       f'Check language, "{text_language}", is supported by tokeniser.')
            else:
                token_list.extend(word_tokenize(tok_string))
        elif tok_tag == "^reserved":
            token_list.append(tok_string)

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    user_id = log_data.get("user_id")
    user_time = log_data.get("time")
    user_date = log_data.get("date")
    for token in token_list:
        # For tokens which have just been tokenised above, create token data for them and add this to indexed list.
        if isinstance(token, str):
            tok_index = string[current_index:].find(token) + current_index
            tok_dict = {"type": "token", "start": tok_index, "end": tok_index + len(token),
                        "text_language": text_language, "token_language": text_language, "data":
                            {'user_id': user_id, 'time': user_time, 'date': user_date, 'reserved': False}}
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
#     res_toks = [{"type": "token", "start": 39, "end": 48, "text_language": "english", "token_language": "english",
#                  "data": {"user_id": 3, "time": "13:53:35", "date": "02/04/2022", "reserved": True}},
#                 {"type": "token", "start": 141, "end": 151, "text_language": "english", "token_language": "english",
#                  "data": {"user_id": 3, "time": "13:53:35", "date": "02/04/2022", "reserved": True}},
#                 {"type": "token", "start": 153, "end": 159, "text_language": "english", "token_language": "irish",
#                  "data": {"user_id": 2, "time": "09:22:18", "date": "23/04/2022", "reserved": True}}]
#
#     test_data = {"user_id": 1, "time": datetime.now().strftime("%H:%M:%S"), "date": date.today().strftime("%d/%m/%Y")}
#
#     # print(cardamom_tokenise(test_en, test_data, "english"))
#     # print(cardamom_tokenise(test_de, test_data, "german"))
#     print(cardamom_tokenise(test_en, test_data, "english", res_toks))
