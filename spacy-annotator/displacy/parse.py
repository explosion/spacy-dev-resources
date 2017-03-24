from __future__ import unicode_literals

from spacy.gold import GoldParse


class Entities(object):
    def __init__(self, nlp, text):
        self.text = text
        self.doc = nlp(text)

    def to_json(self):
        return {
            'text': self.text,
            'tags': [{'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
                     for ent in self.doc.ents]
        }


class TrainEntities(object):
    def __init__(self, nlp, text, tags):
        ner = nlp.entity
        entities = [(tag['start'], tag['start'] + tag['len'], tag['type'])
                    for tag in tags]
        for itn in range(20):
            doc = nlp.make_doc(text)
            gold = GoldParse(doc, entities=entities)
            ner.update(doc, gold)
        ner.model.end_training()
        self.text = text
        self.doc = nlp(text)

    def to_json(self):
        return {
            'text': self.text,
            'tags': [{'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
                     for ent in self.doc.ents]
        }
