"""Class to analyze and manage files in a safe way"""

import hashlib
from dataclasses import KW_ONLY, dataclass, field
from pathlib import Path
from typing import Callable

from firefly.validation.fileIO import validate_existing_file

__all__ = ["SafeFile", "md5_checksum", "sha256_checksum"]

def md5_checksum(file_path: Path) -> str:
    """
    Calculate the MD5 checksum of a existing file.

    Args:
        file_path (Path): The path of the file to calculate the checksum.

    Returns:
        str: The MD5 checksum.
    """

    # Validate the file path
    file_path = validate_existing_file(file_path)

    # Open the file
    with open(file_path, "rb") as file_content:
        # Read the file in chunks
        chunk = 0
        md5 = hashlib.md5()
        while chunk := file_content.read(8192):
            md5.update(chunk)
    # Return the checksum
    return md5.hexdigest()

def sha256_checksum(file_path: Path) -> str:
    """
    Calculate the SHA-256 checksum of a existing file.

    Args:
        file_path (Path): The path of the file to calculate the checksum.

    Returns:
        str: The SHA-256 checksum.
    """
    # Validate the file path
    file_path = validate_existing_file(file_path)

    # Open the file
    with open(file_path, "rb") as file_content:
        # Read the file in chunks
        chunk = 0
        sha256 = hashlib.sha256()
        while chunk := file_content.read(8192):
            sha256.update(chunk)
    # Return the checksum
    return sha256.hexdigest()

@dataclass(frozen=True)
class SafeFile:
    """
    Represents a safe file with a file path and checksum.

    Attributes:
        file_path (Path): The path to the file.
        checksum_method (Callable[[Path], str]): The method used to calculate
        the checksum. Default is md5_checksum.
        checksum (str): The calculated checksum of the file.

    Methods:
        __post_init__(): Validates the file path and calculates the checksum.
        __repr__(): Returns a string representation of the SafeFile object.
        __str__(): Returns a string representation of the SafeFile object.
    """
    file_path: Path
    _ : KW_ONLY
    checksum_method: Callable[[Path], str] = md5_checksum
    checksum: str = field(init=False)

    def __post_init__(self):
        # Calculate and set the checksum
        checksum_value = self.checksum_method(self.file_path)
        object.__setattr__(self, 'checksum', checksum_value)

    def __repr__(self) -> str:
        return f"SafeFile(file_path={self.file_path!r}, checksum={self.checksum!r})"

    def __str__(self) -> str:
        return f"SafeFile: {self.file_path} with checksum {self.checksum}"
