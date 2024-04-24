import copy

import pytest

from magic_list import list


@pytest.mark.parametrize(
    ("prepended_value", "magic_list_instance"),
    [
        (42, "ml_with_one_int_truthy"),
        (0, "ml_with_one_int_falsy"),
        ("hello", "ml_with_one_str"),
        ([3.14159, 2.71828, 9.80665], "ml_with_one_list_nonempty"),
        (list([14, 3, 1872]), "ml_with_one_magic_list_nonempty"),
        (("John", "Doe", 23, 2183.76), "ml_with_one_tuple_nonempty"),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_empty(ml_empty, prepended_value, magic_list_instance):
    l = copy.deepcopy(ml_empty)
    l.prepend(prepended_value)

    assert l == magic_list_instance


@pytest.mark.parametrize(
    ("magic_list_instance", "prepended_value", "expected"),
    [
        ("ml_with_one_int_truthy", 21, list([21, 42])),
        ("ml_with_one_str", "goodbye", list(["goodbye", "hello"])),
        (
            "ml_with_one_list_nonempty",
            [1.51738, 0.21839, -7.37931],
            list([[1.51738, 0.21839, -7.37931], [3.14159, 2.71828, 9.80665]]),
        ),
        ("ml_with_different_several_int", 21, list([21, 76, 39, -7, 0, 15])),
        (
            "ml_with_different_several_list_nonempty",
            [0],
            list([[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        ),
        (
            "ml_with_duplicate_several_magic_list_nonempty",
            list(["goodbye", "world"]),
            list(
                [
                    list(["goodbye", "world"]),
                    list(["hello", "world"]),
                    list(["goodbye", "mars"]),
                    list(["hello", "world"]),
                ],
            ),
        ),
    ],
    indirect=["magic_list_instance"],
)
def test_ml_nonrecursive(magic_list_instance, prepended_value, expected):
    l = copy.deepcopy(magic_list_instance)
    l.prepend(prepended_value)

    assert l == expected


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    l = copy.deepcopy(ml_recursive_with_itself)
    l.prepend(list())

    assert l == list([list(), l])


def test_ml_with_recursive_item(ml_with_recursive_item):
    item = ml_with_recursive_item[0]
    # note: deepcopy leads to a recursion error on the equality
    # copy is good enough anyway, we don't mutate the recursive item
    l = copy.copy(ml_with_recursive_item)
    l.prepend(list())

    assert l == list([list(), item])


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    item = ml_with_mutually_recursive_item[0]
    # it seems that deepcopy improperly copies the inner item
    l = copy.copy(ml_with_mutually_recursive_item)
    l.prepend(list())

    assert l == list([list(), item])
