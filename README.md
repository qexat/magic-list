<!-- markdownlint-disable MD028 -->

# Magic Collections

Magic Collections is a set of the built-in collections equipped with a bunch of additional methods.

> [!WARNING]
> This library is still **in active development**.

> [!NOTE]
> Its development is entirely test-driven: it is battery-tested and requires a
> test coverage of 100%. It also provides typing stub files.

User-friendly documentation is hopefully coming soon.

## Examples

### Fibonacci sequence

In the functional programming spirit, let's write a function that given an integer `n`, returns the fibonacci sequence up to the `n`-th member.

For example, `fibonacci_sequence(10)` would return `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]`.

```py
import operator

from magic_collections import L, list

def fibonacci_sequence(n: int) -> list[int]:
    # let's start by creating a list with the first two members, 0 and 1.
    base = L[0, 1]

    # we define a function that we will use to generate the next members of
    # the sequence
    def next_member(current: list[int]) -> int:
        return current.take_right(2).sum()

    return base.filled(next_member, n - 1)
```

> [!NOTE]\
> The `L[0, 1]` notation is a way to construct magic lists nicely.

> [!IMPORTANT]\
> `list` is from `magic_collections` as a drop-in replacement of the built-in!

### Fibonacci n-th member

Wanted to define a function that returns the `n`-th member of the Fibonacci sequence for a laugh? We have that: it is called [`fibonacci_sequence(n)`](#fibonacci-sequence)`.last`!

### Need fruits

You're a small fruit merchant aiming to manage your inventory using a computer. Using a dictionary that pairs fruit names with their respective quantities, your goal is to identify which fruits are running low so you can restock them. However, there's no need to fret about oranges and mangoes, as their season has concluded, and you won't be able to find them anymore.

```py
from magic_collections import dict, L, list

SEASON_OVER = L["oranges", "mangoes"]

def get_fruits_with_empty_basket(stock: dict[str, int]) -> list[str]:
    return list(
        # only keep what's needed to be bought!
        stock.filter_values(lambda n: n == 0)
        # remove oranges and mangoes cause season is over...
        .filter_keys(lambda fruit: fruit not in SEASON_OVER)
        # we only want fruit names now
        .keys()
    )

```
