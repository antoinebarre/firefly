"""Firefly - Numpy Object Validation"""


from typing import Any
import numpy as np
from beartype import beartype

from .__exception import FireflyValueError

@beartype
def validate_vector_3x1(vector: np.ndarray) -> np.ndarray:
    """Check if a data is mutable to a [3x1] vector numpy array and return it

    Args:
        x_in (Any): data to assess

    Raises:
        ValueError: exception raised if the data is not the appropriate type

    Returns:
        np.ndarray: input as a [3x1] numpy array
    """
    if list(vector.shape) in [[3], [3, 1], [1, 3]]:
        return np.reshape(vector, (3, -1))

    # Raise Error
    raise FireflyValueError(
        expectedProperty="[3x1] Numpy Array",
        currentValue=vector,
        )