import pytest
import os
import hashlib
from pathlib import Path

from firefly.tools.files.__safe_file import sha256_checksum

def create_test_file(filename: str, content: bytes) -> Path:
    """Utility function to create a test file."""
    path = Path(filename)
    with open(path, "wb") as f:
        f.write(content)
    return path

def calculate_sha256_of_bytes(content: bytes) -> str:
    """Utility function to calculate SHA-256 checksum of bytes."""
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()

def test_sha256_checksum_small_file():
    """Test SHA-256 checksum calculation for a small file."""
    content = b"Hello, world!"
    test_file = create_test_file("small_test_file.txt", content)
    expected_checksum = calculate_sha256_of_bytes(content)
    assert sha256_checksum(test_file) == expected_checksum
    test_file.unlink()  # Cleanup

def test_sha256_checksum_large_file():
    """Test SHA-256 checksum calculation for a large file."""
    content = b"a" * 10000  # Larger than 8192 bytes
    test_file = create_test_file("large_test_file.txt", content)
    expected_checksum = calculate_sha256_of_bytes(content)
    assert sha256_checksum(test_file) == expected_checksum
    test_file.unlink()  # Cleanup

def test_sha256_checksum_empty_file():
    """Test SHA-256 checksum calculation for an empty file."""
    test_file = create_test_file("empty_test_file.txt", b"")
    expected_checksum = calculate_sha256_of_bytes(b"")
    assert sha256_checksum(test_file) == expected_checksum
    test_file.unlink()  # Cleanup

# Assuming validate_existing_file raises a ValueError for non-existent files
def test_sha256_checksum_non_existent_file():
    """Test SHA-256 checksum calculation for a non-existent file."""
    with pytest.raises(FileNotFoundError):
        sha256_checksum(Path("non_existent_file.txt"))

def test_sha256_checksum_binary_file():
    """Test SHA-256 checksum calculation for a binary file."""
    # This could be any binary content. Example: a small PNG or JPEG header
    content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    test_file = create_test_file("binary_test_file.png", content)
    expected_checksum = calculate_sha256_of_bytes(content)
    assert sha256_checksum(test_file) == expected_checksum
    test_file.unlink()  # Cleanup
