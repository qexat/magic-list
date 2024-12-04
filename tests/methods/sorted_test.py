import pytest

from testing import reduce_right_sub


def test_ml_empty(ml_empty):
    assert ml_empty.sorted() == ml_empty


@pytest.mark.parametrize(
    ("magic_list_instance", "key"),
    [
        pytest.param("ml_with_one_int_truthy", None, id="with_one_int_truthy"),
        pytest.param("ml_with_one_int_falsy", None, id="with_one_int_falsy"),
        pytest.param("ml_with_one_str", None, id="with_one_str"),
        pytest.param("ml_with_one_str", len, id="len_key_with_one_str"),
        pytest.param("ml_with_one_list_nonempty", None, id="with_one_list_nonempty"),
        pytest.param(
            "ml_with_one_list_nonempty",
            len,
            id="len_key_with_one_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_list_nonempty",
            sum,
            id="sum_key_with_one_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_magic_list_nonempty",
            None,
            id="with_one_magic_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_magic_list_nonempty",
            len,
            id="len_key_with_one_magic_list_nonempty",
        ),
        pytest.param("ml_with_one_tuple_nonempty", None, id="with_one_tuple_nonempty"),
        pytest.param(
            "ml_with_one_tuple_nonempty",
            len,
            id="len_key_with_one_tuple_nonempty",
        ),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_with_one_item(magic_list_instance, key):
    assert magic_list_instance.sorted(key=key) == magic_list_instance


@pytest.mark.parametrize(
    ("magic_list_instance", "key"),
    [
        pytest.param("ml_with_one_int_truthy", None, id="with_one_int_truthy"),
        pytest.param("ml_with_one_int_falsy", None, id="with_one_int_falsy"),
        pytest.param("ml_with_one_str", None, id="with_one_str"),
        pytest.param("ml_with_one_str", len, id="len_key_with_one_str"),
        pytest.param("ml_with_one_list_nonempty", None, id="with_one_list_nonempty"),
        pytest.param(
            "ml_with_one_list_nonempty",
            len,
            id="len_key_with_one_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_list_nonempty",
            sum,
            id="sum_key_with_one_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_magic_list_nonempty",
            None,
            id="with_one_magic_list_nonempty",
        ),
        pytest.param(
            "ml_with_one_magic_list_nonempty",
            len,
            id="len_key_with_one_magic_list_nonempty",
        ),
        pytest.param("ml_with_one_tuple_nonempty", None, id="with_one_tuple_nonempty"),
        pytest.param(
            "ml_with_one_tuple_nonempty",
            len,
            id="len_key_with_one_tuple_nonempty",
        ),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_with_one_item_reverse(magic_list_instance, key):
    assert magic_list_instance.sorted(key=key, reverse=True) == magic_list_instance


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.sorted() == list([-7, 0, 15, 39, 76])


def test_ml_with_different_several_int_reverse(ml_with_different_several_int):
    assert ml_with_different_several_int.sorted(reverse=True) == list(
        [76, 39, 15, 0, -7],
    )


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.sorted() == list([1, 2, 4, 8, 16, 32])


def test_ml_with_different_several_int_truthy_reverse(
    ml_with_different_several_int_truthy,
):
    assert ml_with_different_several_int_truthy.sorted(reverse=True) == list(
        [32, 16, 8, 4, 2, 1],
    )


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.sorted() == list(
        ["", " ", "goodbye", "hello", "mars", "world"],
    )


def test_ml_with_different_several_str_reverse(ml_with_different_several_str):
    assert ml_with_different_several_str.sorted(reverse=True) == list(
        ["world", "mars", "hello", "goodbye", " ", ""],
    )


def test_ml_with_different_several_str_key_len(ml_with_different_several_str):
    assert ml_with_different_several_str.sorted(key=len) == list(
        ["", " ", "mars", "hello", "world", "goodbye"],
    )


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.sorted() == list(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    )


def test_ml_with_different_several_list_nonempty_reverse(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.sorted(reverse=True) == list(
        [[7, 8, 9], [4, 5, 6], [1, 2, 3]],
    )


def test_ml_with_different_several_list_nonempty_key_reduce_right_sub(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.sorted(key=reduce_right_sub) == list(
        [[7, 8, 9], [4, 5, 6], [1, 2, 3]],
    )


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.sorted() == list(
        [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    )


def test_ml_with_different_several_magic_list_nonempty_reverse(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.sorted(reverse=True) == list(
        [[16, 17, 18], [13, 14, 15], [10, 11, 12]],
    )


def test_ml_with_different_several_magic_list_nonempty_key_len(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.sorted(key=len) == list(
        [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    )


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.sorted() == list([-1, 0, 0, 0, 0, 1, 1, 1, 1])


def test_ml_with_duplicate_several_int_reverse(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.sorted(reverse=True) == list(
        [1, 1, 1, 1, 0, 0, 0, 0, -1],
    )


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.sorted() == list(
        [
            list(["goodbye", "mars"]),
            list(["hello", "mars"]),
            list(["hello", "world"]),
            list(["hello", "world"]),
        ],
    )


def test_ml_with_duplicate_several_magic_list_nonempty_reverse(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.sorted(reverse=True) == list(
        [
            list(["hello", "world"]),
            list(["hello", "world"]),
            list(["hello", "mars"]),
            list(["goodbye", "mars"]),
        ],
    )


@pytest.mark.parametrize(
    ("magic_list_instance",),
    [
        pytest.param("ml_with_equal_several_int_truthy"),
        pytest.param("ml_with_equal_several_int_falsy"),
        pytest.param("ml_with_equal_several_list_empty"),
        pytest.param("ml_with_equal_several_magic_list_nonempty"),
        pytest.param("ml_with_equal_several_magic_list_empty"),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_equal_values(magic_list_instance):
    assert magic_list_instance.sorted() == magic_list_instance


@pytest.mark.parametrize(
    ("magic_list_instance",),
    [
        pytest.param("ml_with_equal_several_int_truthy"),
        pytest.param("ml_with_equal_several_int_falsy"),
        pytest.param("ml_with_equal_several_list_empty"),
        pytest.param("ml_with_equal_several_magic_list_nonempty"),
        pytest.param("ml_with_equal_several_magic_list_empty"),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_equal_values_reverse(magic_list_instance):
    assert magic_list_instance.sorted(reverse=True) == magic_list_instance


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    assert ml_recursive_with_itself.sorted() == ml_recursive_with_itself


def test_ml_recursive_with_itself_reverse(ml_recursive_with_itself):
    assert ml_recursive_with_itself.sorted(reverse=True) == ml_recursive_with_itself


def test_ml_with_recursive_item(ml_with_recursive_item):
    assert ml_with_recursive_item.sorted() == ml_with_recursive_item


def test_ml_with_recursive_item_reverse(ml_with_recursive_item):
    assert ml_with_recursive_item.sorted(reverse=True) == ml_with_recursive_item


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    assert ml_with_mutually_recursive_item.sorted() == ml_with_mutually_recursive_item


def test_ml_with_mutually_recursive_item_reverse(ml_with_mutually_recursive_item):
    assert (
        ml_with_mutually_recursive_item.sorted(reverse=True)
        == ml_with_mutually_recursive_item
    )
