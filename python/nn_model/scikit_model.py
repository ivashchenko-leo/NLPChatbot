from sklearn.linear_model import LogisticRegression
import numpy as np
import logging
from nlp_utils import tokenize, stem, bag_of_words
import joblib


class ChatBot:

    def __init__(self, model, all_words, tags):
        self.model = model
        self.all_words = all_words
        self.tags = tags

    def answer(self, sentence):
        X = bag_of_words(tokenize(sentence), self.all_words)
        X = X.reshape(1, X.shape[0])

        output = self.model.predict_proba(X)
        index = output.argmax(1).item()
        prob = output.max(1).item()

        tag = self.tags[index]

        return tag, prob


def get_all_words(intents):
    all_words = []
    xy = []
    for intent in intents:
        for pattern in intent[0]:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, intent[1]))

    return sorted(set([stem(w) for w in all_words if w.isalpha()])), xy


def train(intents, path="../models/bot_model.pth"):
    tags = sorted(set(intent[1] for intent in intents))
    all_words, xy = get_all_words(intents)

    X_train = []
    y_train = []
    for (pattern, tag) in xy:
        bag = bag_of_words(pattern, all_words)
        X_train.append(bag)

        y_train.append(tags.index(tag))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    model = LogisticRegression(C=1e5, verbose=1)
    logger = logging.getLogger()

    logger.info("Start fitting...")

    model.fit(X_train, y_train)

    logger.info("Score " + str(model.score(X_train, y_train)))

    joblib.dump(model, path)

    logger.info(f'Training complete, model saved to {path}')


def load(datasource, language, path="../models/bot_model.pth"):
    model = joblib.load(path)

    intents = datasource.get_patterns(language)
    tags = sorted(set(intent[1] for intent in intents))
    all_words, xy = get_all_words(intents)

    return ChatBot(model, all_words, tags)
