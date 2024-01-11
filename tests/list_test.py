# type: ignore
import operator
import random

import pytest

from .utils import contains_letter_l
from .utils import double
from .utils import greater_than_four
from magic_collections import L
from magic_collections import list


"""
• `test_*_ok` => for function calls that return a result
• `test_*_err` => for function calls that throw an exception

Note that some functions never throw an exception, which means that they don't have a
`test_*_err` variant.
"""


_RANDOM_SEED = 0


@pytest.fixture
def prebuild_list(request):
    match request.param:
        case "list_int_filled":
            return list([3, 5, 20, -1])
        case "list_str_filled":
            return list(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ],
            )
        case "list_empty":
            return list()


# *- PROPERTIES -* #


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 3],
        ["list_str_filled", "hello"],
    ],
    indirect=["prebuild_list"],
)
def test_head_ok(prebuild_list, result):
    assert prebuild_list.head == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_empty", TypeError, "empty list has no head"],
    ],
    indirect=["prebuild_list"],
)
def test_head_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.head


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", [5, 20, -1]],
        [
            "list_str_filled",
            list(["bonjour", "holá", "ciao"]),
        ],
    ],
    indirect=["prebuild_list"],
)
def test_tail_ok(prebuild_list, result):
    assert prebuild_list.tail == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_empty", TypeError, "empty list has no tail"],
    ],
    indirect=["prebuild_list"],
)
def test_tail_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.tail


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", [3, 5, 20]],
        [
            "list_str_filled",
            list(["hello", "bonjour", "holá"]),
        ],
    ],
    indirect=["prebuild_list"],
)
def test_init_ok(prebuild_list, result):
    assert prebuild_list.init == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_empty", TypeError, "empty list has no init"],
    ],
    indirect=["prebuild_list"],
)
def test_init_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.init


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", -1],
        ["list_str_filled", "ciao"],
    ],
    indirect=["prebuild_list"],
)
def test_last_ok(prebuild_list, result):
    assert prebuild_list.last == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_empty", TypeError, "empty list has no last"],
    ],
    indirect=["prebuild_list"],
)
def test_last_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.last


# *- METHODS -* #


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [14], list([14, 3, 5, 20, -1])],
        [
            "list_str_filled",
            ["annyeong"],
            list(
                [
                    "annyeong",
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ],
            ),
        ],
        ["list_empty", [-5], list([-5])],
    ],
    indirect=["prebuild_list"],
)
def test_prepend_ok(prebuild_list, args, result):
    prebuild_list.prepend(*args)
    assert prebuild_list == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list([-1, 20, 5, 3])],
        ["list_str_filled", list(["ciao", "holá", "bonjour", "hello"])],
        ["list_empty", list()],
    ],
    indirect=["prebuild_list"],
)
def test_reversed_ok(prebuild_list, result):
    assert prebuild_list.reversed() == result


@pytest.mark.parametrize(
    ["prebuild_list", "kwargs", "result"],
    [
        ["list_int_filled", {}, list([-1, 3, 5, 20])],
        ["list_str_filled", {"key": len}, list(["holá", "ciao", "hello", "bonjour"])],
        ["list_int_filled", {"reverse": True}, list([20, 5, 3, -1])],
        [
            "list_str_filled",
            {"key": len, "reverse": True},
            list(["bonjour", "hello", "holá", "ciao"]),
        ],
        ["list_empty", {}, list()],
    ],
    indirect=["prebuild_list"],
)
def test_sorted_ok(prebuild_list, kwargs, result):
    assert prebuild_list.sorted(**kwargs) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [], list([-1, 3, 20, 5])],
        ["list_str_filled", [], list(["ciao", "hello", "holá", "bonjour"])],
        ["list_empty", [], list([])],
    ],
    indirect=["prebuild_list"],
)
def test_shuffled_ok(prebuild_list, args, result):
    random.seed(_RANDOM_SEED)
    assert prebuild_list.shuffled(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [double], list([6, 10, 40, -2])],
        [
            "list_str_filled",
            [double],
            list(["hellohello", "bonjourbonjour", "holáholá", "ciaociao"]),
        ],
        ["list_empty", [double], list()],
    ],
    indirect=["prebuild_list"],
)
def test_map_ok(prebuild_list, args, result):
    assert prebuild_list.map(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [], list([-1, 3, 5, 20])],
        ["list_int_filled", [2], list([20, -1, 3, 5])],
        [
            "list_int_filled",
            [-2],
            list([20, -1, 3, 5]),
        ],
        ["list_str_filled", [0], list(["hello", "bonjour", "holá", "ciao"])],
    ],
    indirect=["prebuild_list"],
)
def test_rotate_ok(prebuild_list, args, result):
    assert prebuild_list.rotate(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_empty", [], TypeError, "empty list cannot be rotated"],
    ],
    indirect=["prebuild_list"],
)
def test_rotate_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.rotate(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [greater_than_four], list([5, 20])],
        ["list_str_filled", [contains_letter_l], list(["hello", "holá"])],
        ["list_empty", [greater_than_four], list()],
    ],
    indirect=["prebuild_list"],
)
def test_filter_ok(prebuild_list, args, result):
    assert prebuild_list.filter(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [[0, 1, 0, 1]], list([5, -1])],
        ["list_str_filled", [[1, 0, 0, 0]], list(["hello"])],
        ["list_empty", [[]], list()],
    ],
    indirect=["prebuild_list"],
)
def test_mask_ok(prebuild_list, args, result):
    assert prebuild_list.mask(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [[0, 1]],
            TypeError,
            "mask length must be the same as the list",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_mask_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.mask(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add], 27],
        ["list_str_filled", [operator.add], "hellobonjourholáciao"],
        ["list_int_filled", [operator.mul], -300],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_ok(prebuild_list, args, result):
    assert prebuild_list.reduce(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_str_filled", [operator.mul], TypeError, "can't multiply sequence"],
        [
            "list_empty",
            [operator.add],
            TypeError,
            "the list to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.reduce(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.sub], 19],
        ["list_str_filled", [operator.add], "hellobonjourholáciao"],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_right_ok(prebuild_list, args, result):
    assert prebuild_list.reduce_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_str_filled", [operator.mul], TypeError, "can't multiply sequence"],
        [
            "list_empty",
            [operator.add],
            TypeError,
            "the list to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_right_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.reduce_right(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add, 3], 30],
        ["list_str_filled", [operator.add, "annyeong"], "annyeonghellobonjourholáciao"],
        ["list_int_filled", [operator.mul, 0], 0],
        ["list_empty", [operator.add, 0], 0],
    ],
    indirect=["prebuild_list"],
)
def test_fold_ok(prebuild_list, args, result):
    assert prebuild_list.fold(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_str_filled",
            [operator.mul, "annyeong"],
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fold_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fold(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add, 3], 30],
        ["list_str_filled", [operator.add, "annyeong"], "hellobonjourholáciaoannyeong"],
        ["list_int_filled", [operator.sub, 0], 19],
        ["list_empty", [operator.add, 0], 0],
    ],
    indirect=["prebuild_list"],
)
def test_fold_right_ok(prebuild_list, args, result):
    assert prebuild_list.fold_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_str_filled",
            [operator.mul, "annyeong"],
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fold_right_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fold_right(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add, 0], list([0, 3, 8, 28, 27])],
        [
            "list_str_filled",
            [operator.add, ""],
            list(
                [
                    "",
                    "hello",
                    "hellobonjour",
                    "hellobonjourholá",
                    "hellobonjourholáciao",
                ],
            ),
        ],
        ["list_empty", [operator.add, 0], list([0])],
        ["list_empty", [operator.add, "hello"], list(["hello"])],
    ],
    indirect=["prebuild_list"],
)
def test_scan_ok(prebuild_list, args, result):
    assert prebuild_list.scan(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add, 0], list([0, -1, 19, 24, 27])],
        [
            "list_str_filled",
            [operator.add, ""],
            list(
                [
                    "",
                    "ciao",
                    "holáciao",
                    "bonjourholáciao",
                    "hellobonjourholáciao",
                ],
            ),
        ],
        ["list_empty", [operator.add, 0], list([0])],
        ["list_empty", [operator.add, "hello"], list(["hello"])],
    ],
    indirect=["prebuild_list"],
)
def test_scan_right_ok(prebuild_list, args, result):
    assert prebuild_list.scan_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add, [-1, 4, -9, 16]], list([2, 9, 11, 15])],
        [
            "list_str_filled",
            [operator.add, [".", " !", "...", "?"]],
            list(
                [
                    "hello.",
                    "bonjour !",
                    "holá...",
                    "ciao?",
                ],
            ),
        ],
        ["list_empty", [operator.add, []], list()],
    ],
    indirect=["prebuild_list"],
)
def test_zip_with_ok(prebuild_list, args, result):
    assert prebuild_list.zip_with(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [operator.add, []],
            TypeError,
            "the length of the two sequences must be equal",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_zip_with_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.zip_with(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [], 27],
        ["list_str_filled", [], "hellobonjourholáciao"],
    ],
    indirect=["prebuild_list"],
)
def test_sum_ok(prebuild_list, args, result):
    assert prebuild_list.sum(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_empty", [], TypeError, "cannot perform summation on an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_sum_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.sum(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [], 6.75],
    ],
    indirect=["prebuild_list"],
)
def test_mean_ok(prebuild_list, args, result):
    assert prebuild_list.mean(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_str_filled", [], TypeError, "cannot calculate mean of list of str"],
        ["list_empty", [], TypeError, "cannot calculate mean of empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_mean_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.mean(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [0, 3], list([3, 5, 20, -1, 0, 0, 0])],
        [
            "list_str_filled",
            ["annyeong", 2],
            list(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "annyeong",
                    "annyeong",
                ],
            ),
        ],
        ["list_empty", [10, 5], list([10, 10, 10, 10, 10])],
        ["list_empty", ["hi", 4], list(["hi", "hi", "hi", "hi"])],
        [
            "list_int_filled",
            [sum, 3],
            list([3, 5, 20, -1, 27, 54, 108]),
        ],
        [
            "list_str_filled",
            [lambda lst: lst[-1][::-1], 2],
            list(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "oaic",
                    "ciao",
                ],
            ),
        ],
        ["list_empty", [lambda lst: len(lst), 4], list([0, 1, 2, 3])],
    ],
    indirect=["prebuild_list"],
)
def test_filled_ok(prebuild_list, args, result):
    assert prebuild_list.filled(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [0, -2],
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_filled_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.filled(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [0, 3], list([3, 5, 20, -1, 0, 0, 0])],
        [
            "list_str_filled",
            ["annyeong", 2],
            list(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "annyeong",
                    "annyeong",
                ],
            ),
        ],
        ["list_empty", [10, 5], list([10, 10, 10, 10, 10])],
        ["list_empty", ["hi", 4], list(["hi", "hi", "hi", "hi"])],
        [
            "list_int_filled",
            [sum, 3],
            list([3, 5, 20, -1, 27, 54, 108]),
        ],
        [
            "list_str_filled",
            [lambda lst: lst[-1][::-1], 2],
            list(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "oaic",
                    "ciao",
                ],
            ),
        ],
        ["list_empty", [lambda lst: len(lst), 4], list([0, 1, 2, 3])],
    ],
    indirect=["prebuild_list"],
)
def test_fill_ok(prebuild_list, args, result):
    prebuild_list.fill(*args)
    assert prebuild_list == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [0, -2],
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fill_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fill(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [0], list([3, 0, 5, 0, 20, 0, -1])],
        [
            "list_str_filled",
            [" "],
            list(["hello", " ", "bonjour", " ", "holá", " ", "ciao"]),
        ],
        ["list_int_filled", [lambda p, n: p + n], list([3, 8, 5, 25, 20, 19, -1])],
        [
            "list_str_filled",
            [lambda p, n: p[-1] + n[0]],
            list(["hello", "ob", "bonjour", "rh", "holá", "ác", "ciao"]),
        ],
    ],
    indirect=["prebuild_list"],
)
def test_gap_fill_ok(prebuild_list, args, result):
    assert prebuild_list.gap_fill(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_empty", [None], ValueError, "empty list has no gap to be filled"],
    ],
    indirect=["prebuild_list"],
)
def test_gap_fill_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.gap_fill(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [[1, 3]], list([5, -1])],
        ["list_int_filled", [[]], list()],
        ["list_int_filled", [[2, 0, 0]], list([20, 3, 3])],
        ["list_str_filled", [[1, 2]], list(["bonjour", "holá"])],
        ["list_str_filled", [[-2]], list(["holá"])],
        ["list_empty", [[]], list()],
    ],
    indirect=["prebuild_list"],
)
def test_select_ok(prebuild_list, args, result):
    assert prebuild_list.select(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_int_filled", [[4, 1]], IndexError, "index 4 is out of bounds"],
        ["list_empty", [[0]], IndexError, "index 0 is out of bounds"],
    ],
    indirect=["prebuild_list"],
)
def test_select_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.select(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [2], list([3, 5])],
        ["list_str_filled", [3], list(["hello", "bonjour", "holá"])],
        ["list_int_filled", [0], list()],
        ["list_empty", [0], list()],
    ],
    indirect=["prebuild_list"],
)
def test_take_ok(prebuild_list, args, result):
    assert prebuild_list.take(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [10],
            ValueError,
            "cannot take more items than the list contains",
        ],
        [
            "list_int_filled",
            [-1],
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "list_empty",
            [1],
            ValueError,
            "cannot take more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_take_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.take(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [2], [20, -1]],
        ["list_str_filled", [3], list(["bonjour", "holá", "ciao"])],
        ["list_int_filled", [0], list()],
        ["list_empty", [0], list()],
    ],
    indirect=["prebuild_list"],
)
def test_take_right_ok(prebuild_list, args, result):
    assert prebuild_list.take_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [10],
            ValueError,
            "cannot take more items than the list contains",
        ],
        [
            "list_int_filled",
            [-1],
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "list_empty",
            [1],
            ValueError,
            "cannot take more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_take_right_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.take_right(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [2], list([20, -1])],
        ["list_str_filled", [3], list(["ciao"])],
        ["list_int_filled", [0], list([3, 5, 20, -1])],
        ["list_empty", [0], list()],
    ],
    indirect=["prebuild_list"],
)
def test_drop_ok(prebuild_list, args, result):
    assert prebuild_list.drop(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [10],
            ValueError,
            "cannot drop more items than the list contains",
        ],
        [
            "list_int_filled",
            [-1],
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "list_empty",
            [1],
            ValueError,
            "cannot drop more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_drop_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.drop(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [2], list([3, 5])],
        ["list_str_filled", [3], list(["hello"])],
        ["list_int_filled", [0], list([3, 5, 20, -1])],
        ["list_empty", [0], list()],
    ],
    indirect=["prebuild_list"],
)
def test_drop_right_ok(prebuild_list, args, result):
    assert prebuild_list.drop_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_int_filled",
            [10],
            ValueError,
            "cannot drop more items than the list contains",
        ],
        [
            "list_int_filled",
            [-1],
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "list_empty",
            [1],
            ValueError,
            "cannot drop more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_drop_right_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.drop_right(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [1, 2], list([5, 20])],
        ["list_str_filled", [2, 3], list(["holá", "ciao"])],
        ["list_int_filled", [0, 0], list([3])],
        ["list_str_filled", [3, 3], list(["ciao"])],
    ],
    indirect=["prebuild_list"],
)
def test_slice_ok(prebuild_list, args, result):
    assert prebuild_list.slice(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        ["list_int_filled", [2, 10], ValueError, "slice out of bounds"],
        ["list_empty", [0, 2], ValueError, "slice out of bounds"],
        ["list_int_filled", [2, 1], ValueError, "start cannot be greater than stop"],
    ],
    indirect=["prebuild_list"],
)
def test_slice_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.slice(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [2], (list([3, 5]), list([20, -1]))],
        ["list_int_filled", [0], (list(), list([3, 5, 20, -1]))],
        ["list_int_filled", [4], (list([3, 5, 20, -1]), list())],
        ["list_str_filled", [2], (list(["hello", "bonjour"]), list(["holá", "ciao"]))],
        ["list_str_filled", [6], (list(["hello", "bonjour", "holá", "ciao"]), list())],
    ],
    indirect=["prebuild_list"],
)
def test_bisect_ok(prebuild_list, args, result):
    assert prebuild_list.bisect(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception", "message"],
    [
        [
            "list_str_filled",
            [-2],
            ValueError,
            "cannot bisect after a negative amount of elements",
        ],
        ["list_empty", [2], TypeError, "cannot bisect an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_bisect_err(prebuild_list, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.bisect(*args)


# *- "combined" tests -* #


def test_fib():
    base = L[0, 1]
    result = L[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    assert base.filled(lambda lst: lst.take_right(2).sum(), 9) == result
