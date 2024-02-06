"""
This module provides functions to validate numpy objects according to Google rules.
"""

from typing import Any
import numpy as np
from numpy.typing import NDArray

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
