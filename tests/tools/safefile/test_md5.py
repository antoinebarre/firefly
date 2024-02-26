import pytest
import hashlib
from pathlib import Path
from firefly.validation.fileIO import validate_existing_file
from firefly.tools.files.__safe_file import md5_checksum

# Define a fixture for creating a temporary file with content
@pytest.fixture
def temp_file(tmp_path, request):
    content = request.param.get("content", "")
    file = tmp_path / request.param.get("filename", "test_file.txt")
    file.write_bytes(content.encode())
    return file

# Happy path tests with various realistic test values
@pytest.mark.parametrize("temp_file, expected_md5", [
    ({"content": "Hello, World!", "filename": "hello.txt"}, "65a8e27d8879283831b664bd8b7f0ad4"),
    ({"content": "Another example with more text.", "filename": "example.txt"}, "12677806b89e4e478094f3f0147d8391"),
    ({"content": "", "filename": "empty.txt"}, "d41d8cd98f00b204e9800998ecf8427e"),
], ids=["happy-hello", "happy-example", "happy-empty"], indirect=["temp_file"])
def test_md5_checksum_happy_path(temp_file, expected_md5):
    # Act
    result = md5_checksum(temp_file)

    # Assert
    assert result == expected_md5, f"MD5 checksum for {temp_file.name} should be {expected_md5}"

# Edge cases
@pytest.mark.parametrize("temp_file, expected_md5", [
    ({"content": "a" * 8192, "filename": "exact_block_size.txt"}, hashlib.md5(("a" * 8192).encode()).hexdigest()),
    ({"content": "a" * (8192 + 1), "filename": "just_over_block_size.txt"}, hashlib.md5(("a" * (8192 + 1)).encode()).hexdigest()),
], ids=["edge-exact-block-size", "edge-just-over-block-size"], indirect=["temp_file"])
def test_md5_checksum_edge_cases(temp_file, expected_md5):
    # Act
    result = md5_checksum(temp_file)

    # Assert
    assert result == expected_md5, f"MD5 checksum for {temp_file.name} should be {expected_md5}"

