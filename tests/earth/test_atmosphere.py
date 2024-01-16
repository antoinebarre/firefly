import numpy as np
import pytest
from firefly.earth.atmosphere import USSA76, CurrentAtmosphericParameters
from firefly.earth.atmosphere import Atmosphere

# ============================= TYPE DEFINITION ============================ #
@pytest.mark.parametrize(
    "temperature, pressure, density, speed_of_sound, test_id",
    [
        (15.0, 101325.0, 1.225, 340.29, 'happy_case_typical_conditions'),
        (-56.5, 22632.1, 0.36391, 295.07, 'happy_case_high_altitude'),
        (40.0, 95000.0, 1.127, 354.94, 'happy_case_hot_weather'),
        (-25.0, 108900.0, 1.422, 320.54, 'happy_case_cold_weather'),
    ]
)
def test_current_atmospheric_parameters_happy_path(temperature, pressure, density, speed_of_sound, test_id):
    # Act
    current_atmosphere = CurrentAtmosphericParameters(
        temperature,
        pressure,
        density,
        speed_of_sound)

    # Assert
    assert current_atmosphere.temperature == temperature, f"Test failed for {test_id}: temperature mismatch"
    assert current_atmosphere.pressure == pressure, f"Test failed for {test_id}: pressure mismatch"
    assert current_atmosphere.density == density, f"Test failed for {test_id}: density mismatch"
    assert current_atmosphere.speed_of_sound == speed_of_sound, f"Test failed for {test_id}: speed_of_sound mismatch"

# Edge cases
@pytest.mark.parametrize(
    "temperature, pressure, density, speed_of_sound, test_id",
    [
        (0.0, 0.0, 0.0, 0.0, 'edge_case_zero_values'),
        (-273.15, 0.0, 0.0, 0.0, 'edge_case_absolute_zero_temperature'),
    ]
)
def test_current_atmospheric_parameters_edge_cases(temperature, pressure, density, speed_of_sound, test_id):
    # Act
    current_atmosphere = CurrentAtmosphericParameters(temperature, pressure, density, speed_of_sound)
    # Assert
    assert current_atmosphere.temperature == temperature, f"Test failed for {test_id}: temperature mismatch"
    assert current_atmosphere.pressure == pressure, f"Test failed for {test_id}: pressure mismatch"
    assert current_atmosphere.density == density, f"Test failed for {test_id}: density mismatch"
    assert current_atmosphere.speed_of_sound == speed_of_sound, f"Test failed for {test_id}: speed_of_sound mismatch"

# --------------------------------- MOCK UP -------------------------------- #

# Mock concrete class for Atmosphere to test abstract methods
class MockAtmosphere(Atmosphere):
    @property
    def max_altitude(self) -> float:
        return 100000.

    def current_parameters(
        self,
        altitude: float,
        with_warnings: bool
        ) -> CurrentAtmosphericParameters:
        return CurrentAtmosphericParameters(
            temperature=15.0,
            pressure=1,
            density=0,
            speed_of_sound=1000)  # Dummy value

    def validate_altitude(self, altitude2validate: float) -> float:
        return self._invalidate_negative_altitude(altitude2validate)

# Parametrized test for _invalidate_negative_altitude method
@pytest.mark.parametrize(
    "altitude, expected",
    [
        (0, 0),  # edge case: sea level
        (100, 100),  # happy path: within troposphere
        (100000, 100000),  # edge case: at the edge of space
    ],
    ids=["sea-level", "within-troposphere", "edge-of-space"]
)
def test_invalidate_negative_altitude(altitude, expected):
    # Arrange
    mock_atmosphere = MockAtmosphere()

    # Act
    validated_altitude = mock_atmosphere._invalidate_negative_altitude(altitude)

    # Assert
    assert validated_altitude == expected

# Parametrized test for _invalidate_negative_altitude method error cases
@pytest.mark.parametrize(
    "altitude",
    [
        (-1),  # below sea level
        (-10000),  # unrealistic negative value
    ],
    ids=["below-sea-level", "unrealistic-negative"]
)
def test_invalidate_negative_altitude_errors(altitude):
    # Arrange
    mock_atmosphere = MockAtmosphere()

    # Act & Assert
    with pytest.raises(ValueError):
        mock_atmosphere._invalidate_negative_altitude(altitude)

# Parametrized test for geometric to geopotential altitude conversion



# ============================= INTEGRATION TESTS ============================ #
# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_id, altitude, expected_parameters",
    [
        ("HP-01", 0, CurrentAtmosphericParameters(288.15, 101325, 1.225,340.29 )),
        ("HP-02", 11000, CurrentAtmosphericParameters(216.8, 22.7E3, 0.3648,295.15)),
        ("HP-03", 25000, CurrentAtmosphericParameters(221.6, 2.549E3, 0.040083, 298.39 )),
        ("HP-04", 50000, CurrentAtmosphericParameters(270.7, 79.77, 0.001027, 329.8 )),
        ("HP-05", 75000, CurrentAtmosphericParameters(208.4, 2.387, 3.990919E-5, 289.39 )),
        # ... add more test cases for other layers and altitudes within the range
        # see https://www.digitaldutch.com/atmoscalc/
        # https://www.translatorscafe.com/unit-converter/fr-FR/calculator/altitude/
    ],
)
def test_current_parameters_happy_path(test_id, altitude, expected_parameters):
    # Arrange
    ussa76 = USSA76()

    #altitude = ussa76.geopotential_to_geometric_altitude(altitude)

    # Act
    parameters = ussa76.current_parameters(altitude)

    # Assert
    assert parameters.temperature == pytest.approx(
        expected_parameters.temperature,
        rel=1e-3)
    assert parameters.pressure == pytest.approx(
        expected_parameters.pressure,
        rel=1e-3)
    assert parameters.density == pytest.approx(
        expected_parameters.density,
        rel=1e-3)
    assert parameters.speed_of_sound == pytest.approx(
        expected_parameters.speed_of_sound,
        rel=1e-4)


# Assuming the Atmosphere class has an attribute max_altitude and a private method _invalidate_negative_altitude
# and an instance variable __with_warnings that controls whether warnings are issued.

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "altitude, with_warnings, expected",
    [
        (10000, False, 10000),  # Below max, no warnings
        (500, True, 500),      # At max, no warnings
    ],
    ids=[f"{HAPPY_PATH_ID}_below_max_no_warnings", f"{HAPPY_PATH_ID}_at_max_no_warnings"]
)
def test_validate_altitude_happy_path(altitude, with_warnings, expected):
    # Arrange
    atmosphere = USSA76(with_warnings=with_warnings)

    # Act
    result = atmosphere.validate_altitude(altitude)

    # Assert
    assert result == expected, "The altitude should be validated correctly without warnings."

# Edge cases
@pytest.mark.parametrize(
    "altitude, with_warnings, expected_warning",
    [
        (100000, True, UserWarning),  # Just above max, with warnings
        (-1, False, ValueError),    # Negative altitude, no warnings
    ],
    ids=[f"{EDGE_CASE_ID}_just_above_max_with_warnings", f"{EDGE_CASE_ID}_negative_altitude_no_warnings"]
)
def test_validate_altitude_edge_cases(altitude, with_warnings, expected_warning):
    # Arrange
    atmosphere = USSA76(with_warnings=with_warnings)

# sourcery skip: no-conditionals-in-tests
    if expected_warning is not ValueError:
        # Act
        with pytest.warns(expected_warning):
            result = atmosphere.validate_altitude(altitude)
            # Assert
            assert result == altitude, "A warning should be issued for altitudes above the max."
    else:
        # Act & Assert
        with pytest.raises(expected_warning):
            atmosphere.validate_altitude(altitude)

# Error cases
@pytest.mark.parametrize(
    "altitude, with_warnings",
    [
        ("not_a_float", False),  # Altitude is not a float
    ],
    ids=[f"{ERROR_CASE_ID}_altitude_not_float"]
)
def test_validate_altitude_error_cases(altitude, with_warnings):
    # Arrange
    atmosphere = USSA76(with_warnings=with_warnings)

    # Act & Assert
    with pytest.raises(TypeError):
        atmosphere.validate_altitude(altitude)



# Assuming the get_index method is part of a class named Atmosphere
# If it's not, the staticmethod decorator should be removed and the method should be called directly.

@pytest.mark.parametrize("x, xlevels, expected_index, test_id", [
    # Happy path tests
    (5, [1, 4, 7, 10], 1, "happy_path_mid_range"),
    (1, [1, 3, 5, 7], 0, "happy_path_lower_bound"),
    (7, [1, 3, 5, 7], 3, "happy_path_upper_bound"),
    (0, [1, 3, 5, 7], 0, "happy_path_below_range"),
    (8, [1, 3, 5, 7], 3, "happy_path_above_range"),

    # Edge cases
    (1, [1], 0, "edge_case_single_element"),
    (2, [1, 3], 0, "edge_case_two_elements"),
    (3, [1, 3], 1, "edge_case_exact_match"),

    # Error cases
    # Assuming the method should handle non-numeric inputs and empty lists
    # If not, these tests should be omitted or adjusted to expect exceptions
    ("a", [1, 3, 5, 7], None, "error_case_non_numeric_x"),
    (5, [], None, "error_case_empty_xlevels"),
    (5, ["a", "b", "c"], None, "error_case_non_numeric_xlevels"),
])
def test_get_index(x, xlevels, expected_index, test_id):
    # Arrange
    # No arrangement needed as all input values are provided via test parameters

    # Act
    try:
        result = Atmosphere.get_index(x, np.array(xlevels))
    except Exception as e:
        result = e

    # Assert
    if test_id.startswith("error_case"):
        assert isinstance(result, Exception), f"Test ID: {test_id}"
    else:
        assert result == expected_index, f"Test ID: {test_id}"

@pytest.mark.parametrize("test_id, x, xlevels", [
    # Error cases
    ("ERR-1", 2.5, np.array([4.0, 3.0, 2.0, 1.0])),
    ("ERR-2", 2.5, np.array([2.0, 2.0, 2.0, 2.0])),
    ("ERR-3", 2.5, np.array([1.0, 1.0, 1.0, 1.0])),
])
def test_get_index_error_cases(test_id, x, xlevels):
    # Act and Assert
    with pytest.raises(ValueError) as exc_info:
        Atmosphere.get_index(x, xlevels)
    assert "strictly monotonic increasing" in str(exc_info.value), f"Test ID: {test_id}"
