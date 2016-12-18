"""Set up a model directory."""
from __future__ import unicode_literals

from ast import literal_eval
import math
import gzip
import json

import plac
from pathlib import Path

from shutil import copyfile
from shutil import copytree
from collections import defaultdict
import io

from spacy.vocab import Vocab
from spacy.vocab import write_binary_vectors
from spacy.strings import hash_string
from preshed.counter import PreshCounter

from spacy.parts_of_speech import NOUN, VERB, ADJ
from spacy.util import get_lang_class


try:
    unicode
except NameError:
    unicode = str


def _read_clusters(loc):
    if not loc.exists():
        print("Warning: Clusters file not found")
        return {}
    clusters = {}
    for line in io.open(str(loc), 'r', encoding='utf8'):
        try:
            cluster, word, freq = line.split()
        except ValueError:
            continue
        # If the clusterer has only seen the word a few times, its cluster is
        # unreliable.
        if int(freq) >= 3:
            clusters[word] = cluster
        else:
            clusters[word] = '0'
    # Expand clusters with re-casing
    for word, cluster in list(clusters.items()):
        if word.lower() not in clusters:
            clusters[word.lower()] = cluster
        if word.title() not in clusters:
            clusters[word.title()] = cluster
        if word.upper() not in clusters:
            clusters[word.upper()] = cluster
    return clusters


def _read_probs_from_freqs(loc, max_length=100, min_doc_freq=5, min_freq=200):
    if not loc.exists():
        print("Warning: Frequencies file not found")
        return {}, 0.0
    counts = PreshCounter()
    total = 0
    if str(loc).endswith('gz'):
        file_ = gzip.open(str(loc))
    else:
        file_ = loc.open()
    for i, line in enumerate(file_):
        freq, doc_freq, key = line.rstrip().split('\t', 2)
        freq = int(freq)
        counts.inc(i+1, freq)
        total += freq
    counts.smooth()
    log_total = math.log(total)
    if str(loc).endswith('gz'):
        file_ = gzip.open(str(loc))
    else:
        file_ = loc.open()
    probs = {}
    for line in file_:
        freq, doc_freq, key = line.rstrip().split('\t', 2)
        doc_freq = int(doc_freq)
        freq = int(freq)
        if doc_freq >= min_doc_freq and freq >= min_freq and len(key) < max_length:
            word = literal_eval(key)
            smooth_count = counts.smoother(int(freq))
            probs[word] = math.log(smooth_count) - log_total
    oov_prob = math.log(counts.smoother(0)) - log_total
    return probs, oov_prob


def populate_vocab(vocab, clusters, probs, oov_prob):
    # Ensure probs has entries for all words seen during clustering.
    for word in clusters:
        if word not in probs:
            probs[word] = oov_prob
    #lexicon = []
    #for word, prob in reversed(sorted(list(probs.items()), key=lambda item: item[1])):
    #    # First encode the strings into the StringStore. This way, we can map
    #    # the orth IDs to frequency ranks
    #    orth = vocab.strings[word]
    # Now actually load the vocab
    for word, prob in reversed(sorted(list(probs.items()), key=lambda item: item[1])):
        lexeme = vocab[word]
        lexeme.prob = prob
        lexeme.is_oov = False
        # Decode as a little-endian string, so that we can do & 15 to get
        # the first 4 bits. See _parse_features.pyx
        if word in clusters:
            lexeme.cluster = int(clusters[word][::-1], 2)
        else:
            lexeme.cluster = 0


def write_vectors(src_dir, dst_dir):
    print('Reading vocab from ', src_dir)
    vectors_src = src_dir / 'vectors.bz2'
    if vectors_src.exists():
        write_binary_vectors(vectors_src.as_posix(), (dst_dir / 'vec.bin').as_posix())
    else:
        print("Warning: Word vectors file not found")


def main(lang_id, model_dir, freqs_loc, clusters_loc=None, vectors_loc=None):
    model_dir = Path(model_dir)
    freqs_loc = Path(freqs_loc)
    if clusters_loc is not None:
        clusters_loc = Path(clusters_loc)
    if vectors_loc is not None:
        vectors_loc = Path(vectors_loc)

    if not model_dir.exists():
        model_dir.mkdir()

    vocab = get_lang_class(lang_id).Defaults.create_vocab()

    clusters = _read_clusters(clusters_loc)
    probs, oov_prob = _read_probs_from_freqs(freqs_loc)
    populate_vocab(vocab, clusters, probs, oov_prob)

    if not model_dir.exists():
        model_dir.mkdir()
    if not (model_dir / 'vocab').exists():
        (model_dir / 'vocab').mkdir()
    vocab.dump((model_dir / 'vocab' / 'lexemes.bin').as_posix())
    with (model_dir / 'vocab' / 'strings.json').open('w') as file_:
        vocab.strings.dump(file_)
    with (model_dir / 'vocab' / 'oov_prob').open('w') as file_:
        file_.write('%f' % oov_prob)
    if vectors_loc is not None:
        write_vectors(vectors_loc, model_dir)


if __name__ == '__main__':
    plac.call(main)
