import pytest
from firefly.validation.enum import DetailledEnum

# Define a sample DetailedEnum for testing purposes
class Color(DetailledEnum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

# Happy path tests with various realistic test values
@pytest.mark.parametrize("value, expected_enum", [
    ('red', Color.RED),  # ID: HP-1
    ('green', Color.GREEN),  # ID: HP-2
    ('blue', Color.BLUE),  # ID: HP-3
])
def test_detailed_enum_valid_values(value, expected_enum):
    # Act
    enum_member = Color(value)

    # Assert
    assert enum_member is expected_enum

# Edge cases
# Assuming edge cases for enums could include case sensitivity or type differences
@pytest.mark.parametrize("value", [
    ('RED',),  # ID: EC-1
    ('Green',),  # ID: EC-2
    (1,),  # ID: EC-3
    (None,),  # ID: EC-4
])
def test_detailed_enum_edge_cases(value):
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Color(value)

    # Assert
    assert str(exc_info.value) == f"{value} is not a valid Color. Valid types: 'red', 'green', 'blue'"


# Error cases
# Assuming error cases for enums could include completely invalid values
@pytest.mark.parametrize("value", [
    ('orange',),  # ID: ERR-1
    ('',),  # ID: ERR-2
    ('123',),  # ID: ERR-3
    ('undefined',),  # ID: ERR-4
])
def test_detailed_enum_error_cases(value):
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Color(value)

    # Assert
    assert str(exc_info.value) == f"{value} is not a valid Color. Valid types: 'red', 'green', 'blue'"
