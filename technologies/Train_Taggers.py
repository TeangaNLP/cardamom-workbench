import os
from decimal import *
import nltk
from conllu import parse
from nltk import word_tokenize, sent_tokenize


def list_pos_langs():

    # identify directories
    tech_dir = os.getcwd()
    main_dir = tech_dir[:tech_dir.index("\\technologies")]
    corpora_dir = main_dir + "\\CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + "\\ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora])
    )
    os.chdir(latest_corpus)

    # identify available treebanks
    treebanks = os.listdir()

    # identify languages of available treebanks
    languages = sorted(list(set([" ".join(i[3:i.index("-")].split("_")) for i in treebanks])))

    # return to technologies directory
    os.chdir(tech_dir)

    return languages


def get_treebank_names(language):

    # identify directories
    tech_dir = os.getcwd()
    main_dir = tech_dir[:tech_dir.index("\\technologies")]
    corpora_dir = main_dir + "\\CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + "\\ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora])
    )
    os.chdir(latest_corpus)

    # identify available treebanks
    all_treebanks = os.listdir()

    # identify treebanks for the selected language
    treebanks = [tb for tb in all_treebanks if "UD_" + "_".join(language.split(" ")) + "-" in tb]

    # return to technologies directory
    os.chdir(tech_dir)

    return treebanks


def get_treebanks(language):

    # find treebanks available for the language
    available_treebanks = get_treebank_names(language)

    # identify directories
    tech_dir = os.getcwd()
    main_dir = tech_dir[:tech_dir.index("\\technologies")]
    corpora_dir = main_dir + "\\CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + "\\ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora])
    )
    os.chdir(latest_corpus)

    # extract data from each treebank and put in a list
    treebanks = list()
    for treebank in available_treebanks:
        os.chdir(latest_corpus + "\\" + treebank)
        available_files = os.listdir()
        train_file = [file for file in available_files if "-ud-train.conllu" in file]
        if len(train_file) > 1:
            raise RuntimeError(f"Found too many training files in a single treebank:\n    {train_file}")
        elif len(train_file) == 1:
            train_file = train_file[0]
            with open(train_file, encoding='utf-8') as conllu_file:
                treebanks.append(parse(conllu_file.read()))
        os.chdir(latest_corpus)

    # return to technologies directory
    os.chdir(tech_dir)

    # combine sentences from all treebanks
    combined_banks = list()
    for tree in treebanks:
        for sentence in tree:
            combined_banks.append(sentence)

    return combined_banks


def get_pos_tags(language):

    # collect the CoNLL-U files for the language
    treebanks = get_treebanks(language)

    # extract UD POS-tags for each treebank
    pos_tags = [[(token.get("form"), token.get("upos")) for token in sentence] for sentence in treebanks]

    return pos_tags


def train_pos_tagger(language):

    # load in the pos-tagged corpus
    pos_tagged_text = get_pos_tags(language)

    # train the tagger
    pos_tagger = nltk.UnigramTagger(pos_tagged_text)

    return pos_tagger


# if __name__ == "__main__":
#
#     # available_languages = list_pos_langs()
#     # print(len(available_languages))
#     # print(available_languages)
#
#     # print(get_treebank_names("Irish"))
#     # print(get_treebanks("Ancient Greek"))
#     # print(get_pos_tags("English"))
#
#     gael_tagger = train_pos_tagger("Irish")
#
#     test = "Chonaic mé mo mhadra ag rith. Thit sé agus é á casadh."
#     tokens = ([word_tokenize(sent) for sent in sent_tokenize(test)])
#
#     print(list(gael_tagger.tag([word.lower() for word in sent]) for sent in tokens))
