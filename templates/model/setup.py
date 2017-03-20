#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals

import io
import json
from os import path, walk
from os.path import dirname
from shutil import copy
from setuptools import setup


def load_meta(fp):
    with io.open(fp, encoding='utf8') as f:
        return json.load(f)


def generate_about(fp, data):
    with io.open(fp, 'w', encoding='utf8') as f:
        for key in data.keys():
            line = "__{k}__ = '{v}'\n".format(k=key, v=data[key])
            f.write(line)


def list_files(data_dir):
    output = []
    for root, _, filenames in walk(data_dir):
        for filename in filenames:
            if not filename.startswith('.'):
                output.append(path.join(root, filename))
    output = [path.relpath(p, dirname(data_dir)) for p in output]
    output.append('meta.json')
    return output


def setup_package():
    root = path.abspath(path.dirname(__file__))
    meta_path = path.join(root, 'meta.json')
    meta = load_meta(meta_path)
    model_name = str(meta['lang'] + '_' + meta['name'])
    model_dir = path.join(model_name, model_name + '-' + meta['version'])

    copy(meta_path, path.join(model_name))
    copy(meta_path, model_dir)

    setup(
        name=model_name,
        description=meta['description'],
        author=meta['author'],
        author_email=meta['email'],
        url=meta['url'],
        version=meta['version'],
        license=meta['license'],
        packages=[model_name],
        package_data={model_name: list_files(model_dir)},
        install_requires=['spacy' + meta['spacy_version']],
        zip_safe=False,
    )


if __name__ == '__main__':
    setup_package()
