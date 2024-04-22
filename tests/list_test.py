# type: ignore
import operator
import random

import pytest

from magic_list import L
from magic_list import list

from .utils import contains_letter_l
from .utils import double
from .utils import greater_than_four

"""
• `test_*_ok` => for function calls that return a result
• `test_*_err` => for function calls that throw an exception

Note that some functions never throw an exception, which means that they don't have a
`test_*_err` variant.
"""


_RANDOM_SEED = 0


@pytest.fixture
def prebuild_list(request):
    if request.param == "list_int_filled":
        return list((3, 5, 20, -1))
    elif request.param == "list_str_filled":
        return list(
            (
                "hello",
                "bonjour",
                "holá",
                "ciao",
            ),
        )
    elif request.param == "list_one_int":
        return list((42,))
    elif request.param == "list_empty":
        return list()


@pytest.fixture
def recursive_list(request):
    if request.param == "direct":
        lst = list()
        lst.append(lst)

        return lst
    elif request.param == "subrecursive":
        lst = list()
        sublst = list()
        sublst.append(sublst)
        lst.append(sublst)

        return lst
    elif request.param == "subrecursive_with_builtin":
        lst = list()
        sublst = []
        sublst.append(sublst)
        lst.append(sublst)

        return lst


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
        ["list_int_filled", list((5, 20, -1))],
        [
            "list_str_filled",
            list(("bonjour", "holá", "ciao")),
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
        ["list_int_filled", list((3, 5, 20))],
        [
            "list_str_filled",
            list(("hello", "bonjour", "holá")),
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
    ["prebuild_list", "element", "result"],
    [
        ["list_int_filled", 14, list((14, 3, 5, 20, -1))],
        [
            "list_str_filled",
            "annyeong",
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
        ["list_empty", -5, list((-5,))],
    ],
    indirect=["prebuild_list"],
)
def test_prepend_ok(prebuild_list, element, result):
    prebuild_list.prepend(element)
    assert prebuild_list == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list((-1, 20, 5, 3))],
        ["list_str_filled", list(("ciao", "holá", "bonjour", "hello"))],
        ["list_empty", list()],
    ],
    indirect=["prebuild_list"],
)
def test_reversed_ok(prebuild_list, result):
    assert prebuild_list.reversed() == result


@pytest.mark.parametrize(
    ["prebuild_list", "kwargs", "result"],
    [
        ["list_int_filled", {}, list((-1, 3, 5, 20))],
        ["list_str_filled", {"key": len}, list(("holá", "ciao", "hello", "bonjour"))],
        ["list_int_filled", {"reverse": True}, list((20, 5, 3, -1))],
        [
            "list_str_filled",
            {"key": len, "reverse": True},
            list(("bonjour", "hello", "holá", "ciao")),
        ],
        ["list_empty", {}, list()],
    ],
    indirect=["prebuild_list"],
)
def test_sorted_ok(prebuild_list, kwargs, result):
    assert prebuild_list.sorted(**kwargs) == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list((-1, 3, 20, 5))],
        ["list_str_filled", list(("ciao", "hello", "holá", "bonjour"))],
        ["list_empty", list()],
    ],
    indirect=["prebuild_list"],
)
def test_shuffled_ok(prebuild_list, result):
    random.seed(_RANDOM_SEED)
    assert prebuild_list.shuffled() == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "result"],
    [
        ["list_int_filled", double, list((6, 10, 40, -2))],
        [
            "list_str_filled",
            double,
            list(("hellohello", "bonjourbonjour", "holáholá", "ciaociao")),
        ],
        ["list_empty", double, list()],
    ],
    indirect=["prebuild_list"],
)
def test_map_ok(prebuild_list, function, result):
    assert prebuild_list.map(function) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", (), list((-1, 3, 5, 20))],
        ["list_int_filled", (2,), list((20, -1, 3, 5))],
        [
            "list_int_filled",
            (-2,),
            list((20, -1, 3, 5)),
        ],
        ["list_str_filled", (0,), list(("hello", "bonjour", "holá", "ciao"))],
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
    ["prebuild_list", "function", "result"],
    [
        ["list_int_filled", greater_than_four, list((5, 20))],
        ["list_str_filled", contains_letter_l, list(("hello", "holá"))],
        ["list_empty", greater_than_four, list()],
    ],
    indirect=["prebuild_list"],
)
def test_filter_ok(prebuild_list, function, result):
    assert prebuild_list.filter(function) == result


@pytest.mark.parametrize(
    ["prebuild_list", "mask_seq", "result"],
    [
        ["list_int_filled", [0, 1, 0, 1], list((5, -1))],
        ["list_str_filled", [1, 0, 0, 0], list(("hello",))],
        ["list_empty", [], list()],
    ],
    indirect=["prebuild_list"],
)
def test_mask_ok(prebuild_list, mask_seq, result):
    assert prebuild_list.mask(mask_seq) == result


@pytest.mark.parametrize(
    ["prebuild_list", "mask_seq", "exception", "message"],
    [
        [
            "list_int_filled",
            [0, 1],
            TypeError,
            "mask length must be the same as the list",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_mask_err(prebuild_list, mask_seq, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.mask(mask_seq)


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        [list((3, 0, 0, 1, 98, -1, 1)), list((3, 0, 1, 98, -1))],
        [
            list(("hello", "hello", "world", "goodbye", "bye")),
            list(("hello", "world", "goodbye", "bye")),
        ],
        [list(), list()],
    ],
)
def test_deduplicate_ok(prebuild_list, result):
    assert prebuild_list.deduplicate() == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "result"],
    [
        ["list_int_filled", operator.add, 27],
        ["list_str_filled", operator.add, "hellobonjourholáciao"],
        ["list_int_filled", operator.mul, -300],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_ok(prebuild_list, function, result):
    assert prebuild_list.reduce(function) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "exception", "message"],
    [
        ["list_str_filled", operator.mul, TypeError, "can't multiply sequence"],
        [
            "list_empty",
            operator.add,
            TypeError,
            "the list to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_err(prebuild_list, function, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.reduce(function)


@pytest.mark.parametrize(
    ["prebuild_list", "function", "result"],
    [
        ["list_int_filled", operator.sub, 19],
        ["list_str_filled", operator.add, "hellobonjourholáciao"],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_right_ok(prebuild_list, function, result):
    assert prebuild_list.reduce_right(function) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "exception", "message"],
    [
        ["list_str_filled", operator.mul, TypeError, "can't multiply sequence"],
        [
            "list_empty",
            operator.add,
            TypeError,
            "the list to reduce cannot be empty",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_reduce_right_err(prebuild_list, function, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.reduce_right(function)


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "result"],
    [
        ["list_int_filled", operator.add, 3, 30],
        ["list_str_filled", operator.add, "annyeong", "annyeonghellobonjourholáciao"],
        ["list_int_filled", operator.mul, 0, 0],
        ["list_empty", operator.add, 0, 0],
    ],
    indirect=["prebuild_list"],
)
def test_fold_ok(prebuild_list, function, initial_value, result):
    assert prebuild_list.fold(function, initial_value) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "exception", "message"],
    [
        [
            "list_str_filled",
            operator.mul,
            "annyeong",
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fold_err(prebuild_list, function, initial_value, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fold(function, initial_value)


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "result"],
    [
        ["list_int_filled", operator.add, 3, 30],
        ["list_str_filled", operator.add, "annyeong", "hellobonjourholáciaoannyeong"],
        ["list_int_filled", operator.sub, 0, 19],
        ["list_empty", operator.add, 0, 0],
    ],
    indirect=["prebuild_list"],
)
def test_fold_right_ok(prebuild_list, function, initial_value, result):
    assert prebuild_list.fold_right(function, initial_value) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "exception", "message"],
    [
        [
            "list_str_filled",
            operator.mul,
            "annyeong",
            TypeError,
            "can't multiply sequence",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fold_right_err(prebuild_list, function, initial_value, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fold_right(function, initial_value)


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "result"],
    [
        ["list_int_filled", operator.add, 0, list((0, 3, 8, 28, 27))],
        [
            "list_str_filled",
            operator.add,
            "",
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
        ["list_empty", operator.add, 0, list((0,))],
        ["list_empty", operator.add, "hello", list(("hello",))],
    ],
    indirect=["prebuild_list"],
)
def test_scan_ok(prebuild_list, function, initial_value, result):
    assert prebuild_list.scan(function, initial_value) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "initial_value", "result"],
    [
        ["list_int_filled", operator.add, 0, list((0, -1, 19, 24, 27))],
        [
            "list_str_filled",
            operator.add,
            "",
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
        ["list_empty", operator.add, 0, list((0,))],
        ["list_empty", operator.add, "hello", list(("hello",))],
    ],
    indirect=["prebuild_list"],
)
def test_scan_right_ok(prebuild_list, function, initial_value, result):
    assert prebuild_list.scan_right(function, initial_value) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "other", "result"],
    [
        ["list_int_filled", operator.add, [-1, 4, -9, 16], list((2, 9, 11, 15))],
        [
            "list_str_filled",
            operator.add,
            [".", " !", "...", "?"],
            list(
                [
                    "hello.",
                    "bonjour !",
                    "holá...",
                    "ciao?",
                ],
            ),
        ],
        ["list_empty", operator.add, [], list()],
    ],
    indirect=["prebuild_list"],
)
def test_merge_ok(prebuild_list, function, other, result):
    assert prebuild_list.merge(function, other) == result


@pytest.mark.parametrize(
    ["prebuild_list", "function", "other", "exception", "message"],
    [
        [
            "list_int_filled",
            operator.add,
            [],
            TypeError,
            "the length of the two sequences must be equal",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_merge_err(prebuild_list, function, other, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.merge(function, other)


def test_flatten_ok():
    l0 = list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    l1 = list([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    l2 = list([[[0, 1], [2, 3]], [[4, 5], [6, 7]], [[8, 9], [10, 11]]])

    assert l0.flatten() == l1.flatten() == l2.flatten() == l0


@pytest.mark.parametrize(
    ["recursive_list", "exception", "message"],
    [
        [
            "direct",
            ValueError,
            "cannot flatten list because it contains recursive elements",
        ],
        [
            "subrecursive",
            ValueError,
            "cannot flatten list because it contains recursive elements",
        ],
        [
            "subrecursive_with_builtin",
            ValueError,
            "cannot flatten list because it contains recursive elements",
        ],
    ],
    indirect=["recursive_list"],
)
def test_flatten_err(recursive_list, exception, message):
    with pytest.raises(exception, match=message):
        recursive_list.flatten()


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 27],
        ["list_str_filled", "hellobonjourholáciao"],
    ],
    indirect=["prebuild_list"],
)
def test_sum_ok(prebuild_list, result):
    assert prebuild_list.sum() == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_empty", TypeError, "cannot perform summation on an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_sum_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.sum()


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", -1],
        ["list_one_int", 42],
    ],
    indirect=["prebuild_list"],
)
def test_min_ok(prebuild_list, result):
    assert prebuild_list.min() == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_str_filled", TypeError, "list of str has no minimum"],
        ["list_empty", TypeError, "empty list has no minimum"],
    ],
    indirect=["prebuild_list"],
)
def test_min_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.min()


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 20],
        ["list_one_int", 42],
    ],
    indirect=["prebuild_list"],
)
def test_max_ok(prebuild_list, result):
    assert prebuild_list.max() == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_str_filled", TypeError, "list of str has no maximum"],
        ["list_empty", TypeError, "empty list has no maximum"],
    ],
    indirect=["prebuild_list"],
)
def test_max_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.max()


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 6.75],
    ],
    indirect=["prebuild_list"],
)
def test_mean_ok(prebuild_list, result):
    assert prebuild_list.mean() == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception", "message"],
    [
        ["list_str_filled", TypeError, "cannot calculate mean of list of str"],
        ["list_empty", TypeError, "cannot calculate mean of empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_mean_err(prebuild_list, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.mean()


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "n", "result"],
    [
        ["list_int_filled", 0, 3, list((0, 0, 0, 3, 5, 20, -1))],
        [
            "list_str_filled",
            "annyeong",
            2,
            list(
                (
                    "annyeong",
                    "annyeong",
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ),
            ),
        ],
        ["list_empty", 10, 5, list((10, 10, 10, 10, 10))],
        ["list_empty", "hi", 4, list(("hi", "hi", "hi", "hi"))],
        ["list_int_filled", sum, 3, list((108, 54, 27, 3, 5, 20, -1))],
        [
            "list_str_filled",
            lambda lst: lst[0][::-1],
            2,
            list(
                (
                    "hello",
                    "olleh",
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                ),
            ),
        ],
        ["list_empty", len, 4, list((3, 2, 1, 0))],
    ],
    indirect=["prebuild_list"],
)
def test_fill_left_ok(prebuild_list, filler, n, result):
    assert prebuild_list.fill_left(filler, n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            0,
            -2,
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fill_left_err(prebuild_list, filler, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fill_left(filler, n)


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "n", "result"],
    [
        ["list_int_filled", 0, 3, list((3, 5, 20, -1, 0, 0, 0))],
        [
            "list_str_filled",
            "annyeong",
            2,
            list(
                (
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "annyeong",
                    "annyeong",
                ),
            ),
        ],
        ["list_empty", 10, 5, list((10, 10, 10, 10, 10))],
        ["list_empty", "hi", 4, list(("hi", "hi", "hi", "hi"))],
        [
            "list_int_filled",
            sum,
            3,
            list((3, 5, 20, -1, 27, 54, 108)),
        ],
        [
            "list_str_filled",
            lambda lst: lst[-1][::-1],
            2,
            list(
                (
                    "hello",
                    "bonjour",
                    "holá",
                    "ciao",
                    "oaic",
                    "ciao",
                ),
            ),
        ],
        ["list_empty", len, 4, list((0, 1, 2, 3))],
    ],
    indirect=["prebuild_list"],
)
def test_fill_right_ok(prebuild_list, filler, n, result):
    assert prebuild_list.fill_right(filler, n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            0,
            -2,
            ValueError,
            "the number of times to fill cannot be negative",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_fill_right_err(prebuild_list, filler, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.fill_right(filler, n)


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "result"],
    [
        ["list_int_filled", 0, list((3, 0, 5, 0, 20, 0, -1))],
        [
            "list_str_filled",
            " ",
            list(("hello", " ", "bonjour", " ", "holá", " ", "ciao")),
        ],
        ["list_int_filled", lambda p, n: p + n, list((3, 8, 5, 25, 20, 19, -1))],
        [
            "list_str_filled",
            lambda p, n: p[-1] + n[0],
            list(("hello", "ob", "bonjour", "rh", "holá", "ác", "ciao")),
        ],
    ],
    indirect=["prebuild_list"],
)
def test_interleave_ok(prebuild_list, filler, result):
    assert prebuild_list.interleave(filler) == result


@pytest.mark.parametrize(
    ["prebuild_list", "filler", "exception", "message"],
    [
        ["list_one_int", -1, ValueError, "list has no gap to be filled"],
        ["list_empty", None, ValueError, "list has no gap to be filled"],
    ],
    indirect=["prebuild_list"],
)
def test_interleave_err(prebuild_list, filler, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.interleave(filler)


@pytest.mark.parametrize(
    ["prebuild_list", "indexes", "result"],
    [
        ["list_int_filled", [1, 3], list((5, -1))],
        ["list_int_filled", [], list()],
        ["list_int_filled", [2, 0, 0], list((20, 3, 3))],
        ["list_str_filled", [1, 2], list(("bonjour", "holá"))],
        ["list_str_filled", [-2], list(("holá",))],
        ["list_empty", [], list()],
    ],
    indirect=["prebuild_list"],
)
def test_select_ok(prebuild_list, indexes, result):
    assert prebuild_list.select(indexes) == result


@pytest.mark.parametrize(
    ["prebuild_list", "indexes", "exception", "message"],
    [
        ["list_int_filled", [4, 1], IndexError, "index 4 is out of bounds"],
        ["list_empty", [0], IndexError, "index 0 is out of bounds"],
    ],
    indirect=["prebuild_list"],
)
def test_select_err(prebuild_list, indexes, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.select(indexes)


@pytest.mark.parametrize(
    ["prebuild_list", "n", "result"],
    [
        ["list_int_filled", 2, list((3, 5))],
        ["list_str_filled", 3, list(("hello", "bonjour", "holá"))],
        ["list_int_filled", 0, list()],
        ["list_empty", 0, list()],
    ],
    indirect=["prebuild_list"],
)
def test_take_ok(prebuild_list, n, result):
    assert prebuild_list.take(n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            10,
            ValueError,
            "cannot take more items than the list contains",
        ],
        [
            "list_int_filled",
            -1,
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "list_empty",
            1,
            ValueError,
            "cannot take more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_take_err(prebuild_list, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.take(n)


@pytest.mark.parametrize(
    ["prebuild_list", "n", "result"],
    [
        ["list_int_filled", 2, [20, -1]],
        ["list_str_filled", 3, list(("bonjour", "holá", "ciao"))],
        ["list_int_filled", 0, list()],
        ["list_empty", 0, list()],
    ],
    indirect=["prebuild_list"],
)
def test_take_right_ok(prebuild_list, n, result):
    assert prebuild_list.take_right(n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            10,
            ValueError,
            "cannot take more items than the list contains",
        ],
        [
            "list_int_filled",
            -1,
            ValueError,
            "cannot take a negative amount of items",
        ],
        [
            "list_empty",
            1,
            ValueError,
            "cannot take more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_take_right_err(prebuild_list, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.take_right(n)


@pytest.mark.parametrize(
    ["prebuild_list", "n", "result"],
    [
        ["list_int_filled", 2, list((20, -1))],
        ["list_str_filled", 3, list(("ciao",))],
        ["list_int_filled", 0, list((3, 5, 20, -1))],
        ["list_empty", 0, list()],
    ],
    indirect=["prebuild_list"],
)
def test_drop_ok(prebuild_list, n, result):
    assert prebuild_list.drop(n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            10,
            ValueError,
            "cannot drop more items than the list contains",
        ],
        [
            "list_int_filled",
            -1,
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "list_empty",
            1,
            ValueError,
            "cannot drop more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_drop_err(prebuild_list, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.drop(n)


@pytest.mark.parametrize(
    ["prebuild_list", "n", "result"],
    [
        ["list_int_filled", 2, list((3, 5))],
        ["list_str_filled", 3, list(("hello",))],
        ["list_int_filled", 0, list((3, 5, 20, -1))],
        ["list_empty", 0, list()],
    ],
    indirect=["prebuild_list"],
)
def test_drop_right_ok(prebuild_list, n, result):
    assert prebuild_list.drop_right(n) == result


@pytest.mark.parametrize(
    ["prebuild_list", "n", "exception", "message"],
    [
        [
            "list_int_filled",
            10,
            ValueError,
            "cannot drop more items than the list contains",
        ],
        [
            "list_int_filled",
            -1,
            ValueError,
            "cannot drop a negative amount of items",
        ],
        [
            "list_empty",
            1,
            ValueError,
            "cannot drop more items than the list contains",
        ],
    ],
    indirect=["prebuild_list"],
)
def test_drop_right_err(prebuild_list, n, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.drop_right(n)


@pytest.mark.parametrize(
    ["prebuild_list", "start", "stop", "result"],
    [
        ["list_int_filled", 1, 2, list((5, 20))],
        ["list_str_filled", 2, 3, list(("holá", "ciao"))],
        ["list_int_filled", 0, 0, list((3,))],
        ["list_str_filled", 3, 3, list(("ciao",))],
    ],
    indirect=["prebuild_list"],
)
def test_slice_ok(prebuild_list, start, stop, result):
    assert prebuild_list.slice(start, stop) == result


@pytest.mark.parametrize(
    ["prebuild_list", "start", "stop", "exception", "message"],
    [
        ["list_int_filled", 2, 10, ValueError, "slice out of bounds"],
        ["list_empty", 0, 2, ValueError, "slice out of bounds"],
        ["list_int_filled", 2, 1, ValueError, "start cannot be greater than stop"],
    ],
    indirect=["prebuild_list"],
)
def test_slice_err(prebuild_list, start, stop, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.slice(start, stop)


@pytest.mark.parametrize(
    ["prebuild_list", "index", "result"],
    [
        ["list_int_filled", 2, (list((3, 5)), list((20, -1)))],
        ["list_int_filled", 0, (list(), list((3, 5, 20, -1)))],
        ["list_int_filled", 4, (list((3, 5, 20, -1)), list())],
        ["list_int_filled", -2, (list(), list((3, 5, 20, -1)))],
        ["list_str_filled", 2, (list(("hello", "bonjour")), list(("holá", "ciao")))],
        ["list_str_filled", 6, (list(("hello", "bonjour", "holá", "ciao")), list())],
    ],
    indirect=["prebuild_list"],
)
def test_bisect_ok(prebuild_list, index, result):
    assert prebuild_list.bisect(index) == result


@pytest.mark.parametrize(
    ["prebuild_list", "index", "exception", "message"],
    [
        ["list_empty", 2, TypeError, "cannot bisect an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_bisect_err(prebuild_list, index, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.bisect(index)


@pytest.mark.parametrize(
    ["prebuild_list", "left_index", "right_index", "result"],
    [
        ["list_int_filled", 1, 3, (list((3,)), list((5, 20)), list((-1,)))],
        ["list_int_filled", 0, 4, (list(), list((3, 5, 20, -1)), list())],
        ["list_int_filled", 0, 0, (list(), list(), list((3, 5, 20, -1)))],
        ["list_int_filled", 4, 4, (list((3, 5, 20, -1)), list(), list())],
        ["list_int_filled", -2, 2, (list(), list((3, 5)), list((20, -1)))],
        ["list_int_filled", 2, 8, (list((3, 5)), list((20, -1)), list())],
    ],
    indirect=["prebuild_list"],
)
def test_trisect_ok(prebuild_list, left_index, right_index, result):
    assert prebuild_list.trisect(left_index, right_index) == result


@pytest.mark.parametrize(
    ["prebuild_list", "left_index", "right_index", "exception", "message"],
    [
        ["list_empty", 0, 2, TypeError, "cannot trisect an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_trisect_err(prebuild_list, left_index, right_index, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.trisect(left_index, right_index)


@pytest.mark.parametrize(
    ["prebuild_list", "index", "result"],
    [
        ["list_int_filled", 2, (list((3, 5)), 20, list((-1,)))],
        ["list_int_filled", 0, (list(), 3, list((5, 20, -1)))],
        ["list_int_filled", 3, (list((3, 5, 20)), -1, list())],
    ],
    indirect=["prebuild_list"],
)
def test_partition_ok(prebuild_list, index, result):
    assert prebuild_list.partition(index) == result


@pytest.mark.parametrize(
    ["prebuild_list", "index", "exception", "message"],
    [
        [
            "list_int_filled",
            -1,
            IndexError,
            "partition index cannot be out of bounds",
        ],
        ["list_int_filled", 8, IndexError, "partition index cannot be out of bounds"],
        ["list_empty", 2, TypeError, "cannot partition an empty list"],
    ],
    indirect=["prebuild_list"],
)
def test_partition_err(prebuild_list, index, exception, message):
    with pytest.raises(exception, match=message):
        prebuild_list.partition(index)


# *- "combined" tests -* #


def test_fib():
    base = L[0, 1]
    result = L[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    assert base.fill_right(lambda lst: lst.take_right(2).sum(), 9) == result
