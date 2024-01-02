# type: ignore
import pytest

from magic_collections import Vec
from magic_collections import vec


@pytest.mark.parametrize(
    ["args", "result"],
    [
        [0, Vec([0])],
        [(0, 1, 2), Vec([0, 1, 2])],
        [slice(5), Vec([0, 1, 2, 3, 4])],
        [slice(2, 7), Vec([2, 3, 4, 5, 6])],
        [slice(1, 9, 2), Vec([1, 3, 5, 7])],
        ["hello", Vec(["hello"])],
        [("hello", "world"), Vec(["hello", "world"])],
        [slice("hello", "world"), Vec([slice("hello", "world")])],
    ],
)
def test_magic_list_literal(args, result):
    assert vec[args] == result
