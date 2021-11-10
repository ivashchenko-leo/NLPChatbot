import json
import numpy as np
from python.model import NeuralNet
from python.main import tokenize, stem, bag_of_words

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


def train_model():
    with open('../data/intents.json', 'r') as f:
        intents = json.load(f)

    all_words = []
    tags = sorted(set([intent['tag'] for intent in intents['intents']]))
    xy = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
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

    # Hyperparameters
    batch_size = 8
    input_size = len(X_train[0])
    hidden_size = 8
    output_size = len(tags)
    learning_rate = 0.001
    num_epochs = 500

    dataset = ChatDataset(X_train, y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

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
            print(f'epoch {epoch + 1}/{num_epochs}, loss={loss.item():.4f}')

    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    torch.save(data, "../models/bot_model.pth")
    print(f'training complete, model saved to bot_model.pth')


class ChatDataset(Dataset):

    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train.astype(np.int64)

    def __getitem__(self, item):
        return self.x_data[item], self.y_data[item]

    def __len__(self):
        return self.n_samples
