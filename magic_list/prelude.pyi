"""
Stub file for the module.
"""

import collections
import sys
import typing

import _collections_abc
import _typeshed
import typing_extensions

__all__ = [
    "list",
    "L",
]

_T_co = typing.TypeVar("_T_co", covariant=True)
_T_contra = typing.TypeVar("_T_contra", contravariant=True)
_NumberT = typing.TypeVar("_NumberT", int, float, complex)

class _SupportsAdd[_T](typing.Protocol):
    def __add__(self: _T, other: _T, /) -> _T: ...

class list[_T](collections.UserList[_T]):
    @property
    def head(self) -> _T: ...
    @property
    def tail(self) -> typing_extensions.Self: ...
    @property
    def init(self) -> typing_extensions.Self: ...
    @property
    def last(self) -> _T: ...
    def prepend(self, item: _T) -> None: ...
    def reversed(self) -> typing_extensions.Self: ...
    @typing.overload
    def sorted(
        self: list[_typeshed.SupportsRichComparisonT],
        *,
        key: None = None,
        reverse: bool = False,
    ) -> list[_typeshed.SupportsRichComparisonT]: ...
    @typing.overload
    def sorted(
        self,
        *,
        key: _collections_abc.Callable[[_T], _typeshed.SupportsRichComparison],
        reverse: bool = False,
    ) -> typing_extensions.Self: ...
    def shuffled(self) -> typing_extensions.Self: ...
    # subclasses' `map` return type is also marked as `list` because we cannot make
    # the container generic -- this requires Higher-Kinded Types, which Python does
    # not support (yet? hopefully!)
    def map[_U](self, function: _collections_abc.Callable[[_T], _U]) -> list[_U]: ...
    @typing.overload
    def rotate(self) -> typing_extensions.Self: ...
    @typing.overload
    def rotate(self, n: int = 1) -> typing_extensions.Self: ...
    # *- filter-like HOFs -* #
    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> typing_extensions.Self: ...
    def mask(
        self, mask_seq: _collections_abc.Sequence[bool]
    ) -> typing_extensions.Self: ...
    def deduplicate(self) -> typing_extensions.Self: ...
    # *- reduction-based HOFs -* #
    def reduce(self, function: _collections_abc.Callable[[_T, _T], _T]) -> _T: ...
    def reduce_right(self, function: _collections_abc.Callable[[_T, _T], _T]) -> _T: ...
    def fold(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T: ...
    def fold_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T: ...
    def scan(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> typing_extensions.Self: ...
    def scan_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> typing_extensions.Self: ...
    def merge[_U, _V](
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> list[_V]: ...
    def flatten(self) -> list[typing.Any]: ...
    def sum(self) -> _T: ...
    @typing.overload
    def mean(self: list[int]) -> float: ...
    @typing.overload
    def mean(self: list[float]) -> float: ...
    @typing.overload
    def mean(self: list[complex]) -> complex: ...
    @typing.overload
    def mean(self) -> typing_extensions.Never: ...
    @typing.overload
    def min[NumberT: int | float | complex](self: list[NumberT]) -> NumberT: ...
    @typing.overload
    def min(self) -> typing_extensions.Never: ...
    @typing.overload
    def max[NumberT: int | float](self: list[NumberT]) -> NumberT: ...
    @typing.overload
    def max(self) -> typing_extensions.Never: ...
    # *- expansion-based HOFs -* #
    @typing.overload
    def fill_left(self, filler: _T, n: int) -> typing_extensions.Self: ...
    @typing.overload
    def fill_left(
        self,
        filler: _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self: ...
    @typing.overload
    def fill_right(self, filler: _T, n: int) -> typing_extensions.Self: ...
    @typing.overload
    def fill_right(
        self,
        filler: _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self: ...
    @typing.overload
    def interleave(
        self,
        filler: _T,
    ) -> typing_extensions.Self: ...
    @typing.overload
    def interleave(
        self,
        filler: _collections_abc.Callable[[_T, _T], _T],
    ) -> typing_extensions.Self: ...
    @typing_extensions.deprecated("`gap_fill` has been renamed to `interleave`")
    def gap_fill(
        self,
        filler: _T | _collections_abc.Callable[[_T, _T], _T],
    ) -> typing_extensions.Self: ...
    # *- selectors -* #
    def select(
        self, indexes: _collections_abc.Sequence[int]
    ) -> typing_extensions.Self: ...
    def take(self, n: int) -> typing_extensions.Self: ...
    def take_right(self, n: int) -> typing_extensions.Self: ...
    def drop(self, n: int) -> typing_extensions.Self: ...
    def drop_right(self, n: int) -> typing_extensions.Self: ...
    def slice(self, start: int, stop: int, /) -> typing_extensions.Self: ...
    def partition(
        self,
        index: int,
    ) -> tuple[typing_extensions.Self, _T, typing_extensions.Self]: ...
    def bisect(
        self,
        index: int,
    ) -> tuple[typing_extensions.Self, typing_extensions.Self]: ...
    def trisect(
        self,
        left_index: int,
        right_index: int,
    ) -> tuple[
        typing_extensions.Self, typing_extensions.Self, typing_extensions.Self
    ]: ...

    # *- pre-existing methods (added for documentation) -*

    def append(self, item: _T) -> None:
        """
        Add an item at the end of the list.

        >>> l = L[3, 5, 2]
        >>> l.append(-2)
        >>> print(l)
        [3, 5, 2, -2]
        """

    def insert(self, i: int, item: _T) -> None:
        """
        Insert an item at the index `i` (before the element at this position).

        >>> l = L[3, 5, 2]
        >>> l.insert(1, -2)
        >>> print(l)
        [3, -2, 5, 2]
        """

    @typing.overload
    def pop(self) -> _T: ...
    @typing.overload
    def pop(self, i: int = -1) -> _T: ...
    def pop(self, i: int = -1) -> _T:
        """
        Remove the item at the index `i` if provided or the last and return it.

        >>> l = L[3, 5, 2]
        >>> l.pop()
        2
        >>> print(l)
        [3, 5]
        """

    def remove(self, item: _T) -> None:
        """
        Remove the `item` from the list.

        .. warning:: The item must be present in the list.

        >>> l = L[3, 5, 2]
        >>> l.remove(5)
        >>> print(l)
        [3, 2]
        >>> l.remove(-2)
        *- ValueError: list.remove(x): x not in list -*
        """

    def clear(self) -> None:
        """
        Remove all the items from the list.

        >>> l = L[3, 5, 2]
        >>> l.clear()
        >>> print(l)
        []
        """

    def copy(self) -> typing_extensions.Self:
        """
        Return a shallow copy of the list.

        >>> l0 = L[3, 5, 2]
        >>> l1 = l0.copy()
        >>> print(l1)
        [3, 5, 2]
        >>> l0 is l1
        False
        """

    def count(self, item: _T) -> int:
        """
        Return the number of occurrences of the `item` in the list.

        >>> l = L[3, 5, 2, 5]
        >>> l.count(5)
        2
        >>> l.count(2)
        1
        >>> l.count(-2)
        0
        """

    @typing.overload
    def index(self, item: _T, /) -> int: ...
    @typing.overload
    def index(
        self,
        item: _T,
        start: typing.SupportsIndex = 0,
        stop: typing.SupportsIndex = sys.maxsize,
        /,
    ) -> int: ...
    def index(
        self,
        item: _T,
        start: typing.SupportsIndex = 0,
        stop: typing.SupportsIndex = sys.maxsize,
        /,
    ) -> int:
        """
        Return the first index of the `item` in the list.

        .. warning:: The item must be present in the list.

        >>> l = L[3, 5, 2]
        >>> l.index(5)
        1
        >>> l.index(-2)
        *- ValueError: -2 is not in list -*
        """

    def reverse(self) -> None:
        """
        Reverse the list in place.

        >>> l = L[3, 5, 2]
        >>> l.reverse()
        >>> print(l)
        [2, 5, 3]
        """

    @typing.overload
    def sort[SupportsRichComparisonT: _typeshed.SupportsRichComparison](
        self: list[SupportsRichComparisonT],
        *,
        key: None = None,
        reverse: bool = False,
    ) -> None: ...
    @typing.overload
    def sort(
        self,
        *,
        key: _collections_abc.Callable[[_T], _typeshed.SupportsRichComparison],
        reverse: bool = False,
    ) -> None: ...
    def sort[SupportsRichComparisonT: _typeshed.SupportsRichComparison](  # pyright: ignore[reportIncompatibleMethodOverride]
        self: typing_extensions.Self | list[SupportsRichComparisonT],
        *,
        key: _collections_abc.Callable[[_T], _typeshed.SupportsRichComparison]
        | None = None,
        reverse: bool = False,
    ) -> None:
        """
        Sort the list in place.

        >>> l = [3, 5, 2]
        >>> l.sort()
        >>> print(l)
        [2, 3, 5]
        """

    def extend(self, other: _collections_abc.Iterable[_T]) -> None:
        """
        Append the items of `other` to the list.

        >>> l = [3, 5, 2]
        >>> l.extend([4, 1, 3])
        >>> print(l)
        [3, 5, 2, 4, 1, 3]
        """

@typing.final
class _ListBuilder:
    @typing.overload
    def __getitem__(self, key: slice, /) -> list[int]: ...
    @typing.overload
    def __getitem__[_T](self, key: _T | slice | tuple[_T, ...], /) -> list[_T]: ...

MagicListLiteral: typing.Final = typing.NewType(
    "MagicListLiteral",
    _ListBuilder,
)
L: MagicListLiteral
