from __future__ import unicode_literals

import codecs
import re
from os.path import join

import ftfy
import plac
import spacy
from textacy.corpora.wiki_reader import WikiReader, strip_markup
from tqdm import tqdm

SENT_ENDS = [u".", u"!", u"?"]
TABLE_PREFIX = re.compile(u"\s*(\{\))|(\|)|(\|\})")
TAG = re.compile(u"<[^<>]+>")


def tokenize_sentence_split(text, nlp):
    tokenizer = nlp.tokenizer
    for line in text.split("\n"):
        tok_acc = []
        for tok in tokenizer(line):
            tok_acc.append(tok.text)
            if tok.text in SENT_ENDS:
                yield " ".join(tok_acc)
                tok_acc = []
        if tok_acc:
            yield " ".join(tok_acc)


def clean_lines(txt, min_char_ratio=0.9, min_length=50):
    txt = ftfy.fix_text(txt)
    for line in txt.split(u"\n"):
        line = TAG.sub(u"", line.strip())
        if line and line[0].isalnum() and len(line) > min_length:
            char_ratio = float(sum(ch.islower() for ch in line)) / sum(not ch.isspace() for ch in line)
            if char_ratio > min_char_ratio:
                yield line


def pre_filter(content):
    return "\n".join([line for line in content.split(u"\n") if not TABLE_PREFIX.match(line)])


def extract_text(content, nlp, cleaned):
    sentences = []
    content = strip_markup(pre_filter(content))
    lines = clean_lines(content) if cleaned else content.split("\n")
    for line in lines:
        for sent in tokenize_sentence_split(line, nlp):
            sentences.append(sent)
    return u"\n".join(sentences)


def write_file(id, out_dir, text_content, title):
    fpath = join(out_dir, u"{}.txt".format(id))
    with codecs.open(fpath, "w", encoding="utf8") as f:
        content = title + u"\n" + text_content
        f.write(content)


def main(dump_path, out_dir, lang, cleaned=True):
    reader = WikiReader(dump_path)
    nlp = spacy.load(lang, parser=None, tagger=None)
    for id, title, content in tqdm(reader):
        text_content = extract_text(content, nlp, cleaned)
        if text_content:
            write_file(id, out_dir, text_content, title)


if __name__ == "__main__":
    plac.call(main)
