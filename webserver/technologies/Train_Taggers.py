import os
import platform
import nltk
from ast import literal_eval
from UD_Parser import combine_treebanks, list_ud_langs
import json
from nltk import word_tokenize, sent_tokenize
import pickle as pk

op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"


def get_pos_tags(language):

    # collect the CoNLL-U files for the language
    treebanks = combine_treebanks(language)

    # extract UD POS-tags for each treebank
    pos_tags = [[(token.get("form"), token.get("upos")) for token in sentence] for sentence in treebanks]

    return pos_tags


def get_pos_feats(language):

    # collect the CoNLL-U files for the language
    treebanks = combine_treebanks(language)

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

    # If no list is provided get a list of all languages for which a POS-tagged UD corpus exists
    if not language_list:
        language_list = list_ud_langs()

    # Get all treebanks for the languages specified in the language-list
    all_tbs = list()
    for language in language_list:
        all_tbs.append(combine_treebanks(language))
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

    # put all letters in lowercase for improved tagging accuracy
    pos_tagged_text = [[(token[0].lower(), token[1]) for token in sentence] for sentence in pos_tagged_text]

    # train the tagger
    pos_tagger = nltk.PerceptronTagger(pos_tagged_text)

    return pos_tagger


def save_pos_tagger(language, models_directory="language_models", overwrite_old_model=False):
    """Saves a POS-tagger model for a selected language in a models folder"""

    # Set directories, create models directory if none exists
    cur_dir = os.getcwd()
    if f"{slash}code" in cur_dir:
        server_dir = cur_dir
    else:
        server_dir = cur_dir[:cur_dir.index(f"{slash}technologies")]
    models_dir = server_dir + slash + models_directory
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
    if f"{slash}code" in cur_dir:
        server_dir = cur_dir
    else:
        server_dir = cur_dir[:cur_dir.index(f"{slash}technologies")]
    models_dir = server_dir + slash + models_directory

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

    supported_languages = list_ud_langs()

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
#     # train_pos_tagger("Irish")
#     save_language_taggers(overwrite_old_model=True)
#
#     # gael_tagger = load_tagger("Irish")
#     # test = "Chonaic mé mo mhadra ag rith. Thit sé agus é á casadh."
#     # tokens = ([word_tokenize(sent) for sent in sent_tokenize(test)])
#     #
#     # print(list(gael_tagger.tag([word.lower() for word in sent]) for sent in tokens))
