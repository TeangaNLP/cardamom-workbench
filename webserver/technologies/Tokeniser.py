from UD_Parser import create_isodict
from nltk.tokenize import word_tokenize
import regex as re
import os
import platform


op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"


def discrete_tokenise(string, language):
    supported = ['latin', 'old irish']

    if language not in supported:
        raise RuntimeError(f"Language, {language}, passed to Cardamom tokeniser, but language is not supported.")

    elif language == 'latin':
        toks = word_tokenize(string)

        # Replace double quotes which are broken by NLTK during tokenisation
        toks = [tok if tok not in ["``", "''"] else '"' for tok in toks]

        # Separate word tokens from single quotes where they have been combined
        for toknum, token in enumerate(toks):
            try:
                if len(token) > 1 and token[0] == "'":
                    toks = toks[:toknum] + [token[:1], token[1:]] + toks[toknum + 1:]
            except KeyError:
                pass

        # Separate tokens where, in Latin text, words are separated using the interpunct instead of spacing
        for index, token in enumerate(toks):
            if "·" in token:
                subtoks = token.split("·")
                subtoks = [[i, "·"] for i in subtoks]
                subtoks = [a for b in subtoks for a in b][:-1]
                toks = toks[:index] + subtoks + toks[index + 1:]

    elif language == 'old irish':
        saved_indices = list()

        # Save indices of enclosing punctus, eg. ".i."
        pucnt_pat = re.compile(r'(((?<=\s)|(?<=^))[.·]\w{1,5}[.·](?=\s|$))')
        pucnt_patitir = pucnt_pat.finditer(string)
        if pucnt_patitir:
            for patfind in pucnt_patitir:
                if patfind.group()[0] == patfind.group()[-1]:
                    saved_indices.append(patfind.span())

        # Save indices of punctuation marking verbal stress
        stressed_pat = re.compile(r'(((?<=\s\w+)|(?<=^\w+))[.·-](?=\w+\s|$))')
        stressed_patitir = stressed_pat.finditer(string)
        if stressed_patitir:
            for patfind in stressed_patitir:
                saved_indices.append(patfind.span())
        saved_indices = sorted(saved_indices)

        # Tokenise strings between saved indices, and recombine with the tokens between the saved indices
        token_list = list()
        cur_ind = 0
        for indeces in saved_indices:
            next_ind = indeces[0]
            this_string = string[cur_ind:next_ind]
            if this_string:
                token_list.append(word_tokenize(this_string))
            token_list.append([string[indeces[0]:indeces[1]]])
            cur_ind = indeces[1]
        last_string = string[cur_ind:]
        if last_string:
            token_list.append(word_tokenize(last_string))

        # Replace double quotes which are broken by NLTK during tokenisation
        token_list = [tok if tok not in ["``", "''"] else '"' for tok in token_list]

        # Separate word tokens from single quotes where they have been combined
        for toknum, token in enumerate(token_list):
            try:
                if len(token) > 1 and token[0] == "'":
                    token_list = token_list[:toknum] + [token[:1], token[1:]] + token_list[toknum + 1:]
            except KeyError:
                pass

        toks = [a for b in token_list for a in b]

    else:
        raise RuntimeError(f"Language, {language}, passed to Cardamom tokeniser, "
                           f"should be supported but cannot be found.")

    return toks


def tokenise(string, iso_code=None, reserved_toks=None, uploaded_file_id=None):
    """Tokenises a string of text and returns a list containing data for each token.
       Data for each token appears in the form of a discrete dictionary:

       [{"reserved_token": False, "start_index": int, "end_index": int, "token_language_id": iso_code,
         "type_": "auto", "uploaded_file_id": uploaded_file_id}, {...}, ...]"""

    # Identify languages for which we have corpora.
    corp_langs = create_isodict()

    # Identify languages currently supported by NLTK's tokeniser.
    nltk_langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french',
                  'german', 'greek', 'italian', 'norwegian', 'polish', 'portuguese', 'russian',
                  'slovene', 'spanish', 'swedish', 'turkish']
    # Identify languages currently supported by Cardamom's tokenisation.
    cardamom_langs = ['latin', 'old irish']

    # If reserved tokens are passed to the tokeniser, do not alter tokenisation between their indices.
    # Check to make sure reserved tokens are in order, do not overlap, and no duplicates exist.
    # Check to make sure reserved tokens contain the correct data.
    # Separate substrings which can be tokenised from reserved tokens which cannot be tokenised.
    if reserved_toks:
        # Check that reserved tokens are in the correct format (a list of dictionaries),
        # if not raise error with informative message.
        if not isinstance(reserved_toks, list):
            raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                               f"[{{'reserved_token': False, 'start_index': 0, 'end_index': 5,"
                               f"'token_language_id': 'en', 'type_': 'auto', 'uploaded_file_id': 1}}, {{...}}, ...]\n"
                               f"Instead, got {type(reserved_toks).__name__} class entry:\n{reserved_toks}."
                               )
        for indset in reserved_toks:
            if not isinstance(indset, dict):
                raise RuntimeError(f"\nExpected array of reserved tokens where each token is of type 'dict',\neg. "
                                   f"[{{'reserved_token': False, 'start_index': 0, 'end_index': 5,"
                                   f"'token_language_id': 'en', 'type_': 'auto', 'uploaded_file_id': 1}}, {{...}},"
                                   f"...]\n"
                                   f"Problem found in '{type(indset).__name__}' class entry: {indset}.")
        stringlist = list()
        current_index = 0
        for indset in reserved_toks:

            # Check that there are no duplicate entries in reserved tokens, if there are raise error.
            if reserved_toks.count(indset) > 1:
                raise RuntimeError(f"Duplicate token found in reserved tokens' list: {indset}")

            # Check that reserved tokens contain the correct key-value pairs, if not raise error.
            checklist = ["reserved_token", "start_index", "end_index", "token_language_id", "type_", "uploaded_file_id"]
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

            tok_type = indset.get("type_")
            # Check that the value for the reserved token's form is a string.
            if not isinstance(tok_type, str):
                raise RuntimeError(f"Expected value of type 'str' for key, 'type'. "
                                   f"Got value of type '{type(tok_type).__name__}':\n{indset}")
            elif tok_type != "manual":
                raise RuntimeError(f"Expected value 'manual' for key, 'type'. "
                                   f"Got value '{tok_type}':\n{indset}")

            start_index = indset.get("start_index")
            end_index = indset.get("end_index")
            # Check that values of start_index and end_index indices for reserved tokens are integers
            # If not, raise error.
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
                raise RuntimeError(f"Reserved tokens overlap or are not in order of occurrence.\nstart_indexing index "
                                   f"({start_index}) of token, {indset}, precedes end_index index of preceding token "
                                   f"({current_index}).")
            string_to_tok = string[current_index:start_index]
            stringlist.extend([("^tokenise", string_to_tok), ("^reserved", indset)])
            current_index = end_index
        string_to_end_index = string[current_index:]
        stringlist.append(("^tokenise", string_to_end_index))

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
                elif matrix_language in cardamom_langs:
                    token_list.extend(discrete_tokenise(tok_string, matrix_language))
                else:
                    token_list.extend(word_tokenize(tok_string))
            else:
                token_list.extend(word_tokenize(tok_string))
        elif tok_tag == "^reserved":
            token_list.append(tok_string)

    # Replace double quotes which are broken by NLTK during tokenisation
    token_list = [tok if tok not in ["``", "''"] else '"' for tok in token_list]

    # Separate word tokens from single quotes where they have been combined
    for toknum, token in enumerate(token_list):
        try:
            if len(token) > 1 and token[0] == "'":
                token_list = token_list[:toknum] + [token[:1], token[1:]] + token_list[toknum + 1:]
        except KeyError:
            pass

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    for token in token_list:

        # For tokens which have just been tokenised above, create token data for them and add this to indexed list.
        if isinstance(token, str):
            tok_index = string[current_index:].find(token) + current_index
            tok_dict = {"reserved_token": False, "start_index": tok_index, "end_index": tok_index + len(token),
                        "token_language_id": iso_code, "type_": "auto", "uploaded_file_id": uploaded_file_id}

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
#               "hat sich inzwischen zu einer hochmodernen, in manchen Gegend_indexen multikulturellen " \
#               "Industrie- und Dienstleistungsgesellschaft gewandelt. Es hat jährlich 10 " \
#               "Millionen ausländische Touristen (Stand 2017).\n\nLaut einer repräsentativen " \
#               "Umfrage des Worldwide Independ_indexent Network und der Gallup International " \
#               "Association, die zwischen 2011 und 2012 durchgeführt wurde, bezeichneten sich " \
#               "zehn Prozent der befragten Iren als „überzeugter Atheist“, 44 Prozent nannten " \
#               "sich „nicht-religiös“ und 47 Prozent gaben an, eine religiöse Person zu sein."
#
#     res_toks_en = [{"reserved_token": True, "start_index": 51, "end_index": 60, "token_language_id": "en",
#                     "type_": "manual", "uploaded_file_id": 2},
#                    {"reserved_token": True, "start_index": 153, "end_index": 163, "token_language_id": "en",
#                     "type_": "manual", "uploaded_file_id": 2},
#                    {"reserved_token": True, "start_index": 165, "end_index": 171, "token_language_id": "ga",
#                     "type_": "manual", "uploaded_file_id": 3}]
#
#     # print(tokenise(test_de, "de"))
#     # print(tokenise(test_en, "en"))
#     # print(tokenise(test_en, "en", res_toks_en))
#     for token in tokenise(test_en, "en", res_toks_en):
#         print(f"{test_en[token.get('start_index'):token.get('end_index')]}: {token.get('reserved_token')}")
#
#
#     test_la = 'NEQVEPORROQVISQVAMESTQVIDOLOREMIPSVMQVIADOLORSITAMETCONSECTETVRADIPISCIVELIT\n\n' \
#               'NEQVE·PORRO·QVISQVAM·EST·QVI·DOLOREM·IPSVM·QVIA·DOLOR·SIT·AMET·CONSECTETVR·ADIPISCI·VELIT\n\n' \
#               'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit'
#
#     print(discrete_tokenise(test_la, 'latin'))
#     print(tokenise(test_la, "la"))
#
#     test_sga = '.i. biuusa ocirbáig darfarcennsi frimaccidóndu\n\n' \
#                '.i. ni·arformut fribsi as·biursa ·inso· arropad maith limsa labrad ilbelre dúibsi\n\n' \
#                '.i. isipersin crist dagníusa sin\n\n' \
#                '.i. ó dom·anicc foirbthetu ní denim gnímu macthi act rísam nem bimmi æcni et bimmi foirbthi uili\n\n' \
#                '.i. isocprecept soscéli attó\n\n' \
#                '.i. ished inso noguidimm .i. ' \
#                'conducaid etargne ṅ dǽ et conaroib temel innatol domunde tarrosc fornanme\n\n' \
#                '.i. hore nondobmolorsa et nom móidim indib\n\n.i. amal nondafrecṅdirccsa\n\n' \
#                '.i. is inse ṅduit nitú nodnai(l) acht ishé not ail\n\n' \
#                '.i. madarlóg pridchasa .i. armetiuth et mothoschith nímbia fochricc dar hési moprecepte\n\n' \
#                '.i. coníarimse peccad libsi uili ɫ. aratartsa fortacht dúibsi arnap trom fuirib fornóinur\n\n' \
#                '.i. cote mothorbese dúib madamne labrar\n\n.i. nihed notbeir ínem ciabaloingthech\n\n' \
#                'Acht nammáa issamlid istorbe són co etercerta anasbera et conrucca inætarcne cáich\n\n' \
#                '.i. léic uáit innabiada mílsi ettomil innahí siu dommeil do chenél arnáphé som conéit détso\n\n' \
#                '.i. isamlid dorígeni dia corp duini ó ilballaib\n\n.i. act basamlid dúib cid immeícndarcus'
#
#     print(discrete_tokenise(test_sga, 'old irish'))
#     print(tokenise(test_sga, "sga"))
#
#     # identify directories
#     tech_dir = os.getcwd()
#     if f"{slash}code" in tech_dir:
#         main_dir = tech_dir
#     else:
#         main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
#     webserver_dir = main_dir + f"{slash}webserver"
#
#     # navigate to directory containing UD corpora
#     os.chdir(webserver_dir)
#
#     file_name = "test_file.txt"
#     with open(file_name, encoding='utf-8') as test_file:
#         test_text = test_file.read()
#
#     # return to technologies directory
#     os.chdir(tech_dir)
#
#     tokens = tokenise(test_text, "en")
#     tok_list = [test_text[token.get("start_index"):token.get("end_index")] for token in tokens]
#     print(" ".join(tok_list))
