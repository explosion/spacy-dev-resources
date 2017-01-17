#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import falcon
import spacy
import json

from spacy.pipeline import EntityRecognizer

import spacy.util
from spacy.tagger import Tagger

from .parse import Entities, TrainEntities


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


def update_vocabulary(model, text):
    doc = model.make_doc(text)
    for word in doc:
        _ = model.vocab[word.orth]


class EntResource(object):
    """Parse text and return displaCy ent's expected output."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            entities = Entities(model, text)
            resp.body = json.dumps(entities.to_json(), sort_keys=True, indent=2)
            resp.content_type = 'text/string'
            resp.append_header('Access-Control-Allow-Origin', "*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


class TrainEntResource(object):
    """Parse text and use it to train the entity recognizer."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        tags = json_data.get('tags')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            update_vocabulary(model, text)
            entities = TrainEntities(model, text, tags)
            resp.body = json.dumps(entities.to_json(), sort_keys=True, indent=2)
            resp.content_type = 'text/string'
            resp.append_header('Access-Control-Allow-Origin', "*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500

APP = falcon.API()
APP.add_route('/ent', EntResource())
APP.add_route('/train', TrainEntResource())
