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

import numpy as np
from numpy.typing import NDArray

from firefly.types import Vector
from firefly.validation import validate_float, validate_numpy_vector


# ============================= ARRAY HANDLING ============================= #

def sort_arrays(
        array1: NDArray[np.float64],
        array2: NDArray[np.float64],
        ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Sort two arrays based on the values of the first array.

    Args:
        array1 (1D Numpy Array): The first array.
        array2 (1D Numpy Array): The second array.

    Returns:
        (1D Numpy Array, 1D Numpy Array): The sorted arrays.

    """
    # validate the input data
    array1 = validate_numpy_vector(array1)
    array2 = validate_numpy_vector(array2)

    # check if the arrays have the same length
    if array1.shape != array2.shape:
        raise ValueError("The arrays must have the same length.")

    # sort the arrays based on the first array
    sort_indices = np.argsort(array1)
    array1 = array1[sort_indices]
    array2 = array2[sort_indices]

    return array1, array2

def is_value_in_interval(
        value: float,
        interval: NDArray[np.float64]) -> bool:
    """
    Check if a value is within the specified interval.

    Args:
        value (float): The value to check.
        interval (1D Np Array): The interval represented as a vector.

    Returns:
        bool: True if the value is within the interval, False otherwise.

    """

    # validate the input data
    value = validate_float(value)
    interval = validate_numpy_vector(interval)

    # sort the interval in place
    interval.sort()

    return interval[0] <= value <= interval[-1]

def is_values_in_interval(
        values: NDArray[np.float64],
        interval: NDArray[np.float64]) -> bool:
    """
    Check if all values are within the specified interval.

    Args:
        values (1D Numpy Array): The values to check.
        interval (1D Numpy Array): The interval represented as a vector.

    Returns:
        bool: True if all values are within the interval, False otherwise.

    """
    # validate the input data
    values_array = validate_numpy_vector(values)
    interval_array = validate_numpy_vector(interval)

    # sort the interval in place
    interval_array.sort()

    return (bool(np.all(interval_array[0] <= values_array)) and
            bool(np.all(values_array <= interval_array[-1])))

# ============================= ARRAY ANALYSIS ============================= #

def is_monotonic(array: Vector) -> bool:
    """
    Returns True if the array is monotonic, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic, False otherwise.
    """
    #validate the input data
    array = validate_numpy_vector(array)
    
    return bool(np.all(np.diff(array) >= 0) or np.all(np.diff(array) <= 0))


def is_monotonic_increasing(array: Vector) -> bool:
    """
    Returns True if the array is monotonic increasing, False otherwise.

    Args:
        array (1D np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic increasing, False otherwise.
    """
    #validate the input data
    array = validate_numpy_vector(array)

    return bool(np.all(np.diff(array) >= 0))


def is_monotonic_decreasing(array: Vector) -> bool:
    """
    Returns True if the array is monotonic decreasing, False otherwise.

    Args:
        array (1D np.ndarray): The array to check.

    Returns:
        bool: True if the array is monotonic decreasing, False otherwise.
    """
    #validate the input data
    array = validate_numpy_vector(array)

    return bool(np.all(np.diff(array) <= 0))


def is_strictly_monotonic(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic, False otherwise.

    Args:
        array (1D np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic, False otherwise.
    """

    #validate the input data
    array = validate_numpy_vector(array)

    return bool(np.all(np.diff(array) > 0) or np.all(np.diff(array) < 0))


def is_strictly_monotonic_increasing(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic increasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic increasing, False otherwise.
    """
    #validate the input data
    array = validate_numpy_vector(array)

    return bool(np.all(np.diff(array) > 0))


def is_strictly_monotonic_decreasing(array: Vector) -> bool:
    """
    Returns True if the array is strictly monotonic decreasing, False otherwise.

    Args:
        array (np.ndarray): The array to check.

    Returns:
        bool: True if the array is strictly monotonic decreasing, False otherwise.
    """

    #validate the input data
    array = validate_numpy_vector(array)

    return bool(np.all(np.diff(array) < 0))


if __name__ == "__main__":

    a = np.array([1,2,3,4,5])
    print(is_value_in_interval(3.0, a))