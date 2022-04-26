from nltk.tokenize import word_tokenize


def cardamom_tokenize(string, language, indices=None):
    """Tokenises a string of text and returns a list of indices for each token within the string.
       Does not tokenise the contents of substrings between reserved indices."""

    # Identify languages currently supported by NLTK's tokeniser.
    nltk_langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french', 'german', 'greek', 'italian',
                  'norwegian', 'polish', 'portuguese', 'russian', 'slovene', 'spanish', 'swedish', 'turkish']

    # If reserved indices are passed to the tokeniser, do not alter tokenisation between those indices.
    # Split the string into substrings which can be tokenised, and which cannot be tokenised.
    if indices:
        stringlist = list()
        current_index = 0
        for indset in indices:
            start = indset[0]
            end = indset[-1]
            string_to_tok = string[current_index:start]
            reserved_token = string[start:end]
            stringlist.extend([("^tokenise", string_to_tok), ("^reserved", reserved_token)])
            current_index = end
        string_to_end = string[current_index:]
        stringlist.append(("^tokenise", string_to_end))
    # If no reserved indices are passed to the tokeniser, tokenise the whole string.
    # Create a list containing only the one string and mark it for tokenisation.
    else:
        stringlist = [("^tokenise", string)]

    # Tokenise substrings which are tagged for tokenisation, add reserved substrings to token list without tokenising.
    if language in nltk_langs:
        token_list = list()
        for substring in stringlist:
            tok_tag = substring[0]
            tok_string = substring[1]
            if tok_tag == "^tokenise":
                token_list.extend(word_tokenize(tok_string, language))
            elif tok_tag == "^reserved":
                token_list.append(tok_string)
    else:
        return "Could not tokenize text. Check language is supported."

    # Iterate through the string to find the indices of each token, add these to a list for output.
    indexed_tokens = list()
    current_index = 0
    for token in token_list:
        tok_index = string[current_index:].find(token) + current_index
        tok_indices = {"start": tok_index, "end": tok_index + len(token), "type": "token", "language": language}
        indexed_tokens.append(tok_indices)
        current_index = tok_indices.get("start")

    return indexed_tokens


# if __name__ == "__main__":
#
#     test_en = "This is some test text. It doesn't say very much. But, it is useful for the sake of testing!\nI " \
#               "hope it works because I don't want it to be a time-waste."
#
#     test_de = "Das lange Zeit verarmte und daher von Auswanderung betroffene Irland hat sich inzwischen zu einer " \
#               "hochmodernen, in manchen Gegenden multikulturellen Industrie- und Dienstleistungsgesellschaft " \
#               "gewandelt. Es hat jährlich 10 Millionen ausländische Touristen (Stand 2017).\n\nLaut einer " \
#               "repräsentativen Umfrage des Worldwide Independent Network und der Gallup International Association, " \
#               "die zwischen 2011 und 2012 durchgeführt wurde, bezeichneten sich zehn Prozent der befragten Iren " \
#               "als „überzeugter Atheist“, 44 Prozent nannten sich „nicht-religiös“ und 47 Prozent gaben an, eine " \
#               "religiöse Person zu sein."
#
#     no_tok = [(39, 48), (141, 151)]
#
#     # print(cardamom_tokenize(test_en, "english"))
#     # print(cardamom_tokenize(test_de, "german"))
#     print(cardamom_tokenize(test_en, "english", indices=no_tok))
