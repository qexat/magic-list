import functools
import operator


def double(x):
    return x * 2


def greater_than_four(x):
    return x > 4


def contains_letter_l(x):
    return "l" in x


def reduce_right_sub(l):
    return functools.reduce(operator.sub, reversed(l), 0)
