# type: ignore
import random
import re

import pytest

from magic_collections import dict
from magic_collections import list
from tests.utils import len_mean

"""
• `test_*_ok` => for function calls that return a result
• `test_*_err` => for function calls that throw an exception

Note that some functions never throw an exception, which means that they don't have a
`test_*_err` variant.
"""

_RANDOM_SEED = 0


@pytest.fixture
def prebuild_dict(request):
    match request.param:
        case "dict_int_int_filled":
            return dict({0: 3, 1: 5, 2: 20, 3: -1, -8: 0})
        case "dict_str_int_filled":
            return dict(
                {
                    "apples": 3,
                    "bananas": 5,
                    "oranges": 20,
                    "tangerines": -1,
                },
            )
        case "dict_str_list_filled":
            return dict(
                {
                    "hello": ["hi", "sup", "goodday"],
                    "goodbye": ["bye", "ciao"],
                },
            )
        case "dict_empty":
            return dict()


@pytest.mark.parametrize(
    ["prebuild_dict", "result"],
    [
        ["dict_int_int_filled", dict({3: 0, 5: 1, 20: 2, -1: 3, 0: -8})],
        [
            "dict_str_int_filled",
            dict(
                {
                    3: "apples",
                    5: "bananas",
                    20: "oranges",
                    -1: "tangerines",
                },
            ),
        ],
        ["dict_empty", dict()],
    ],
    indirect=["prebuild_dict"],
)
def test___invert___ok(prebuild_dict, result):
    assert ~prebuild_dict == result


@pytest.mark.parametrize(
    ["prebuild_dict", "exception", "message"],
    [
        [
            "dict_str_list_filled",
            TypeError,
            f"value {['hi', 'sup', 'goodday']} cannot be hashed to a key",
        ],
    ],
    indirect=["prebuild_dict"],
)
def test___invert___err(prebuild_dict, exception, message):
    with pytest.raises(exception, match=re.escape(message)):
        ~prebuild_dict


@pytest.mark.parametrize(
    ["prebuild_dict", "kwargs", "result"],
    [
        [
            "dict_int_int_filled",
            {},
            dict(
                {
                    -8: 0,
                    0: 3,
                    1: 5,
                    2: 20,
                    3: -1,
                },
            ),
        ],
        [
            "dict_int_int_filled",
            {"reverse": True},
            dict(
                {
                    3: -1,
                    2: 20,
                    1: 5,
                    0: 3,
                    -8: 0,
                },
            ),
        ],
        [
            "dict_str_int_filled",
            {"key": len},
            dict(
                {
                    "apples": 3,
                    "bananas": 5,
                    "oranges": 20,
                    "tangerines": -1,
                },
            ),
        ],
        ["dict_empty", {}, dict()],
    ],
    indirect=["prebuild_dict"],
)
def test_sorted_ok(prebuild_dict, kwargs, result):
    assert prebuild_dict.sorted(**kwargs) == result


@pytest.mark.parametrize(
    ["prebuild_dict", "result"],
    [
        [
            "dict_int_int_filled",
            dict(
                {
                    3: -1,
                    0: 3,
                    2: 20,
                    -8: 0,
                    1: 5,
                },
            ),
        ],
        [
            "dict_str_int_filled",
            dict(
                {
                    "tangerines": -1,
                    "apples": 3,
                    "oranges": 20,
                    "bananas": 5,
                },
            ),
        ],
        [
            "dict_str_list_filled",
            dict(
                {
                    "goodbye": ["bye", "ciao"],
                    "hello": ["hi", "sup", "goodday"],
                },
            ),
        ],
        [
            "dict_empty",
            dict(),
        ],
    ],
    indirect=["prebuild_dict"],
)
def test_shuffled_ok(prebuild_dict, result):
    random.seed(_RANDOM_SEED)

    # We must compare them as lists, because dicts are always
    # equal as long as their pairs are the same, even if they're
    # not in the same order.
    assert list(prebuild_dict.shuffled()) == list(result)


@pytest.mark.parametrize(
    ["prebuild_dict", "args", "result"],
    [
        ["dict_int_int_filled", [lambda k, v: (v - k) >= 5], dict({2: 20, -8: 0})],
        [
            "dict_str_int_filled",
            [lambda k, v: len(k) >= v],
            dict(
                {
                    "apples": 3,
                    "bananas": 5,
                    "tangerines": -1,
                },
            ),
        ],
        [
            "dict_str_list_filled",
            [lambda k, v: len(k) > len_mean(v)],
            dict(
                {
                    "hello": ["hi", "sup", "goodday"],
                    "goodbye": ["bye", "ciao"],
                },
            ),
        ],
        ["dict_empty", [lambda k, v: k == v], dict()],
    ],
    indirect=["prebuild_dict"],
)
def test_filter_ok(prebuild_dict, args, result):
    assert prebuild_dict.filter(*args) == result


@pytest.mark.parametrize(
    ["prebuild_dict", "args", "result"],
    [
        ["dict_int_int_filled", [lambda key: key > 1], dict({2: 20, 3: -1})],
        ["dict_str_int_filled", [lambda key: key[-2] != "e"], dict({"bananas": 5})],
        [
            "dict_str_list_filled",
            [lambda key: key == "hello"],
            dict({"hello": ["hi", "sup", "goodday"]}),
        ],
        ["dict_empty", [lambda _: True], dict()],
    ],
    indirect=["prebuild_dict"],
)
def test_filter_keys_ok(prebuild_dict, args, result):
    assert prebuild_dict.filter_keys(*args) == result


@pytest.mark.parametrize(
    ["prebuild_dict", "result"],
    [
        [
            "dict_int_int_filled",
            list(
                [
                    (0, 3),
                    (1, 5),
                    (2, 20),
                    (3, -1),
                    (-8, 0),
                ],
            ),
        ],
        [
            "dict_str_int_filled",
            list(
                [
                    ("apples", 3),
                    ("bananas", 5),
                    ("oranges", 20),
                    ("tangerines", -1),
                ],
            ),
        ],
        [
            "dict_str_list_filled",
            list(
                [
                    ("hello", ["hi", "sup", "goodday"]),
                    ("goodbye", ["bye", "ciao"]),
                ],
            ),
        ],
        ["dict_empty", list()],
    ],
    indirect=["prebuild_dict"],
)
def test_as_list_ok(prebuild_dict, result):
    assert prebuild_dict.as_list() == result
