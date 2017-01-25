from os.path import exists, join

from fabric.api import lcd, local
from fabric.decorators import task

from .utils import optional_venv

DEFAULT_DATE = "latest"
DUMP_FILE = "{lang}wiki-{date}-pages-articles.xml.bz2"
DUMP_URL = "http://download.wikimedia.org/{lang}wiki/{date}/" + DUMP_FILE


@task
def download(corpus_dir, out_file, lang, date=DEFAULT_DATE):
    data_dir = corpus_dir
    if exists(join(data_dir, out_file)):
        return

    url = DUMP_URL.format(lang=lang, date=date)
    local("mkdir -p {dir}".format(dir=data_dir))
    with lcd(data_dir):
        local("wget {}".format(url))
        local("mv {} {}".format(DUMP_FILE.format(lang=lang, date=date), out_file))


@task
def extract(venv, wiki_dump_path, wiki_pages_dir, corpus_path, lang):
    if not exists(corpus_path):
        with optional_venv(venv, local=True):
            local("mkdir -p {}".format(wiki_pages_dir))
            local(
                "python ./corpus-utils/wiki2txt.py {dump} {out} {lang}".format(dump=wiki_dump_path, out=wiki_pages_dir,
                                                                               lang=lang))
            local(
                "find {path} -name '*.txt' | xargs cat > {out_file}".format(path=wiki_pages_dir, out_file=corpus_path))
