import nltk


def tokenize(word):
    tokens = nltk.word_tokenize(word.lower())
    return tokens
