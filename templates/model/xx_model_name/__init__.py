# coding: utf8
from __future__ import unicode_literals

from spacy.util import load_model_from_init_py, get_model_meta


__version__ = get_model_meta(__file__)['version']


def load(**overrides):
    return load_model_from_init_py(__file__, **overrides)
