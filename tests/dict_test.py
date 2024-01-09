# type: ignore
import re

import pytest

from magic_collections import dict

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
