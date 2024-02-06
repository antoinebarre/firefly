import pytest
import numpy as np
from firefly.rocket.propulsion.flow_rate import ConstantFlowRate, VariableFlowRate

# ============================== CONSTANT FLOW RATE TESTS ============================== #

@pytest.mark.parametrize("test_id, flow_rate, combustion_duration, time_since_ignition, expected_flow, expected_mass, expected_total_mass", [
    # Happy path tests
    ("C1", 100.0, 10.0, 5.0, 100.0, 500.0, 1000.0),
    ("C2", 50.0, 20.0, 0.0, 50.0, 0.0, 1000.0),
    ("C3", 75.0, 15.0, 15.0, 75.0, 1125.0, 1125.0),
    # Edge cases
    ("C4", 100.0, 10.0, 10.0, 100.0, 1000.0, 1000.0),
    ("C4", 100.0, 10.0, 10.1, 0.0, 1000.0, 1000.0),
    ("C5", 100.0, 10.0, 0.0, 100.0, 0.0, 1000.0),
    # Error cases
    ("C6", -1.0, 10.0, 5.0, None, None, None),
    ("C7", 100.0, -1.0, 5.0, None, None, None),
    ("C8", 100.0, 10.0, -1.0, None, None, None),
])
def test_constant_flow_rate(test_id, flow_rate, combustion_duration, time_since_ignition, expected_flow, expected_mass, expected_total_mass):
    # Arrange
    if test_id.startswith("C6"):  # Invalid flow rate
        with pytest.raises(ValueError):
            ConstantFlowRate(flow_rate=flow_rate, combustion_duration=combustion_duration)
        return
    elif test_id.startswith("C7"):  # Invalid combustion duration
        with pytest.raises(ValueError):
            ConstantFlowRate(flow_rate=flow_rate, combustion_duration=combustion_duration)
        return
    else:
        constant_flow = ConstantFlowRate(flow_rate=flow_rate, combustion_duration=combustion_duration)

    # Act & Assert
    if test_id.startswith("C8"):  # Invalid time since ignition
        with pytest.raises(ValueError):
            constant_flow.get_current(time_since_ignition)
        with pytest.raises(ValueError):
            constant_flow.get_current_used_propellant_mass(time_since_ignition)
    else:
        assert constant_flow.get_current(time_since_ignition) == expected_flow
        assert constant_flow.get_current_used_propellant_mass(time_since_ignition) == expected_mass
        assert constant_flow.get_total_propellant_mass() == expected_total_mass

# ============================== VARIABLE FLOW RATE TESTS ============================== #

@pytest.mark.parametrize("test_id, times_flow_rate, values_flow_rate, time_since_ignition, expected_flow, expected_mass, expected_total_mass", [
    # Happy path tests
    ("V1", np.array([0.0, 10.0, 20.0]), np.array([100.0, 50.0, 10.0]), 5.0, 75.0, 437.5, 1050.0),
    ("V2", np.array([0.0, 5.0, 10.0]), np.array([200.0, 100.0, 0.0]), 10.0, 0.0, 1000.0, 1000.0),
    # Edge cases
    ("V3", np.array([0.0, 10.0, 20.0]), np.array([100.0, 50.0, 10.0]), 20.0, 10.0, 1050.0, 1050.0),
    ("V4", np.array([0.0, 10.0, 20.0]), np.array([100.0, 50.0, 10.0]), 0.0, 100.0, 0.0, 1050.0),
    # Error cases
    ("V5", np.array([-1.0, 10.0, 20.0]), np.array([100.0, 50.0, 10.0]), 5.0, None, None, None),
    ("V6", np.array([0.0, 10.0, 20.0]), np.array([-100.0, 50.0, 10.0]), 5.0, None, None, None),
    ("V7", np.array([0.0, 10.0, 20.0]), np.array([100.0, 50.0, 10.0]), -1.0, None, None, None),
])
def test_variable_flow_rate(test_id, times_flow_rate, values_flow_rate, time_since_ignition, expected_flow, expected_mass, expected_total_mass):
    # Arrange
    if test_id.startswith("V5"):  # Invalid times for flow rate
        with pytest.raises(ValueError):
            VariableFlowRate(times_flow_rate=times_flow_rate, values_flow_rate=values_flow_rate)
        return
    elif test_id.startswith("V6"):  # Invalid values for flow rate
        with pytest.raises(ValueError):
            VariableFlowRate(times_flow_rate=times_flow_rate, values_flow_rate=values_flow_rate)
        return
    else:
        variable_flow = VariableFlowRate(times_flow_rate=times_flow_rate, values_flow_rate=values_flow_rate)

    # Act & Assert
    if test_id.startswith("V7"):  # Invalid time since ignition
        with pytest.raises(ValueError):
            variable_flow.get_current(time_since_ignition)
        with pytest.raises(ValueError):
            variable_flow.get_current_used_propellant_mass(time_since_ignition)
    else:
        assert variable_flow.get_current(time_since_ignition) == expected_flow
        assert variable_flow.get_current_used_propellant_mass(time_since_ignition) == expected_mass
        assert variable_flow.get_total_propellant_mass() == expected_total_mass
