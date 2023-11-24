"""
This module contains all the classes, functions and identifiers available in
the package base. They can be imported by doing the following:

```py
from magic_collections import *
```

Note on imports:
    We are making imports private in order to avoid collisions with the user
    namespace as this library is intended to be star-imported -- this style is
    often considered bad practice, but here the user desires to override the
    built-ins, so it's fine.
"""
from __future__ import annotations

import collections as _collections
import collections.abc as _collections_abc
import functools as _functools
import typing as _typing


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
_V = _typing.TypeVar("_V")


class list(_collections.UserList[_T]):
    @property
    def head(self) -> _T:
        """
        First item of the list.

        Raises an exception if the list is empty.

        >>> list([3, 5, 2]).head
        3
        >>> list().head
        *- TypeError: empty list has no head -*
        """

        if not self:
            raise TypeError("empty list has no head")

        return self[0]

    @property
    def tail(self) -> _typing.Self:
        """
        List without its first item.

        Raises an exception if the list is empty.

        >>> list([3, 5, 2]).tail
        [5, 2]
        >>> list().tail
        *- TypeError: empty list has no tail -*
        """

        if not self:
            raise TypeError("empty list has no tail")

        return self[1:]

    @property
    def init(self) -> _typing.Self:
        """
        List without its last item.

        Raises an exception if the list is empty.

        >>> list([3, 5, 2]).init
        [3, 5]
        >>> list().init
        *- TypeError: empty list has no init -*
        """

        if not self:
            raise TypeError("empty list has no init")

        return self[:-1]

    @property
    def last(self) -> _T:
        """
        Last item of the list.

        Raises an exception if the list is empty.

        >>> list([3, 5, 2]).last
        2
        >>> list().last
        *- TypeError: empty list has no last -*
        """

        if not self:
            raise TypeError("empty list has no last")

        return self[-1]

    def prepend(self, item: _T) -> None:
        """
        Add an item at the beginning of the list.

        >>> l = list([3, 5, 2])
        >>> l.prepend(-2)
        >>> print(l)
        [-2, 3, 5, 2]
        """

        self.insert(0, item)

    def reversed(self) -> _typing.Self:
        """
        Return a reversed version of the list.

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
        Return a sorted version of the list.

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

    def map_two(
        self,
        function1: _collections_abc.Callable[[_T], _U],
        function2: _collections_abc.Callable[[_U], _V],
    ) -> list[_V]:
        """
        Apply `function1` then `function2` on each item of the list.

        >>> list([3, 5, 2]).map_two(str, ord)
        [51, 53, 50]
        >>> list().map(str)
        []
        """

        return self.map(function1).map(function2)

    def rotate(self, n: int = 1) -> _typing.Self:
        """
        Shift the list `n` times to the right. The items that overflow get prepended.

        If `n` is negative, the shift goes to the left.

        >>> list([3, 5, 2]).rotate()
        [2, 3, 5]
        >>> list([3, 5, 2]).rotate(2)
        [5, 2, 3]
        >>> list([3, 5, 2]).rotate(-1)
        [5, 2, 3]
        >>> list().rotate()
        *- TypeError: empty list cannot be rotated -*
        """

        if not self:
            raise TypeError("empty list cannot be rotated")

        if n == 0:
            return self

        returned_list = self.copy()

        if n > 0:
            xpend_method = returned_list.prepend
            popped_index = -1
        else:
            xpend_method = returned_list.append
            popped_index = 0

        for _ in range(abs(n)):
            xpend_method(returned_list.pop(popped_index))

        return returned_list

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

    def mask(self, mask_seq: _collections_abc.Sequence[bool]) -> _typing.Self:
        """
        Keep every element at index `i` of the list if the corresponding
        element at index `i` of the mask sequence is `True` ; else, discard
        it. Return the filtered list.

        >>> list([3, 5, 2]).mask([True, False, True])
        [3, 2]
        >>> list().mask([])
        []
        >>> list([3, 5, 2]).mask([True, False])
        *- TypeError: mask length must be the same as the list -*
        """

        if len(self) != len(mask_seq):
            raise TypeError("mask length must be the same as the list")

        return self.__class__(item for item, bit in zip(self, mask_seq) if bit)

    def reduce(self, function: _collections_abc.Callable[[_T, _T], _T]) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from left to right and return the result.

        The first element of the list is used as the leftmost value ;
        therefore, if the list is empty, it will raise an exception.

        >>> list([3, 5, 2]).reduce(operator.add)  # (3 + 5) + 2
        10
        >>> list().reduce(operator.mul)
        *- TypeError: the list to reduce cannot be empty -*
        """

        if not self:
            raise TypeError("the list to reduce cannot be empty")

        return _functools.reduce(function, self)

    def reduce_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from right to left and return the result.

        The last element of the list is used as the leftmost value ;
        therefore, if the list is empty, it will raise an exception.

        >>> list([3, 5, 2]).reduce_right(operator.add)  # 3 + (5 + 2)
        10
        >>> list([3, 5, 2]).reduce_right(operator.sub)  # 3 - (5 - 2)
        0
        >>> list().reduce_right(operator.add)
        *- TypeError: the list to reduce cannot be empty -*
        """

        if not self:
            raise TypeError("the list to reduce cannot be empty")

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

        The `initial_value` is used as the leftmost value, and is the
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
                ),
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

        The `initial_value` is used as the leftmost value, and is the only
        value of the returned list if the original list is empty.

        >>> list([3, 5, 2]).scan_right(operator.add, 0)  # [0, (2 + 0), (5 + 2 + 0), (3 + 5 + 2 + 0)]
        [0, 2, 7, 10]
        >>> list().scan_right(operator.add, 0)
        [0]
        """

        return self.reversed().scan(lambda a, b: function(b, a), initial_value)

    def merge(
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> list[_V]:
        """
        Build a new list from the result of each `function(s_i, o_i)` where
        `s_i` and `o_i` are the items at index `i` of `self` and `other`
        respectively.

        >>> list([3, 5, 2]).merge(operator.add, [-1, 4, -9])
        [2, 9, -7]
        >>> list().merge(operator.sub, [])
        []
        >>> list([3, 5, 2]).merge(operator.add, [6])
        *- TypeError: the length of the two sequences must be equal -*
        """

        if len(self) != len(other):
            raise TypeError("the length of the two sequences must be equal")

        return _typing.cast(
            list[_V],
            self.__class__(function(a, b) for a, b in zip(self, other)),
        )

    def filled(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> _typing.Self:
        """
        Fill on the right the list with `filler` and return the result.

        If `filler` is a function, it takes the current list (at the current
        filling iteration) and produces a new value to be appended.

        >>> list([3, 5, 2]).filled(0, 5)
        [3, 5, 2, 0, 0, 0, 0, 0]
        >>> list([3, 5, 2]).filled(sum, 3)
        [3, 5, 2, 10, 20, 40]
        >>> list().filled(1, 10)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        >>> list([3, 5, 2]).filled(0, -1)
        *- ValueError: the number of times to fill cannot be negative -*
        """

        if n < 0:
            raise ValueError("the number of times to fill cannot be negative")

        returned_list = self.copy()

        for _ in range(n):
            returned_list.append(filler(returned_list) if callable(filler) else filler)

        return returned_list

    def fill(
        self,
        filler: _T | _collections_abc.Callable[[list[_T]], _T],
        n: int,
    ) -> None:
        """
        In-place equivalent of `filled`.

        >>> lst = list([3, 5, 2])
        >>> lst.fill(0, 5)
        >>> print(lst)
        [3, 5, 2, 0, 0, 0, 0, 0]
        >>> lst.fill(0, -1)
        *- ValueError: the number of times to fill cannot be negative -*
        """

        if n < 0:
            raise ValueError("the number of times to fill cannot be negative")

        for _ in range(n):
            self.append(filler(self) if callable(filler) else filler)

    def gap_fill(
        self,
        filler: _T | _collections_abc.Callable[[_T, _T], _T],
    ) -> _typing.Self:
        """
        Fill in-between the items with `filler` and return the result.

        If `filler` is a function, it takes the two items surrounding the gap
        that is about to be filled and produces a new value to be inserted.

        >>> list([3, 5, 2]).gap_fill(0)
        [3, 0, 5, 0, 2]
        >>> list([3, 5, 2]).gap_fill(operator.add)
        [3, 8, 5, 7, 2]
        >>> list().gap_fill(0)
        *- ValueError: empty list has no gap to be filled -*
        """

        if not self:
            raise ValueError("empty list has no gap to be filled")

        returned_list = self.__class__([self.head])

        for i in range(1, len(self)):
            returned_list.append(
                filler(self[i - 1], self[i]) if callable(filler) else filler,
            )
            returned_list.append(self[i])

        return returned_list

    def select(self, indexes: _collections_abc.Sequence[int]) -> _typing.Self:
        """
        Select items at provided indexes. If an index is present several
        times, this will be reflected in the resulting list.

        >>> list([3, 5, 2]).select([1, 2, 0, 0])
        [5, 2, 3, 3]
        >>> list().select([])
        []
        >>> list([3, 5, 2]).select([4, 1])
        *- IndexError: index 4 is out of bounds -*
        """

        returned_list = self.__class__()

        for index in indexes:
            if index >= len(self) or index < -len(self):
                raise IndexError(f"index {index} is out of bounds")

            returned_list.append(self[index])

        return returned_list

    def take(self, n: int) -> _typing.Self:
        """
        Take `n` items from the list and return them.

        >>> list([3, 5, 2]).take(2)
        [3, 5]
        >>> list([3, 5, 2]).take(0)
        []
        >>> list([3, 5, 2]).take(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> list([3, 5, 2]).take(5)
        *- ValueError: cannot take more items than the list contains -*
        """

        if n < 0:
            raise ValueError("cannot take a negative amount of items")

        if n > len(self):
            raise ValueError("cannot take more items than the list contains")

        return self.__class__(self[i] for i in range(n))

    def take_right(self, n: int) -> _typing.Self:
        """
        Take `n` items from the right of the list and return them.

        List original order is preserved.

        >>> list([3, 5, 2]).take_right(2)
        [5, 2]
        >>> list([3, 5, 2]).take_right(0)
        []
        >>> list([3, 5, 2]).take_right(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> list([3, 5, 2]).take_right(5)
        *- ValueError: cannot take more items than the list contains -*
        """

        if n < 0:
            raise ValueError("cannot take a negative amount of items")

        if n > len(self):
            raise ValueError("cannot take more items than the list contains")

        return self.__class__(item for item in self[len(self) - n :])

    def drop(self, n: int) -> _typing.Self:
        """
        Drop `n` items from the list and return the rest.

        >>> list([3, 5, 2]).drop(2)
        [2]
        >>> list([3, 5, 2]).drop(0)
        [3, 5, 2]
        >>> list([3, 5, 2]).drop(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> list([3, 5, 2]).drop(5)
        *- ValueError: cannot drop more items than the list contains -*
        """

        if n < 0:
            raise ValueError("cannot drop a negative amount of items")

        if n > len(self):
            raise ValueError("cannot drop more items than the list contains")

        return self[n:]

    def drop_right(self, n: int) -> _typing.Self:
        """
        Drop `n` items from the right of the list and return the rest.

        >>> list([3, 5, 2]).drop_right(2)
        [3]
        >>> list([3, 5, 2]).drop_right(0)
        [3, 5, 2]
        >>> list([3, 5, 2]).drop_right(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> list([3, 5, 2]).drop_right(5)
        *- ValueError: cannot drop more items than the list contains -*
        """

        if n < 0:
            raise ValueError("cannot drop a negative amount of items")

        if n > len(self):
            raise ValueError("cannot drop more items than the list contains")

        return self[: len(self) - n]

    def slice(self, start: int, stop: int) -> _typing.Self:
        """
        Slice the list from `start` to `stop` and return the result.

        This method is NOT equivalent to the `self[start:stop]` notation.
        If `start` or `stop` are out of bounds of the list or `start` is
        greater than `stop`, it will raise an exception.

        >>> list([2, 4, 8, 16, 32]).slice(1, 3)
        [4, 8, 16]
        >>> list([2, 4, 8, 16, 32]).slice(0, 2)
        [2, 4, 8]
        >>> list([2, 4, 8, 16, 32]).slice(3, 5)
        [8, 16, 32]
        >>> list([2, 4, 8, 16, 32]).slice(2, 2)
        [8]
        >>> list([2, 4, 8, 16, 32]).slice(1, 10)
        *- ValueError: slice out of bounds -*
        >>> list([2, 4, 8, 16, 32]).slice(4, 2)
        *- ValueError: start cannot be greater than stop -*

        Tip: if `start` is 0, you can do `.take(stop - 1)` instead.
        Symmetrically, if `stop` is the index of the last item, go for a
        `.drop(start)`!
        """

        if start > stop:
            raise ValueError("start cannot be greater than stop")

        if start < 0 or stop >= len(self):
            raise ValueError("slice out of bounds")

        return self[start : stop + 1]


class dict:
    ...


class str:
    ...
