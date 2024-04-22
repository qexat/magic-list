<!-- markdownlint-disable MD033 -->

# Notes to developers

Links: [Building docs](#building-docs) · [Testing](#testing) · [Bumping the version](#bumping-the-version) · [Building the wheel](#building) · [Releasing on PyPI](#releasing)

## Setting up the environment

Most commands in this document require dependencies. It is best to work on a
virtual environment to avoid interferences with your system-level Python
installation.

### Virtual environment

> **Qexat:** I advise to have [`virtualenv`](https://virtualenv.pypa.io/en/latest/) installed globally on your machine.

For everything except documentation, I recommend **using the lowest Python
version that Magic List supports**, i.e. 3.9 at the time of writing.

```sh
virtualenv .venv -ppython39
source .venv/bin/activate.fish  # remove `.fish` if you use bash
```

Since documentation uses the type stubs, which is written with the new syntax
features of more recent versions of Python, they should be built with the
latest one.

```sh
virtualenv .venv-docs -ppython312
source .venv-docs/bin/activate.fish  # remove `.fish` if you use bash
```

### Local editable installation

Since you intend to work on Magic List, you will use the editable installation
(`-e`) feature of `pip`.
You will also need the development dependencies (`[dev]`).

```sh
pip install -e .[dev]
```

---

## Contributing

<sup>Dependencies: `pre-commit`, `pyright`, `ruff`</sup>

First of all, thank you for your contribution 💞

- Types are checked against the [Pyright](https://github.com/microsoft/pyright) static type checker.
- Linting and formatting are handled by [Ruff](https://github.com/astral-sh/ruff).
- Few other checks are performed as well using [pre-commit](https://pre-commit.com).

In order to provide some guarantees on code quality, they will be enforced on your pull requests.
They are not meant to dissuade people from contributing, but **to prevent common bugs and mistakes**,
as well as to fulfill the common guidelines of Python.

## Building docs

<sup>Dependencies: `pdoc`</sup>

Documentation is automatically built on every pull request, and deployed at
every commit on the `main` branch. The command is provided in case you need to
run them manually and/or locally.

```sh
pdoc magic_list/ -n -d numpy -o docs/
```

## Testing

<sup>Dependencies: `pytest`, `coverage`</sup>

Tests are automatically run on pull requests. Here are the commands in case
you need to run them manually/locally.

### Run tests

```sh
coverage run -m pytest
```

### Check coverage

```sh
coverage report --show-missing --fail-under=100
```

> **Qexat:** personally, I have a shell alias `report` to that command.

## Bumping the version

**It should be done via a PR so the docs get updated upon merging.**

Magic List carefully follows semantic versioning:

- if there are breaking changes, increment the major number
- if there are a few new features, increment the minor number
- if there are only bug fixes, increment the patch number

Regarding bug fixes, it is best if a patch version is released for each.

It is manual for now, but I am not opposed to automate the process if you have
compelling arguments.

## Releasing

<sup>Dependencies: `build`, `twine`</sup>

> [!WARNING]
> Do NOT make a release if at least one of the status checks are failing.

Once you have [locally built](#building) the wheel, make a release on GitHub including it.
You can check past releases to see how it was done. **Make sure to have bumped
the version beforehand.**

> [!NOTE]
> A GitHub action will handle uploading it to the PyPI.

### Building

To build locally, run the following command:

```sh
python -m build
```

### Uploading to the PyPI

In case the GitHub action is unavailable for one reason or another:

```sh
twine upload dist/* --skip-existing
```

---

Written with 🩷 by [Qexat](https://github.com/qexat).
Thank you for your kind contribution to this project!
