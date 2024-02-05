"""Tests for the Interp1D class."""

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
        Interp1D(1, 4) # type: ignore

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
    with pytest.raises(TypeError): # type: ignore
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
    with pytest.raises(TypeError): # type: ignore
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

def test_full_range_integration():
    """
    Test the integrate_all method returns the correct integrated value over the full range of x.
    """
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    interp = Interp1D(x, y)
    result = interp.integrate_all()
    expected = 1.839  # Approximate expected value over the full range
    np.testing.assert_almost_equal(result, expected, decimal=3)


import numpy as np
import pytest
from firefly.math.interp1D import Interp1D

# Test IDs for parametrization
happy_path_ids = [
    "monotonic_increasing",
    "monotonic_increasing_with_negative_values",
    "monotonic_increasing_large_dataset"
]

edge_case_ids = [
    "monotonic_increasing_single_element",
    "monotonic_increasing_two_elements"
]

error_case_ids = [
    "non_monotonic_increasing",
    "x_and_y_different_shapes",
    "x_and_y_different_lengths"
]

# Happy path test values
happy_path_values = [
    (np.array([1, 2, 3]), np.array([4, 5, 6])),
    (np.array([-3, -2, -1]), np.array([1, 2, 3])),
    (np.linspace(0, 1000, 1001), np.linspace(1000, 2000, 1001))
]

# Edge case test values
edge_case_values = [
    (np.array([42]), np.array([42])),
    (np.array([0, 1]), np.array([1, 2]))
]

# Error case test values
error_case_values = [
    (np.array([1, 3, 2]), np.array([4, 5, 6])),
    (np.array([1, 2]), np.array([4, 5, 6])),
    (np.array([1, 2, 3]), np.array([4, 5]))
]

@pytest.mark.parametrize("x, y", happy_path_values, ids=happy_path_ids)
def test_interp1d_happy_path(x, y):
    # Arrange
    interp = Interp1D(x=x, y=y)

    # Act
    # __post_init__ is called during object initialization, so no action is required here

    # Assert
    assert interp.x.shape == interp.y.shape
    assert np.all(np.diff(interp.x) > 0), "x is not strictly monotonically increasing"

@pytest.mark.parametrize("x, y", edge_case_values, ids=edge_case_ids)
def test_interp1d_edge_cases(x, y):
    # Arrange
    interp = Interp1D(x=x, y=y)

    # Act
    # __post_init__ is called during object initialization, so no action is required here

    # Assert
    assert interp.x.shape == interp.y.shape
    assert np.all(np.diff(interp.x) >= 0), "x is not monotonically increasing"

@pytest.mark.parametrize("x, y", error_case_values, ids=error_case_ids)
def test_interp1d_error_cases(x, y):
    # Act & Assert
    with pytest.raises(ValueError):
        Interp1D(x=x, y=y)
        

# Test IDs for parametrization
happy_path_ids = [
    "monotonic_increasing",
    "monotonic_increasing_with_negative_values",
    "monotonic_increasing_large_dataset"
]

edge_case_ids = [
    "monotonic_increasing_single_element",
    "monotonic_increasing_two_elements"
]

error_case_ids = [
    "non_monotonic_increasing",
    "x_and_y_different_shapes",
    "x_and_y_different_lengths"
]

# Happy path test values
happy_path_values = [
    (np.array([1, 2, 3]), np.array([4, 5, 6])),
    (np.array([-3, -2, -1]), np.array([1, 2, 3])),
    (np.linspace(0, 1000, 1001), np.linspace(1000, 2000, 1001))
]

# Edge case test values
edge_case_values = [
    (np.array([42]), np.array([42])),
    (np.array([0, 1]), np.array([1, 2]))
]

# Error case test values
error_case_values = [
    (np.array([1, 3, 2]), np.array([4, 5, 6])),
    (np.array([1, 2]), np.array([4, 5, 6])),
    (np.array([1, 2, 3]), np.array([4, 5]))
]

@pytest.mark.parametrize("x, y", happy_path_values, ids=happy_path_ids)
def test_interp1d_happy_path2(x, y):
    # Arrange
    interp = Interp1D(x=x, y=y)

    # Act
    # __post_init__ is called during object initialization, so no action is required here

    # Assert
    assert interp.x.shape == interp.y.shape
    assert np.all(np.diff(interp.x) > 0), "x is not strictly monotonically increasing"

@pytest.mark.parametrize("x, y", edge_case_values, ids=edge_case_ids)
def test_interp1d_edge_cases2(x, y):
    # Arrange
    interp = Interp1D(x=x, y=y)

    # Act
    # __post_init__ is called during object initialization, so no action is required here

    # Assert
    assert interp.x.shape == interp.y.shape
    assert np.all(np.diff(interp.x) >= 0), "x is not monotonically increasing"

@pytest.mark.parametrize("x, y", error_case_values, ids=error_case_ids)
def test_interp1d_error_cases2(x, y):
    # Act & Assert
    with pytest.raises(ValueError):
        Interp1D(x=x, y=y)

# Test cases for the min_x property
# Each test case is a tuple with the following structure:
# (test_id, x_values, expected_min_x)

test_cases = [
    # Happy path tests with various realistic test values
    ("happy-1", [1.5, 2.5, 3.5], 1.5),
    ("happy-2", [0.0, 1.0, 2.0], 0.0),
    ("happy-3", [-1.0, 0.0, 1.0], -1.0),


# Error cases are not applicable here since the property only returns a value
# and does not raise exceptions
]

@pytest.mark.parametrize("test_id, x_values, expected_min_x", test_cases)
def test_min_x(test_id, x_values, expected_min_x):
    # Arrange
    interp1d_instance = Interp1D(x_values, np.zeros(len(x_values)))

    # Act
    result = interp1d_instance.min_x

    # Assert
    assert result == expected_min_x, f"Test {test_id} failed: min_x={result}, expected={expected_min_x}"


# Test cases for the max_x property
# Each test case is a tuple with the following structure:
# (test_id, input_data, expected_output)

test_cases = [
    # Happy path tests with various realistic test values
    ("happy-1", [1, 2, 3, 4, 5], 5.0),
    ("happy-2", [10.5, 20.3, 30.7], 30.7),
    ("happy-3", [-5, 0, 5], 5.0),
    
    # Edge cases
    ("edge-3", [-1, -0.5, 0], 0.0),  # Non-positive elements
    
    # Error cases are not applicable here since the property should always return the last element
    # as a float and the input is controlled by the class itself.
]

@pytest.mark.parametrize("test_id, input_data, expected_output", test_cases)
def test_max_x(test_id, input_data, expected_output):
    # Arrange
    interp1d_instance = Interp1D(x=input_data,y=np.zeros(len(input_data)))  # Assuming Interp1D takes x as an initialization parameter

    # Act
    result = interp1d_instance.max_x

    # Assert
    assert result == expected_output, f"Test {test_id} failed: max_x({input_data}) == {result}, expected {expected_output}"



# Test cases for the Interp1D class

def test_successful_initialization2():
    """
    Test that an Interp1D instance is successfully created with valid numpy
    arrays.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert isinstance(interp, Interp1D)

def test_initialization_with_non_numpy_arrays2():
    """
    Test that initializing Interp1D with non-numpy arrays raises a TypeError.
    """
    with pytest.raises(TypeError):
        Interp1D(1, 4) # type: ignore

def test_initialization_with_mismatched_shapes2():
    """
    Test that initializing Interp1D with arrays of mismatched shapes raises
    a ValueError.
    """
    with pytest.raises(ValueError):
        Interp1D(np.array([1, 2, 3]), np.array([4, 5]))

def test_initialization_with_non_monotonic_x2():
    """
    Test that initializing Interp1D with a non-monotonically increasing 'x'
    array raises a ValueError.
    """
    with pytest.raises(ValueError):
        Interp1D(np.array([1, 3, 2]), np.array([4, 5, 6]))

def test_get_value2():
    """
    Test the get_value method returns the correct interpolated value for a
    given single 'new_x' value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert interp.get_value(2.) == 5.

def test_get_value_with_invalid_input2():
    """
    Test that the get_value method raises a TypeError when passed a non-numeric 'new_x' value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(TypeError): # type: ignore
        interp.get_value("invalid") # type: ignore

def test_get_values_with_valid_input2():
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

def test_get_values_with_empty_input2():
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

def test_get_values_with_out_of_bounds_input2():
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

def test_get_values_with_invalid_type_input2():
    """
    Test that the get_values method raises a TypeError when passed a 'new_x'
    value of incorrect type.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(TypeError): # type: ignore
        interp.get_values("invalid")  # type: ignore # Passing a string instead of an array

def test_get_values_no_extrapolation_allowed2():
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

def test_get_value_no_extrapolation_allowed2():
    """
    Test the get_value method raises a ValueError when extrapolation is not allowed
    and the new_x value is outside the range of x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    with pytest.raises(ValueError):
        interp.get_value(0., allow_extrapolation=False)

def test_full_range_integration2():
    """
    Test the integrate_all method returns the correct integrated value over the full range of x.
    """
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    interp = Interp1D(x, y)
    result = interp.integrate_all()
    expected = 1.839  # Approximate expected value over the full range
    np.testing.assert_almost_equal(result, expected, decimal=3)

def test_min_x2():
    """
    Test the min_x property returns the minimum x value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert interp.min_x == 1.0

def test_max_x2():
    """
    Test the max_x property returns the maximum x value.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert interp.max_x == 3.0

def test_is_in_x_range():
    """
    Test the is_in_x_range method returns True if a value is within the range of x, False otherwise.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    assert interp.is_in_x_range(2.5) == True
    assert interp.is_in_x_range(4.0) == False

def test_add_points():
    """
    Test the add_points method adds new points to the interpolation data.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    new_x = np.array([1.5, 2.5])
    new_y = np.array([4.5, 5.5])
    interp.add_points(new_x, new_y)
    expected_x = np.array([1, 1.5, 2, 2.5, 3])
    expected_y = np.array([4, 4.5, 5, 5.5, 6])
    np.testing.assert_array_equal(interp.x, expected_x)
    np.testing.assert_array_equal(interp.y, expected_y)

def test_integrate():
    """
    Test the integrate method calculates the integral of the function over the specified interval.
    """
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    interp = Interp1D(x, y)
    result = interp.integrate(0.5, 2.5)
    expected = 1.67873  # Approximate expected value over the interval
    np.testing.assert_almost_equal(result, expected, decimal=3)

def test_cummulative_integral():
    """
    Test the cummulative_integral method calculates the cumulative integral up to the given x value.
    """
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    interp = Interp1D(x, y)
    result = interp.cummulative_integral(2.5)
    expected = 1.801 # Approximate expected value up to the given x value
    np.testing.assert_almost_equal(result, expected, decimal=3)

def test_benchmark2():
    """
    Test the benchmark method runs without error.
    """
    Interp1D.benchmark()

def test_benchmark_integration():
    """
    Test the benchmark_integration method runs without error.
    """
    Interp1D.benchmark_integration()
    
    
def test_cummulative_integral_within_range():
    """
    Test that the cummulative_integral method returns the correct cumulative integral
    up to the given x value within the range of x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 2.5
    expected = 7.125  # Expected cumulative integral
    result = interp.cummulative_integral(current_x)
    assert result == expected

def test_cummulative_integral_at_min_x():
    """
    Test that the cummulative_integral method returns 0.0 when the given x value is equal to min_x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 1.0
    expected = 0.0
    result = interp.cummulative_integral(current_x)
    assert result == expected

def test_cummulative_integral_at_max_x():
    """
    Test that the cummulative_integral method returns the result of integrate_all when the given x value is equal to max_x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 3.0
    expected = interp.integrate_all()
    result = interp.cummulative_integral(current_x)
    assert result == expected

def test_cummulative_integral_at_existing_x():
    """
    Test that the cummulative_integral method returns the correct cumulative integral
    up to the given x value when the x value exists in the x array.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 2.0
    expected = 4.5  # Expected cumulative integral
    result = interp.cummulative_integral(current_x)
    assert result == expected

def test_cummulative_integral_at_new_x():
    """
    Test that the cummulative_integral method returns the correct cumulative integral
    up to the given x value when the x value does not exist in the x array.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 2.5
    expected = 7.125  # Expected cumulative integral
    result = interp.cummulative_integral(current_x)
    assert result == expected

def test_cummulative_integral_out_of_range():
    """
    Test that the cummulative_integral method raises a ValueError when the given x value is outside the range of x.
    """
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    interp = Interp1D(x, y)
    current_x = 4.0
    with pytest.raises(ValueError):
        interp.cummulative_integral(current_x)