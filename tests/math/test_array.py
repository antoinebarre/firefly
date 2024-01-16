"""Test of the array module."""

import pytest
import numpy as np
from firefly.math.array import (
    is_monotonic,
    is_monotonic_increasing,
    is_monotonic_decreasing,
    is_strictly_monotonic,
    is_strictly_monotonic_increasing,
    is_strictly_monotonic_decreasing,
)

# Test data for is_monotonic
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([1, 2, 2, 3]), True, "monotonic_increasing_with_repeats"),
    (np.array([3, 2, 2, 1]), True, "monotonic_decreasing_with_repeats"),
    (np.array([1, 3, 2, 4]), False, "non_monotonic"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_monotonic(array, expected, test_id):
    # Act
    result = is_monotonic(array)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Test data for is_monotonic_increasing
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([1, 2, 3, 4]), True, "strictly_increasing"),
    (np.array([1, 1, 2, 2]), True, "increasing_with_repeats"),
    (np.array([4, 3, 2, 1]), False, "decreasing"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_monotonic_increasing(array, expected, test_id):
    # Act
    result = is_monotonic_increasing(array)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Test data for is_monotonic_decreasing
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([4, 3, 2, 1]), True, "strictly_decreasing"),
    (np.array([2, 2, 1, 1]), True, "decreasing_with_repeats"),
    (np.array([1, 2, 3, 4]), False, "increasing"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_monotonic_decreasing(array, expected, test_id):
    # Act
    result = is_monotonic_decreasing(array)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Test data for is_strictly_monotonic
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([1, 2, 3, 4]), True, "strictly_increasing"),
    (np.array([4, 3, 2, 1]), True, "strictly_decreasing"),
    (np.array([1, 2, 2, 3]), False, "increasing_with_repeats"),
    (np.array([3, 2, 2, 1]), False, "decreasing_with_repeats"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_strictly_monotonic(array, expected, test_id):
    # Act
    result = is_strictly_monotonic(array)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Test data for is_strictly_monotonic_increasing
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([1, 2, 3, 4]), True, "strictly_increasing"),
    (np.array([1, 1, 2, 3]), False, "increasing_with_repeats"),
    (np.array([4, 3, 2, 1]), False, "decreasing"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_strictly_monotonic_increasing(array, expected, test_id):
    # Act
    result = is_strictly_monotonic_increasing(array)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Test data for is_strictly_monotonic_decreasing
@pytest.mark.parametrize("array, expected, test_id", [
    (np.array([4, 3, 2, 1]), True, "strictly_decreasing"),
    (np.array([2, 2, 1, 0]), False, "decreasing_with_repeats"),
    (np.array([1, 2, 3, 4]), False, "increasing"),
    (np.array([1]), True, "single_element"),
    (np.array([]), True, "empty_array"),
])
def test_is_strictly_monotonic_decreasing(array, expected, test_id):
    # Act
    result = is_strictly_monotonic_decreasing(array)

    # Assert
    assert result == expected, f"Failed {test_id}"
