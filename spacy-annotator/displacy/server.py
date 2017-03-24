#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import falcon
import spacy
import json
import sys

from spacy.pipeline import EntityRecognizer

import spacy.util
from spacy.tagger import Tagger

from .parse import Entities, TrainEntities
from falcon_cors import CORS

try:
    unicode
except NameError:
    unicode = str


_models = {}

def get_model(model_name):
    if model_name not in _models:
        model = spacy.load(model_name)
        if model.tagger is None:
            model.tagger = Tagger(model.vocab, features=Tagger.feature_templates)
        if model.entity is None:
            model.entity = EntityRecognizer(model.vocab, entity_types=['PERSON', 'NORP', 'FACILITY', 'ORG', 'GPE',
                                                                       'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
                                                                       'LANGUAGE', 'DATE', 'TIME', 'PERCENT',
                                                                       'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'])
        model.pipeline = [model.tagger, model.entity, model.parser]
        _models[model_name] = model
    return _models[model_name]


def update_vocabulary(model, texts):
    for text in texts:
        doc = model.make_doc(text)
        for word in doc:
            _ = model.vocab[word.orth]


class EntResource(object):
    """Parse text and return displaCy ent's expected output."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        paragraphs = json_data.get('paragraphs')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            entities = []
            for p in paragraphs:
                e = Entities(model, p.get('text'))
                entities.append(e.to_json())
            resp.body = json.dumps(entities, sort_keys=True, indent=2)
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


class TrainEntResource(object):
    """Parse text and use it to train the entity recognizer."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        paragraphs = json_data.get('paragraphs')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            texts = [paragraph.get('text') for paragraph in paragraphs]
            update_vocabulary(model, texts)
            entities = []
            for p in paragraphs:
                e = TrainEntities(model, p.get('text'), p.get('tags'))
                entities.append(e.to_json())
            resp.body = json.dumps(entities, sort_keys=True, indent=2)
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            resp.status = falcon.HTTP_500

cors = CORS(allow_all_origins=True)
APP = falcon.API(middleware=[cors.middleware])
APP.add_route('/ent', EntResource())
APP.add_route('/train', TrainEntResource())
