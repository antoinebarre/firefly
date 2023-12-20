"""Tests for the Interp1D class."""

import beartype
import pytest
import numpy as np
from firefly.math import Interp1D  # Import your Interp1D class

def test_successful_initialization():
    """
    Test that an Interp1D instance is successfully created with valid numpy
    arrays.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert isinstance(interp, Interp1D)

def test_benchmark():
    """
    Test that the benchmark method runs without error.
    """
    Interp1D.benchmark()

def test_initialization_with_non_numpy_arrays():
    """
    Test that initializing Interp1D with non-numpy arrays raises a TypeError.
    """
    with pytest.raises(TypeError):
        Interp1D([1, 2, 3], [4, 5, 6]) # type: ignore

def test_initialization_with_mismatched_shapes():
    """
    Test that initializing Interp1D with arrays of mismatched shapes raises
    a ValueError.
    """
    with pytest.raises(ValueError):
        Interp1D(np.array([1, 2, 3]), np.array([4, 5]))

def test_initialization_with_non_monotonic_x():
    """
    Test that initializing Interp1D with a non-monotonically increasing 'x'
    array raises a ValueError.
    """
    with pytest.raises(ValueError):
        Interp1D(np.array([1, 3, 2]), np.array([4, 5, 6]))

def test_get_value():
    """
    Test the get_value method returns the correct interpolated value for a
    given single 'new_x' value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert interp.get_value(2.) == 5.

def test_get_value_with_invalid_input():
    """
    Test that the get_value method raises a TypeError when passed a non-numeric 'new_x' value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation): # type: ignore
        interp.get_value("invalid") # type: ignore



def test_get_values_with_valid_input():
    """
    Test the get_values method returns correct interpolated values for a given
    array of valid 'new_x' values.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    new_x = np.array([1.5, 2.5])
    expected = np.array([4.5, 5.5])  # Expected interpolated values
    np.testing.assert_array_almost_equal(interp.get_values(new_x), expected)

def test_get_values_with_empty_input():
    """
    Test the get_values method returns an empty array when given an empty array
    of 'new_x' values.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    new_x = np.array([])
    expected = np.array([])
    np.testing.assert_array_almost_equal(interp.get_values(new_x), expected)

def test_get_values_with_out_of_bounds_input():
    """
    Test the get_values method handles 'new_x' values that are outside the
    bounds of the 'x' array.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    new_x = np.array([0., 4.])  # Values outside the range of x
    # Expected behavior: extrapolation or default behavior of np.interp for
    # out-of-bounds values
    expected = np.array([4, 6])
    np.testing.assert_array_almost_equal(interp.get_values(new_x), expected)

def test_get_values_with_invalid_type_input():
    """
    Test that the get_values method raises a TypeError when passed a 'new_x'
    value of incorrect type.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation): # type: ignore
        interp.get_values("invalid")  # type: ignore # Passing a string instead of an array

def test_get_values_no_extrapolation_allowed():
    """
    Test the get_values method raises a ValueError when extrapolation is not allowed
    and at least one value in new_x array is outside the range of x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    new_x = np.array([0.5, 2.5])
    with pytest.raises(ValueError):
        interp.get_values(new_x, allow_extrapolation=False)

def test_get_value_no_extrapolation_allowed():
    """
    Test the get_value method raises a ValueError when extrapolation is not allowed
    and the new_x value is outside the range of x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(ValueError):
        interp.get_value(0., allow_extrapolation=False)
