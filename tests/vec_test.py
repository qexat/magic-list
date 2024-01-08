# type: ignore
import operator
import random

import pytest

from magic_collections import Vec
from magic_collections import vec


"""
• `test_*_ok` => for function calls that return a result
• `test_*_err` => for function calls that throw an exception

Note that some functions never throw an exception, which means that they don't have a
`test_*_err` variant.
"""


_RANDOM_SEED = 0


@pytest.fixture
def prebuild_vec(request):
    match request.param:
        case "vec_int_filled":
            return Vec([3, 5, 20, -1])
        case "vec_str_filled":
            return Vec(
                [
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ],
            )
        case "vec_empty":
            return Vec()


def double(x):
    return x * 2


def greater_than_four(x):
    return x > 4


def contains_letter_l(x):
    return "l" in x


# *- PROPERTIES -* #


@pytest.mark.parametrize(
    ["prebuild_vec", "result"],
    [
        ["vec_int_filled", 3],
        ["vec_str_filled", "hello"],
    ],
    indirect=["prebuild_vec"],
)
def test_head_ok(prebuild_vec, result):
    assert prebuild_vec.head == result


@pytest.mark.parametrize(
    ["prebuild_vec", "exception", "message"],
    [
        ["vec_empty", TypeError, "empty vector has no head"],
    ],
    indirect=["prebuild_vec"],
)
def test_head_err(prebuild_vec, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.head


@pytest.mark.parametrize(
    ["prebuild_vec", "result"],
    [
        ["vec_int_filled", [5, 20, -1]],
        [
            "vec_str_filled",
            Vec(["bonjour", "holá", "ciao"]),
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_tail_ok(prebuild_vec, result):
    assert prebuild_vec.tail == result


@pytest.mark.parametrize(
    ["prebuild_vec", "exception", "message"],
    [
        ["vec_empty", TypeError, "empty vector has no tail"],
    ],
    indirect=["prebuild_vec"],
)
def test_tail_err(prebuild_vec, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.tail


@pytest.mark.parametrize(
    ["prebuild_vec", "result"],
    [
        ["vec_int_filled", [3, 5, 20]],
        [
            "vec_str_filled",
            Vec(["hello", "bonjour", "holá"]),
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_init_ok(prebuild_vec, result):
    assert prebuild_vec.init == result


@pytest.mark.parametrize(
    ["prebuild_vec", "exception", "message"],
    [
        ["vec_empty", TypeError, "empty vector has no init"],
    ],
    indirect=["prebuild_vec"],
)
def test_init_err(prebuild_vec, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.init


@pytest.mark.parametrize(
    ["prebuild_vec", "result"],
    [
        ["vec_int_filled", -1],
        ["vec_str_filled", "ciao"],
    ],
    indirect=["prebuild_vec"],
)
def test_last_ok(prebuild_vec, result):
    assert prebuild_vec.last == result


@pytest.mark.parametrize(
    ["prebuild_vec", "exception", "message"],
    [
        ["vec_empty", TypeError, "empty vector has no last"],
    ],
    indirect=["prebuild_vec"],
)
def test_last_err(prebuild_vec, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.last


# *- METHODS -* #


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [14], Vec([14, 3, 5, 20, -1])],
        [
            "vec_str_filled",
            ["annyeong"],
            Vec(
                [
                    "annyeong",
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ],
            ),
        ],
        ["vec_empty", [-5], Vec([-5])],
    ],
    indirect=["prebuild_vec"],
)
def test_prepend_ok(prebuild_vec, args, result):
    prebuild_vec.prepend(*args)
    assert prebuild_vec == result


@pytest.mark.parametrize(
    ["prebuild_vec", "result"],
    [
        ["vec_int_filled", Vec([-1, 20, 5, 3])],
        ["vec_str_filled", Vec(["ciao", "holá", "bonjour", "hello"])],
        ["vec_empty", Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_reversed_ok(prebuild_vec, result):
    assert prebuild_vec.reversed() == result


@pytest.mark.parametrize(
    ["prebuild_vec", "kwargs", "result"],
    [
        ["vec_int_filled", {}, Vec([-1, 3, 5, 20])],
        ["vec_str_filled", {"key": len}, Vec(["holá", "ciao", "hello", "bonjour"])],
        ["vec_int_filled", {"reverse": True}, Vec([20, 5, 3, -1])],
        [
            "vec_str_filled",
            {"key": len, "reverse": True},
            Vec(["bonjour", "hello", "holá", "ciao"]),
        ],
        ["vec_empty", {}, Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_sorted_ok(prebuild_vec, kwargs, result):
    assert prebuild_vec.sorted(**kwargs) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [], Vec([-1, 3, 20, 5])],
        ["vec_str_filled", [], Vec(["ciao", "hello", "holá", "bonjour"])],
        ["vec_empty", [], Vec([])],
    ],
    indirect=["prebuild_vec"],
)
def test_shuffled_ok(prebuild_vec, args, result):
    random.seed(_RANDOM_SEED)
    assert prebuild_vec.shuffled(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [double], Vec([6, 10, 40, -2])],
        [
            "vec_str_filled",
            [double],
            Vec(["hellohello", "bonjourbonjour", "holáholá", "ciaociao"]),
        ],
        ["vec_empty", [double], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_map_ok(prebuild_vec, args, result):
    assert prebuild_vec.map(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [], Vec([-1, 3, 5, 20])],
        ["vec_int_filled", [2], Vec([20, -1, 3, 5])],
        [
            "vec_int_filled",
            [-2],
            Vec([20, -1, 3, 5]),
        ],
        ["vec_str_filled", [0], Vec(["hello", "bonjour", "holá", "ciao"])],
    ],
    indirect=["prebuild_vec"],
)
def test_rotate_ok(prebuild_vec, args, result):
    assert prebuild_vec.rotate(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_empty", [], TypeError, "empty vector cannot be rotated"],
    ],
    indirect=["prebuild_vec"],
)
def test_rotate_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.rotate(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [greater_than_four], Vec([5, 20])],
        ["vec_str_filled", [contains_letter_l], Vec(["hello", "holá"])],
        ["vec_empty", [greater_than_four], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_filter_ok(prebuild_vec, args, result):
    assert prebuild_vec.filter(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [[0, 1, 0, 1]], Vec([5, -1])],
        ["vec_str_filled", [[1, 0, 0, 0]], Vec(["hello"])],
        ["vec_empty", [[]], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_mask_ok(prebuild_vec, args, result):
    assert prebuild_vec.mask(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [[0, 1]],
            TypeError,
            "mask length must be the same as the vector",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_mask_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.mask(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add], 27],
        ["vec_str_filled", [operator.add], "hellobonjourholáciao"],
        ["vec_int_filled", [operator.mul], -300],
    ],
    indirect=["prebuild_vec"],
)
def test_reduce_ok(prebuild_vec, args, result):
    assert prebuild_vec.reduce(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_str_filled", [operator.mul], TypeError, "can't multiply sequence"],
        [
            "vec_empty",
            [operator.add],
            TypeError,
            "the vector to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_reduce_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.reduce(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.sub], 19],
        ["vec_str_filled", [operator.add], "hellobonjourholáciao"],
    ],
    indirect=["prebuild_vec"],
)
def test_reduce_right_ok(prebuild_vec, args, result):
    assert prebuild_vec.reduce_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_str_filled", [operator.mul], TypeError, "can't multiply sequence"],
        [
            "vec_empty",
            [operator.add],
            TypeError,
            "the vector to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_reduce_right_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.reduce_right(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add, 3], 30],
        ["vec_str_filled", [operator.add, "annyeong"], "annyeonghellobonjourholáciao"],
        ["vec_int_filled", [operator.mul, 0], 0],
        ["vec_empty", [operator.add, 0], 0],
    ],
    indirect=["prebuild_vec"],
)
def test_fold_ok(prebuild_vec, args, result):
    assert prebuild_vec.fold(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_str_filled",
            [operator.mul, "annyeong"],
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_fold_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.fold(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add, 3], 30],
        ["vec_str_filled", [operator.add, "annyeong"], "hellobonjourholáciaoannyeong"],
        ["vec_int_filled", [operator.sub, 0], 19],
        ["vec_empty", [operator.add, 0], 0],
    ],
    indirect=["prebuild_vec"],
)
def test_fold_right_ok(prebuild_vec, args, result):
    assert prebuild_vec.fold_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_str_filled",
            [operator.mul, "annyeong"],
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_fold_right_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.fold_right(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add, 0], Vec([0, 3, 8, 28, 27])],
        [
            "vec_str_filled",
            [operator.add, ""],
            Vec(
                [
                    "",
                    "hello",
                    "hellobonjour",
                    "hellobonjourholá",
                    "hellobonjourholáciao",
                ],
            ),
        ],
        ["vec_empty", [operator.add, 0], Vec([0])],
        ["vec_empty", [operator.add, "hello"], Vec(["hello"])],
    ],
    indirect=["prebuild_vec"],
)
def test_scan_ok(prebuild_vec, args, result):
    assert prebuild_vec.scan(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add, 0], Vec([0, -1, 19, 24, 27])],
        [
            "vec_str_filled",
            [operator.add, ""],
            Vec(
                [
                    "",
                    "ciao",
                    "holáciao",
                    "bonjourholáciao",
                    "hellobonjourholáciao",
                ],
            ),
        ],
        ["vec_empty", [operator.add, 0], Vec([0])],
        ["vec_empty", [operator.add, "hello"], Vec(["hello"])],
    ],
    indirect=["prebuild_vec"],
)
def test_scan_right_ok(prebuild_vec, args, result):
    assert prebuild_vec.scan_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [operator.add, [-1, 4, -9, 16]], Vec([2, 9, 11, 15])],
        [
            "vec_str_filled",
            [operator.add, [".", " !", "...", "?"]],
            Vec(
                [
                    "hello.",
                    "bonjour !",
                    "holá...",
                    "ciao?",
                ],
            ),
        ],
        ["vec_empty", [operator.add, []], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_merge_ok(prebuild_vec, args, result):
    assert prebuild_vec.merge(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [operator.add, []],
            TypeError,
            "the length of the two sequences must be equal",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_merge_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.merge(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [], 27],
        ["vec_str_filled", [], "hellobonjourholáciao"],
    ],
    indirect=["prebuild_vec"],
)
def test_sum_ok(prebuild_vec, args, result):
    assert prebuild_vec.sum(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_empty", [], TypeError, "cannot perform summation on an empty vector"],
    ],
    indirect=["prebuild_vec"],
)
def test_sum_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.sum(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [], 6.75],
    ],
    indirect=["prebuild_vec"],
)
def test_mean_ok(prebuild_vec, args, result):
    assert prebuild_vec.mean(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_str_filled", [], TypeError, "cannot calculate mean of vector of str"],
        ["vec_empty", [], TypeError, "cannot calculate mean of empty vector"],
    ],
    indirect=["prebuild_vec"],
)
def test_mean_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.mean(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [0, 3], Vec([3, 5, 20, -1, 0, 0, 0])],
        [
            "vec_str_filled",
            ["annyeong", 2],
            Vec(
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
        ["vec_empty", [10, 5], Vec([10, 10, 10, 10, 10])],
        ["vec_empty", ["hi", 4], Vec(["hi", "hi", "hi", "hi"])],
        [
            "vec_int_filled",
            [sum, 3],
            Vec([3, 5, 20, -1, 27, 54, 108]),
        ],
        [
            "vec_str_filled",
            [lambda lst: lst[-1][::-1], 2],
            Vec(
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
        ["vec_empty", [lambda lst: len(lst), 4], Vec([0, 1, 2, 3])],
    ],
    indirect=["prebuild_vec"],
)
def test_filled_ok(prebuild_vec, args, result):
    assert prebuild_vec.filled(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [0, -2],
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_filled_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.filled(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [0, 3], Vec([3, 5, 20, -1, 0, 0, 0])],
        [
            "vec_str_filled",
            ["annyeong", 2],
            Vec(
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
        ["vec_empty", [10, 5], Vec([10, 10, 10, 10, 10])],
        ["vec_empty", ["hi", 4], Vec(["hi", "hi", "hi", "hi"])],
        [
            "vec_int_filled",
            [sum, 3],
            Vec([3, 5, 20, -1, 27, 54, 108]),
        ],
        [
            "vec_str_filled",
            [lambda lst: lst[-1][::-1], 2],
            Vec(
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
        ["vec_empty", [lambda lst: len(lst), 4], Vec([0, 1, 2, 3])],
    ],
    indirect=["prebuild_vec"],
)
def test_fill_ok(prebuild_vec, args, result):
    prebuild_vec.fill(*args)
    assert prebuild_vec == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [0, -2],
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_fill_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.fill(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [0], Vec([3, 0, 5, 0, 20, 0, -1])],
        [
            "vec_str_filled",
            [" "],
            Vec(["hello", " ", "bonjour", " ", "holá", " ", "ciao"]),
        ],
        ["vec_int_filled", [lambda p, n: p + n], Vec([3, 8, 5, 25, 20, 19, -1])],
        [
            "vec_str_filled",
            [lambda p, n: p[-1] + n[0]],
            Vec(["hello", "ob", "bonjour", "rh", "holá", "ác", "ciao"]),
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_gap_fill_ok(prebuild_vec, args, result):
    assert prebuild_vec.gap_fill(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_empty", [None], ValueError, "empty vector has no gap to be filled"],
    ],
    indirect=["prebuild_vec"],
)
def test_gap_fill_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.gap_fill(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [[1, 3]], Vec([5, -1])],
        ["vec_int_filled", [[]], Vec()],
        ["vec_int_filled", [[2, 0, 0]], Vec([20, 3, 3])],
        ["vec_str_filled", [[1, 2]], Vec(["bonjour", "holá"])],
        ["vec_str_filled", [[-2]], Vec(["holá"])],
        ["vec_empty", [[]], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_select_ok(prebuild_vec, args, result):
    assert prebuild_vec.select(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_int_filled", [[4, 1]], IndexError, "index 4 is out of bounds"],
        ["vec_empty", [[0]], IndexError, "index 0 is out of bounds"],
    ],
    indirect=["prebuild_vec"],
)
def test_select_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.select(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [2], Vec([3, 5])],
        ["vec_str_filled", [3], Vec(["hello", "bonjour", "holá"])],
        ["vec_int_filled", [0], Vec()],
        ["vec_empty", [0], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_take_ok(prebuild_vec, args, result):
    assert prebuild_vec.take(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [10],
            ValueError,
            "cannot take more items than the vector contains",
        ],
        [
            "vec_int_filled",
            [-1],
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "vec_empty",
            [1],
            ValueError,
            "cannot take more items than the vector contains",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_take_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.take(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [2], [20, -1]],
        ["vec_str_filled", [3], Vec(["bonjour", "holá", "ciao"])],
        ["vec_int_filled", [0], Vec()],
        ["vec_empty", [0], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_take_right_ok(prebuild_vec, args, result):
    assert prebuild_vec.take_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [10],
            ValueError,
            "cannot take more items than the vector contains",
        ],
        [
            "vec_int_filled",
            [-1],
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "vec_empty",
            [1],
            ValueError,
            "cannot take more items than the vector contains",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_take_right_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.take_right(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [2], Vec([20, -1])],
        ["vec_str_filled", [3], Vec(["ciao"])],
        ["vec_int_filled", [0], Vec([3, 5, 20, -1])],
        ["vec_empty", [0], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_drop_ok(prebuild_vec, args, result):
    assert prebuild_vec.drop(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [10],
            ValueError,
            "cannot drop more items than the vector contains",
        ],
        [
            "vec_int_filled",
            [-1],
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "vec_empty",
            [1],
            ValueError,
            "cannot drop more items than the vector contains",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_drop_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.drop(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [2], Vec([3, 5])],
        ["vec_str_filled", [3], Vec(["hello"])],
        ["vec_int_filled", [0], Vec([3, 5, 20, -1])],
        ["vec_empty", [0], Vec()],
    ],
    indirect=["prebuild_vec"],
)
def test_drop_right_ok(prebuild_vec, args, result):
    assert prebuild_vec.drop_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_int_filled",
            [10],
            ValueError,
            "cannot drop more items than the vector contains",
        ],
        [
            "vec_int_filled",
            [-1],
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "vec_empty",
            [1],
            ValueError,
            "cannot drop more items than the vector contains",
        ],
    ],
    indirect=["prebuild_vec"],
)
def test_drop_right_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.drop_right(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [1, 2], Vec([5, 20])],
        ["vec_str_filled", [2, 3], Vec(["holá", "ciao"])],
        ["vec_int_filled", [0, 0], Vec([3])],
        ["vec_str_filled", [3, 3], Vec(["ciao"])],
    ],
    indirect=["prebuild_vec"],
)
def test_slice_ok(prebuild_vec, args, result):
    assert prebuild_vec.slice(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        ["vec_int_filled", [2, 10], ValueError, "slice out of bounds"],
        ["vec_empty", [0, 2], ValueError, "slice out of bounds"],
        ["vec_int_filled", [2, 1], ValueError, "start cannot be greater than stop"],
    ],
    indirect=["prebuild_vec"],
)
def test_slice_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.slice(*args)


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "result"],
    [
        ["vec_int_filled", [2], (Vec([3, 5]), Vec([20, -1]))],
        ["vec_int_filled", [0], (Vec(), Vec([3, 5, 20, -1]))],
        ["vec_int_filled", [4], (Vec([3, 5, 20, -1]), Vec())],
        ["vec_str_filled", [2], (Vec(["hello", "bonjour"]), Vec(["holá", "ciao"]))],
        ["vec_str_filled", [6], (Vec(["hello", "bonjour", "holá", "ciao"]), Vec())],
    ],
    indirect=["prebuild_vec"],
)
def test_cut_ok(prebuild_vec, args, result):
    assert prebuild_vec.cut(*args) == result


@pytest.mark.parametrize(
    ["prebuild_vec", "args", "exception", "message"],
    [
        [
            "vec_str_filled",
            [-2],
            ValueError,
            "cannot cut after a negative amount of elements",
        ],
        ["vec_empty", [2], TypeError, "cannot cut an empty vector"],
    ],
    indirect=["prebuild_vec"],
)
def test_cut_err(prebuild_vec, args, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_vec.cut(*args)


# *- "combined" tests -* #


def test_fib():
    base = vec[0, 1]
    result = vec[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    assert base.filled(lambda lst: lst.take_right(2).sum(), 9) == result
