# -*- coding: UTF-8 -*-

import os
import sys
import gensim
import logging
import argparse
import subprocess


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


def train_model(data_path, window=5, size=100, min_count=2, workers=5, epochs=100, alpha=0.1, sg=0,
                max_vocab_size=10 ** 6, logs=logging.INFO):

    """
    Trains a FastText model.
    :param data_path: path to the training data in txt format (str)
    :return: FastTextKeyedVectors object
    """

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logs)

    f = open(data_path, 'r', encoding='utf-8')
    data = gensim.models.word2vec.LineSentence(f)

    # number of sentences (examples)
    sents = [s for s in data]
    total = len(sents)

    # number of tokens and types
    words = []
    for sent in sents:
        words += sent
    n_words = len(words)
    n_types = len(set(words))
    print("Tokens: %s\nTypes:%s\n" % (n_words, n_types))

    # selecting hyperparameters based on the number of types
    #     if 1000 <= n_types < 10000:
    #         size = 25
    #     elif 10000 <= n_types < 50000:
    #         size = 50
    #     elif 50000 <= n_types < 100000:
    #         size = 50
    #         min_count = 2
    #     elif 100000 <= n_types < 200000:
    #         min_count = 3
    #     else:
    #         min_count = 5

    model = gensim.models.fasttext.FastText(window=window, vector_size=size, min_count=min_count, workers=workers,
                                            alpha=alpha, sg=sg, max_vocab_size=max_vocab_size)
    model.build_vocab(corpus_iterable=data)
    model.train(corpus_iterable=data, total_examples=total, total_words=n_words, epochs=epochs)
    f.close()

    return model


def save_model(model, filename, compressed=True, binary=True):
    """
    Saves a model in preferred format.
    :param model: FastTextKeyedVectors object
    :param filename: file name for the model (str)
    :param compressed: save in compressed w2v format or not
    :param binary: if compressed, save as a binary or a text file
    """
    ext = '.bin' if binary else '.txt'
    path = '_'.join([filename, str(model.vector_size), str(model.window), str(model.min_count)]) + ext
    if compressed:
        model.wv.save_word2vec_format(path, binary=binary)
    else:
        ext = '.bin'
        model.save(path)


def convert_to_tf(input_file, output_file):
    res = subprocess.run(['python', 'gensim.scripts.word2vec2tensor', '--input', input_file,
                          '--output', output_file], capture_output=True, text=True, check=False)
    return {'stdout': res.stdout, 'stderr': res.stderr}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_folder", type=str, help="Path to data folder", required=True)
    parser.add_argument("-m", "--models_folder", type=str, help="Path to models folder", required=True)
    parser.add_argument("-w", "--window", type=int, help="Context window size", default=5)
    parser.add_argument("-s", "--emb_size", type=int, help="Embedding size", default=100)
    parser.add_argument("-e", "--epochs", type=int, help="N of training epochs", default=100)
    parser.add_argument("-min", "--min_count", type=int, help="Min word count to be included in vocabulary", default=2)
    parser.add_argument("-max", "--max_count", type=int, help="Max number of words in vocabulary", default=10 ** 6)
    parser.add_argument("-l", "--logfile", type=str, help="Path to log file", default="./logs/ft_training.log")

    args = parser.parse_args()
    logfile = "_".join([args.logfile, str(args.window), str(args.emb_size), str(args.min_count)]) + ".log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s: %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler()]
    )

    logger = logging.getLogger(__name__)

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    ### TRAINING

    sys.stdout.write("TRAINING MODELS...\n")

    for root, dirs, files in os.walk(args.data_folder):
        for f in files:
            if f.endswith(".txt"):
                model = train_model(os.path.join(root, f), min_count=args.min_count, size=args.emb_size,
                                    window=args.window, max_vocab_size=args.max_count, epochs=args.epochs)
                save_model(model, os.path.join(args.models_folder, f.replace(".txt", "_ft")))