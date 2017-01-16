from __future__ import unicode_literals

import codecs
from os.path import join

import plac
import spacy
from textacy.corpora.wiki_reader import WikiReader, strip_markup
from tqdm import tqdm

SENT_ENDS = [u".", u"!", u"?"]


def tokenize_sentence_split(text, nlp):
    for line in text.split("\n"):
        tok_acc = []
        for tok in nlp(line):
            tok_acc.append(tok.text)
            if tok.text in SENT_ENDS:
                yield " ".join(tok_acc)
                tok_acc = []
        if tok_acc:
            yield " ".join(tok_acc)


def clean_text(txt, min_char_ratio=0.9, min_length=50):
    for line in txt.split(u"\n"):
        line = line.strip()
        if line:
            line_length = len(line)
            char_ratio = float(sum(ch.islower() for ch in line)) / sum(not ch.isspace() for ch in line)
            starts_with_uppercase = line[0].isupper()
            if line_length > min_length and char_ratio > min_char_ratio and starts_with_uppercase:
                yield line


def extract_text(content, nlp, cleaned):
    text_content = strip_markup(content)
    if cleaned:
        text_content = u"\n".join(list(clean_text(text_content)))
    if nlp:
        text_content = "\n".join(tokenize_sentence_split(text_content, nlp))
    return text_content


def write_file(id, out_dir, text_content, title):
    fpath = join(out_dir, u"{}.txt".format(id))
    with codecs.open(fpath, "w", encoding="utf8") as f:
        content = title + u"\n" + text_content
        f.write(content)


def main(dump_path, out_dir, lang, cleaned=True):
    reader = WikiReader(dump_path)
    nlp = spacy.load(lang)
    for id, title, content in tqdm(reader):
        text_content = extract_text(content, nlp, cleaned)
        if text_content:
            write_file(id, out_dir, text_content, title)


if __name__ == "__main__":
    plac.call(main)
