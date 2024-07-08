import pytest

from magic_list import list


def test_ml_empty(ml_empty):
    with pytest.raises(TypeError) as ctx:
        ml_empty.tail

        assert str(ctx.value) == "empty list has no tail"


def test_ml_with_one_int_truthy(ml_with_one_int_truthy):
    assert ml_with_one_int_truthy.tail == list()


def test_ml_with_one_int_falsy(ml_with_one_int_falsy):
    assert ml_with_one_int_falsy.tail == list()


def test_ml_with_one_str(ml_with_one_str):
    assert ml_with_one_str.tail == list()


def test_ml_with_one_list_nonempty(ml_with_one_list_nonempty):
    assert ml_with_one_list_nonempty.tail == list()


def test_ml_with_one_magic_list_nonempty(ml_with_one_magic_list_nonempty):
    assert ml_with_one_magic_list_nonempty.tail == list()


def test_ml_with_one_tuple_nonempty(ml_with_one_tuple_nonempty):
    assert ml_with_one_tuple_nonempty.tail == list()


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.tail == list([39, -7, 0, 15])


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.tail == list([2, 4, 8, 16, 32])


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.tail == list(
        ["", "world", "goodbye", " ", "mars"],
    )


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.tail == list([[4, 5, 6], [7, 8, 9]])


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.tail == list(
        [list([13, 14, 15]), list([16, 17, 18])],
    )


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    assert ml_with_different_several_tuple_nonempty.tail == list([(6, 5, 4), (3, 2, 1)])


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.tail == list([0, 0, 1, 0, 1, -1, 1, 0])


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.tail == list(
        [
            list(["hello", "world"]),
            list(["goodbye", "mars"]),
            list(["hello", "world"]),
        ],
    )


def test_ml_with_equal_several_int_truthy(ml_with_equal_several_int_truthy):
    assert ml_with_equal_several_int_truthy.tail == list([23, 23, 23])


def test_ml_with_equal_several_int_falsy(ml_with_equal_several_int_falsy):
    assert ml_with_equal_several_int_falsy.tail == list([0, 0, 0])


def test_ml_with_equal_several_list_empty(ml_with_equal_several_list_empty):
    assert ml_with_equal_several_list_empty.tail == list([[], [], []])


def test_ml_with_equal_several_magic_list_nonempty(
    ml_with_equal_several_magic_list_nonempty,
):
    assert ml_with_equal_several_magic_list_nonempty.tail == list(
        [list([3, 5, 2]), list([3, 5, 2])],
    )


def test_ml_with_equal_several_magic_list_empty(ml_with_equal_several_magic_list_empty):
    assert ml_with_equal_several_magic_list_empty.tail == list([list(), list(), list()])


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    assert ml_recursive_with_itself.tail == list()


def test_ml_with_recursive_item(ml_with_recursive_item):
    assert ml_with_recursive_item.tail == list()


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    assert ml_with_mutually_recursive_item.tail == list()
