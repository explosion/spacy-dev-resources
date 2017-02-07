<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy annotator – a trainable displaCy ENT server
**by [@tcrossland](https://github.com/tcrossland)**

This directory contains a customized version of the [displaCy REST microservice](https://github.com/explosion/spacy-services) which includes an endpoint for training the named entity recognition of a model.

The customized version of the service exposes two endpoints:

 * `POST /ent/` Performs named entity recognition on the text of the request
 * `POST /train/` Retrains the named entity recognizer of a model using an annotated text

The server can be integrated with an annotation frontend, for example, the experimental [spaCy annotator](https://github.com/tcrossland/spacy-annotator).

To run the server locally, install the dependencies and execute `python app.py`.

---

## `POST` `/ent/`

Example request:

```json
{
    "model": "en",
    "paragraphs": [
        {
            "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
        }
    ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `model` | string | identifier string for a model installed on the server  |
| `paragraphs` | array | paragraphs to be parsed |

Example response:

```json
[
    {
        "tags": [
            { "end": 20, "start": 5,  "type": "PERSON" },
            { "end": 67, "start": 61, "type": "ORG" },
            { "end": 75, "start": 71, "type": "DATE" }
        ],
        "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
    }
]
```

The response contains an array of paragraphs, each paragraph has the following properties:

| Name | Type | Description |
| --- | --- | --- |
| `tags` | array | array of tags (see below) |
| `text` | string | the text of the paragraph |

Each tag has the following properties:

| Name | Type | Description |
| --- | --- | --- |
| `end` | integer | character offset the entity ends **after** |
| `start` | integer | character offset the entity starts **on** |
| `type` | string | entity type |

---

## `POST` `/train`

Example request:

```json
{
  "model": "en",
  "paragraphs": [
    {
      "text": "Banco Bilbao Vizcaya Argentaria (BBVA) es una entidad bancaria española, presidida por Francisco González Rodríguez.",
      "tags": [
        {
          "start": 0,
          "len": 31,
          "type": "ORG"
        },
        {
          "start": 33,
          "len": 4,
          "type": "ORG"
        },
        {
          "start": 63,
          "len": 8,
          "type": "NORP"
        },
        {
          "start": 87,
          "len": 28,
          "type": "PERSON"
        }
        ]
    }
  ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `model` | string | identifier string for a model installed on the server  |
| `paragraphs` | array | paragraphs to be parsed |

Each paragraph has the following properties:

| Name | Type | Description |
| --- | --- | --- |
| `tags` | array | array of tags (see below) |
| `text` | string | the text of the paragraph |

Example response:

```json
{
  "paragraphs": [
    {
      "tags": [
        {
          "end": 31,
          "start": 0,
          "type": "ORG"
        },
        {
          "end": 37,
          "start": 33,
          "type": "ORG"
        },
        {
          "end": 71,
          "start": 63,
          "type": "NORP"
        },
        {
          "end": 115,
          "start": 87,
          "type": "PERSON"
        }
      ],
      "text": "Banco Bilbao Vizcaya Argentaria (BBVA) es una entidad bancaria española, presidida por Francisco González Rodríguez."
    }
  ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `paragraphs` | array | parse result for each paragraph |

The response contains an array of paragraphs, each paragraph has the following properties:

| Name | Type | Description |
| --- | --- | --- |
| `tags` | array | array of tags (see below) |
| `text` | string | the text of the paragraph |

Each tag has the following properties:

| Name | Type | Description |
| --- | --- | --- |
| `end` | integer | character offset the entity ends **after** |
| `start` | integer | character offset the entity starts **on** |
| `type` | string | entity type |
