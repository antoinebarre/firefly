import pytest
import numpy as np
from firefly.rocket.propulsion import GenericTimedData

# Assuming START_TIME is a constant defined in the module that needs to be imported
from firefly.rocket.propulsion import START_TIME

# Happy path tests with various realistic test values
@pytest.mark.parametrize("test_id, times, values, expected", [
    ("HP-1", [START_TIME, 10, 20], [0, 5, 10], [0, 5, 10]),
    ("HP-2", [START_TIME, 5, 15], [3, 6, 9], [3, 6, 9]),
    # Add more test cases as needed
])
def test_generic_timed_data_happy_path(test_id, times, values, expected):
    # Arrange
    times = np.array(times)
    values = np.array(values)

    # Act
    gtd = GenericTimedData(times, values)

    # Assert
    for t, e in zip(times, expected):
        assert gtd.current_value(t) == e, f"Test ID: {test_id}"

# Edge cases
@pytest.mark.parametrize("test_id, times, values, current_time, expected", [
    ("EC-1", [START_TIME, 10], [1, 1], START_TIME, 1),
    ("EC-2", [START_TIME, 10], [1, 1], 10, 1),
    # Add more edge cases as needed
])
def test_generic_timed_data_edge_cases(test_id, times, values, current_time, expected):
    # Arrange
    times = np.array(times)
    values = np.array(values)

    # Act
    gtd = GenericTimedData(times, values)

    # Assert
    assert gtd.current_value(current_time) == expected, f"Test ID: {test_id}"

# Error cases
@pytest.mark.parametrize("test_id, times, values, current_time, exception", [
    ("ERR-1", [1, 10], [1, 1], START_TIME, ValueError),  # First time value is not START_TIME
    ("ERR-2", [START_TIME, 10], [1, 1], -1, ValueError),  # current_time is less than START_TIME
    # Add more error cases as needed
])
def test_generic_timed_data_error_cases(test_id, times, values, current_time, exception):
    # Arrange
    times = np.array(times)
    values = np.array(values)

    # Act / Assert
    if test_id == "ERR-1":
        with pytest.raises(exception, match="The first time value must be"):
            GenericTimedData(times, values)
    elif test_id == "ERR-2":
        gtd = GenericTimedData(np.array([START_TIME, 10]), np.array([1, 1]))
        with pytest.raises(exception, match="negative time value is not allowed"):
            gtd.current_value(current_time)
