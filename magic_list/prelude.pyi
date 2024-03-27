"""
Stub file for the `prelude` module.
"""

# We are making imports private in order to avoid collisions with the user namespace
# as this library is intended to be star-imported -- this style is often considered
# bad practice, but here the user desires to override the built-ins, so it's fine.
import collections as _collections
import typing as _typing

import _collections_abc
import _typeshed
import typing_extensions as _typing_extensions

__all__ = [
    "list",
    "L",
]

_T = _typing.TypeVar("_T")
_U = _typing.TypeVar("_U")
_V = _typing.TypeVar("_V")
_T_co = _typing.TypeVar("_T_co", covariant=True)
_T_contra = _typing.TypeVar("_T_contra", contravariant=True)
_NumberT = _typing.TypeVar("_NumberT", int, float, complex)

class _SupportsAdd(_typing.Protocol[_T]):
    def __add__(self: _T, other: _T, /) -> _T: ...

class list(_collections.UserList[_T]):
    @property
    def head(self) -> _T: ...
    @property
    def tail(self) -> _typing_extensions.Self: ...
    @property
    def init(self) -> _typing_extensions.Self: ...
    @property
    def last(self) -> _T: ...
    def prepend(self, item: _T) -> None: ...
    def reversed(self) -> _typing_extensions.Self: ...
    @_typing.overload
    def sorted(
        self: list[_typeshed.SupportsRichComparisonT],
        *,
        key: None = None,
        reverse: bool = False,
    ) -> list[_typeshed.SupportsRichComparisonT]: ...
    @_typing.overload
    def sorted(
        self,
        *,
        key: _collections_abc.Callable[[_T], _typeshed.SupportsRichComparison],
        reverse: bool = False,
    ) -> _typing_extensions.Self: ...
    def shuffled(self) -> _typing_extensions.Self: ...
    # subclasses' `map` return type is also marked as `list` because we cannot make
    # the container generic -- this requires Higher-Kinded Types, which Python does
    # not support (yet? hopefully!)
    def map(self, function: _collections_abc.Callable[[_T], _U]) -> list[_U]: ...
    def rotate(self, n: int = 1) -> _typing_extensions.Self: ...
    # *- filter-like HOFs -* #
    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> _typing_extensions.Self: ...
    def mask(
        self, mask_seq: _collections_abc.Sequence[bool]
    ) -> _typing_extensions.Self: ...
    def deduplicate(self) -> _typing_extensions.Self: ...
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
    ) -> _typing_extensions.Self: ...
    def scan_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _typing_extensions.Self: ...
    def zip_with(
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> list[_V]: ...
    def sum(self) -> _T: ...
    @_typing.overload
    def mean(self: list[int]) -> float: ...
    @_typing.overload
    def mean(self: list[float]) -> float: ...
    @_typing.overload
    def mean(self: list[complex]) -> complex: ...
    # *- expansion-based HOFs -* #
    def fill(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> None: ...
    def filled(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> _typing_extensions.Self: ...
    def gap_fill(
        self,
        filler: _T | _collections_abc.Callable[[_T, _T], _T],
    ) -> _typing_extensions.Self: ...
    # *- selectors -* #
    def select(
        self, indexes: _collections_abc.Sequence[int]
    ) -> _typing_extensions.Self: ...
    def take(self, n: int) -> _typing_extensions.Self: ...
    def take_right(self, n: int) -> _typing_extensions.Self: ...
    def drop(self, n: int) -> _typing_extensions.Self: ...
    def drop_right(self, n: int) -> _typing_extensions.Self: ...
    def slice(self, start: int, stop: int, /) -> _typing_extensions.Self: ...
    def partition(
        self, index: int
    ) -> tuple[_typing_extensions.Self, _T, _typing_extensions.Self]: ...
    def bisect(
        self, index: int
    ) -> tuple[_typing_extensions.Self, _typing_extensions.Self]: ...
    def trisect(
        self,
        left_index: int,
        right_index: int,
    ) -> tuple[
        _typing_extensions.Self, _typing_extensions.Self, _typing_extensions.Self
    ]: ...

@_typing.final
class _ListBuilder:
    @_typing.overload
    def __getitem__(self, key: slice, /) -> list[int]: ...
    @_typing.overload
    def __getitem__(self, key: _T | slice | tuple[_T, ...], /) -> list[_T]: ...

MagicListLiteral: _typing.Final = _typing.NewType(
    "MagicListLiteral",
    _ListBuilder,
)
L: MagicListLiteral
