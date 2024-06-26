from __future__ import annotations

import collections
import collections.abc
import functools
import operator
import random
import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    import _typeshed
    import typing_extensions

__all__ = [
    "list",
    "L",
]

_T = typing.TypeVar("_T")
_U = typing.TypeVar("_U")
_V = typing.TypeVar("_V")


class list(collections.UserList[_T]):  # noqa: A001, N801
    """
    Mutable homogeneous sequence.
    Drop-in replacement for the built-in `list` type.
    """

    @property
    def head(self) -> _T:
        """
        First item of the list.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].head
        3
        >>> list().head
        *- TypeError: empty list has no head -*
        """

        if not self:
            msg = "empty list has no head"
            raise TypeError(msg)

        return self[0]

    @property
    def tail(self) -> typing_extensions.Self:
        """
        List without its first item.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].tail
        [5, 2]
        >>> list().tail
        *- TypeError: empty list has no tail -*
        """

        if not self:
            msg = "empty list has no tail"
            raise TypeError(msg)

        return self.__class__(self[1:])

    @property
    def init(self) -> typing_extensions.Self:
        """
        List without its last item.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].init
        [3, 5]
        >>> list().init
        *- TypeError: empty list has no init -*
        """

        if not self:
            msg = "empty list has no init"
            raise TypeError(msg)

        return self.__class__(self[:-1])

    @property
    def last(self) -> _T:
        """
        Last item of the list.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].last
        2
        >>> list().last
        *- TypeError: empty list has no last -*
        """

        if not self:
            msg = "empty list has no last"
            raise TypeError(msg)

        return self[-1]

    def prepend(self, item: _T) -> None:
        """
        Add an item at the beginning of the list.

        >>> l = L[3, 5, 2]
        >>> l.prepend(-2)
        >>> print(l)
        [-2, 3, 5, 2]
        """

        self.insert(0, item)

    def reversed(self) -> typing_extensions.Self:
        """
        Return a reversed version of the list.

        >>> L[1, 2, 3].reversed()
        [3, 2, 1]
        """

        # we avoid constructing a whole `reversed` object
        return self.__class__(self.__reversed__())

    def sorted(
        self,
        *,
        key: collections.abc.Callable[[_T], _typeshed.SupportsRichComparison]
        | None = None,
        reverse: bool = False,
    ) -> typing_extensions.Self:
        """
        Return a sorted version of the list.

        >>> L[3, 5, 2].sorted()
        [2, 3, 5]
        >>> list("gala").sorted(key=ord)
        ["a", "a", "g", "l"]
        """

        return self.__class__(sorted(self, key=key, reverse=reverse))  # pyright: ignore[reportCallIssue, reportArgumentType]

    def shuffled(self) -> typing_extensions.Self:
        """
        Return a shuffled version of the list.

        >>> L[3, 5, 2].shuffled()
        [5, 2, 3]
        >>> L[3, 5, 2].shuffled()
        [2, 5, 3]
        >>> list().shuffled()
        []
        """

        result = self.copy()
        random.shuffle(result)

        return result

    def map(self, function: collections.abc.Callable[[_T], _U]) -> list[_U]:
        """
        Apply `function` on each item of the list.

        >>> L[3, 5, 2].map(str)
        ["3", "5", "2"]
        >>> L[3, 5, 2].map(lambda n: n * 2)
        [6, 10, 4]
        >>> list().map(lambda n: n * 20)
        []
        """

        # subclasses' `map` return type is also marked as `list` because we
        # cannot make the container generic -- this requires Higher-Kinded
        # Types, which Python does not support (yet? hopefully!)

        return typing.cast(list[_U], self.__class__(map(function, self)))

    def rotate(self, n: int = 1) -> typing_extensions.Self:
        """
        Shift the list `n` times to the right. The items that overflow get prepended.

        If `n` is negative, the shift goes to the left.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].rotate()
        [2, 3, 5]
        >>> L[3, 5, 2].rotate(2)
        [5, 2, 3]
        >>> L[3, 5, 2].rotate(-1)
        [5, 2, 3]
        >>> list().rotate()
        *- TypeError: empty list cannot be rotated -*
        """

        if not self:
            msg = "empty list cannot be rotated"
            raise TypeError(msg)

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
        function: collections.abc.Callable[[_T], bool],
    ) -> typing_extensions.Self:
        """
        Discard each item `i` of the list if `function(i)` is `False`.

        >>> L[3, 5, 2].filter(lambda n: n % 2 == 1)
        [3, 5]
        >>> L["hello", "hola", "bonjour"].filter(lambda s: "l" in s)
        ["hello", "hola"]
        >>> list().filter(lambda n: n > 0)
        []
        """

        return self.__class__(filter(function, self))

    def mask(
        self,
        mask_seq: collections.abc.Sequence[bool],
    ) -> typing_extensions.Self:
        """
        Keep every item at index `i` of the list if the corresponding
        item at index `i` of the mask sequence is `True` ; else, discard
        it. Return the filtered list.

        .. warning:: The mask sequence must be of the same length as the list.

        >>> L[3, 5, 2].mask([True, False, True])
        [3, 2]
        >>> list().mask([])
        []
        >>> L[3, 5, 2].mask([True, False])
        *- TypeError: mask length must be the same as the list -*
        """

        if len(self) != len(mask_seq):
            msg = "mask length must be the same as the list"
            raise TypeError(msg)

        return self.__class__(item for item, bit in zip(self, mask_seq) if bit)

    def deduplicate(self) -> typing_extensions.Self:
        """
        Remove duplicate elements from left to right (and keep original ones).
        Return the deduplicated list.

        >>> L[3, 0, 0, 1, 18].deduplicate()
        [3, 0, 1, 18]
        >>> L["hello", "hello", "world", "world"].deduplicate()
        ["hello", "world"]
        >>> list().deduplicate()
        []
        """

        returned_list: typing_extensions.Self = self.__class__()

        for elem in self:
            if elem not in returned_list:
                returned_list.append(elem)

        return returned_list

    def reduce(self, function: collections.abc.Callable[[_T, _T], _T]) -> _T:
        """
        "Insert" an operator (called a reducing function) between each item
        from left to right and return the result.

        The first item of the list is used as the leftmost value ;
        therefore, if the list is empty, it will raise an exception.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].reduce(operator.add)  # (3 + 5) + 2
        10
        >>> list().reduce(operator.mul)
        *- TypeError: the list to reduce cannot be empty -*
        """

        if not self:
            msg = "the list to reduce cannot be empty"
            raise TypeError(msg)

        return functools.reduce(function, self)

    def reduce_right(
        self,
        function: collections.abc.Callable[[_T, _T], _T],
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each item
        from right to left and return the result.

        The last item of the list is used as the leftmost value ;
        therefore, if the list is empty, it will raise an exception.

        .. warning:: The list must be non-empty.

        >>> L[3, 5, 2].reduce_right(operator.add)  # 3 + (5 + 2)
        10
        >>> L[3, 5, 2].reduce_right(operator.sub)  # 3 - (5 - 2)
        0
        >>> list().reduce_right(operator.add)
        *- TypeError: the list to reduce cannot be empty -*
        """

        if not self:
            msg = "the list to reduce cannot be empty"
            raise TypeError(msg)

        return functools.reduce(lambda a, b: function(b, a), self.reversed())

    def fold(
        self,
        function: collections.abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each item
        from left to right and return the result.

        The `initial_value` is used as the leftmost value, and is the returned
        value if the list is empty.

        >>> L[3, 5, 2].fold(operator.add, -3)  # ((-3 + 3) + 5) + 2
        7
        >>> list().fold(operator.mul, 0)
        0
        """

        return functools.reduce(function, self, initial_value)

    def fold_right(
        self,
        function: collections.abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> _T:
        """
        "Insert" an operator (called a reducing function) between each item
        from right to left and return the result.

        The `initial_value` is used as the leftmost value, and is the
        returned value if the list is empty.

        >>> L[3, 5, 2].fold_right(operator.sub, -3)  # -3 - (3 - (5 - 2))
        0
        >>> list().fold_right(operator.mul, 0)
        0
        """

        return functools.reduce(
            lambda a, b: function(b, a),
            self.reversed(),
            initial_value,
        )

    def scan(
        self,
        function: collections.abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> typing_extensions.Self:
        """
        "Insert" an operator (called a reducing function) between each item
        from left to right and return the intermediate values followed by the
        result.

        The `initial_value` is used as the leftmost value, and is the only
        value of the returned list if the original list is empty.

        >>> # [0, (0 + 3), (0 + 3 + 5), (0 + 3 + 5 + 2)]
        >>> L[3, 5, 2].scan(operator.add, 0)
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
        function: collections.abc.Callable[[_T, _T], _T],
        initial_value: _T,
    ) -> typing_extensions.Self:
        """
        "Insert" an operator (called a reducing function) between each item
        from right to left and return the intermediate values followed by the
        result.

        The `initial_value` is used as the leftmost value, and is the only
        value of the returned list if the original list is empty.

        >>> # [0, (2 + 0), (5 + 2 + 0), (3 + 5 + 2 + 0)]
        >>> L[3, 5, 2].scan_right(operator.add, 0)
        [0, 2, 7, 10]
        >>> list().scan_right(operator.add, 0)
        [0]
        """

        return self.reversed().scan(lambda a, b: function(b, a), initial_value)

    def merge(
        self,
        function: collections.abc.Callable[[_T, _U], _V],
        other: collections.abc.Sequence[_U],
    ) -> list[_V]:
        """
        Build a new list from the result of each `function(s_i, o_i)` where
        `s_i` and `o_i` are the items at index `i` of `self` and `other`
        respectively.

        .. warning:: The list and the sequence must have the same length.

        >>> L[3, 5, 2].merge(operator.add, [-1, 4, -9])
        [2, 9, -7]
        >>> list().merge(operator.sub, [])
        []
        >>> L[3, 5, 2].merge(operator.add, [6])
        *- TypeError: the length of the two sequences must be equal -*
        """

        if len(self) != len(other):
            msg = "the length of the two sequences must be equal"
            raise TypeError(msg)

        return typing.cast(
            list[_V],
            self.__class__(function(a, b) for a, b in zip(self, other)),
        )

    def flatten(self, *, _base: list[typing.Any] | None = None) -> list[typing.Any]:
        """
        Flatten the contents to a 1-dimension list. If the list contains
        itself, it cannot be flattened and a `ValueError` is raised.

        .. warning:: The list cannot contain recursive elements.

        >>> L[[3, 5, 2], [8, 4, 1], [7, 6, 9]].flatten()
        [3, 5, 2, 8, 4, 1, 7, 6, 9]
        >>> list().flatten()
        []
        >>> l = list()
        >>> l.append(l)
        >>> l.flatten()
        *- ValueError: cannot flatten list because it contains recursive elements -*
        """

        err = ValueError("cannot flatten list because it contains recursive elements")

        result: list[typing.Any] = list()

        for item in self:
            if item is self or item is _base:
                raise err

            base = self if _base is None else _base

            if isinstance(item, list):
                result.extend(item.flatten(_base=base))
            elif isinstance(item, collections.abc.Iterable):
                try:
                    result.extend(
                        list(
                            typing.cast(collections.abc.Iterable[typing.Any], item),
                        ).flatten(_base=base),
                    )
                except RecursionError:
                    # a bit dirty but I can't think of any other solution 😅
                    raise err from None
            else:
                result.append(item)

        return result

    def sum(self) -> _T:
        """
        Return the sum of the list. The elements must support addition,
        otherwise an exception is raised.

        .. warning:: The list must contain values that support the `+` \
            operator, and be non-empty.

        >>> L[3, 5, 2].sum()
        10
        >>> L["hello", "world"].sum()
        "helloworld"
        >>> list().sum()
        *- TypeError: cannot perform summation on an empty list -*
        """

        if not self:
            msg = "cannot perform summation on an empty list"
            raise TypeError(msg)

        return self.reduce(operator.add)

    def mean(self: list[int] | list[float] | list[complex]) -> float | complex:
        """
        Return the mean of the list. The elements must be numbers.

        .. warning:: The list must contain numbers and be non-empty.

        >>> L[3, 5, 2].mean()
        3.3333333333333335
        >>> L["hello", "world"].mean()
        *- TypeError: cannot calculate mean of list of str -*
        >>> list().mean()
        *- TypeError: cannot calculate mean of empty list -*
        """

        if not self:
            msg = "cannot calculate mean of empty list"
            raise TypeError(msg)

        if not hasattr(self[0], "__truediv__"):
            msg = f"cannot calculate mean of list of {self[0].__class__.__name__}"
            raise TypeError(
                msg,
            )

        return sum(self) / len(self)

    def min(self: list[int] | list[float]) -> int | float:
        """
        Return the minimum value of the list.

        .. warning:: The list must be non-empty and contain numbers.

        >>> L[3, 5, 2].min()
        2
        >>> L["hello", "world"].min()
        *- TypeError: list of str has no minimum -*
        >>> list().min()
        *- TypeError: empty list has no minimum -*
        """

        if not self:
            msg = "empty list has no minimum"
            raise TypeError(msg)

        if not isinstance(self.head, (int, float)):  # pyright: ignore[reportUnnecessaryIsInstance]
            msg = f"list of {type(self.head).__name__} has no minimum"
            raise TypeError(msg)

        return min(self)

    def max(self: list[int] | list[float]) -> int | float:
        """
        Return the maximum value of the list.

        .. warning:: The list must be non-empty and contain numbers.

        >>> L[3, 5, 2].max()
        2
        >>> L["hello", "world"].max()
        *- TypeError: list of str has no maximum -*
        >>> list().max()
        *- TypeError: empty list has no maximum -*
        """

        if not self:
            msg = "empty list has no maximum"
            raise TypeError(msg)

        if not isinstance(self.head, (int, float)):  # pyright: ignore[reportUnnecessaryIsInstance]
            msg = f"list of {type(self.head).__name__} has no maximum"
            raise TypeError(msg)

        return max(self)

    def fill_left(
        self,
        filler: _T | collections.abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self:
        """
        Fill on the left the list with `filler` and return the result.

        If `filler` is a function, it takes the current list (at the current
        filling iteration) and produces a new value to be appended.

        .. warning:: `n` must be non-negative.

        >>> L[3, 5, 2].fill_left(0, 5)
        [0, 0, 0, 0, 0, 3, 5, 2]
        >>> L[3, 5, 2].fill_left(sum, 3)
        [40, 20, 10, 3, 5, 2]
        >>> list().fill_left(1, 10)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        >>> L[3, 5, 2].fill_left(0, -1)
        *- ValueError: the number of times to fill cannot be negative -*
        """

        if n < 0:
            msg = "the number of times to fill cannot be negative"
            raise ValueError(msg)

        returned_list = self.copy()

        for _ in range(n):
            returned_list.prepend(filler(returned_list) if callable(filler) else filler)

        return returned_list

    def fill_right(
        self,
        filler: _T | collections.abc.Callable[[list[_T]], _T],
        n: int,
    ) -> typing_extensions.Self:
        """
        Fill on the right the list with `filler` and return the result.

        If `filler` is a function, it takes the current list (at the current
        filling iteration) and produces a new value to be appended.

        .. warning:: `n` must be non-negative.

        >>> L[3, 5, 2].fill_right(0, 5)
        [3, 5, 2, 0, 0, 0, 0, 0]
        >>> L[3, 5, 2].fill_right(sum, 3)
        [3, 5, 2, 10, 20, 40]
        >>> list().fill_right(1, 10)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        >>> L[3, 5, 2].fill_right(0, -1)
        *- ValueError: the number of times to fill cannot be negative -*
        """

        if n < 0:
            msg = "the number of times to fill cannot be negative"
            raise ValueError(msg)

        returned_list = self.copy()

        for _ in range(n):
            returned_list.append(filler(returned_list) if callable(filler) else filler)

        return returned_list

    def interleave(
        self,
        filler: _T | collections.abc.Callable[[_T, _T], _T],
    ) -> typing_extensions.Self:
        """
        Fill in-between the items with `filler` and return the result.

        If `filler` is a function, it takes the two items surrounding the gap
        that is about to be filled and produces a new value to be inserted.

        .. warning:: The list must contain at least two items.

        >>> L[3, 5, 2].interleave(0)
        [3, 0, 5, 0, 2]
        >>> L[3, 5, 2].interleave(operator.add)
        [3, 8, 5, 7, 2]
        >>> L[0].interleave(1)
        *- ValueError: list has no gap to be filled -*
        >>> list().interleave(0)
        *- ValueError: list has no gap to be filled -*
        """

        if len(self) <= 1:
            msg = "list has no gap to be filled"
            raise ValueError(msg)

        returned_list = self.__class__([self.head])

        for i in range(1, len(self)):
            returned_list.append(
                filler(self[i - 1], self[i]) if callable(filler) else filler,
            )
            returned_list.append(self[i])

        return returned_list

    gap_fill = interleave
    """
    .. warning:: This alias is deprecated.

    Alias of `interleave`.
    """

    def select(
        self,
        indexes: collections.abc.Sequence[int],
    ) -> typing_extensions.Self:
        """
        Select items at provided indexes. If an index is present several
        times, this will be reflected in the resulting list.

        .. warning:: All the indexes must be in bounds.

        >>> L[3, 5, 2].select([1, 2, 0, 0])
        [5, 2, 3, 3]
        >>> list().select([])
        []
        >>> L[3, 5, 2].select([4, 1])
        *- IndexError: index 4 is out of bounds -*
        """

        returned_list = self.__class__()

        for index in indexes:
            if index >= len(self) or index < -len(self):
                msg = f"index {index} is out of bounds"
                raise IndexError(msg)

            returned_list.append(self[index])

        return returned_list

    def take(self, n: int) -> typing_extensions.Self:
        """
        Take `n` items from the list and return them.

        .. warning:: `n` must be non-negative and less than the list length.

        >>> L[3, 5, 2].take(2)
        [3, 5]
        >>> L[3, 5, 2].take(0)
        []
        >>> L[3, 5, 2].take(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> L[3, 5, 2].take(5)
        *- ValueError: cannot take more items than the list contains -*
        """

        if n < 0:
            msg = "cannot take a negative amount of items"
            raise ValueError(msg)

        if n > len(self):
            msg = "cannot take more items than the list contains"
            raise ValueError(msg)

        return self.__class__(self[i] for i in range(n))

    def take_right(self, n: int) -> typing_extensions.Self:
        """
        Take `n` items from the right of the list and return them.

        List original order is preserved.

        .. warning:: `n` must be non-negative and less than the list length.

        >>> L[3, 5, 2].take_right(2)
        [5, 2]
        >>> L[3, 5, 2].take_right(0)
        []
        >>> L[3, 5, 2].take_right(-1)
        *- ValueError: cannot take a negative amount of items -*
        >>> L[3, 5, 2].take_right(5)
        *- ValueError: cannot take more items than the list contains -*
        """

        if n < 0:
            msg = "cannot take a negative amount of items"
            raise ValueError(msg)

        if n > len(self):
            msg = "cannot take more items than the list contains"
            raise ValueError(msg)

        return self.__class__(item for item in self[len(self) - n :])

    def drop(self, n: int) -> typing_extensions.Self:
        """
        Drop `n` items from the list and return the rest.

        .. warning:: `n` must be non-negative and less than the list length.

        >>> L[3, 5, 2].drop(2)
        [2]
        >>> L[3, 5, 2].drop(0)
        [3, 5, 2]
        >>> L[3, 5, 2].drop(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> L[3, 5, 2].drop(5)
        *- ValueError: cannot drop more items than the list contains -*
        """

        if n < 0:
            msg = "cannot drop a negative amount of items"
            raise ValueError(msg)

        if n > len(self):
            msg = "cannot drop more items than the list contains"
            raise ValueError(msg)

        return self.__class__(self[n:])

    def drop_right(self, n: int) -> typing_extensions.Self:
        """
        Drop `n` items from the right of the list and return the rest.

        .. warning:: `n` must be non-negative and less than the list length.

        >>> L[3, 5, 2].drop_right(2)
        [3]
        >>> L[3, 5, 2].drop_right(0)
        [3, 5, 2]
        >>> L[3, 5, 2].drop_right(-1)
        *- ValueError: cannot drop a negative amount of items -*
        >>> L[3, 5, 2].drop_right(5)
        *- ValueError: cannot drop more items than the list contains -*
        """

        if n < 0:
            msg = "cannot drop a negative amount of items"
            raise ValueError(msg)

        if n > len(self):
            msg = "cannot drop more items than the list contains"
            raise ValueError(msg)

        return self.__class__(self[: len(self) - n])

    def slice(self, start: int, stop: int) -> typing_extensions.Self:
        """
        Slice the list from `start` to `stop` and return the result.

        This method is NOT equivalent to the `self[start:stop]` notation.
        If `start` or `stop` are out of bounds of the list or `start` is
        greater than `stop`, it will raise an exception.

        .. warning:: `start` and `stop` must be in bounds.

        >>> L[2, 4, 8, 16, 32].slice(1, 3)
        [4, 8, 16]
        >>> L[2, 4, 8, 16, 32].slice(0, 2)
        [2, 4, 8]
        >>> L[2, 4, 8, 16, 32].slice(3, 5)
        [8, 16, 32]
        >>> L[2, 4, 8, 16, 32].slice(2, 2)
        [8]
        >>> L[2, 4, 8, 16, 32].slice(1, 10)
        *- ValueError: slice out of bounds -*
        >>> L[2, 4, 8, 16, 32].slice(4, 2)
        *- ValueError: start cannot be greater than stop -*

        Tip: if `start` is 0, you can do `.take(stop - 1)` instead.
        Symmetrically, if `stop` is the index of the last item, go for a
        `.drop(start)`!
        """

        if start > stop:
            msg = "start cannot be greater than stop"
            raise ValueError(msg)

        if start < 0 or stop >= len(self):
            msg = "slice out of bounds"
            raise ValueError(msg)

        return self.__class__(self[start : stop + 1])

    def partition(
        self,
        index: int,
    ) -> tuple[typing_extensions.Self, _T, typing_extensions.Self]:
        """
        Return the item at index `index`, but also the two list slices
        before and after that item, in this order: (left, item, right).

        .. warning:: The list must be non-empty, and the partition index in bounds.

        >>> L[2, 4, 8, 16, 32].partition(2)
        ([2, 4], 8, [16, 32])
        >>> L[2, 4, 8, 16, 32].partition(0)
        ([], 2, [4, 8, 16, 32])
        >>> L[2, 4, 8, 16, 32].partition(4)
        ([2, 4, 8, 16], 32, [])
        >>> L[2, 4, 8, 16, 32].partition(-2)
        *- IndexError: partition index cannot be out of bounds -*
        >>> list().partition(2)
        *- TypeError: cannot partition an empty list -*
        """

        if not self:
            msg = "cannot partition an empty list"
            raise TypeError(msg)

        if not (0 <= index < len(self)):
            msg = "partition index cannot be out of bounds"
            raise IndexError(msg)

        return self.take(index), self[index], self.drop(index + 1)

    def bisect(
        self,
        index: int,
    ) -> tuple[typing_extensions.Self, typing_extensions.Self]:
        """
        Bisect the list after `index` elements and return a pair of the produced
        lists.

        .. warning:: The list must be non-empty.

        >>> L[2, 4, 8, 16, 32].bisect(2)
        ([2, 4], [8, 16, 32])
        >>> L[2, 4, 8, 16, 32].bisect(0)
        ([], [2, 4, 8, 16, 32])
        >>> L[2, 4, 8, 16, 32].bisect(8)
        ([2, 4, 8, 16, 32], [])
        >>> L[2, 4, 8, 16, 32].bisect(-3)
        ([], [2, 4, 8, 16, 32])
        >>> list().bisect(2)
        *- TypeError: cannot bisect an empty list -*
        """

        if not self:
            msg = "cannot bisect an empty list"
            raise TypeError(msg)

        _n = _minmax(index, 0, len(self))

        return self.take(_n), self.drop(_n)

    def trisect(
        self,
        first_index: int,
        second_index: int,
    ) -> tuple[
        typing_extensions.Self,
        typing_extensions.Self,
        typing_extensions.Self,
    ]:
        """
        Trisect the list at `first_index` and `second_index` and return a
        triple of the produced lists.

        The left and right cutting indexes are determined by the smallest and
        largest value of the two arguments respectively ; `first_index` is not
        required to be smaller.

        .. warning:: The list must be non-empty.
        """

        if not self:
            msg = "cannot trisect an empty list"
            raise TypeError(msg)

        _left = _minmax(min(first_index, second_index), 0, len(self))
        _right = _minmax(max(first_index, second_index), 0, len(self))

        return self.take(_left), self[_left:_right], self.drop(_right)


class _ListBuilder:
    def __getitem__(self, key: _T | slice | tuple[_T, ...], /) -> list[_T] | list[int]:
        if isinstance(key, slice) and _is_range_slice(key):
            return list(range(key.start or 0, key.stop, key.step or 1))

        return list(typing.cast(tuple[_T], key if isinstance(key, tuple) else (key,)))


def _is_range_slice(value: typing.Any, /) -> bool:
    return (
        isinstance(value, slice)
        and isinstance(value.stop, int)
        and all(isinstance(v, (int, type(None))) for v in (value.start, value.step))
    )


def _minmax(value: int, left: int, right: int) -> int:
    return max(left, min(value, right))


MagicListLiteral = typing.NewType(
    "MagicListLiteral",
    _ListBuilder,
)

L = MagicListLiteral(_ListBuilder())
"""Literal-like for magic lists."""
