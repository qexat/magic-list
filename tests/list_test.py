# type: ignore
import operator

import pytest

from magic_collections import list
import magic_collections.features as _features

if _features.OPTION:
    import option


"""
• `test_*_ok` => for function calls that return a result
• `test_*_err` => for function calls that throw an exception

Note that some functions never throw an exception, which means that they don't have a
`test_*_err` variant.
"""


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
                ]
            )
        case "list_empty":
            return list()


def double(x):
    return x * 2


def greater_than_four(x):
    return x > 4


def contains_letter_l(x):
    return "l" in x


# *- PROPERTIES -* #


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 3],
        ["list_str_filled", "hello"],
    ],
    indirect=["prebuild_list"],
)
def test_list_head_ok(prebuild_list, result):
    assert prebuild_list.head == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception"],
    [
        ["list_empty", ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_head_err(prebuild_list, exception):
    with pytest.raises(exception):
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
def test_list_tail_ok(prebuild_list, result):
    assert prebuild_list.tail == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception"],
    [
        ["list_empty", ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_tail_err(prebuild_list, exception):
    with pytest.raises(exception):
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
def test_list_init_ok(prebuild_list, result):
    assert prebuild_list.init == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception"],
    [
        ["list_empty", ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_init_err(prebuild_list, exception):
    with pytest.raises(exception):
        prebuild_list.init


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", -1],
        ["list_str_filled", "ciao"],
    ],
    indirect=["prebuild_list"],
)
def test_list_last_ok(prebuild_list, result):
    assert prebuild_list.last == result


@pytest.mark.parametrize(
    ["prebuild_list", "exception"],
    [
        ["list_empty", ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_last_err(prebuild_list, exception):
    with pytest.raises(exception):
        prebuild_list.last


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", 3],
        ["list_str_filled", "hello"],
        ["list_empty", None],
    ],
    indirect=["prebuild_list"],
)
def test_list_head_safe_ok(prebuild_list, result):
    assert prebuild_list.head_safe == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list([5, 20, -1])],
        [
            "list_str_filled",
            list(["bonjour", "holá", "ciao"]),
        ],
        ["list_empty", None],
    ],
    indirect=["prebuild_list"],
)
def test_list_tail_safe_ok(prebuild_list, result):
    assert prebuild_list.tail_safe == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list([3, 5, 20])],
        [
            "list_str_filled",
            list(["hello", "bonjour", "holá"]),
        ],
        ["list_empty", None],
    ],
    indirect=["prebuild_list"],
)
def test_list_init_safe_ok(prebuild_list, result):
    assert prebuild_list.init_safe == result


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", -1],
        ["list_str_filled", "ciao"],
        ["list_empty", None],
    ],
    indirect=["prebuild_list"],
)
def test_list_last_safe_ok(prebuild_list, result):
    assert prebuild_list.last_safe == result


if _features.OPTION:

    @pytest.mark.parametrize(
        ["prebuild_list", "result"],
        [
            ["list_int_filled", option.Some(3)],
            ["list_str_filled", option.Some("hello")],
            ["list_empty", option.NONE],
        ],
        indirect=["prebuild_list"],
    )
    def test_list_head_maybe_ok(prebuild_list, result):
        assert prebuild_list.head_maybe == result

    @pytest.mark.parametrize(
        ["prebuild_list", "result"],
        [
            ["list_int_filled", option.Some(list([5, 20, -1]))],
            [
                "list_str_filled",
                option.Some(list(["bonjour", "holá", "ciao"])),
            ],
            ["list_empty", option.NONE],
        ],
        indirect=["prebuild_list"],
    )
    def test_list_tail_maybe_ok(prebuild_list, result):
        assert prebuild_list.tail_maybe == result

    @pytest.mark.parametrize(
        ["prebuild_list", "result"],
        [
            ["list_int_filled", option.Some(list([3, 5, 20]))],
            [
                "list_str_filled",
                option.Some(list(["hello", "bonjour", "holá"])),
            ],
            ["list_empty", option.NONE],
        ],
        indirect=["prebuild_list"],
    )
    def test_list_init_maybe_ok(prebuild_list, result):
        assert prebuild_list.init_maybe == result

    @pytest.mark.parametrize(
        ["prebuild_list", "result"],
        [
            ["list_int_filled", option.Some(-1)],
            ["list_str_filled", option.Some("ciao")],
            ["list_empty", option.NONE],
        ],
        indirect=["prebuild_list"],
    )
    def test_list_last_maybe_ok(prebuild_list, result):
        assert prebuild_list.last_maybe == result


# *- METHODS -* #


@pytest.mark.parametrize(
    ["prebuild_list", "result"],
    [
        ["list_int_filled", list([-1, 20, 5, 3])],
        ["list_str_filled", list(["ciao", "holá", "bonjour", "hello"])],
        ["list_empty", list()],
    ],
    indirect=["prebuild_list"],
)
def test_list_reversed_ok(prebuild_list, result):
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
def test_list_sorted_ok(prebuild_list, kwargs, result):
    assert prebuild_list.sorted(**kwargs) == result


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
def test_list_map_ok(prebuild_list, args, result):
    assert prebuild_list.map(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [greater_than_four], list([5, 20])],
        ["list_str_filled", [contains_letter_l], list(["hello", "holá"])],
        ["list_empty", [greater_than_four], list()],
    ],
    indirect=["prebuild_list"],
)
def test_list_filter_ok(prebuild_list, args, result):
    assert prebuild_list.filter(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.add], 27],
        ["list_str_filled", [operator.add], "hellobonjourholáciao"],
        ["list_int_filled", [operator.mul], -300],
    ],
    indirect=["prebuild_list"],
)
def test_list_reduce_ok(prebuild_list, args, result):
    assert prebuild_list.reduce(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception"],
    [
        ["list_str_filled", [operator.mul], TypeError],
        ["list_empty", [operator.add], TypeError],
    ],
    indirect=["prebuild_list"],
)
def test_list_reduce_err(prebuild_list, args, exception):
    with pytest.raises(exception):
        prebuild_list.reduce(*args)


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [operator.sub], 19],
        ["list_str_filled", [operator.add], "hellobonjourholáciao"],
    ],
    indirect=["prebuild_list"],
)
def test_list_reduce_right_ok(prebuild_list, args, result):
    assert prebuild_list.reduce_right(*args) == result


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
def test_list_fold_ok(prebuild_list, args, result):
    assert prebuild_list.fold(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception"],
    [
        ["list_str_filled", [operator.mul, "annyeong"], TypeError],
    ],
    indirect=["prebuild_list"],
)
def test_list_fold_err(prebuild_list, args, exception):
    with pytest.raises(exception):
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
def test_list_fold_right_ok(prebuild_list, args, result):
    assert prebuild_list.fold_right(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception"],
    [
        ["list_str_filled", [operator.mul, "annyeong"], TypeError],
    ],
    indirect=["prebuild_list"],
)
def test_list_fold_right_err(prebuild_list, args, exception):
    with pytest.raises(exception):
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
def test_list_scan_ok(prebuild_list, args, result):
    assert prebuild_list.scan(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "result"],
    [
        ["list_int_filled", [[0, 1, 0, 1]], list([5, -1])],
        ["list_str_filled", [[1, 0, 0, 0]], list(["hello"])],
        ["list_empty", [[]], list()],
    ],
    indirect=["prebuild_list"],
)
def test_list_mask_ok(prebuild_list, args, result):
    assert prebuild_list.mask(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception"],
    [
        # list and mask of different length
        ["list_int_filled", [[0, 1]], ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_mask_err(prebuild_list, args, exception):
    with pytest.raises(exception):
        prebuild_list.mask(*args)


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
def test_list_gap_fill_ok(prebuild_list, args, result):
    assert prebuild_list.gap_fill(*args) == result


@pytest.mark.parametrize(
    ["prebuild_list", "args", "exception"],
    [
        ["list_empty", [None], ValueError],
    ],
    indirect=["prebuild_list"],
)
def test_list_gap_fill_err(prebuild_list, args, exception):
    with pytest.raises(exception):
        prebuild_list.gap_fill(*args)


if _features.OPTION:

    @pytest.mark.parametrize(
        ["prebuild_list", "args", "result"],
        [
            ["list_int_filled", [[0, 1, 0, 1]], option.Ok(list([5, -1]))],
            ["list_str_filled", [[1, 0, 0, 0]], option.Ok(list(["hello"]))],
            ["list_empty", [[]], option.Ok(list())],
            [
                "list_empty",
                [[0, 1]],
                option.Err("mask length must be the same as the list"),
            ],
        ],
        indirect=["prebuild_list"],
    )
    def test_list_mask_pure_ok(prebuild_list, args, result):
        assert prebuild_list.mask_pure(*args) == result
