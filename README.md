<!-- markdownlint-disable MD028 -->

# Magic List

![Logo](./docs/magic_list_banner.png)

[![Palestine support banner](https://raw.githubusercontent.com/Safouene1/support-palestine-banner/master/banner-support.svg)](https://irusa.org/middle-east/palestine/)

[![PyPI badge](https://img.shields.io/pypi/v/magic-list)](<https://pypi.org/project/magic-list/>)
[![Downloads](https://static.pepy.tech/badge/magic-list)](https://pepy.tech/project/magic-list)
[![Tests](https://github.com/qexat/magic-list/actions/workflows/tests.yml/badge.svg)](https://github.com/qexat/magic-list/actions)
[![Ruff](https://github.com/qexat/magic-list/actions/workflows/ruff.yml/badge.svg)](https://github.com/qexat/magic-list/actions)
[![Typechecking](https://github.com/qexat/magic-list/actions/workflows/typechecking.yml/badge.svg)](https://github.com/qexat/magic-list/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

Magic List is a module that extends the built-in list type.

[Documentation](https://qexat.github.io/magic-list/) · [PyPI package](https://pypi.org/project/magic-list/) · [How to install](#installation) · [Notes for contributors and maintainers](./README-dev.md)

> [!NOTE]
> Its development is entirely test-driven: it is battery-tested and requires a
> test coverage of 100%. It also provides type stubs.

## Installation

```sh
pip install magic-list
```

## Examples

### Fibonacci sequence

Let's write a function that given an integer `n`, returns the fibonacci sequence up to the `n`-th member.

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

> [!NOTE]
> The `L[0, 1]` notation is a way to construct magic lists nicely.

## Contributing

First of all, thank you for taking your time to participate in this project! 💕

You might want to check those:

- [Code of Conduct](./CODE_OF_CONDUCT.md) · a document to set standards for respectful and inclusive behavior within the community
- [README-dev.md](./README-dev.md) · documentation to help you familiarize with Magic List's workflow
- [Feature proposals](https://github.com/qexat/magic-list/issues/50) · a list of the proposed features in the past, present and future
