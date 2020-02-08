import os
import json
import math
import codecs
from collections import defaultdict
from nltk.stem import PorterStemmer
from utils.utils_data_process import split_sent, normalize_unicode
from optparse import OptionParser
ps = PorterStemmer()


datasets = ['train', 'dev', 'raw-dev']
files = ['a.toks', 'b.toks']


def idf(freq, total_freq):
    return math.log(1 + total_freq*1.0/freq)


def generate_idf(base_dir):
    freq_dict = {"unigram": defaultdict(int),
                 "bigram": defaultdict(int),
                 "trigram": defaultdict(int)}

    total_word_freq, total_bigram_freq, total_ngram_freq = 0, 0, 0

    for dataset in datasets:
        for file in files:
            path = '%s/%s/%s' % (base_dir, dataset, file)
            if os.path.exists(path):
                with codecs.open(path, 'r', 'UTF-8') as f:
                    for i, line in enumerate(f):
                        tokens = split_sent(normalize_unicode(line.strip()), "word")
                        for j in range(len(tokens)):
                            freq_dict["unigram"][tokens[j].lower()] += 1
                            #freq_dict["word"][ps.stem(tokens[j])] += 1
                            if j >= 1:
                                bigram = " ".join([token.lower() for token in tokens[j - 1:j + 1]])
                                #bigram = " ".join([ps.stem(token) for token in tokens[j-1:j+1]])
                                freq_dict["bigram"][bigram] += 1
                            if j >= 2:
                                trigram = " ".join([token.lower() for token in tokens[j - 2:j + 1]])
                                #trigram = " ".join([ps.stem(token) for token in tokens[j-2:j+1]])
                                freq_dict["trigram"][trigram] += 1
                        total_word_freq += len(tokens)

    json.dump(freq_dict, open("%s/collection_raw_idf.json" % base_dir, "w"))
    return freq_dict, total_word_freq


def normalize_idf(base_dir, freq_dict, total_word_freq):
    max_freq, min_freq = {}, {}
    max_idf, min_idf = {}, {}
    for key in freq_dict:
        max_freq[key], min_freq[key] = max(freq_dict[key].values()), min(freq_dict[key].values())
        max_idf[key], min_idf[key] = idf(min_freq[key], total_word_freq), idf(max_freq[key], total_word_freq)
    #print(max_idf, min_idf)

    for key in freq_dict:
        for token in freq_dict[key].keys():
            token_idf = idf(freq_dict[key][token], total_word_freq)
            norm_idf = (token_idf - min_idf[key]) / (max_idf[key] - min_idf[key])
            freq_dict[key][token] = norm_idf

    print("Total words: %d" % total_word_freq)
    print('Unique unigrams: %d, bigrams: %d, trigrams: %d' %
          (len(freq_dict['unigram']), len(freq_dict['bigram']), len(freq_dict['trigram'])))
    print('Dump IDF weights into %s/collection_word_idf.json' % base_dir)
    json.dump(freq_dict, open("%s/collection_word_idf.json" % base_dir, "w"))


def create_option_parser():
    parser = OptionParser()
    parser.add_option("-d", "--dataset", action="store", type=str, dest="dataset")
    return parser


if __name__ == "__main__":
    parser = create_option_parser()
    options, arguments = parser.parse_args()
    dataset = getattr(options, "dataset")
    base_dir = dataset
    freq_dict, total_word_freq = generate_idf(base_dir)
    normalize_idf(base_dir, freq_dict, total_word_freq)
