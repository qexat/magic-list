# type: ignore
from magic_collections import list


def double(x):
    return x * 2


def greater_than_four(x):
    return x > 4


def contains_letter_l(x):
    return "l" in x


def len_mean(words):
    return list(words).map(len).mean()
