from os.path import join, dirname

from fabric.api import lcd, local
from fabric.decorators import task

import wikipedia
from .utils import optional_venv

SCRIPTS_DIR = "./scripts"
BROWN_DIR = SCRIPTS_DIR + "/" + "brown"
CORPUS_DIR = "./data/corpora/{lang}"
MODEL_DIR = "./data/model/{lang}"


@task
def clean_corpora(language):
    local("rm -rf {}".format(CORPUS_DIR.format(lang=language)))


@task
def clean_models(language):
    local("rm -rf {}".format(MODEL_DIR.format(lang=language)))


@task
def clean_data(language):
    clean_corpora(language)
    clean_models(language)


@task
def clean():
    clean_data("")


@task
def build_brown(path=BROWN_DIR):
    local("mkdir -p {}".format(path))
    local("git clone git@github.com:percyliang/brown-cluster.git ./{}".format(path))
    with lcd(path):
        local("make")


@task
def env(env_dir=None):
    if env_dir is not None:
        local("virtualenv {}".format(env_dir))
    with optional_venv(env_dir, local=True):
        local("pip install textacy==0.3.2 plac==0.9.6 spacy==1.6 gensim==0.13.4 tqdm")
    build_brown()


@task
def wiki_model(language, env=None):
    corpus_dir = CORPUS_DIR.format(lang=language)
    out_file = "{}_wiki.xml.bz2".format(language)
    dump_path = join(corpus_dir, out_file)
    wiki_corpus_path = join(corpus_dir, "{}_wiki.fabfile".format(language))
    wiki_pages_dir = join(corpus_dir, "wiki")
    model_dir = MODEL_DIR.format(lang=language)

    word_freq_path = join(model_dir, "{}_wiki.freqs".format(language))
    word2vec_model_path = join(model_dir, "{}_wiki.word2vec".format(language))
    brown_out_dir = join(model_dir, "brown")

    wikipedia.download(corpus_dir, out_file, language)
    wikipedia.extract(env, dump_path, wiki_pages_dir, wiki_corpus_path, language)

    word_counts(wiki_pages_dir + "/*", word_freq_path)
    # word2vec(wiki_pages_dir, word2vec_model_path, language)
    word2vec(wiki_corpus_path, word2vec_model_path, language)
    brown_clusters(wiki_corpus_path, brown_out_dir)
    local(
        "python training/init.py {lang} ./{dir}/vocab {freq} {brown}/paths {w2v}.bz2".format(
            lang=language,
            dir=model_dir,
            freq=word_freq_path,
            brown=brown_out_dir,
            w2v=word2vec_model_path
        ))


@task
def word2vec(corpus_path, out_path, language, dim=128, threads=4, min_count=5):
    local("mkdir -p {}".format(dirname(out_path)))
    local(
        "python -m gensim.scripts.word2vec_standalone " +
        "-train {corpus_file} -output {file} -size {dim} -threads {threads} -min_count {min} 2>&1 > {file}.log".format(
            corpus_file=corpus_path,
            dim=dim,
            file=out_path,
            threads=threads,
            min=min_count
        )
    )
    local("bzip2 {}".format(out_path))
    # local(
    #     "python training/word_vectors.py {lang} {in_dir} {out_file} -n {threads} -d {dim}".format(
    #         dim=dim,
    #         in_dir=corpus_path,
    #         out_file=out_path,
    #         threads=threads,
    #         lang=language,
    #     )
    # )


@task
def word_counts(input_glob, out_path):
    local("python training/plain_word_freqs.py \"{input_glob}\" {out}".format(input_glob=input_glob, out=out_path))


@task
def brown_clusters(corpus_path, output_dir, clusters=2 ** 13, threads=4):
    local("mkdir -p {}".format(output_dir))
    brown_script = join(BROWN_DIR, "wcluster")
    local(
        "{bs} --text ./{corpus_file} --c {clusters} --output_dir {output_dir} --threads {threads}".format(
            bs=brown_script,
            corpus_file=corpus_path,
            clusters=clusters,
            threads=threads,
            output_dir=output_dir
        )
    )
