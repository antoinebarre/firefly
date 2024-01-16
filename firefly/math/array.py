"""
This module provides functions for working with arrays.

For more information, see the documentation at:
https://example.com/firefly/math/array

Google Python Style Guide:
https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
"""

# export
__all__ = [
    "is_monotonic",
    "is_monotonic_increasing",
    "is_monotonic_decreasing",
    "is_strictly_monotonic",
    "is_strictly_monotonic_increasing",
    "is_strictly_monotonic_decreasing",
]

# Imports

from beartype import beartype
import numpy as np

from firefly.types import Vector

# ============================= ARRAY ANALYSIS ============================= #
@beartype
def is_monotonic(array: Vector) -> bool:
    """
    Returns True if the array is monotonic, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic, False otherwise.
    """
    return bool(np.all(np.diff(array) >= 0) or np.all(np.diff(array) <= 0))

@beartype
def is_monotonic_increasing(array: Vector) -> bool:
    """
    Returns True if the array is monotonic increasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic increasing, False otherwise.
    """
    return bool(np.all(np.diff(array) >= 0))

@beartype
def is_monotonic_decreasing(array: Vector) -> bool:
    """
    Returns True if the array is monotonic decreasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic decreasing, False otherwise.
    """
    return bool(np.all(np.diff(array) <= 0))

@beartype
def is_strictly_monotonic(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic, False otherwise.
    """
    return bool(np.all(np.diff(array) > 0) or np.all(np.diff(array) < 0))

@beartype
def is_strictly_monotonic_increasing(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic increasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic increasing, False otherwise.
    """
    return bool(np.all(np.diff(array) > 0))

@beartype
def is_strictly_monotonic_decreasing(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic decreasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic decreasing, False otherwise.
    """
    return bool(np.all(np.diff(array) < 0))
