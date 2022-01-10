import torch
import numpy as np
import torch.nn as nn
import logging
from nn_model.chat import ChatBot
from torch.utils.data import Dataset, DataLoader
from nlp_utils import tokenize, stem, bag_of_words


class NeuralNet(nn.Module):

    def __init__(self, input_size, hidden_size, n_classes):
        super().__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, n_classes)

        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.relu(self.l1(x))
        out = self.relu(self.l2(out))

        return self.l3(out)


class ChatDataset(Dataset):

    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train.astype(np.int64)

    def __getitem__(self, item):
        return self.x_data[item], self.y_data[item]

    def __len__(self):
        return self.n_samples


"""
intents -> [(['sixty eight'], 'sixty eight'), (['text', 'sixty nine'], 'sixty nine')]
list of tuples, each tuple contains a list of patterns and a group tag
"""


def train(intents, batch_size=8, hidden_size=8, learning_rate=0.001, num_epochs=500, path="../models/bot_model.pth"):
    all_words = []
    tags = sorted(set(intent[1] for intent in intents))
    xy = []
    for intent in intents:
        for pattern in intent[0]:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, intent[1]))

    all_words = sorted(set([stem(w) for w in all_words if w.isalpha()]))

    X_train = []
    y_train = []
    for (pattern, tag) in xy:
        bag = bag_of_words(pattern, all_words)
        X_train.append(bag)

        y_train.append(tags.index(tag))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    input_size = len(X_train[0])
    output_size = len(tags)

    dataset = ChatDataset(X_train, y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=1)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    logger = logging.getLogger()

    logger.info("Start fitting...")
    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)

            outputs = model.forward(words)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 100 == 0:
            logger.info(f'Epoch {epoch + 1}/{num_epochs}, loss={loss.item():.4f}')

    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    torch.save(data, path)
    logger.info(f'Training complete, model saved to {path}')


def load():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

    return ChatBot(model, all_words, tags)
