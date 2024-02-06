import pytest
import numpy as np
from firefly.rocket.specific_impulse import NoSpecificImpulse, ConstantSpecificImpulse, VariableSpecificImpulse

# ======================== NoSpecificImpulse Tests ======================== #
@pytest.mark.parametrize("time_since_ignition, expected_output", [
    (0, 0.0),  # ID: Test-NoISP-TimeZero
    (1, 0.0),  # ID: Test-NoISP-PositiveTime
    (100, 0.0),  # ID: Test-NoISP-LargePositiveTime
])
def test_no_specific_impulse(time_since_ignition, expected_output):
    # Act
    no_isp = NoSpecificImpulse()
    result = no_isp.get_current(time_since_ignition)

    # Assert
    assert result == expected_output, "NoSpecificImpulse should always return 0.0"
    
def test_negative_time_error():
    # Assert
    with pytest.raises(ValueError):
        # Act
        NoSpecificImpulse().get_current(-1)

# ======================== ConstantSpecificImpulse Tests ======================== #
@pytest.mark.parametrize("specific_impulse, time_since_ignition, expected_output", [
    (300, 0, 300),  # ID: Test-ConstISP-TimeZero
    (300, 1, 300),  # ID: Test-ConstISP-PositiveTime
    (300, 100, 300),  # ID: Test-ConstISP-LargePositiveTime
])
def test_constant_specific_impulse(specific_impulse, time_since_ignition, expected_output):
    # Arrange
    const_isp = ConstantSpecificImpulse(specific_impulse=specific_impulse)

    # Act
    result = const_isp.get_current(time_since_ignition)

    # Assert
    assert result == expected_output, "ConstantSpecificImpulse should always return the same value"

@pytest.mark.parametrize("specific_impulse", [
    -1,  # ID: Test-ConstISP-NegativeValue
])
def test_constant_specific_impulse_negative_value_error(specific_impulse):
    # Assert
    with pytest.raises(ValueError):
        # Act
        ConstantSpecificImpulse(specific_impulse=specific_impulse)

# ======================== VariableSpecificImpulse Tests ======================== #
@pytest.mark.parametrize("time_specific_impulse, values_specific_impulse, time_since_ignition, expected_output", [
    (np.array([0, 1, 2]), np.array([300, 350, 400]), 0, 300),  # ID: Test-VarISP-TimeZero
    (np.array([0, 1, 2]), np.array([300, 350, 400]), 1, 350),  # ID: Test-VarISP-ExactTime
    (np.array([0, 1, 2]), np.array([300, 350, 400]), 1.5, 375),  # ID: Test-VarISP-InterpolatedTime
    (np.array([0, 1, 2]), np.array([300, 350, 400]), 3, 400),  # ID: Test-VarISP-ExtrapolatedTime
])
def test_variable_specific_impulse(time_specific_impulse, values_specific_impulse, time_since_ignition, expected_output):
    # Arrange
    var_isp = VariableSpecificImpulse(time_specific_impulse=time_specific_impulse, values_specific_impulse=values_specific_impulse)

    # Act
    result = var_isp.get_current(time_since_ignition)

    # Assert
    assert result == expected_output, "VariableSpecificImpulse should return the correct interpolated value"

@pytest.mark.parametrize("time_specific_impulse, values_specific_impulse", [
    (np.array([-1, 1, 2]), np.array([300, 350, 400])),  # ID: Test-VarISP-InvalidStartTime
    (np.array([0, 1, 2]), np.array([-300, 350, 400])),  # ID: Test-VarISP-NegativeISPValue
])
def test_variable_specific_impulse_value_error(time_specific_impulse, values_specific_impulse):
    # Assert
    with pytest.raises(ValueError):
        # Act
        VariableSpecificImpulse(time_specific_impulse=time_specific_impulse, values_specific_impulse=values_specific_impulse)
