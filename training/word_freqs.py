#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import plac
import joblib
import os
import io
import bz2
import ujson
from preshed.counter import PreshCounter
from joblib import Parallel, delayed
from pathlib import Path

from spacy.en import English
from spacy.strings import StringStore
from spacy.attrs import ORTH
from spacy.tokenizer import Tokenizer
from spacy.vocab import Vocab
import spacy.util


def iter_comments(loc):
    with bz2.BZ2File(loc) as file_:
        for line in file_:
            yield ujson.loads(line)


def count_freqs(Language, input_loc, output_loc):
    print(output_loc)
    tokenizer = Language.Defaults.create_tokenizer()

    counts = PreshCounter()
    for json_comment in iter_comments(input_loc):
        doc = tokenizer(json_comment['body'])
        doc.count_by(ORTH, counts=counts)

    with io.open(output_loc, 'w', 'utf8') as file_:
        for orth, freq in counts:
            string = tokenizer.vocab.strings[orth]
            if not string.isspace():
                file_.write('%d\t%s\n' % (freq, string))


def parallelize(func, iterator, n_jobs):
    Parallel(n_jobs=n_jobs)(delayed(func)(*item) for item in iterator)


def merge_counts(locs, out_loc):
    string_map = StringStore()
    counts = PreshCounter()
    for loc in locs:
        with io.open(loc, 'r', encoding='utf8') as file_:
            for line in file_:
                freq, word = line.strip().split('\t', 1)
                orth = string_map[word]
                counts.inc(orth, int(freq))
    with io.open(out_loc, 'w', encoding='utf8') as file_:
        for orth, count in counts:
            string = string_map[orth]
            file_.write('%d\t%s\n' % (count, string))


@plac.annotations(
    lang=("Language to tokenize", "positional"),
    input_loc=("Location of input file list", "positional", None, Path),
    freqs_dir=("Directory for frequency files", "positional", None, Path),
    output_loc=("Location for output file", "positional", None, Path),
    n_jobs=("Number of workers", "option", "n", int),
    skip_existing=("Skip inputs where an output file exists", "flag", "s", bool),
)
def main(lang, input_loc, freqs_dir, output_loc, n_jobs=2, skip_existing=False):
    Language = spacy.util.get_lang_class(lang)
    tasks = []
    outputs = []
    for input_path in input_loc.open():
        input_path = Path(input_path.strip())
        if not input_path:
            continue
        filename = input_path.parts[-1]
        output_path = freqs_dir / filename.replace('bz2', 'freq')
        outputs.append(output_path)
        if not output_path.exists() or not skip_existing:
            tasks.append((Language, input_path, output_path))

    if tasks:
        parallelize(count_freqs, tasks, n_jobs)

    print("Merge")
    merge_counts(outputs, output_loc)
                

if __name__ == '__main__':
    plac.call(main)
