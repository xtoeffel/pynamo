"""Utility functions and helper classes for strings."""


def require_non_empty(string: str, name: str = "string") -> None:
    """Raises a ValueError if string is empty or None for evaluation of strings.

    :param string: string to evaluate
    :type string: str
    :param name: name of the string (to evaluate)
    :type name: str

    :raises ValueError: as intended - if string is None or empty; unintended - if name is None or empty
    """
    if name is None or len(name) == 0:
        raise ValueError(f"Undefined or empty name string")
    if string is None:
        raise ValueError(f"Undefined {name}")
    if len(string) == 0:
        raise ValueError(f"Empty {name}")
