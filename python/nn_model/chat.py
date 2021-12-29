import random
import torch
from python.nlp_utils import bag_of_words, tokenize


class ChatBot:

    def __init__(self, model, all_words, tags, intents):
        self.model = model
        self.all_words = all_words
        self.tags = tags
        self.intents = intents

    def answer(self, sentence) -> str:
        X = bag_of_words(tokenize(sentence), self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        prob = torch.softmax(output, dim=1)[0][predicted.item()]

        if prob.item() > 0.75:
            responses = next(filter(lambda intent: intent['tag'] == tag, self.intents['intents']))['responses']
            response = random.choice(responses)
        else:
            response = "I don't understand..."

        return response



