import pytest

from magic_list import list

RANDOM_SEED = 0


@pytest.fixture(scope="session")
def ml_empty():
    """
    Empty Magic List.
    """

    return list()


@pytest.fixture(scope="session")
def ml_with_one_int_truthy():
    """
    Magic List with one integer, truthy (non-zero).
    """

    return list([42])


@pytest.fixture(scope="session")
def ml_with_one_int_falsy():
    """
    Magic List with one integer, falsy (zero).
    """

    return list([0])


@pytest.fixture(scope="session")
def ml_with_one_str():
    """
    Magic List with one string, truthy (non-empty).
    """

    return list(["hello"])


@pytest.fixture(scope="session")
def ml_with_one_list_nonempty():
    """
    Magic List with one list, truthy (non-empty).
    """

    return list([[3.14159, 2.71828, 9.80665]])


@pytest.fixture(scope="session")
def ml_with_one_magic_list_nonempty():
    """
    Magic List with one magic list, truthy (non-empty).
    """

    return list([list([14, 3, 1872])])


@pytest.fixture(scope="session")
def ml_with_one_tuple_nonempty():
    """
    Magic List with one tuple, truthy (non-empty).
    """

    return list([("John", "Doe", 23, 2183.76)])


@pytest.fixture(scope="session")
def ml_with_different_several_int():
    """
    Magic List with 2+ integers, all different, mixed (zero & non-zero).
    """

    return list([76, 39, -7, 0, 15])


@pytest.fixture(scope="session")
def ml_with_different_several_int_truthy():
    """
    Magic List with 2+ integers, all different, truthy (non-zero).
    """

    return list([1, 2, 4, 8, 16, 32])


@pytest.fixture(scope="session")
def ml_with_different_several_str():
    """
    Magic List with 2+ strings, all different, mixed (empty & non-empty).
    """

    return list(["hello", "", "world", "goodbye", " ", "mars"])


@pytest.fixture(scope="session")
def ml_with_different_several_list_nonempty():
    """
    Magic List with 2+ lists, all different, truthy (non-empty).
    """

    return list([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


@pytest.fixture(scope="session")
def ml_with_different_several_magic_list_nonempty():
    """
    Magic List with 2+ magic lists, all different, truthy (non-empty).
    """

    return list([list([10, 11, 12]), list([13, 14, 15]), list([16, 17, 18])])


@pytest.fixture(scope="session")
def ml_with_different_several_tuple_nonempty():
    """
    Magic List with 2+ tuples, all different, truthy (non-empty).
    """

    return list([(9, 8, 7), (6, 5, 4), (3, 2, 1)])


@pytest.fixture(scope="session")
def ml_with_duplicate_several_int():
    """
    Magic List with 2+ integers, with duplicates, mixed (zero & non-zero).
    """

    return list([1, 0, 0, 1, 0, 1, -1, 1, 0])


@pytest.fixture(scope="session")
def ml_with_duplicate_several_magic_list_nonempty():
    """
    Magic List with 2+ magic lists, with duplicates, truthy (non-empty).
    """

    return list(
        [
            list(["hello", "mars"]),
            list(["hello", "world"]),
            list(["goodbye", "mars"]),
            list(["hello", "world"]),
        ],
    )


@pytest.fixture(scope="session")
def ml_with_equal_several_int_truthy():
    """
    Magic List with 2+ integers, all equal, truthy (non-zero).
    """

    return list([23, 23, 23, 23])


@pytest.fixture(scope="session")
def ml_with_equal_several_int_falsy():
    """
    Magic List with 2+ integers, all equal, false (zero).
    """

    return list([0, 0, 0, 0])


@pytest.fixture(scope="session")
def ml_with_equal_several_list_empty():
    """
    Magic List with 2+ lists, all equal, falsy (empty).
    """

    return list([[], [], [], []])


@pytest.fixture(scope="session")
def ml_with_equal_several_magic_list_nonempty():
    """
    Magic List with 2+ magic lists, all equal, truthy (non-empty).
    """

    return list([list([3, 5, 2]), list([3, 5, 2]), list([3, 5, 2])])


@pytest.fixture(scope="session")
def ml_with_equal_several_magic_list_empty():
    """
    Magic List with 2+ magic lists, all equal, falsy (empty).
    """

    return list([list(), list(), list(), list()])


@pytest.fixture(scope="session")
def ml_recursive_with_itself():
    """
    Magic List with one magic list (itself), truthy (non-empty).
    """

    l = list()
    l.append(l)

    return l


@pytest.fixture(scope="session")
def ml_with_recursive_item():
    """
    Magic List with one recursive list, truthy (non-empty).
    """

    item = []
    item.append(item)

    return list([item])


@pytest.fixture(scope="session")
def ml_with_mutually_recursive_item():
    """
    Magic List with one list that contains the magic list, truthy (non-empty).
    """

    l = list()
    l.append([l])

    return l


@pytest.fixture(
    scope="session",
    params=[
        # *- empty -* #
        ml_empty,
        # *- one item -* #
        ml_with_one_int_truthy,
        ml_with_one_int_falsy,
        ml_with_one_str,
        ml_with_one_list_nonempty,
        ml_with_one_magic_list_nonempty,
        ml_with_one_tuple_nonempty,
        # *- 2+ items, different -* #
        ml_with_different_several_int,
        ml_with_different_several_int_truthy,
        ml_with_different_several_str,
        ml_with_different_several_list_nonempty,
        ml_with_different_several_magic_list_nonempty,
        ml_with_different_several_tuple_nonempty,
        # *- 2+ items, with duplicates -* #
        ml_with_duplicate_several_int,
        ml_with_duplicate_several_magic_list_nonempty,
        # *- 2+ items, only duplicates -* #
        ml_with_equal_several_int_truthy,
        ml_with_equal_several_int_falsy,
        ml_with_equal_several_list_empty,
        ml_with_equal_several_magic_list_nonempty,
        ml_with_equal_several_magic_list_empty,
        # *- recursives -* #
        ml_recursive_with_itself,
        ml_with_recursive_item,
        ml_with_mutually_recursive_item,
    ],
)
def magic_list_instance(request):
    """
    Instance of a magic list.
    """

    return request.getfixturevalue(request.param)


@pytest.fixture(scope="session")
def mask_empty():
    """
    Sequence of booleans, empty.
    """

    return []


@pytest.fixture(scope="session")
def mask_len4():
    """
    Sequence of booleans, length 4, false & true.
    """

    return [True, False, False, True]


@pytest.fixture(scope="session")
def mask_len4_all_true():
    """
    Sequence of booleans, length 4, all true.
    """

    return [True, True, True, True]


@pytest.fixture(scope="session")
def mask_len4_all_false():
    """
    Sequence of booleans, length 4, all false.
    """

    return [False, False, False, False]


@pytest.fixture(scope="session")
def mask_len5():
    """
    Sequence of booleans, length 5, true & false.
    """

    return [False, True, False, True, True]


@pytest.fixture(scope="session")
def mask_len5_all_true():
    """
    Sequence of booleans, length 5, all true.
    """

    return [True, True, True, True, True]


@pytest.fixture(scope="session")
def mask_len5_all_false():
    """
    Sequence of booleans, length 5, all false.
    """

    return [False, False, False, False]


@pytest.fixture(
    scope="session",
    params=[
        mask_empty,
        mask_len4,
        mask_len4_all_true,
        mask_len4_all_false,
        mask_len5,
        mask_len5_all_true,
        mask_len5_all_false,
    ],
)
def mask_instance(request):
    """
    Sequence of booleans.
    """

    return request.getfixturevalue(request.param)
