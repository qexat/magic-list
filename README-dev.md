# Notes to developers

## Testing

Tests are automatically run on pull requests.

### Run tests

```sh
coverage run -m pytest
```

### Check coverage

```sh
coverage report --show-missing --fail-under=100
```

## Releasing

PyPI Releases are automatically done when making a GitHub release.

### Building

```sh
python -m build
```

### Uploading to the PyPI

```sh
twine upload dist/* --skip-existing
```
