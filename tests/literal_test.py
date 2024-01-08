# type: ignore
import pytest

from magic_collections import L
from magic_collections import list


@pytest.mark.parametrize(
    ["args", "result"],
    [
        [0, list([0])],
        [(0, 1, 2), list([0, 1, 2])],
        [slice(5), list([0, 1, 2, 3, 4])],
        [slice(2, 7), list([2, 3, 4, 5, 6])],
        [slice(1, 9, 2), list([1, 3, 5, 7])],
        ["hello", list(["hello"])],
        [("hello", "world"), list(["hello", "world"])],
        [slice("hello", "world"), list([slice("hello", "world")])],
    ],
)
def test_magic_list_literal(args, result):
    assert L[args] == result
