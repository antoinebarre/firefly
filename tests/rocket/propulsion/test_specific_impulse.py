import numpy as np
import pytest
from firefly.rocket.propulsion import SpecificImpulse

# Constants for testing
START_TIME = 0.0

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Happy path test values
happy_path_params = [
    (np.array([0, 10, 20]), np.array([300, 310, 320]), 15, 315),
    (np.array([0, 5]), np.array([250, 250]), 2.5, 250),
]

# Edge case test values
edge_case_params = [
    (np.array([0]), np.array([300]), 0, 300),
    (np.array([0, 10]), np.array([300, 300]), 10, 300),
]

# Error case test values
error_case_params = [
    (np.array([0, -10]), np.array([300, 310]), 15, ValueError),
    (np.array([0, 10]), np.array([300]), 5, ValueError),
]

@pytest.mark.parametrize("times, ISP, current_time, expected", happy_path_params, ids=[HAPPY_PATH_ID]*len(happy_path_params))
def test_specific_impulse_happy_path(times, ISP, current_time, expected):
    # Arrange
    specific_impulse = SpecificImpulse(times, ISP)

    # Act
    result = specific_impulse.current(current_time)

    # Assert
    assert result == expected, f"Expected {expected}, got {result}"

@pytest.mark.parametrize("times, ISP, current_time, expected", edge_case_params, ids=[EDGE_CASE_ID]*len(edge_case_params))
def test_specific_impulse_edge_cases(times, ISP, current_time, expected):
    # Arrange
    specific_impulse = SpecificImpulse(times, ISP)

    # Act
    result = specific_impulse.current(current_time)

    # Assert
    assert result == expected, f"Expected {expected}, got {result}"

@pytest.mark.parametrize("times, ISP, current_time, expected_exception", error_case_params, ids=[ERROR_CASE_ID]*len(error_case_params))
def test_specific_impulse_error_cases(times, ISP, current_time, expected_exception):
    # Act / Assert
    with pytest.raises(expected_exception):
        SpecificImpulse(times, ISP).current(current_time)
