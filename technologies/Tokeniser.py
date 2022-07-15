from nltk.tokenize import word_tokenize


def cardamom_tokenise(string, provenance=None, matrix_language=None):
    """Tokenises a string of text and returns a list containing data for each token dictionaries:

       [{'type': 'token', 'start': int, 'end': int, 'provenance': int}, ...]"""

    # Identify languages currently supported by NLTK's tokeniser.
    nltk_langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french', 'german', 'greek', 'italian',
                  'norwegian', 'polish', 'portuguese', 'russian', 'slovene', 'spanish', 'swedish', 'turkish']

    # Tokenise the string of text using the primary language of the document if supplied.
    if matrix_language:
        if matrix_language in nltk_langs:
            token_list = word_tokenize(string, matrix_language)
        else:
            raise RuntimeError(f'Could not tokenise text. '
                               f'Check language, "{matrix_language}", is supported by tokeniser.')
    else:
        token_list = word_tokenize(string)

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    for token in token_list:
        tok_index = string[current_index:].find(token) + current_index
        tok_dict = {"type": "auto", "start_index": tok_index, "end_index": tok_index + len(token), "provenance": provenance}
        indexed_tokens.append(tok_dict)
        current_index = tok_dict.get("end_index")
    return indexed_tokens


# if __name__ == "__main__":

#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."

#     test_de = "Das lange Zeit verarmte und daher von Auswanderung betroffene Irland " \
#               "hat sich inzwischen zu einer hochmodernen, in manchen Gegenden multikulturellen " \
#               "Industrie- und Dienstleistungsgesellschaft gewandelt. Es hat jährlich 10 " \
#               "Millionen ausländische Touristen (Stand 2017).\n\nLaut einer repräsentativen " \
#               "Umfrage des Worldwide Independent Network und der Gallup International " \
#               "Association, die zwischen 2011 und 2012 durchgeführt wurde, bezeichneten sich " \
#               "zehn Prozent der befragten Iren als „überzeugter Atheist“, 44 Prozent nannten " \
#               "sich „nicht-religiös“ und 47 Prozent gaben an, eine religiöse Person zu sein."

#     # print(cardamom_tokenise(test_de, 1, "german"))
#     print(cardamom_tokenise(test_en, 1, "english"))
