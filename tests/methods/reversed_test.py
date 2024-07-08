import pytest

from magic_list import list


def test_ml_empty(ml_empty):
    assert ml_empty.reversed() == list()


@pytest.mark.parametrize(
    ("magic_list_instance",),
    [
        pytest.param("ml_with_one_int_truthy", id="with_one_int_truthy"),
        pytest.param("ml_with_one_int_falsy", id="with_one_int_falsy"),
        pytest.param("ml_with_one_str", id="with_one_str"),
        pytest.param("ml_with_one_list_nonempty", id="with_one_list_nonempty"),
        pytest.param(
            "ml_with_one_magic_list_nonempty",
            id="with_one_magic_list_nonempty",
        ),
        pytest.param("ml_with_one_tuple_nonempty", id="with_one_tuple_nonempty"),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_with_one_item(magic_list_instance):
    assert magic_list_instance.reversed() == magic_list_instance


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.reversed() == list([15, 0, -7, 39, 76])


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.reversed() == list([32, 16, 8, 4, 2, 1])


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.reversed() == list(
        ["mars", " ", "goodbye", "world", "", "hello"],
    )


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.reversed() == list(
        [[7, 8, 9], [4, 5, 6], [1, 2, 3]],
    )


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.reversed() == list(
        [[16, 17, 18], [13, 14, 15], [10, 11, 12]],
    )


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    assert ml_with_different_several_tuple_nonempty.reversed() == list(
        [(3, 2, 1), (6, 5, 4), (9, 8, 7)],
    )


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.reversed() == list(
        [0, 1, -1, 1, 0, 1, 0, 0, 1],
    )


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.reversed() == list(
        [
            list(["hello", "world"]),
            list(["goodbye", "mars"]),
            list(["hello", "world"]),
            list(["hello", "mars"]),
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
def test_ml_with_equal_items(magic_list_instance):
    assert magic_list_instance.reversed() == magic_list_instance


@pytest.mark.parametrize(
    ("magic_list_instance",),
    [
        pytest.param("ml_recursive_with_itself"),
        pytest.param("ml_with_recursive_item"),
        pytest.param("ml_with_mutually_recursive_item"),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_recursives(magic_list_instance):
    assert magic_list_instance.reversed() == magic_list_instance
