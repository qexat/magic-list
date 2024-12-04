import pytest

from magic_list import list


def test_ml_empty(ml_empty):
    with pytest.raises(TypeError) as ctx:
        ml_empty.init

        assert str(ctx.value) == "empty list has no init"


def test_ml_with_one_int_truthy(ml_with_one_int_truthy):
    assert ml_with_one_int_truthy.init == list()


def test_ml_with_one_int_falsy(ml_with_one_int_falsy):
    assert ml_with_one_int_falsy.init == list()


def test_ml_with_one_str(ml_with_one_str):
    assert ml_with_one_str.init == list()


def test_ml_with_one_list_nonempty(ml_with_one_list_nonempty):
    assert ml_with_one_list_nonempty.init == list()


def test_ml_with_one_magic_list_nonempty(ml_with_one_magic_list_nonempty):
    assert ml_with_one_magic_list_nonempty.init == list()


def test_ml_with_one_tuple_nonempty(ml_with_one_tuple_nonempty):
    assert ml_with_one_tuple_nonempty.init == list()


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.init == list([76, 39, -7, 0])


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.init == list([1, 2, 4, 8, 16])


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.init == list(
        ["hello", "", "world", "goodbye", " "],
    )


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.init == list([[1, 2, 3], [4, 5, 6]])


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.init == list(
        [list([10, 11, 12]), list([13, 14, 15])],
    )


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    assert ml_with_different_several_tuple_nonempty.init == list([(9, 8, 7), (6, 5, 4)])


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.init == list([1, 0, 0, 1, 0, 1, -1, 1])


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.init == list(
        [
            list(["hello", "mars"]),
            list(["hello", "world"]),
            list(["goodbye", "mars"]),
        ],
    )


def test_ml_with_equal_several_int_truthy(ml_with_equal_several_int_truthy):
    assert ml_with_equal_several_int_truthy.init == list([23, 23, 23])


def test_ml_with_equal_several_int_falsy(ml_with_equal_several_int_falsy):
    assert ml_with_equal_several_int_falsy.init == list([0, 0, 0])


def test_ml_with_equal_several_list_empty(ml_with_equal_several_list_empty):
    assert ml_with_equal_several_list_empty.init == list([[], [], []])


def test_ml_with_equal_several_magic_list_nonempty(
    ml_with_equal_several_magic_list_nonempty,
):
    assert ml_with_equal_several_magic_list_nonempty.init == list(
        [list([3, 5, 2]), list([3, 5, 2])],
    )


def test_ml_with_equal_several_magic_list_empty(ml_with_equal_several_magic_list_empty):
    assert ml_with_equal_several_magic_list_empty.init == list([list(), list(), list()])


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    assert ml_recursive_with_itself.init == list()


def test_ml_with_recursive_item(ml_with_recursive_item):
    assert ml_with_recursive_item.init == list()


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    assert ml_with_mutually_recursive_item.init == list()
