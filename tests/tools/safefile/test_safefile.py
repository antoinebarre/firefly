import pytest
from pathlib import Path

from firefly.tools.files.__safe_file import SafeFile

# Assuming md5_checksum is defined somewhere
def md5_checksum(file_path: Path) -> str:
    return "dummy_checksum"

# Fake checksum method for testing
def fake_checksum_method(file_path: Path) -> str:
    return "fake_checksum"

def test_safe_file_with_default_checksum_method(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, world!")

    # Test SafeFile with the default checksum method
    safe_file = SafeFile(file_path=test_file, checksum_method=md5_checksum)
    assert safe_file.checksum == "dummy_checksum", "Checksum should match the dummy checksum"

def test_safe_file_with_custom_checksum_method(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, pytest!")

    # Test SafeFile with a custom checksum method
    safe_file = SafeFile(file_path=test_file, checksum_method=fake_checksum_method)
    assert safe_file.checksum == "fake_checksum", "Checksum should match the fake checksum"

def test_safe_file_repr_and_str_methods(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Testing repr and str")

    # Test the __repr__ and __str__ methods
    safe_file = SafeFile(file_path=test_file, checksum_method=md5_checksum)
    expected_repr = f"SafeFile(file_path={test_file!r}, checksum='dummy_checksum')"
    assert repr(safe_file) == expected_repr, "__repr__ does not match expected representation"
    
    expected_str = f"SafeFile: {test_file} with checksum dummy_checksum"
    assert str(safe_file) == expected_str, "__str__ does not match expected string representation"

