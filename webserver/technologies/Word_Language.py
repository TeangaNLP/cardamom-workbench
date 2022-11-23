from __future__ import absolute_import
from __future__ import division
import os
import platform

op_sys = platform.system()
if op_sys == "Windows":
    slash = "\\"
else:
    slash = "/"

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
import torch
from language_identification_word import constant
from nltk.tokenize import word_tokenize

char2id = {'<UNK>': 0, ' ': 1, 'त': 2, 'भ': 3, 'ी': 4, 'ब': 5, 'ा': 6, 'र': 7, 'ि': 8, 'श': 9, 'ह': 10, 'ु': 11,
           'ई': 12, 'थ': 13, 'ज': 14, 'स': 15, 'क': 16, 'ग': 17, 'ल': 18, 'प': 19, 'न': 20, 'इ': 21, 'म': 22, 'ू': 23,
           '्': 24, 'य': 25, 'ो': 26, 'ं': 27, 'व': 28, 'े': 29, 'ए': 30, 'अ': 31, 'द': 32, 'ै': 33, '.': 34, 'फ': 35,
           '़': 36, 'ध': 37, 'छ': 38, '/': 39, 'च': 40, 'ट': 41, 'ठ': 42, 'ऊ': 43, 'ण': 44, 'ड': 45, 'औ': 46, ',': 47,
           'ँ': 48, 'आ': 49, 'ख': 50, 'ढ': 51, 'ष': 52, 'ञ': 53, '।': 54, 'उ': 55, '-': 56, 'ऐ': 57, '?': 58, 'घ': 59,
           'ौ': 60, 'ओ': 61, '2': 62, '4': 63, ':': 64, '”': 65, 'ड़': 66, '!': 67, '‘': 68, 'ऽ': 69, 'झ': 70, 'फ़': 71,
           ';': 72, 'ढ़': 73, '\u200d': 74, 'ज़': 75, '1': 76, '9': 77, '0': 78, '6': 79, 'ृ': 80, 'ऋ': 81, 'ऑ': 82,
           '(': 83, ')': 84, "'": 85, '२': 86, 'क़': 87, '5': 88, '%': 89, '|': 90, 'ॉ': 91, '…': 92, '१': 93, '९': 94,
           '४': 95, '०': 96, 's': 97, 'ॊ': 98, '’': 99, '॥': 100, '३': 101, '“': 102, 'ः': 103, '8': 104, '3': 105,
           '\ufeff': 106, '+': 107, '८': 108, '५': 109, '६': 110, '*': 111, '7': 112, '७': 113, '[': 114, ']': 115,
           '\u200c': 116, 'ख़': 117, '_': 118, 'ग़': 119, 'ॠ': 120, 'ॐ': 121, '॰': 122, 'ॅ': 123, '–': 124, 'ऱ': 125,
           'i': 126, 'ङ': 127, 'w': 128, 'a': 129, 'k': 130, 'h': 131, 'r': 132, 'c': 133, 'o': 134, 'm': 135, 'ॆ': 136,
           'g': 137, 'ऎ': 138, 'e': 139, 'z': 140, 'n': 141, '—': 142, '●': 143, '©': 144, '&': 145, 'ऒ': 146, '`': 147,
           '\uf0e8': 148, '>': 149, 't': 150, 'ऩ': 151, '=': 152, 'ळ': 153, 'ऍ': 154, '}': 155, '{': 156, 'ॡ': 157,
           'd': 158, 'y': 159, 'p': 160, 'l': 161, 'u': 162, '#': 163, 'ॄ': 164, 'b': 165, '•': 166, '~': 167, 'f': 168,
           '\u200b': 169, '·': 170, 'j': 171, '@': 172, 'य़': 173, '\\': 174, '°': 175, '$': 176, '<': 177, 'લ': 178,
           'ો': 179, 'થ': 180, 'v': 181, 'q': 182, '\xad': 183, '£': 184, '॒': 185, '॔': 186}

# PATH = "{}/{}.pt".format(constant.params["model_dir"], constant.params["save_path"])
PATH = f"language_identification_word{slash}saved_models{slash}MODEL{slash}model.pt"
model = torch.load(PATH, map_location=torch.device('cpu'))

if constant.USE_CUDA:
    model = model.cuda()

# for param in model.state_dict():
#     print(param)

model.eval()
vocab = model.vocab
# text_pipeline = vocab(word_tokenize())

label2id = {'BRA': 0, 'AWA': 1, 'MAG': 2, 'HIN': 3, 'BHO': 4}
id2label = {0: 'BRA', 1: 'AWA', 2: 'MAG', 3: 'HIN', 4: 'BHO'}


def get_tokens_id(text):
    tokens = word_tokenize(text)
    token_id = []
    for token in tokens:
        if token in vocab:
            token_id.append(vocab[token])
        else:
            token_id.append(0)
    return token_id


def get_char_id(text):
    """
    convert char to id
    :param text:
    :return:
    """
    char_id_list = []
    for char in text:
        if char in char2id:
            char_id_list.append(char2id[char])
        else:
            char_id_list.append(0)
    # padding for kernel
    while len(char_id_list) < 6:
        # append whitespace
        char_id_list.append(1)
    return char_id_list


def predict_label_id(model_lang, sentence, sentence_length, sent_word, sentence_word_lengths):
    with torch.no_grad():
        sent_word = torch.tensor([sent_word])
        sentence = torch.tensor([sentence])
        _, output = model_lang(X=sentence, X_lengths=sentence_length, supv_unsupv="un_supv", train_test="test",
                          x_word=sent_word, sentence_word_lengths=sentence_word_lengths)
        return output.argmax(1).item()


def lang_identify(model_lang, text):

    tokens_ids = get_tokens_id(text)
    sentence_token_length = len(tokens_ids)

    char_id_list = get_char_id(text)
    sentence_length = len(char_id_list)
    label_id = predict_label_id(model_lang, char_id_list, sentence_length, tokens_ids, sentence_token_length)
    lang_id = id2label[label_id]
    return lang_id


def main(model_lang, input_text_list):
    for text in input_text_list:
        word_tokens = word_tokenize(text)
        for word in word_tokens:
            lang = lang_identify(model_lang, word)
            print("-"*50)
            print(f"origin text: {word} \tdetected lang: {lang}")


# if __name__ == "__main__":
#     input_text = [
#         "यामें द्वैत  अद्वैत पुन्न पाप सब एक कोंने में धरि जाँय"
#         "बेटवा से कहलक कि देरी होतउ तऽ एकरा उतार दोहे"
#     ]
#     main(model, input_text)
