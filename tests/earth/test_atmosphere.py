import pytest
import warnings
from firefly.geography.atmosphere import USSA76, CurrentAtmosphericParameters

# Assuming CurrentAtmosphericParameters is a simple data class that holds
# temperature, pressure, and density

# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_id, altitude, expected_parameters",
    [
        ("HP-01", 0, CurrentAtmosphericParameters(288.15, 101325, 1.225)),
        ("HP-02", 11000, CurrentAtmosphericParameters(216.65, 22632.1, 0.36391)),
        ("HP-03", 20000, CurrentAtmosphericParameters(216.65, 5474.89, 0.08803)),
        ("HP-04", 50000, CurrentAtmosphericParameters(270.65, 75.9448, 0.000977525)),
        # ... add more test cases for other layers and altitudes within the range
        # see https://www.digitaldutch.com/atmoscalc/
    ],
)
def test_current_parameters_happy_path(test_id, altitude, expected_parameters):
    # Arrange
    ussa76 = USSA76()

    # Act
    parameters = ussa76.current_parameters(altitude)

    # Assert
    assert parameters.temperature == pytest.approx(expected_parameters.temperature)
    assert parameters.pressure == pytest.approx(expected_parameters.pressure)
    assert parameters.density == pytest.approx(expected_parameters.density)

# Edge cases
@pytest.mark.parametrize(
    "test_id, altitude, expected_layer_index",
    [
        ("EC-01", -1, 0),  # Below the first layer
        ("EC-02", 71000, 6),  # At the start of the last layer
        ("EC-03", 86000, 6),  # At the maximum altitude
        # ... add more edge cases if necessary
    ],
)
def test_get_layer_edge_cases(test_id, altitude, expected_layer_index):
    # Arrange
    ussa76 = USSA76()

    # Act
    layer_index = ussa76._USSA76__get_layer(altitude)  # Accessing the private method directly for testing

    # Assert
    assert layer_index == expected_layer_index

# Error cases
@pytest.mark.parametrize(
    "test_id, altitude",
    [
        ("ER-01", -100),  # Negative altitude
        ("ER-02", 100000),  # Altitude above the maximum
        # ... add more error cases if necessary
    ],
)
def test_validate_altitude_error_cases(test_id, altitude):
    # Arrange
    ussa76 = USSA76()

    # Act
    with pytest.warns(UserWarning):
        valid_altitude = ussa76.validate_altitude(altitude)

    # Assert
    if altitude < 0:
        assert valid_altitude == 0
    else:
        assert valid_altitude == altitude
