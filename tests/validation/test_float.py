from firefly.validation import validate_float

def test_validate_float():
    # Test valid float value
    assert validate_float(3.14) == 3.14

    # Test valid integer value
    assert validate_float(5) == 5.0

    # Test valid string value
    assert validate_float("2.718") == 2.718

    # Test invalid value
    try:
        validate_float("abc")
    except TypeError as e:
        assert str(e) == "value must be a float or convertible to a float. Got abc - <class 'str'>"
    else:
        assert False, "Expected TypeError to be raised for invalid value"