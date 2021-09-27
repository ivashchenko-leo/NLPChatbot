import json
import numpy as np
from main import tokenize, stem, bag_of_words


def train_main():
    with open('../data/intents.json', 'r') as f:
        intents = json.load(f)

    all_words = []
    tags = sorted(set([intent['tag'] for intent in intents['intents']]))
    xy = []
    for intent in intents['intents']:
        for pattern in intents['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, intent['tag']))

    all_words = sorted(set([stem(w) for w in all_words if w.isalpha()]))

    X_train = []
    y_train = []
    for (pattern, tag) in xy:
        bag = bag_of_words(pattern, all_words)
        X_train.append(bag)

        y_train.append(tags.index(tag))

    X_train = np.array(X_train)
    y_train = np.array(y_train)
