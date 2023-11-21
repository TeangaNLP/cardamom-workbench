import os
import platform
from decimal import *
from conllu import parse

op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"


def list_ud_langs():
    """Returns a list of all languages for which treebanks are available
       in the latest UD folder in the CorporaUD directory"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}webserver")]
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
    """Returns a list of all treebanks for a given language
       which are available in the latest UD folder in the CorporaUD directory"""

    # identify directories
    tech_dir = os.getcwd()
    if f"{slash}code" in tech_dir:
        main_dir = tech_dir
    else:
        main_dir = tech_dir[:tech_dir.index(f"{slash}webserver")]
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
        main_dir = tech_dir[:tech_dir.index(f"{slash}webserver")]
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
    treebanks = list()
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
        main_dir = tech_dir[:tech_dir.index(f"{slash}webserver")]
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

