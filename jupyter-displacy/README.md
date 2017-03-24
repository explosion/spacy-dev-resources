<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# displaCy Jupyter extension
**by [@ines](https://github.com/ines)**

Simple extension for [Jupyter](http://jupyter.org/) (formerly iPython) Notebook that lets you visualize a JSON-formatted dependency parse using the [displaCy visualizer](https://github.com/explosion/displacy).

![displaCy Jupyter extension](displacy_jupyter.gif)

**Example parse:**
```json
{
    "arcs": [
        {"dir": "left", "end": 1, "label": "nsubj", "start": 0},
        {"dir": "right", "end": 2, "label": "acomp", "start": 1}
    ],

    "words": [
        {"tag": "NNP", "text": "Jupyter"},
        {"tag": "VBZ", "text": "is"},
        {"tag": "JJ", "text": "cool"}
    ]
}
```

To render the visualization, select the cell containing the parse and click the magic wand button in your toolbar.

## Installation

The extension can be installed straight from GitHub:

```bash
# install and enable extension
jupyter nbextension install https://github.com/explosion/spacy-dev-resources/tree/master/jupyter-displacy
jupyter nbextension enable displacy

# run notebook server
jupyter notebook
```

## Configuration

You can override the following settings in your notebook meta data:

```json
{
    "displacy": {
        "distance": 200,
        "offsetX": 50,
        "arrowSpacing": 20,
        "arrowWidth": 10,
        "arrowStroke": 2,
        "wordSpacing": 75,
        "font": "inherit",
        "color": "#000000",
        "bg": "#ffffff"
    }
}
```

| Setting | Description | Default |
| --- | --- | --- |
| **distance** | distance between words in px | `200` |
| **offsetX** | spacing on left side of the SVG in px | `50` |
| **arrowSpacing** | spacing between arrows in px to avoid overlaps | `20` |
| **arrowWidth** | width of arrow head in px | `10` |
| **arrowStroke** | width of arc in px | `2` |
| **wordSpacing** | spacing between words and arcs in px | `75` |
| **font** | font face for all text | `'inherit'` |
| **color** | text color, HEX, RGB or color names | `'#000000'` |
| **bg** | background color, HEX, RGB or color names | `'#ffffff'` |

For example:

```json
{
    "displacy": {
        "arrowStroke": 3,
        "font": "Georgia",
        "color": "blue"
    }
}
```


## Todo / Ideas

There's still a lot to be done to make this extension actually useful and make sure it integrates well with people's workflows. I'm pretty new to Jupyter and Jupyter extensions, so feedback and pull requests are appreciated.

- [ ] add option to render parses on load (?)
- [ ] use parameters / different method for configuration (?)
- [ ] make sure visualizations can be exported
- [ ] add keyboard shortcuts
- [ ] integrate with [displaCy service](https://github.com/explosion/spacy-services) to parse text via [spaCy](https://spacy.io) from within the notebook
