# coding: utf8
from __future__ import unicode_literals

from spacy.util import load_model_from_init_py


def load(**overrides):
    return load_model_from_init_py(__file__, **overrides)
