import torch
from python.nlp_utils import bag_of_words, tokenize


class ChatBot:

    def __init__(self, model, all_words, tags):
        self.model = model
        self.all_words = all_words
        self.tags = tags

    def answer(self, sentence):
        X = bag_of_words(tokenize(sentence), self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        prob = torch.softmax(output, dim=1)[0][predicted.item()]

        return tag, prob



