import os
import platform
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pickle as pk
from decimal import *
from conllu import parse

op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"


def make_corpdir():
    """Make a folder for UD Corpora if one doesn't already exist"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to directory containing UD corpora
    # if it doesn't exist, make it
    try:
        os.chdir(corpora_dir)
    except FileNotFoundError:
        os.chdir(main_dir)
        os.mkdir("CorporaUD")

    # return to technologies directory
    os.chdir(tech_dir)


# def fill_corpdir():
#     """Fill an empty UD Corpora folder if it is empty"""
#
#     # identify directories
#     tech_dir = os.getcwd()
#     if f"{slash}code" in tech_dir:
#         main_dir = tech_dir
#     else:
#         main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
#     corpora_dir = main_dir + f"{slash}CorporaUD"
#
#     # navigate to directory containing UD corpora
#     try:
#         os.chdir(corpora_dir)
#     except FileNotFoundError:
#         make_corpdir()
#         os.chdir(corpora_dir)
#
#     # Get the html for the UD website
#     url_UD = """https://universaldependencies.org/"""
#     ud_response = requests.get(url_UD).text
#     ud_soup = BeautifulSoup(ud_response, 'html.parser')
#
#     # Get the link to the repo for the latest UD corpora
#     dl_path = None
#     for link in ud_soup.find_all('a'):
#         path = link.get('href')
#         if path and path.startswith("""http://hdl.handle.net"""):
#             dl_path = path
#
#     # If a link to the latest version to download has not been found raise an error
#     if not dl_path:
#         raise RuntimeError("Could not find link to download latest UD treebanks.")
#
#     # If a link to the latest version to download has been found, navigate to it
#     # Get the html for the download link
#     dl_response = requests.get(dl_path).text
#     dl_soup = BeautifulSoup(dl_response, 'html.parser')
#
#     # Get the
#     for link in dl_soup.find_all('a'):
#         if link.get("id") == "download-all-button":
#             path = link.get('href')
#             print(link)
#             break
#
#         # if path and link.get("id") == "download-all-button":
#         #     print(path)
#
#     # return to technologies directory
#     os.chdir(tech_dir)


def list_ud_langs():
    """Returns a list of all languages for which treebanks are available
       in the latest UD folder in the CorporaUD directory"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to directory containing UD corpora
    try:
        os.chdir(corpora_dir)
    except FileNotFoundError:
        make_corpdir()
        os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    print(available_corpora)
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
    """Returns a list of all treebanks for a given language
       which are available in the latest UD folder in the CorporaUD directory"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
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


def get_iso(language):
    """Returns the ISO code used by all its UD treebanks for a specific language"""

    # find treebanks available for the language
    available_treebanks = get_treebank_names(language)

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
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

    # get iso code from language's treebanks
    iso_code = None
    for treebank in available_treebanks:
        os.chdir(latest_corpus + slash + treebank)
        available_files = os.listdir()
        retrieved_file = [file for file in available_files if ".conllu" in file]
        for file in retrieved_file:
            if not iso_code:
                iso_code = file[:file.index("_")]
            elif iso_code:
                if iso_code != file[:file.index("_")]:
                    raise RuntimeError(f"Multiple distinct ISO codes found in use for language, {language}: "
                                       f"{iso_code} and {file[:file.index('_')]}")

    # return to technologies directory
    os.chdir(tech_dir)

    return iso_code


def create_isodict():
    """Generates a dictionary of iso/language pairs for all languages
       which are supported in the latest UD folder in the CorporaUD directory"""

    iso_dict = dict()
    for lang in list_ud_langs():
        lan_iso = get_iso(lang)
        iso_dict[lan_iso] = lang

    return iso_dict


def load_langsupport():
    """Loads a dictionary of languages which are supported by the workbench and their iso codes"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"

    # navigate to the supported languages list, if it exists, and load it using pickle
    available_models = os.listdir(corpora_dir)
    if "supported_languages.pkl" in available_models:
        os.chdir(corpora_dir)
        with open("supported_languages.pkl", "rb") as tagger_file:
            sup_list = pk.load(tagger_file)
        os.chdir(tech_dir)
    # if it does not exist, return an empty list
    else:
        sup_list = dict()

    return sup_list


def generate_langlist():
    """Create an ordered dictionary of languages and iso codes which are supported by the workbench"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}technologies")]
    corpora_dir = main_dir + f"{slash}CorporaUD"
    models_dir = main_dir + f"{slash}language_models"

    # identify languages for which a POS-tagger is available (as this is the most basic level of support)
    available_models = os.listdir(models_dir)

    # separate language names from tagger file extensions
    supported_langs = [lang[:lang.index("_tagger.pkl")] for lang in available_models if "_tagger.pkl" in lang]

    # get the iso code for each supported language and add it to a dictionary as the value for the language key
    supported_langs = {get_iso(lang): lang for lang in supported_langs}

    # check for an older list of supported languages which may differ from the newly generated one
    old_sup = load_langsupport()

    # if both dictionaries don't contain the same keys, add any extras from the old dictionary to the new one
    old_only = list()
    if sorted(list(set([lang for lang in supported_langs]))) != sorted(list(set([lang for lang in old_sup]))):
        old_only = [i for i in old_sup if i not in supported_langs]
    for obsolete in old_only:
        supported_langs[obsolete] = old_sup.get(obsolete)

    # save the new list of supported languages to the language models folder
    os.chdir(corpora_dir)
    with open("supported_languages.pkl", "wb") as sup_file:
        pk.dump(supported_langs, sup_file)
    os.chdir(tech_dir)


def get_treebanks(language):
    """Returns the contents of all conllu files for all treebanks for a given language
       which is supported in the latest UD folder in the CorporaUD directory
       in the format: [[Treebank_Name, File_Type, File_Contents], [...], ...]"""

    # find treebanks available for the language
    available_treebanks = get_treebank_names(language)

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
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

    # get conllu data from each treebank and put it in a list
    treebanks = list()
    for treebank in available_treebanks:
        os.chdir(latest_corpus + slash + treebank)
        available_files = os.listdir()
        retrieved_file = [file for file in available_files if ".conllu" in file]

        for file in retrieved_file:
            file_type = file[file.index("-ud-")+4:file.index(".conllu")]
            if file_type not in ("test", "train", "dev"):
                raise RuntimeError(f"CoNLL-U file of type {file_type} found\n    "
                                   f"Files must be of type 'test', 'train', or 'dev'")
            with open(file, encoding='utf-8') as conllu_file:
                treebanks.append([treebank, file_type, parse(conllu_file.read())])

    # return to technologies directory
    os.chdir(tech_dir)

    return treebanks


def combine_treebanks(language, file_type="all"):
    """Combines the contents of all conllu files for all treebanks for a given language
       which are available in the latest UD folder in the CorporaUD directory"""

    # get all treebank content
    treebanks = get_treebanks(language)

    # ensure file_type is possible:
    if file_type not in ("test", "train", "dev", "all"):
        raise RuntimeError(f"CoNLL-U file of type {file_type} requested\n    "
                           f"Files must be of type 'test', 'train', 'dev' or 'all'")

    # remobe unwanted file types, leave only the requested file type
    if file_type in ("test", "train", "dev"):
        treebanks = [tb for tb in treebanks if tb[1] == file_type]

    # combine treebank contents for required treebank type/types
    combined_treebanks = [tb[2] for tb in treebanks]

    # ensure at least one conllu file of this type is available
    if len(combined_treebanks) == 0:
        raise RuntimeError(f"No treebanks found for language: {language}")

    # combine sentences from all treebanks
    combined_treebanks = [i for j in combined_treebanks for i in j]

    return combined_treebanks


# if __name__ == "__main__":
#
#     available_languages = list_ud_langs()
#     print(len(available_languages))
#     print(available_languages)
#
#     print(get_treebank_names("Irish"))
#     # print(get_treebanks("Irish"))
#     # print(combine_treebanks("Ancient Greek"))
#
#     print(get_iso("Old Irish"))
#     supported_isos = create_isodict()
#     print(supported_isos.get("sga"))
#
#     # generate_langlist()
#     print(load_langsupport())
