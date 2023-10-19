from __future__ import annotations

# We are making imports private in order to avoid collisions with the user
# namespace as this library is intended to be star-imported -- this style is
# often considered bad practice, but here the user desires to override the
# built-ins, so it's fine.
import builtins as _builtins
import collections as _collections
import collections.abc as _collections_abc
import functools as _functools
import typing as _typing

import magic_collections.features as _features

if _features.OPTION:
    from option import Err as _Err
    from option import maybe as _maybe
    from option import Ok as _Ok
    from option import Option as _Option
    from option import Result as _Result

if _typing.TYPE_CHECKING:  # pragma: no cover
    import _typeshed

__all__ = [
    "list",
    "dict",
    "str",
]

_K = _typing.TypeVar("_K")
_T = _typing.TypeVar("_T")
_U = _typing.TypeVar("_U")


class list(_collections.UserList[_T]):
    @property
    def head(self) -> _T:
        """
        First item of the list.

        Raises an exception if the list is empty.
        """

        if not self:
            raise ValueError("empty list has no head")

        return self[0]

    @property
    def tail(self) -> _typing.Self:
        """
        List without its head element (first item).

        Raises an exception if the list is empty.
        """

        if not self:
            raise ValueError("empty list has no tail")

        return self[1:]

    @property
    def init(self) -> _typing.Self:
        """
        List without its last item.

        Raises an exception if the list is empty.
        """

        if not self:
            raise ValueError("empty list has no init")

        return self[:-1]

    @property
    def last(self) -> _T:
        """
        Last item of the list.

        Raises an exception if the list is empty.
        """

        if not self:
            raise ValueError("empty list has no last")

        return self[-1]

    @property
    def head_safe(self) -> _T | None:
        """
        First item of the list, or `None` if the list is empty.
        """

        return self[0] if self else None

    @property
    def tail_safe(self) -> _typing.Self | None:
        """
        List without its head element (first item), or `None` if the list is
        empty.
        """

        return self[1:] if self else None

    @property
    def init_safe(self) -> _typing.Self | None:
        """
        List without its last element, or `None` if the list is empty.
        """

        return self[:-1] if self else None

    @property
    def last_safe(self) -> _T | None:
        """
        Last item of the list, or `None` if the list is empty.
        """

        return self[-1] if self else None

    def reversed(self) -> _typing.Self:
        """
        Returns a reversed version of the list.

        >>> list([1, 2, 3]).reversed()
        [3, 2, 1]
        """

        # we avoid constructing a whole `reversed` object
        return self.__class__(self.__reversed__())

    def sorted(
        self,
        *,
        key: _collections_abc.Callable[[_T], _typeshed.SupportsRichComparison]
        | None = None,
        reverse: bool = False,
    ) -> _typing.Self:
        """
        Returns a sorted version of the list.

        >>> list([3, 5, 2]).sorted()
        [2, 3, 5]
        >>> list("gala").sorted(key=ord)
        ["a", "a", "g", "l"]
        """

        return self.__class__(sorted(self, key=key, reverse=reverse))  # type: ignore

    def map(self, function: _collections_abc.Callable[[_T], _U]) -> list[_U]:
        """
        Apply `function` on each item of the list.

        >>> list([3, 5, 2]).map(str)
        ["3", "5", "2"]
        >>> list([3, 5, 2]).map(lambda n: n * 2)
        [6, 10, 4]
        >>> list().map(lambda n: n * 20)
        []
        """

        # subclasses' `map` return type is also marked as `list` because we
        # cannot make the container generic -- this requires Higher-Kinded
        # Types, which Python does not support (yet? hopefully!)

        return _typing.cast(list[_U], self.__class__(map(function, self)))

    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> _typing.Self:
        """
        Discard each item `i` of the list if `function(i)` is `False`.

        >>> list([3, 5, 2]).filter(lambda n: n % 2 == 1)
        [3, 5]
        >>> list(["hello", "hola", "bonjour"]).filter(lambda s: "l" in s)
        ["hello", "hola"]
        >>> list().filter(lambda n: n > 0)
        []
        """

        return self.__class__(filter(function, self))

    def reduce(self, function: _collections_abc.Callable[[_T, _T], _T]) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from left to right and return the result.

        The first element of the list is used as the leftmost value ;
        therefore, if the list is empty, it will raise an exception.

        >>> list([3, 5, 2]).reduce(operator.add)  # (3 + 5) + 2
        10
        >>> list().reduce(operator.mul)
        # TypeError exception: the list to reduce cannot be empty
        """

        return _functools.reduce(function, self)

    def reduce_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from right to left and return the result.

        The last element of the list is used as the rightmost value ;
        therefore, if the list is empty, it will raise an exception.

        >>> list([3, 5, 2]).reduce_right(operator.add)  # 3 + (5 + 2)
        10
        >>> list([3, 5, 2]).reduce_right(operator.sub)  # 3 - (5 - 2)
        0
        >>> list().reduce_right(operator.add)
        # TypeError exception: the list to reduce cannot be empty
        """

        return _functools.reduce(lambda a, b: function(b, a), self.reversed())

    def fold(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from left to right and return the result.

        The `initial_value` is used as the leftmost value, and is the returned
        value if the list is empty.

        >>> list([3, 5, 2]).fold(operator.add, -3)  # ((-3 + 3) + 5) + 2
        7
        >>> list().fold(operator.mul, 0)
        0
        """

        return _functools.reduce(function, self, initial_value)

    def fold_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from right to left and return the result.

        The `initial_value` is used as the rightmost value, and is the
        returned value if the list is empty.

        >>> list([3, 5, 2]).fold_right(operator.sub, -3)  # -3 - (3 - (5 - 2))
        0
        >>> list().fold_right(operator.mul, 0)
        0
        """

        return _functools.reduce(
            lambda a, b: function(b, a),
            self.reversed(),
            initial_value,
        )

    def scan(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _typing.Self:
        """
        "Insert" an operator (called a reducing function) between each element
        from left to right and return the intermediate values followed by the
        result.

        The `initial_value` is used as the leftmost value, and is the only
        value of the returned list if the original list is empty.

        >>> list([3, 5, 2]).scan(operator.add, 0)  # [0, (0 + 3), (0 + 3 + 5), (0 + 3 + 5 + 2)]
        [0, 3, 8, 10]
        >>> list().scan(operator.add, 0)
        [0]
        """

        result_tail = self.__class__()

        if self:
            head, *tail = self
            result_tail.extend(
                self.__class__(tail).scan(
                    function,
                    function(initial_value, head),
                )
            )

        return self.__class__([initial_value]) + result_tail

    def scan_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _typing.Self:
        """
        "Insert" an operator (called a reducing function) between each element
        from right to left and return the intermediate values followed by the
        result.

        The `initial_value` is used as the rightmost value, and is the only
        value of the returned list if the original list is empty.

        >>> list([3, 5, 2]).scan_right(operator.add, 0)  # [0, (2 + 0), (5 + 2 + 0), (3 + 5 + 2 + 0)]
        [0, 2, 7, 10]
        >>> list().scan_right(operator.add, 0)
        [0]
        """

        return self.reversed().scan(lambda a, b: function(b, a), initial_value)

    def mask(self, mask_seq: _collections_abc.Sequence[bool]) -> _typing.Self:
        if len(self) != len(mask_seq):
            raise ValueError("mask length must be the same as the list")

        return self.__class__(item for item, bit in zip(self, mask_seq) if bit)

    def gap_fill(
        self,
        fill: _T | _collections_abc.Callable[[_T, _T], _T],
    ) -> _typing.Self:
        if not self:
            raise ValueError("empty list has no gaps to be filled")

        returned_list = self.__class__([self.head])

        for i in range(1, len(self)):
            returned_list.append(fill(self[i - 1], self[i]) if callable(fill) else fill)
            returned_list.append(self[i])

        return returned_list

    if _features.OPTION:

        @property
        def head_maybe(self) -> _Option[_T]:
            """
            First item of the list.
            Returns an `Option` from the [`option`](https://pypi.org/project/option/) package.
            """

            return _maybe(self.head_safe)

        @property
        def tail_maybe(self) -> _Option[_typing.Self]:
            """
            List without its head element (first item), or `None` if the list
            is empty.
            Returns an `Option` from the [`option`](https://pypi.org/project/option/) package.
            """

            return _maybe(self.tail_safe)

        @property
        def init_maybe(self) -> _Option[_typing.Self]:
            """
            List without its last element, or `None` if the list is empty.
            Returns an `Option` from the [`option`](https://pypi.org/project/option/) package.
            """

            return _maybe(self.init_safe)

        @property
        def last_maybe(self) -> _Option[_T]:
            """
            Last item of the list, or `None` if the list is empty.
            Returns an `Option` from the [`option`](https://pypi.org/project/option/) package.
            """

            return _maybe(self.last_safe)

        def mask_pure(
            self,
            mask_seq: _collections_abc.Sequence[bool],
        ) -> _Result[_typing.Self, _builtins.str]:
            if len(self) != len(mask_seq):
                return _Err("mask length must be the same as the list")

            return _Ok(self.__class__(item for item, bit in zip(self, mask_seq) if bit))


class dict:
    ...


class str:
    ...
