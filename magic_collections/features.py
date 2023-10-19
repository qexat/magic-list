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
