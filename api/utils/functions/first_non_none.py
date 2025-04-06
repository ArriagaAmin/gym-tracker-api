from typing import TypeVar


T = TypeVar("T")

def first_non_none(*args: T | None) -> T:
    for arg in args:
        if arg != None:
            return arg
    raise ValueError("One of the values must be not None")
