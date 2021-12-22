import random
import json
import torch
from python.model import NeuralNet
from python.main import bag_of_words, tokenize


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


def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('../data/intents.json', 'r') as f:
        intents = json.load(f)

    data = torch.load("../models/bot_model.pth")
    input_size = data["input_size"]
    output_size = data["output_size"]
    hidden_size = data["hidden_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    return ChatBot(model, all_words, tags, intents)
