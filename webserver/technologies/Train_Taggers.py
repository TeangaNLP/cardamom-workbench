import os
import platform
from decimal import *
import nltk
from conllu import parse
from ast import literal_eval
import json
from nltk import word_tokenize, sent_tokenize
import pickle as pk

op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"


def list_pos_langs():

    # identify directories
    tech_dir = os.getcwd()
    main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + f"{slash}ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora if "ud-treebanks-v" in corpus])
    )
    os.chdir(latest_corpus)

    # identify available treebanks
    treebanks = os.listdir()

    # identify languages of available treebanks
    languages = sorted(list(set([" ".join(i[3:i.index("-")].split("_")) for i in treebanks if i[:2] == "UD"])))

    # return to technologies directory
    os.chdir(tech_dir)

    return languages


def get_treebank_names(language):

    # identify directories
    tech_dir = os.getcwd()
    main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + f"{slash}ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora if "ud-treebanks-v" in corpus])
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
    main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + f"{slash}ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora if "ud-treebanks-v" in corpus])
    )
    os.chdir(latest_corpus)

    # extract data from each treebank and put in a list
    treebanks = list()
    for treebank in available_treebanks:
        os.chdir(latest_corpus + slash + treebank)
        available_files = os.listdir()
        retrieved_file = [file for file in available_files if ".conllu" in file]
        if len(retrieved_file) > 1:
            for file in retrieved_file:
                with open(file, encoding='utf-8') as conllu_file:
                    treebanks.append(parse(conllu_file.read()))
        elif len(retrieved_file) == 1:
            retrieved_file = retrieved_file[0]
            with open(retrieved_file, encoding='utf-8') as conllu_file:
                treebanks.append(parse(conllu_file.read()))
        elif len(retrieved_file) < 1:
            raise RuntimeError(f"No treebanks found for language, {language}, in folder: {treebank}")
        os.chdir(latest_corpus)
    if len(treebank) == 0:
        raise RuntimeError(f"No treebanks found for language: {language}")

    # return to technologies directory
    os.chdir(tech_dir)

    # combine sentences from all treebanks
    combined_banks = [[sentence for sentence in tree] for tree in treebanks]
    combined_banks = [i for j in combined_banks for i in j]

    return combined_banks


def get_pos_tags(language):

    # collect the CoNLL-U files for the language
    treebanks = get_treebanks(language)

    # extract UD POS-tags for each treebank
    pos_tags = [[(token.get("form"), token.get("upos")) for token in sentence] for sentence in treebanks]

    return pos_tags


def get_pos_feats(language):

    # collect the CoNLL-U files for the language
    treebanks = get_treebanks(language)

    # extract UD POS-tags for each treebank
    pos_tags = [[(token.get("upos"), token.get("feats")) for token in sentence] for sentence in treebanks]

    return pos_tags


def get_langfeats(language):
    """Gets all POS-feature combinations used in UD corpora for a specific language"""

    # get all POS information used in the language, format: [(POS, None), (POS, {Feature: Value}), ...]
    featslist = get_pos_feats(language)
    # remove duplicate items
    featslist = [i for j in featslist for i in j]

    # generate a list of just the parts-of-speech used
    poslist = sorted(list(set([i[0] for i in featslist])))
    # generate a list of just parts-of-speech whose features are not null
    featslist = [i for i in featslist if i[1]]
    # turn dictionaries for features into strings to compare (non hashable dicts cannot be compared)
    featslist = [[i[0], str(i[1])] for i in featslist]
    # get a list of all feature-strings associated with each POS tag
    featslist = [[i, [j[1] for j in featslist if j[0] == i]] for i in poslist]
    # remove duplicate POS strings for each POS tag
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]
    # turn the remaining feature-strings back into dictionaries for each POS tag
    featslist = [[i[0], [literal_eval(j) for j in i[1]]] for i in featslist]

    # change feature dicts for each POS into lists of tuples
    featslist = [[i[0], [[(k, j.get(k)) for k in j] for j in i[1]]] for i in featslist]
    # combine feature lists into one single list of feature tuples for each POS
    featslist = [[i[0], [j for k in i[1] for j in k]] for i in featslist]
    # remove duplicate feature tuples for each POS
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]

    # create a list of all possible values for each feature for each POS tag,
    # and turn each feature-value list into a string to compare (non hashable lists cannot be compared)
    featslist = [[i[0], [str([j[0], [k[1] for k in i[1] if k[0] == j[0]]]) for j in i[1]]] for i in featslist]
    # remove duplicate feature-value lists
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]
    # turn the remaining feature-value strings back into lists for each POS tag
    featslist = [[i[0], [literal_eval(j) for j in i[1]]] for i in featslist]

    # turn feature-value lists into dictionaries
    featslist = [[i[0], {j[0]: j[1] for j in i[1]}] for i in featslist]
    # turn POS-feature lists into dictionaries
    featslist = {i[0]: i[1] for i in featslist}

    return featslist


def get_valid_features(language_list=None):
    """Gets all POS-feature combinations used in UD corpora for a range of languages"""

    # Specify a limited number of languages if no list is provided
    if not language_list:
        language_list = ["English", "French", "German", "Irish", "Latin", "Old Irish", "Spanish"]
    # Get a list of all languages for which a POS-tagged corpus exists
    languages = list_pos_langs()

    # Get all treebanks for the languages specified in the language-list
    all_tbs = list()
    for language in language_list:
        all_tbs.append(get_treebanks(language))
    # Combine the treebanks for all languages into a single treebank containing the text from all specified languages
    one_tb = [[sentence for sentence in tree] for tree in all_tbs]
    one_tb = [i for j in one_tb for i in j]

    # get all POS information used in the single treebank, format: [(POS, None), (POS, {Feature: Value}), ...]
    featslist = [[(token.get("upos"), token.get("feats")) for token in sentence] for sentence in one_tb]
    # remove duplicate items
    featslist = [i for j in featslist for i in j]

    # generate a list of just the parts-of-speech used
    poslist = sorted(list(set([i[0] for i in featslist])))
    # generate a list of just parts-of-speech whose features are not null
    featslist = [i for i in featslist if i[1]]
    # turn dictionaries for features into strings to compare (non hashable dicts cannot be compared)
    featslist = [[i[0], str(i[1])] for i in featslist]
    # get a list of all feature-strings associated with each POS tag
    featslist = [[i, [j[1] for j in featslist if j[0] == i]] for i in poslist]
    # remove duplicate POS strings for each POS tag
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]
    # turn the remaining feature-strings back into dictionaries for each POS tag
    featslist = [[i[0], [literal_eval(j) for j in i[1]]] for i in featslist]

    # change feature dicts for each POS into lists of tuples
    featslist = [[i[0], [[(k, j.get(k)) for k in j] for j in i[1]]] for i in featslist]
    # combine feature lists into one single list of feature tuples for each POS
    featslist = [[i[0], [j for k in i[1] for j in k]] for i in featslist]
    # remove duplicate feature tuples for each POS
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]

    # create a list of all possible values for each feature for each POS tag,
    # and turn each feature-value list into a string to compare (non hashable lists cannot be compared)
    featslist = [[i[0], [str([j[0], [k[1] for k in i[1] if k[0] == j[0]]]) for j in i[1]]] for i in featslist]
    # remove duplicate feature-value lists
    featslist = [[i[0], sorted(list(set(i[1])))] for i in featslist]
    # turn the remaining feature-value strings back into lists for each POS tag
    featslist = [[i[0], [literal_eval(j) for j in i[1]]] for i in featslist]

    # turn feature-value lists into dictionaries
    featslist = [[i[0], {j[0]: j[1] for j in i[1]}] for i in featslist]
    # turn POS-feature lists into dictionaries
    featslist = {i[0]: i[1] for i in featslist}

    return featslist


def train_pos_tagger(language):
    """Train's a POS-tagger model for a selected language"""

    # load in the pos-tagged corpus
    pos_tagged_text = get_pos_tags(language)

    # train the tagger
    pos_tagger = nltk.UnigramTagger(pos_tagged_text)

    return pos_tagger


def save_pos_tagger(language, models_directory="language_models", overwrite_old_model=False):
    """Saves a POS-tagger model for a selected language in a models folder"""

    # Set directories, create models directory if none exists
    cur_dir = os.getcwd()
    models_dir = cur_dir + slash + models_directory
    try:
        available_models = os.listdir(models_dir)
    except FileNotFoundError:
        os.mkdir(models_directory)
        available_models = os.listdir(models_dir)

    if f"{language}_tagger.pkl" not in available_models:
        print(f"Training POS-tagger for language: {language}")
        this_model = train_pos_tagger(language)
        os.chdir(models_dir)
        with open(f"{language}_tagger.pkl", "wb") as tagger_file:
            pk.dump(this_model, tagger_file)
        os.chdir(cur_dir)
    elif overwrite_old_model:
        print(f"Training POS-tagger for language: {language}")
        this_model = train_pos_tagger(language)
        os.chdir(models_dir)
        with open(f"{language}_tagger.pkl", "wb") as tagger_file:
            pk.dump(this_model, tagger_file)
        os.chdir(cur_dir)


def load_tagger(language, models_directory="language_models"):
    """Loads a POS-tagger model from a .pkl file if one exists
       If no tagger exists, one is trained instead"""

    # Set directories, create models directory if none exists
    cur_dir = os.getcwd()
    models_dir = cur_dir + slash + models_directory
    try:
        available_models = os.listdir(models_dir)
        model_filename = f"{language}_tagger.pkl"
        if model_filename in available_models:
            os.chdir(models_dir)
            with open(f"{language}_tagger.pkl", "rb") as tagger_file:
                tagger = pk.load(tagger_file)
            os.chdir(cur_dir)
        else:
            tagger = train_pos_tagger(language)

    except FileNotFoundError:
        tagger = train_pos_tagger(language)

    return tagger


def save_language_taggers(language_list=None, models_dir="language_models",
                          overwrite_old_model=False, overwrite_old_directory=False):
    """Generate POS-tagger models for each supported language, or each in a specified list if supported"""

    supported_languages = list_pos_langs()

    if not language_list:
        available_languages = supported_languages
    elif all(lang in language_list for lang in supported_languages):
        available_languages = language_list[:]
    else:
        available_languages = [lang for lang in language_list if lang in supported_languages]

    if models_dir not in os.listdir():
        os.mkdir(models_dir)
    elif overwrite_old_directory:
        os.mkdir(models_dir)

    for lang_available in available_languages:
        save_pos_tagger(lang_available, models_dir, overwrite_old_model)


# if __name__ == "__main__":
#
#     # available_languages = list_pos_langs()
#     # print(len(available_languages))
#     # print(available_languages)
#
#     # print(get_treebank_names("Irish"))
#     # print(get_treebanks("Ancient Greek"))
#     # print(get_pos_tags("English"))
#     # print(json.dumps(get_langfeats("Irish")))
#     # print(json.dumps(get_valid_features(["Irish", "Old Irish"])))
#
#     # save_language_taggers()
#
#     gael_tagger = load_tagger("Irish")
#     test = "Chonaic mé mo mhadra ag rith. Thit sé agus é á casadh."
#     tokens = ([word_tokenize(sent) for sent in sent_tokenize(test)])
#
#     print(list(gael_tagger.tag([word.lower() for word in sent]) for sent in tokens))
