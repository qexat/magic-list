<!-- markdownlint-disable MD028, MD033 -->

# Magic List

[![Palestine support banner](https://raw.githubusercontent.com/Safouene1/support-palestine-banner/master/banner-support.svg)](https://irusa.org/middle-east/palestine/)

[![PyPI badge](https://img.shields.io/pypi/v/magic-list)](<https://pypi.org/project/magic-list/>)
[![Downloads](https://static.pepy.tech/badge/magic-list)](https://pepy.tech/project/magic-list)
[![Tests](https://github.com/qexat/magic-list/actions/workflows/tests.yml/badge.svg)](https://github.com/qexat/magic-list/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

Magic List is a module that extends the built-in list type.

> [!NOTE]
> Its development is entirely test-driven: it is battery-tested and requires a
> test coverage of 100%. It also provides typing stub files.

## Documentation

Documentation can be found [here](https://qexat.github.io/magic-list/).

## Installation

### Pip

```sh
pip install magic-list
```

<details>
<summary>Package managers</summary>

### Conda

```sh
conda install magic-list
```

### Pipenv

```sh
pipenv install magic-list
```

### pipx

```sh
pipx install magic-list
```

### Poetry

```sh
poetry add magic-list
```

### uv

```sh
uv pip install magic-list
```

</details>

## Examples

### Fibonacci sequence

In the functional programming spirit, let's write a function that given an integer `n`, returns the fibonacci sequence up to the `n`-th member.

For example, `fibonacci_sequence(10)` would return `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]`.

```py
import operator

from magic_list import L, list

def fibonacci_sequence(n: int) -> list[int]:
    # let's start by creating a list with the first two members, 0 and 1.
    base = L[0, 1]

    # we define a function that we will use to generate the next members of
    # the sequence
    def next_member(current: list[int]) -> int:
        return current.take_right(2).sum()

    return base.fill_right(next_member, n - 1)
```

> [!NOTE]\
> The `L[0, 1]` notation is a way to construct magic lists nicely.
