import pytest
import falcon.testing
import json

from ..server import APP


class TestAPI(falcon.testing.TestCase):
    def __init__(self):
        self.api = APP


def test_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "Google is a company.", "model": "en"}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]


def test_train_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/train',
                body='''{"text": "Google es una empresa.", "model": "es",
                         "tags": [{"start": 0, "len": 6, "type": "ORG"}]}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]


def test_train_and_query_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/train',
                body='''{"text": "Google es una empresa.", "model": "es",
                         "tags": [{"start": 0, "len": 6, "type": "ORG"}]}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "Google es una empresa.", "model": "es"}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]
