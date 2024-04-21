"""
This module contains two symbols:

- `list`, a type that extends the built-in equivalent
- `L`, a pseudo-literal which can be used to create magic lists similarly to built-in ones.

They can be imported as following:

```py
from magic_list import list, L
```
"""

from magic_list.prelude import L
from magic_list.prelude import list

__all__ = ["list", "L"]
