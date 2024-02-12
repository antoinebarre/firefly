"""Collection of functions for validating integer values."""

def validate_integer(value: int) -> int:
    """
    Validates if the given value is an integer.

    Args:
        value (int): The value to be validated.

    Returns:
        int: The validated integer value.

    Raises:
        TypeError: If the value is not an integer.

    """
    if not isinstance(value, int):
        raise TypeError(f'Expected an integer, but got {type(value).__name__}.')

    return value

def validate_positive_integer(value: int) -> int:
    """
    Validate if the given value is a positive integer.

    Args:
        value (int): The value to be validated.

    Returns:
        int: The validated positive integer.

    Raises:
        ValueError: If the value is not a positive integer.

    """
    value = validate_integer(value)

    if value < 0:
        raise ValueError('Expected a positive integer.')

    return value
