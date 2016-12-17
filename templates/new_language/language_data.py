# encoding: utf8
from __future__ import unicode_literals

from ..symbols import *
from ..language_data import PRON_LEMMA
from ..language_data import TOKENIZER_PREFIXES
from ..language_data import TOKENIZER_SUFFIXES
from ..language_data import TOKENIZER_INFIXES


TAG_MAP = {
    "ADV":      {POS: ADV},
    "NOUN":     {POS: NOUN},
    "ADP":      {POS: ADP},
    "PRON":     {POS: PRON},
    "SCONJ":    {POS: SCONJ},
    "PROPN":    {POS: PROPN},
    "DET":      {POS: DET},
    "SYM":      {POS: SYM},
    "INTJ":     {POS: INTJ},
    "PUNCT":    {POS: PUNCT},
    "NUM":      {POS: NUM},
    "AUX":      {POS: AUX},
    "X":        {POS: X},
    "CONJ":     {POS: CONJ},
    "ADJ":      {POS: ADJ},
    "VERB":     {POS: VERB}
}


STOP_WORDS = set("""

""".split())


TOKENIZER_EXCEPTIONS = {

}


ORTH_ONLY = [
    "a.",
    "b.",
    "c.",
    "d.",
    "e.",
    "f.",
    "g.",
    "h.",
    "i.",
    "j.",
    "k.",
    "l.",
    "m.",
    "n.",
    "o.",
    "p.",
    "q.",
    "r.",
    "s.",
    "t.",
    "u.",
    "v.",
    "w.",
    "x.",
    "y.",
    "z."
]
