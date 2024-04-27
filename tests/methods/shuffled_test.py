import random

import pytest

from tests.conftest import RANDOM_SEED


def test_ml_empty(ml_empty):
    assert ml_empty.shuffled() == ml_empty


@pytest.mark.parametrize(
    ("magic_list_instance",),
    [
        pytest.param("ml_with_one_int_truthy"),
        pytest.param("ml_with_one_int_falsy"),
        pytest.param("ml_with_one_str"),
        pytest.param("ml_with_one_list_nonempty"),
        pytest.param("ml_with_one_magic_list_nonempty"),
        pytest.param("ml_with_one_tuple_nonempty"),
    ],
    indirect=["magic_list_instance"],
)
def test_with_one_item(magic_list_instance):
    random.seed(RANDOM_SEED)

    assert magic_list_instance.shuffled() == magic_list_instance


def test_ml_with_different_several_list_nonempty(
    ml_with_different_several_list_nonempty,
):
    random.seed(RANDOM_SEED)

    assert ml_with_different_several_list_nonempty.shuffled() == list(
        [[1, 2, 3], [7, 8, 9], [4, 5, 6]],
    )


def test_ml_with_different_several_magic_list_nonempty(
    ml_with_different_several_magic_list_nonempty,
):
    random.seed(RANDOM_SEED)

    assert ml_with_different_several_magic_list_nonempty.shuffled() == list(
        [list([10, 11, 12]), list([16, 17, 18]), list([13, 14, 15])],
    )


def test_ml_with_different_several_tuple_nonempty(
    ml_with_different_several_tuple_nonempty,
):
    random.seed(RANDOM_SEED)

    assert ml_with_different_several_tuple_nonempty.shuffled() == list(
        [(9, 8, 7), (3, 2, 1), (6, 5, 4)],
    )


def test_ml_with_duplicate_several_int(ml_with_duplicate_several_int):
    random.seed(RANDOM_SEED)

    assert ml_with_duplicate_several_int.shuffled() == list(
        [1, 1, 0, 1, 0, 0, 1, 0, -1],
    )


def test_ml_with_duplicate_several_magic_list_nonempty(
    ml_with_duplicate_several_magic_list_nonempty,
):
    random.seed(RANDOM_SEED)

    assert ml_with_duplicate_several_magic_list_nonempty.shuffled() == list(
        [
            ["goodbye", "mars"],
            ["hello", "mars"],
            ["hello", "world"],
            ["hello", "world"],
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
def test_ml_with_equal_values(magic_list_instance):
    random.seed(RANDOM_SEED)

    assert magic_list_instance.shuffled() == magic_list_instance


def test_ml_recursive_with_itself(ml_recursive_with_itself):
    random.seed(RANDOM_SEED)

    assert ml_recursive_with_itself.shuffled() == ml_recursive_with_itself


def test_ml_with_recursive_item(ml_with_recursive_item):
    random.seed(RANDOM_SEED)

    assert ml_with_recursive_item.shuffled() == ml_with_recursive_item


def test_ml_with_mutually_recursive_item(ml_with_mutually_recursive_item):
    random.seed(RANDOM_SEED)

    assert ml_with_mutually_recursive_item.shuffled() == ml_with_mutually_recursive_item
