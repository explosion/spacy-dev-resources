from pathlib import Path
from spacy.util import get_lang_class
import pkg_resources
import json


def load_meta():
    with (Path(__file__).parent / 'meta.json').open() as f:
        return json.load(f)


def load(**kwargs):
    meta = load_meta()
    version = meta['version']
    data_dir = pkg_resources.resource_filename(__name__, __name__ + '-' + version)
    lang = get_lang_class(meta['lang'])
    return lang(path=Path(data_dir), **kwargs)
