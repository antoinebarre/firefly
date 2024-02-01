import pytest
import numpy as np
from firefly.rocket.propulsion import FlowRate

# Constants for testing
START_TIME = 0.0

# Test cases for FlowRate.__init__
@pytest.mark.parametrize("times, flow_rate, test_id", [
    (np.array([0, 1, 2]), np.array([10, 15, 20]), "init_happy"),
    (np.array([0]), np.array([5]), "init_single_point"),
    (np.array([0, 1, 2]), np.array([0, 0, 0]), "init_zero_flow"),
], ids=lambda test_id: test_id)
def test_flow_rate_init(times, flow_rate, test_id):
    # Arrange

    # Act
    flow_rate_instance = FlowRate(times, flow_rate)

    # Assert
    assert np.array_equal(flow_rate_instance.x, times)
    assert np.array_equal(flow_rate_instance.y, flow_rate)

# Test cases for FlowRate.create_constant_flow_rate
@pytest.mark.parametrize("value, t_end_combustion, test_id", [
    (10.0, 5.0, "constant_positive"),
], ids=lambda test_id: test_id)
def test_create_constant_flow_rate(value, t_end_combustion, test_id):
    # Act
    constant_flow_rate = FlowRate.create_constant_flow_rate(value, t_end_combustion)

    # Assert
    assert np.array_equal(constant_flow_rate.x, np.array([START_TIME, t_end_combustion]))
    assert np.all(constant_flow_rate.y == value)

# Test cases for FlowRate.create_variable_flow_rate
@pytest.mark.parametrize("times, flow_rate, test_id", [
    (np.array([0, 1, 2]), np.array([10, 15, 20]), "variable_normal"),
    (np.array([0, 1, 2]), np.array([20, 15, 10]), "variable_decreasing"),
    (np.array([0, 0.5, 1]), np.array([10, 10, 10]), "variable_constant"),
], ids=lambda test_id: test_id)
def test_create_variable_flow_rate(times, flow_rate, test_id):
    # Act
    variable_flow_rate = FlowRate.create_variable_flow_rate(times, flow_rate)

    # Assert
    assert np.array_equal(variable_flow_rate.x, times)
    assert np.array_equal(variable_flow_rate.y, flow_rate)

# Test cases for FlowRate.current
@pytest.mark.parametrize("times, flow_rate, current_time, expected, test_id", [
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 1.5, 17.5, "current_midpoint"),
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 0, 10, "current_start"),
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 2, 20, "current_end"),
], ids=lambda test_id: test_id)
def test_current(times, flow_rate, current_time, expected, test_id):
    # Arrange
    flow_rate_instance = FlowRate(times, flow_rate)

    # Act
    result = flow_rate_instance.current(current_time)

    # Assert
    assert result == expected

# Test cases for FlowRate.is_valid
@pytest.mark.parametrize("times, flow_rate, total_propelant_mass, combustion_time, expected, test_id", [
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 30, 2, True, "valid_exact_mass"),
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 28, 2, False, "valid_insufficient_mass"),
    (np.array([0, 1, 2]), np.array([10, 15, 20]), 40, 2, True, "valid_excess_mass"),
], ids=lambda test_id: test_id)
def test_is_valid(times, flow_rate, total_propelant_mass, combustion_time, expected, test_id):
    # Arrange
    flow_rate_instance = FlowRate(times, flow_rate)

    # Act
    result = flow_rate_instance.is_valid(total_propelant_mass, combustion_time)

    # Assert
    assert result == expected

# Test cases for FlowRate.is_valid with ValueError
@pytest.mark.parametrize("times, flow_rate, total_propelant_mass, combustion_time, test_id", [
    (np.array([0, 1, 3]), np.array([10, 15, 20]), 45, 2, "invalid_combustion_time"),
], ids=lambda test_id: test_id)
def test_is_valid_error(times, flow_rate, total_propelant_mass, combustion_time, test_id):
    # Arrange
    flow_rate_instance = FlowRate(times, flow_rate)

    # Act / Assert
    with pytest.raises(ValueError):
        flow_rate_instance.is_valid(total_propelant_mass, combustion_time)
