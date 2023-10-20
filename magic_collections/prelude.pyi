"""
Stub file for the `prelude` module.
"""

# We are making imports private in order to avoid collisions with the user namespace
# as this library is intended to be star-imported -- this style is often considered
# bad practice, but here the user desires to override the built-ins, so it's fine.
import collections as _collections
import _collections_abc
import _typeshed
import typing as _typing

import magic_collections.features as _features

if _features.OPTION:
    import option as _option

__all__ = [
    "list",
    "dict",
    "str",
]

_K = _typing.TypeVar("_K")
_T = _typing.TypeVar("_T")
_U = _typing.TypeVar("_U")
_V = _typing.TypeVar("_V")

class list(_collections.UserList[_T]):
    @property
    def head(self) -> _T: ...
    @property
    def tail(self) -> _typing.Self: ...
    @property
    def init(self) -> _typing.Self: ...
    @property
    def last(self) -> _T: ...
    def reversed(self) -> _typing.Self: ...
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
    ) -> _typing.Self: ...
    # subclasses' `map` return type is also marked as `list` because we cannot make
    # the container generic -- this requires Higher-Kinded Types, which Python does
    # not support (yet? hopefully!)
    def map(self, function: _collections_abc.Callable[[_T], _U]) -> list[_U]: ...
    def rotate(self, n: int = 1) -> _typing.Self: ...
    # *- filter-like HOFs -* #
    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> _typing.Self: ...
    def mask(self, mask_seq: _collections_abc.Sequence[bool]) -> _typing.Self: ...
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
    ) -> _typing.Self: ...
    def scan_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _typing.Self: ...
    def merge(
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> list[_V]: ...
    # *- expansion-based HOFs -* #
    def gap_fill(
        self,
        fill: _T | _collections_abc.Callable[[_T, _T], _T],
    ) -> _typing.Self: ...
    # *- selectors -* #
    def select(self, indexes: _collections_abc.Sequence[int]) -> _typing.Self: ...
    def take(self, n: int) -> _typing.Self: ...
    def drop(self, n: int) -> _typing.Self: ...
    @_typing.overload
    def slice(self, stop: int, /) -> _typing.Self: ...
    @_typing.overload
    def slice(self, start: int, stop: int, /) -> _typing.Self: ...

    # *- additional features -* #

    if _features.OPTION:
        @property
        def head_maybe(self) -> _option.Option[_T]: ...
        @property
        def tail_maybe(self) -> _option.Option[_typing.Self]: ...
        @property
        def init_maybe(self) -> _option.Option[_typing.Self]: ...
        @property
        def last_maybe(self) -> _option.Option[_T]: ...
        def mask_pure(
            self,
            mask_seq: _collections_abc.Sequence[bool],
        ) -> _option.Result[_typing.Self, str]: ...

class dict(_collections.UserDict[_K, _T]):
    def __neg__(self) -> dict[_T, _K]: ...
    def map(
        self,
        function: _collections_abc.Callable[[_K, _T], _U],
    ) -> dict[_K, _U]: ...
    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> _typing.Self: ...
    def filter_keys(
        self,
        function: _collections_abc.Callable[[_K], bool],
    ) -> _typing.Self: ...
    def as_list(self) -> list[tuple[_K, _T]]: ...

class str(_collections.UserString):
    @_typing.overload
    def map(
        self,
        function: _collections_abc.Callable[[_typing.Self], _typing.Self],
    ) -> _typing.Self: ...
    @_typing.overload
    def map(
        self,
        function: _collections_abc.Callable[[_typing.Self], _T],
    ) -> _collections_abc.Sequence[_T]: ...
    def map(
        self,
        function: _collections_abc.Callable[[_typing.Self], _T],
    ) -> _collections_abc.Sequence[_T]: ...
    def filter(
        self,
        function: _collections_abc.Callable[[_typing.Self], bool],
    ) -> _typing.Self: ...
    def reduce(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
    ) -> _typing.Self: ...
    def reduce_right(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
    ) -> _typing.Self: ...
    def fold(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
        initial_value: _typing.Self,
    ) -> _typing.Self: ...
    def fold_right(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
        initial_value: _typing.Self,
    ) -> _typing.Self: ...
    def scan(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
        initial_value: _typing.Self,
    ) -> _typing.Self: ...
    def scan_right(
        self,
        function: _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
        initial_value: _typing.Self,
    ) -> _typing.Self: ...
    def mask(self, mask_seq: _collections_abc.Sequence[bool]) -> _typing.Self: ...
    def gap_fill(
        self,
        fill: _typing.Self
        | _collections_abc.Callable[[_typing.Self, _typing.Self], _typing.Self],
    ) -> _typing.Self: ...
