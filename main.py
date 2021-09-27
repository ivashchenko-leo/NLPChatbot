import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence: str):
    return nltk.word_tokenize(sentence, "english")


def stem(word: str):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    stemmed_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for i, w in enumerate(all_words):
        if w in stemmed_sentence:
            bag[i] = 1.0

    return bag
