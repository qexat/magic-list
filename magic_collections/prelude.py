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
import operator as _operator
import random as _random
import typing as _typing


if _typing.TYPE_CHECKING:  # pragma: no cover
    import _typeshed

__all__ = [
    "Vec",
    "dict",
    "str",
    "vec",
]

_K = _typing.TypeVar("_K")
_T = _typing.TypeVar("_T")
_U = _typing.TypeVar("_U")
_V = _typing.TypeVar("_V")
_NumberT = _typing.TypeVar("_NumberT", int, float, complex)


class Vec(_collections.UserList[_T]):
    """
    Mutable heterogeneous sequence.
    Drop-in replacement for the built-in `list` type.
    """

    @property
    def head(self) -> _T:
        """
        First item of the vector.

        Raises an exception if the vector is empty.

        >>> vec[3, 5, 2].head
        3
        >>> Vec().head
        *- TypeError: empty vector has no head -*
        """

        if not self:
            raise TypeError("empty vector has no head")

        return self[0]

    @property
    def tail(self) -> _typing.Self:
        """
        Vector without its first item.

        Raises an exception if the vector is empty.

        >>> vec[3, 5, 2].tail
        [5, 2]
        >>> Vec().tail
        *- TypeError: empty vector has no tail -*
        """

        if not self:
            raise TypeError("empty vector has no tail")

        return self.__class__(self[1:])

    @property
    def init(self) -> _typing.Self:
        """
        Vector without its last item.

        Raises an exception if the vector is empty.

        >>> vec[3, 5, 2].init
        [3, 5]
        >>> Vec().init
        *- TypeError: empty vector has no init -*
        """

        if not self:
            raise TypeError("empty vector has no init")

        return self.__class__(self[:-1])

    @property
    def last(self) -> _T:
        """
        Last item of the vector.

        Raises an exception if the vector is empty.

        >>> vec[3, 5, 2].last
        2
        >>> Vec().last
        *- TypeError: empty vector has no last -*
        """

        if not self:
            raise TypeError("empty vector has no last")

        return self[-1]

    def prepend(self, item: _T) -> None:
        """
        Add an item at the beginning of the vector.

        >>> l = vec[3, 5, 2]
        >>> l.prepend(-2)
        >>> print(l)
        [-2, 3, 5, 2]
        """

        self.insert(0, item)

    def reversed(self) -> _typing.Self:
        """
        Return a reversed version of the vector.

        >>> vec[1, 2, 3].reversed()
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
        Return a sorted version of the vector.

        >>> vec[3, 5, 2].sorted()
        [2, 3, 5]
        >>> Vec("gala").sorted(key=ord)
        ["a", "a", "g", "l"]
        """

        return self.__class__(sorted(self, key=key, reverse=reverse))  # type: ignore

    def shuffled(self) -> _typing.Self:
        """
        Return a shuffled version of the vector.

        >>> vec[3, 5, 2].shuffled()
        [5, 2, 3]
        >>> vec[3, 5, 2].shuffled()
        [2, 5, 3]
        >>> Vec().shuffled()
        []
        """

        result = self.__class__()

        while len(result) != len(self):
            item = _random.choice(self)

            if item not in result:
                result.append(item)

        return result

    def map(self, function: _collections_abc.Callable[[_T], _U]) -> Vec[_U]:
        """
        Apply `function` on each item of the vector.

        >>> vec[3, 5, 2].map(str)
        ["3", "5", "2"]
        >>> vec[3, 5, 2].map(lambda n: n * 2)
        [6, 10, 4]
        >>> Vec().map(lambda n: n * 20)
        []
        """

        # subclasses' `map` return type is also marked as `vec` because we
        # cannot make the container generic -- this requires Higher-Kinded
        # Types, which Python does not support (yet? hopefully!)

        return _typing.cast(Vec[_U], self.__class__(map(function, self)))

    def rotate(self, n: int = 1) -> _typing.Self:
        """
        Shift the vector `n` times to the right. The items that overflow get prepended.

        If `n` is negative, the shift goes to the left.

        >>> vec[3, 5, 2].rotate()
        [2, 3, 5]
        >>> vec[3, 5, 2].rotate(2)
        [5, 2, 3]
        >>> vec[3, 5, 2].rotate(-1)
        [5, 2, 3]
        >>> Vec().rotate()
        *- TypeError: empty vector cannot be rotated -*
        """

        if not self:
            raise TypeError("empty vector cannot be rotated")

        if n == 0:
            return self

        returned_vec = self.copy()

        if n > 0:
            xpend_method = returned_vec.prepend
            popped_index = -1
        else:
            xpend_method = returned_vec.append
            popped_index = 0

        for _ in range(abs(n)):
            xpend_method(returned_vec.pop(popped_index))

        return returned_vec

    def filter(
        self,
        function: _collections_abc.Callable[[_T], bool],
    ) -> _typing.Self:
        """
        Discard each item `i` of the vector if `function(i)` is `False`.

        >>> vec[3, 5, 2].filter(lambda n: n % 2 == 1)
        [3, 5]
        >>> vec["hello", "hola", "bonjour"].filter(lambda s: "l" in s)
        ["hello", "hola"]
        >>> Vec().filter(lambda n: n > 0)
        []
        """

        return self.__class__(filter(function, self))

    def mask(self, mask_seq: _collections_abc.Sequence[bool]) -> _typing.Self:
        """
        Keep every element at index `i` of the vector if the corresponding
        element at index `i` of the mask sequence is `True` ; else, discard
        it. Return the filtered vector.

        >>> vec[3, 5, 2].mask([True, False, True])
        [3, 2]
        >>> Vec().mask([])
        []
        >>> vec[3, 5, 2].mask([True, False])
        *- TypeError: mask length must be the same as the vector -*
        """

        if len(self) != len(mask_seq):
            raise TypeError("mask length must be the same as the vector")

        return self.__class__(item for item, bit in zip(self, mask_seq) if bit)

    def reduce(self, function: _collections_abc.Callable[[_T, _T], _T]) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from left to right and return the result.

        The first element of the vector is used as the leftmost value ;
        therefore, if the vector is empty, it will raise an exception.

        >>> vec[3, 5, 2].reduce(operator.add)  # (3 + 5) + 2
        10
        >>> Vec().reduce(operator.mul)
        *- TypeError: the vector to reduce cannot be empty -*
        """

        if not self:
            raise TypeError("the vector to reduce cannot be empty")

        return _functools.reduce(function, self)

    def reduce_right(
        self,
        function: _collections_abc.Callable[[_T, _T], _T],
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each element
        from right to left and return the result.

        The last element of the vector is used as the leftmost value ;
        therefore, if the vector is empty, it will raise an exception.

        >>> vec[3, 5, 2].reduce_right(operator.add)  # 3 + (5 + 2)
        10
        >>> vec[3, 5, 2].reduce_right(operator.sub)  # 3 - (5 - 2)
        0
        >>> Vec().reduce_right(operator.add)
        *- TypeError: the vector to reduce cannot be empty -*
        """

        if not self:
            raise TypeError("the vector to reduce cannot be empty")

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
        value if the vector is empty.

        >>> vec[3, 5, 2].fold(operator.add, -3)  # ((-3 + 3) + 5) + 2
        7
        >>> Vec().fold(operator.mul, 0)
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
        returned value if the vector is empty.

        >>> vec[3, 5, 2].fold_right(operator.sub, -3)  # -3 - (3 - (5 - 2))
        0
        >>> Vec().fold_right(operator.mul, 0)
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
        value of the returned vector if the original vector is empty.

        >>> vec[3, 5, 2].scan(operator.add, 0)  # [0, (0 + 3), (0 + 3 + 5), (0 + 3 + 5 + 2)]
        [0, 3, 8, 10]
        >>> Vec().scan(operator.add, 0)
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
        value of the returned vector if the original vector is empty.

        >>> vec[3, 5, 2].scan_right(operator.add, 0)  # [0, (2 + 0), (5 + 2 + 0), (3 + 5 + 2 + 0)]
        [0, 2, 7, 10]
        >>> Vec().scan_right(operator.add, 0)
        [0]
        """

        return self.reversed().scan(lambda a, b: function(b, a), initial_value)

    def merge(
        self,
        function: _collections_abc.Callable[[_T, _U], _V],
        other: _collections_abc.Sequence[_U],
    ) -> Vec[_V]:
        """
        Build a new vector from the result of each `function(s_i, o_i)` where
        `s_i` and `o_i` are the items at index `i` of `self` and `other`
        respectively.

        >>> vec[3, 5, 2].merge(operator.add, [-1, 4, -9])
        [2, 9, -7]
        >>> Vec().merge(operator.sub, [])
        []
        >>> vec[3, 5, 2].merge(operator.add, [6])
        *- TypeError: the length of the two sequences must be equal -*
        """

        if len(self) != len(other):
            raise TypeError("the length of the two sequences must be equal")

        return _typing.cast(
            Vec[_V],
            self.__class__(function(a, b) for a, b in zip(self, other)),
        )

    def sum(self) -> _T:
        """
        Return the sum of the vector. The elements must support addition,
        otherwise an exception is raised.

        >>> vec[3, 5, 2].sum()
        10
        >>> vec["hello", "world"].sum()
        "helloworld"
        >>> Vec().sum()
        *- TypeError: cannot perform summation on an empty vector -*
        """

        if not self:
            raise TypeError("cannot perform summation on an empty vector")

        return self.reduce(_operator.add)

    def mean(self: Vec[_NumberT]) -> _NumberT | float:
        """
        Return the mean of the vector. The elements must be numbers.

        >>> vec[3, 5, 2].mean()
        3.3333333333333335
        >>> vec["hello", "world"].mean()
        *- TypeError: cannot calculate mean of vector of str -*
        >>> Vec().mean()
        *- TypeError: cannot calculate mean of empty vector -*
        """

        if not self:
            raise TypeError("cannot calculate mean of empty vector")

        if not hasattr(self[0], "__truediv__"):
            raise TypeError(
                f"cannot calculate mean of vector of {self[0].__class__.__name__}",
            )

        return sum(self) / len(self)

    def filled(
        self,
        filler: _T | _collections_abc.Callable[[Vec[_T]], _T],
        n: int,
    ) -> _typing.Self:
        """
        Fill on the right the vector with `filler` and return the result.

        If `filler` is a function, it takes the current vector (at the current
        filling iteration) and produces a new value to be appended.

        >>> vec[3, 5, 2].filled(0, 5)
        [3, 5, 2, 0, 0, 0, 0, 0]
        >>> vec[3, 5, 2].filled(sum, 3)
        [3, 5, 2, 10, 20, 40]
        >>> Vec().filled(1, 10)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        >>> Vec([3, 5, 2]).filled(0, -1)
        *- ValueError: the number of times to fill cannot be negative -*
        """

        if n < 0:
            raise ValueError("the number of times to fill cannot be negative")

        returned_vec = self.copy()

        for _ in range(n):
            returned_vec.append(filler(returned_vec) if callable(filler) else filler)

        return returned_vec

    def fill(
        self,
        filler: _T | _collections_abc.Callable[[Vec[_T]], _T],
        n: int,
    ) -> None:
        """
        In-place equivalent of `filled`.

        >>> lst = vec[3, 5, 2]
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

        >>> vec[3, 5, 2].gap_fill(0)
        [3, 0, 5, 0, 2]
        >>> vec[3, 5, 2].gap_fill(operator.add)
        [3, 8, 5, 7, 2]
        >>> Vec().gap_fill(0)
        *- ValueError: empty vector has no gap to be filled -*
        """

        if not self:
            raise ValueError("empty vector has no gap to be filled")

        returned_vec = self.__class__([self.head])

        for i in range(1, len(self)):
            returned_vec.append(
                filler(self[i - 1], self[i]) if callable(filler) else filler,
            )
            returned_vec.append(self[i])

        return returned_vec

    def select(self, indexes: _collections_abc.Sequence[int]) -> _typing.Self:
        """
        Select items at provided indexes. If an index is present several
        times, this will be reflected in the resulting vector.

        >>> vec[3, 5, 2].select([1, 2, 0, 0])
        [5, 2, 3, 3]
        >>> Vec().select([])
        []
        >>> vec[3, 5, 2].select([4, 1])
        *- IndexError: index 4 is out of bounds -*
        """

        returned_vec = self.__class__()

        for index in indexes:
            if index >= len(self) or index < -len(self):
                raise IndexError(f"index {index} is out of bounds")

            returned_vec.append(self[index])

        return returned_vec

    def take(self, n: int) -> _typing.Self:
        """
        Take `n` items from the vector and return them.

        >>> vec[3, 5, 2].take(2)
        [3, 5]
        >>> vec[3, 5, 2].take(0)
        []
        >>> vec[3, 5, 2].take(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> vec[3, 5, 2].take(5)
        *- ValueError: cannot take more items than the vector contains -*
        """

        if n < 0:
            raise ValueError("cannot take a negative amount of items")

        if n > len(self):
            raise ValueError("cannot take more items than the vector contains")

        return self.__class__(self[i] for i in range(n))

    def take_right(self, n: int) -> _typing.Self:
        """
        Take `n` items from the right of the vector and return them.

        Vector original order is preserved.

        >>> vec[3, 5, 2].take_right(2)
        [5, 2]
        >>> vec[3, 5, 2].take_right(0)
        []
        >>> vec[3, 5, 2].take_right(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> vec[3, 5, 2].take_right(5)
        *- ValueError: cannot take more items than the vector contains -*
        """

        if n < 0:
            raise ValueError("cannot take a negative amount of items")

        if n > len(self):
            raise ValueError("cannot take more items than the vector contains")

        return self.__class__(item for item in self[len(self) - n :])

    def drop(self, n: int) -> _typing.Self:
        """
        Drop `n` items from the vector and return the rest.

        >>> vec[3, 5, 2].drop(2)
        [2]
        >>> vec[3, 5, 2].drop(0)
        [3, 5, 2]
        >>> vec[3, 5, 2].drop(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> vec[3, 5, 2].drop(5)
        *- ValueError: cannot drop more items than the vector contains -*
        """

        if n < 0:
            raise ValueError("cannot drop a negative amount of items")

        if n > len(self):
            raise ValueError("cannot drop more items than the vector contains")

        return self.__class__(self[n:])

    def drop_right(self, n: int) -> _typing.Self:
        """
        Drop `n` items from the right of the vector and return the rest.

        >>> vec[3, 5, 2].drop_right(2)
        [3]
        >>> vec[3, 5, 2].drop_right(0)
        [3, 5, 2]
        >>> vec[3, 5, 2].drop_right(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> vec[3, 5, 2].drop_right(5)
        *- ValueError: cannot drop more items than the vector contains -*
        """

        if n < 0:
            raise ValueError("cannot drop a negative amount of items")

        if n > len(self):
            raise ValueError("cannot drop more items than the vector contains")

        return self.__class__(self[: len(self) - n])

    def slice(self, start: int, stop: int) -> _typing.Self:
        """
        Slice the vector from `start` to `stop` and return the result.

        This method is NOT equivalent to the `self[start:stop]` notation.
        If `start` or `stop` are out of bounds of the vector or `start` is
        greater than `stop`, it will raise an exception.

        >>> vec[2, 4, 8, 16, 32].slice(1, 3)
        [4, 8, 16]
        >>> vec[2, 4, 8, 16, 32].slice(0, 2)
        [2, 4, 8]
        >>> vec[2, 4, 8, 16, 32].slice(3, 5)
        [8, 16, 32]
        >>> vec[2, 4, 8, 16, 32].slice(2, 2)
        [8]
        >>> vec[2, 4, 8, 16, 32].slice(1, 10)
        *- ValueError: slice out of bounds -*
        >>> vec[2, 4, 8, 16, 32].slice(4, 2)
        *- ValueError: start cannot be greater than stop -*

        Tip: if `start` is 0, you can do `.take(stop - 1)` instead.
        Symmetrically, if `stop` is the index of the last item, go for a
        `.drop(start)`!
        """

        if start > stop:
            raise ValueError("start cannot be greater than stop")

        if start < 0 or stop >= len(self):
            raise ValueError("slice out of bounds")

        return self.__class__(self[start : stop + 1])

    def cut(self, n: int) -> tuple[_typing.Self, _typing.Self]:
        """
        Cut the vector after `n` elements and return a pair of the produced
        vectors.

        >>> vec[2, 4, 8, 16, 32].cut(2)
        ([2, 4], [8, 16, 32])
        >>> vec[2, 4, 8, 16, 32].cut(0)
        ([], [2, 4, 8, 16, 32])
        >>> vec[2, 4, 8, 16, 32].cut(8)
        ([2, 4, 8, 16, 32], [])
        >>> vec[2, 4, 8, 16, 32].cut(-3)
        *- ValueError: cannot cut after a negative amount of elements -*
        >>> Vec().cut(2)
        *- TypeError: cannot cut an empty vector -*
        """

        if not self:
            raise TypeError("cannot cut an empty vector")

        if n < 0:
            raise ValueError("cannot cut after a negative amount of elements")

        _n = min(n, len(self))

        return self.take(_n), self.drop(_n)


class dict(_collections.UserDict[_K, _V]):
    ...


class str(_collections.UserString):
    ...


class _VecBuilder:
    def __getitem__(self, key: _T | slice | tuple[_T, ...], /) -> Vec[_T] | Vec[int]:
        if isinstance(key, slice):
            if _is_range_slice(key):
                return Vec(range(key.start or 0, key.stop, key.step or 1))

        return Vec(_typing.cast(tuple[_T], key if isinstance(key, tuple) else (key,)))


def _is_range_slice(value: _typing.Any, /) -> _typing.TypeGuard[slice]:
    return (
        isinstance(value, slice)
        and isinstance(value.stop, int)
        and all(isinstance(v, int | None) for v in (value.start, value.step))
    )


_VecLiteral = _typing.NewType("[Vector Literal]", _VecBuilder)
vec = _VecLiteral(_VecBuilder())
"""
Literal-like for magic vectors.
"""
