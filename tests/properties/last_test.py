import pytest

from magic_list import list


def test_ml_empty(ml_empty):
    with pytest.raises(TypeError) as ctx:
        ml_empty.last

        assert str(ctx.value) == "empty list has no last"


def test_ml_with_one_int_truthy(ml_with_one_int_truthy):
    assert ml_with_one_int_truthy.last == 42


def test_ml_with_one_int_falsy(ml_with_one_int_falsy):
    assert ml_with_one_int_falsy.last == 0


def test_ml_with_one_str(ml_with_one_str):
    assert ml_with_one_str.last == "hello"


def test_ml_with_one_list_nonempty(ml_with_one_list_nonempty):
    assert ml_with_one_list_nonempty.last == [3.14159, 2.71828, 9.80665]


def test_ml_with_one_magic_list_nonempty(ml_with_one_magic_list_nonempty):
    assert ml_with_one_magic_list_nonempty.last == list([14, 3, 1872])


def test_ml_with_one_tuple_nonempty(ml_with_one_tuple_nonempty):
    assert ml_with_one_tuple_nonempty.last == ("John", "Doe", 23, 2183.76)


def test_ml_with_different_several_int(ml_with_different_several_int):
    assert ml_with_different_several_int.last == 15


def test_ml_with_different_several_int_truthy(ml_with_different_several_int_truthy):
    assert ml_with_different_several_int_truthy.last == 32


def test_ml_with_different_several_str(ml_with_different_several_str):
    assert ml_with_different_several_str.last == "mars"


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    assert ml_with_different_several_list_nonempty.last == [7, 8, 9]


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    assert ml_with_different_several_magic_list_nonempty.last == list([16, 17, 18])


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    assert ml_with_different_several_tuple_nonempty.last == (3, 2, 1)


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    assert ml_with_duplicate_several_int.last == 0


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    assert ml_with_duplicate_several_magic_list_nonempty.last == list(
        ["hello", "world"],
    )


def test_ml_with_equal_several_int_truthy(ml_with_equal_several_int_truthy):
    assert ml_with_equal_several_int_truthy.last == 23


def test_ml_with_equal_several_int_falsy(ml_with_equal_several_int_falsy):
    assert ml_with_equal_several_int_falsy.last == 0


def test_ml_with_equal_several_list_empty(ml_with_equal_several_list_empty):
    assert ml_with_equal_several_list_empty.last == []


def test_ml_with_equal_several_magic_list_nonempty(
    ml_with_equal_several_magic_list_nonempty,
):
    assert ml_with_equal_several_magic_list_nonempty.last == list([3, 5, 2])


def test_ml_with_equal_several_magic_list_empty(ml_with_equal_several_magic_list_empty):
    assert ml_with_equal_several_magic_list_empty.last == list()


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    assert ml_recursive_with_itself.last == ml_recursive_with_itself
    assert ml_recursive_with_itself.last.last == ml_recursive_with_itself.last


def test_ml_with_recursive_item(ml_with_recursive_item):
    assert ml_with_recursive_item.last == ml_with_recursive_item.last[0]


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    assert ml_with_mutually_recursive_item == ml_with_mutually_recursive_item.last[0]
    assert (
        ml_with_mutually_recursive_item.last
        == ml_with_mutually_recursive_item.last[0].last
    )
