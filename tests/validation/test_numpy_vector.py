import pytest
import numpy as np
from firefly.validation import validate_numpy_vector

# Happy path tests with various realistic test values
@pytest.mark.parametrize("input_value, expected_output", [
    (pytest.param([1.0, 2.0, 3.0], np.array([1.0, 2.0, 3.0], dtype=np.float64), id="list_of_floats")),
    (pytest.param(np.array([1, 2, 3]), np.array([1.0, 2.0, 3.0], dtype=np.float64), id="numpy_int_array")),
    (pytest.param((0.5, 1.5, 2.5), np.array([0.5, 1.5, 2.5], dtype=np.float64), id="tuple_of_floats")),
    (pytest.param([], np.array([], dtype=np.float64), id="empty_list")),
    (pytest.param(np.array([3.14159]), np.array([3.14159], dtype=np.float64), id="single_float_in_numpy_array")),
])
def test_validate_numpy_vector_happy_path(input_value, expected_output):
    # Act
    result = validate_numpy_vector(input_value)

    # Assert
    np.testing.assert_array_equal(result, expected_output)

# Edge cases
@pytest.mark.parametrize("input_value", [
    (pytest.param(np.array([[1.0, 2.0], [3.0, 4.0]]), id="2D_numpy_array")),
    (pytest.param(np.array([[[1.0]]]), id="3D_numpy_array_with_single_element")),
    (pytest.param(np.array([], dtype=np.float64).reshape(0, 2), id="empty_2D_numpy_array")),
])
def test_validate_numpy_vector_edge_cases(input_value):
    # Act & Assert
    with pytest.raises(TypeError):
        validate_numpy_vector(input_value)

# Error cases
@pytest.mark.parametrize("input_value", [
    (pytest.param("not_a_numpy_array", id="string_instead_of_numpy_array")),
    (pytest.param(None, id="none_value")),
    (pytest.param([1.0, "two", 3.0], id="list_with_non_numeric_value")),
    (pytest.param([1.0, [2.0], 3.0], id="list_with_nested_list")),
    (pytest.param({"a": 1.0, "b": 2.0}, id="dict_instead_of_numpy_array")),
])
def test_validate_numpy_vector_error_cases(input_value):
    # Act & Assert
    with pytest.raises(TypeError):
        validate_numpy_vector(input_value)
