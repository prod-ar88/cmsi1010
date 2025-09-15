import random

words = {
    "noun": ["dog", "carrot", "chair", "toy", "rice cake", "apartment", "boulevard"],
    "verb": ["ran", "barked", "squeaked", "flew", "fell", "whistled", "exhausted"],
    "adjective": ["small", "great", "fuzzy", "funny", "light", "hilarious"],
    "preposition": ["through", "over", "under", "beyond", "across"],
    "adverb": ["barely", "mostly", "easily", "already", "just"],
    "color": ["pink", "blue", "mauve", "red", "transparent", "turqoise", "gold"],
    "slang": ["skibidi", "rizz", "brainrot", "67", "41", "sigma", "beta", "ohio", "mewing", "gamma"]
}

template = """
    Yesterday the color noun
    verb preposition the coach’s slang
    adjective color noun that was
    adverb adjective before slang
    """


def random_sentence():
    sentence = []
    for token in template.split():
        if token in words:
            sentence.append(random.choice(words[token]))
        else:
            sentence.append(token)
    return " ".join(sentence) + "."


for _ in range(5):
    print(random_sentence())
