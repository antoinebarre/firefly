"""Validation - additional generic validation functions."""


from typing import Any

import numpy as np
from numpy.typing import NDArray


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

# ============================== NUMPY VECTOR ============================== #

def validate_numpy_vector(
    value: Any,
) -> NDArray[np.float64]:
    """
    Validate that the value is a Numpy vector.

    Args:
        value (Any): The value to validate.

    Returns:
        Any: The validated value.

    Raises:
        TypeError: If the value is not a Numpy vector.

    """
    try:
        vector = np.asarray(value,dtype=np.float64)
        if vector.ndim != 1:
            raise ValueError(f"value must be a 1D Numpy array. Got {vector.ndim}D")
        else:
            return vector
    except (ValueError, TypeError) as e:
        msg = f"value must be a Numpy vector. Got {value} - {type(value)}"
        raise TypeError(msg) from e


# ================================= STRING ================================= #

def validate_string(
    value: Any,
) -> str:
    """
    Validate that the value is a string.

    Args:
        value (Any): The value to validate.

    Returns:
        str: The validated value.

    Raises:
        TypeError: If the value is not a string.

    """
    if not isinstance(value, str):
        raise TypeError(f"value must be a string. Got {value} - {type(value)}")
    return value
