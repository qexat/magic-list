"""
Stub file for the `prelude` module.
"""

import collections
import typing as typing

import _collections_abc
import _typeshed
import typing_extensions

__all__ = [
    "list",
    "L",
]

_T = typing.TypeVar("_T")
_U = typing.TypeVar("_U")
_V = typing.TypeVar("_V")
_T_co = typing.TypeVar("_T_co", covariant=True)
_T_contra = typing.TypeVar("_T_contra", contravariant=True)
_NumberT = typing.TypeVar("_NumberT", int, float, complex)

class _SupportsAdd(typing.Protocol[_T]):
    def __add__(self: _T, other: _T, /) -> _T: ...

class list(collections.UserList[_T]):
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
    def map(self, function: _collections_abc.Callable[[_T], _U]) -> list[_U]: ...
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
    def merge(
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> list[_V]: ...
    def sum(self) -> _T: ...
    @typing.overload
    def mean(self: list[int]) -> float: ...
    @typing.overload
    def mean(self: list[float]) -> float: ...
    @typing.overload
    def mean(self: list[complex]) -> complex: ...
    # *- expansion-based HOFs -* #
    def fill_left(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self: ...
    def fill_right(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self: ...
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
        self, index: int
    ) -> tuple[typing_extensions.Self, _T, typing_extensions.Self]: ...
    def bisect(
        self, index: int
    ) -> tuple[typing_extensions.Self, typing_extensions.Self]: ...
    def trisect(
        self,
        left_index: int,
        right_index: int,
    ) -> tuple[
        typing_extensions.Self, typing_extensions.Self, typing_extensions.Self
    ]: ...

@typing.final
class _ListBuilder:
    @typing.overload
    def __getitem__(self, key: slice, /) -> list[int]: ...
    @typing.overload
    def __getitem__(self, key: _T | slice | tuple[_T, ...], /) -> list[_T]: ...

MagicListLiteral: typing.Final = typing.NewType(
    "MagicListLiteral",
    _ListBuilder,
)
L: MagicListLiteral
