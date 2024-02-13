"""Validation - additional generic validation functions."""


from typing import Any


# ============================== FLOAT OBJECTS ============================= #

def validate_float(
    value: Any,
) -> float:
    """
    Validate that the value is a float.

    Args:
        value (Any): The value to validate.

    Returns:
        float: The validated value.

    Raises:
        TypeError: If the value is not a float.

    """
    try:
        return float(value)
    except (ValueError, TypeError) as e:
        msg = f"value must be a float or convertible to a float. Got {value} - {type(value)}"
        raise TypeError(msg) from e

# ================================== BOOL ================================== #

def validate_bool(
    value: Any,
) -> bool:
    """
    Validate that the value is a boolean.

    Args:
        value (Any): The value to validate.

    Returns:
        bool: The validated value.

    Raises:
        TypeError: If the value is not a boolean.

    """
    if not isinstance(value, bool):
        raise TypeError(f"value must be a boolean. Got {value} - {type(value)}")
    return value
