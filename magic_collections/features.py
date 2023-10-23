"""
This module contains all the feature flags of the current `magic_collections`
installation. It allows to perform some checks to avoid making features
available when they shouldn't, and vice-versa.
"""
# pyright: reportUnusedCallResult = false
import importlib as _importlib


def _is_available(package_name: str) -> bool:  # pragma: no cover
    try:
        _importlib.import_module(package_name)
    except (ImportError, Exception):
        return False
    else:
        return True


OPTION = _is_available("option")
