from __future__ import unicode_literals

import codecs
import glob
from collections import Counter

import plac
from multiprocessing import Pool
from tqdm import tqdm


def count_words(fpath):
    with codecs.open(fpath, encoding="utf8") as f:
        words = f.read().split()
        counter = Counter(words)
    return counter


def main(input_glob, out_loc, workers=4):
    p = Pool(processes=workers)
    counts = p.map(count_words, tqdm(list(glob.glob(input_glob))))
    df_counts = Counter()
    word_counts = Counter()
    for wc in tqdm(counts):
        df_counts.update(wc.keys())
        word_counts.update(wc)
    with codecs.open(out_loc, "w", encoding="utf8") as f:
        for word, df in df_counts.iteritems():
            f.write(u"{freq}\t{df}\t{word}\n".format(word=repr(word), df=df, freq=word_counts[word]))


if __name__ == "__main__":
    plac.call(main)
