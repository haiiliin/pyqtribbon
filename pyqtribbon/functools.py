import functools
from functools import *
from typing import TypeVar

T = TypeVar('T')


def partialmethod(func: T, /, *args, **kwargs) -> T:
    """Wapper around functools.partialmethod."""
    return functools.partialmethod(func, *args, **kwargs)
