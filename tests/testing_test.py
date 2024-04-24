# type: ignore

import pytest

from testing import contains_letter_l
from testing import double
from testing import greater_than_four


@pytest.mark.parametrize(
    ["x", "result"],
    [
        [3, 6],
        ["h", "hh"],
        ["do", "dodo"],
        [[3, 5, 2], [3, 5, 2, 3, 5, 2]],
        [(3, 5, 2), (3, 5, 2, 3, 5, 2)],
    ],
)
def test_double_ok(x, result):
    assert double(x) == result


@pytest.mark.parametrize(
    ["x", "result"],
    [
        [20, True],
        [5, True],
        [4, False],
        [3, False],
        [0, False],
        [-1, False],
        [-5, False],
    ],
)
def test_greater_than_four_ok(x, result):
    assert greater_than_four(x) is result


@pytest.mark.parametrize(
    ["x", "result"],
    [
        ["ball", True],
        ["sand", False],
        ["l", True],
        ["", False],
    ],
)
def test_contains_letter_l_ok(x, result):
    assert contains_letter_l(x) is result
