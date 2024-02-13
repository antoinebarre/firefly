"""Collection of string validation functions"""

from typing import Any

def validate_string(
    value: Any,
    empty_allowed: bool = True,
) -> str:
    """
    Validates if the given value is a string and optionally checks if it is empty.

    Args:
        value (Any): The value to be validated.
        empty_allowed (bool, optional): Flag indicating if an empty string is
        allowed. Defaults to True.

    Raises:
        TypeError: If the value is not a string.
        ValueError: If the value is an empty string and empty_allowed is False.

    Returns:
        str: The validated string value.
    """

    # Check if the value is a string
    if not isinstance(value, str):
        raise TypeError(f"value must be a string. Got {value} - {type(value)}")

    # Check if the string is empty
    if not empty_allowed and len(value) == 0:
        raise ValueError("value cannot be an empty string")

    return value
