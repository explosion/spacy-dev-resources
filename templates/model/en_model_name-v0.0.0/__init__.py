from pathlib import Path
from spacy.util import get_lang_class
import pkg_resources


def load_meta():
    with io.open('meta.json', encoding='utf8') as f:
        return json.load(f)


def load(**kwargs):
    version = load_meta()['version']
    data_dir = pkg_resources.resource_filename(__name__, __name__ + '-' + version)
    lang = get_lang_class(about.__lang__)
    return lang(path=Path(data_dir), **kwargs)
