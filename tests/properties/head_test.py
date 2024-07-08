import pytest

from magic_list import list


def test_ml_empty(ml_empty):
    with pytest.raises(TypeError) as ctx:
        ml_empty.head

        assert str(ctx.value) == "empty list has no head"


def test_ml_with_one_int_truthy(ml_with_one_int_truthy):
    assert ml_with_one_int_truthy.head == 42


def test_ml_with_one_int_falsy(ml_with_one_int_falsy):
    assert ml_with_one_int_falsy.head == 0


def test_ml_with_one_str(ml_with_one_str):
    assert ml_with_one_str.head == "hello"


def test_ml_with_one_list_nonempty(ml_with_one_list_nonempty):
    assert ml_with_one_list_nonempty.head == [3.14159, 2.71828, 9.80665]


def test_ml_with_one_magic_list_nonempty(ml_with_one_magic_list_nonempty):
    assert ml_with_one_magic_list_nonempty.head == list([14, 3, 1872])


def test_ml_with_one_tuple_nonempty(ml_with_one_tuple_nonempty):
    assert ml_with_one_tuple_nonempty.head == ("John", "Doe", 23, 2183.76)


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.head == 76


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.head == 1


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.head == "hello"


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.head == [1, 2, 3]


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.head == list([10, 11, 12])


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    assert ml_with_different_several_tuple_nonempty.head == (9, 8, 7)


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.head == 1


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.head == list(
        ["hello", "mars"],
    )


def test_ml_with_equal_several_int_truthy(ml_with_equal_several_int_truthy):
    assert ml_with_equal_several_int_truthy.head == 23


def test_ml_with_equal_several_int_falsy(ml_with_equal_several_int_falsy):
    assert ml_with_equal_several_int_falsy.head == 0


def test_ml_with_equal_several_list_empty(ml_with_equal_several_list_empty):
    assert ml_with_equal_several_list_empty.head == []


def test_ml_with_equal_several_magic_list_nonempty(
    ml_with_equal_several_magic_list_nonempty,
):
    assert ml_with_equal_several_magic_list_nonempty.head == list([3, 5, 2])


def test_ml_with_equal_several_magic_list_empty(ml_with_equal_several_magic_list_empty):
    assert ml_with_equal_several_magic_list_empty.head == list()


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    assert ml_recursive_with_itself.head == ml_recursive_with_itself
    assert ml_recursive_with_itself.head.head == ml_recursive_with_itself.head


def test_ml_with_recursive_item(ml_with_recursive_item):
    assert ml_with_recursive_item.head == ml_with_recursive_item.head[0]


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    assert ml_with_mutually_recursive_item == ml_with_mutually_recursive_item.head[0]
    assert (
        ml_with_mutually_recursive_item.head
        == ml_with_mutually_recursive_item.head[0].head
    )
