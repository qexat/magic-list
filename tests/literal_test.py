import pytest

from magic_list import L
from magic_list import list


@pytest.mark.parametrize(
    ("input_value", "output_arg"),
    [
        pytest.param(0, [0], id="single_integer"),
        pytest.param("hello", ["hello"], id="single_string"),
    ],
)
def test_single_value(input_value, output_arg):
    assert L[input_value] == list(output_arg)


@pytest.mark.parametrize(
    ("input_tuple", "output_arg"),
    [
        pytest.param((0, 1, 2), [0, 1, 2], id="several_integers"),
        pytest.param(("hello", "world"), ["hello", "world"], id="several_strings"),
        pytest.param(
            ([8, 13, 21], [21, 34, 55]),
            [[8, 13, 21], [21, 34, 55]],
            id="several_lists",
        ),
        pytest.param(
            ((0, 1, 2), (2, 3, 4), (4, 5, 6)),
            [(0, 1, 2), (2, 3, 4), (4, 5, 6)],
            id="several_tuples",
        ),
    ],
)
def test_several_values(input_tuple, output_arg):
    assert L[input_tuple] == list(output_arg)


@pytest.mark.parametrize(
    ("input_slice", "output_arg"),
    [
        pytest.param(
            slice(5),
            [0, 1, 2, 3, 4],
            id="stop_only_integer_slice",
        ),
        pytest.param(
            slice(2, 7),
            [2, 3, 4, 5, 6],
            id="start_stop_integer_slice",
        ),
        pytest.param(
            slice(1, 9, 2),
            [1, 3, 5, 7],
            id="start_stop_step_integer_slice",
        ),
    ],
)
def test_integer_slice(input_slice, output_arg):
    assert L[input_slice] == list(output_arg)


@pytest.mark.parametrize(
    ("input_slice", "output_list_arg"),
    [
        pytest.param(
            slice("hello", "world"),
            [slice("hello", "world")],
            id="string_slice",
        ),
        pytest.param(
            slice([2, 3], [-1, 5]),
            [slice([2, 3], [-1, 5])],
            id="integer_slice",
        ),
    ],
)
def test_noninteger_slice(input_slice, output_list_arg):
    assert L[input_slice] == list(output_list_arg)


def test_empty():
    assert L[()] == list()
