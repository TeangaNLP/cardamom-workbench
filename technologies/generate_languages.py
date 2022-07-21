import os
from decimal import *


def collect_languages():

    # identify directories
    cur_dir = os.getcwd()
    main_dir = cur_dir[:cur_dir.index("/technologies")]
    corpora_dir = main_dir + "/CorporaUD"

    # navigate to directory containing UD corpora
    os.chdir(corpora_dir)

    # navigate to directory containing most recent UD corpus
    available_corpora = os.listdir()
    latest_corpus = corpora_dir + "/ud-treebanks-v" + str(
        max([Decimal(corpus[len("ud-treebanks-v"):]) for corpus in available_corpora if "ud-treebanks-v" in corpus])
    )
    os.chdir(latest_corpus)

    # identify available treebanks
    all_treebanks = os.listdir()

    # identify languages of available treebanks
    languages = sorted(list(set([" ".join(i[3:i.index("-")].split("_")) for i in all_treebanks])))

    # identify language iso codes
    iso_languages = list()
    for lang_num, language in enumerate(languages):
        iso_code = None
        # identify treebanks for the selected language
        treebanks = [tb for tb in all_treebanks if "UD_" + "_".join(language.split(" ")) + "-" in tb]
        for treebank in treebanks:
            os.chdir(treebank)
            treebank_files = os.listdir()
            for tb_file in treebank_files:
                if tb_file[-7:] == ".conllu":
                    iso_code = tb_file[:tb_file.find("_")]
                    break
            os.chdir(latest_corpus)
            if iso_code:
                break
        iso_languages.append((language, iso_code))

    # return to technologies directory
    os.chdir(cur_dir)

    return iso_languages


# if __name__ == "__main__":
#
#     available_languages = collect_languages()
#     # print(len(available_languages))
#     # print(available_languages)
#     for lang in available_languages:
#         print(f"INSERT INTO languages (language_name, iso_code, requested) VALUES ('{lang[0]}', '{lang[1]}', FALSE);")
