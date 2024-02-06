

from pathlib import Path

from .list import validate_list


def validate_path(file_path: Path) -> Path:
    """
    Validate the given file path.

    Args:
        file_path (Path): The file path to validate.

    Returns:
        Path: The validated file path.

    Raises:
        TypeError: If the file path is not a string or a Path object.
    """
    try:
        file_path = Path(file_path)
        return file_path
    except TypeError as e:
        raise TypeError(
            "The file path must be a string or a Path object.",
            f"Received: {file_path}, type {type(file_path)}"
        ) from e


def validate_existing_file(file_path: Path) -> Path:
    """
    Validates the existence of a file at the given file path.

    Args:
        file_path (Path): The path to the file.

    Returns:
        Path: The validated file path.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    # validate path
    file_path = validate_path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return file_path


def validate_existing_directory(dir_path: Path) -> Path:
    """
    Validates the existence of a directory.

    Args:
        dir_path (Path): The path to the directory.

    Returns:
        Path: The validated directory path.

    Raises:
        FileNotFoundError: If the directory does not exist.
    """
    # validate path
    dir_path = validate_path(dir_path)

    if not dir_path.is_dir():
        raise FileNotFoundError(f"The directory {dir_path} does not exist.")
    return dir_path


def validate_file_extension(file_path: Path, extension: list[str]) -> Path:
    """
    Validates the file extension of a given file path.

    Args:
        file_path (Path): The path of the file to validate.
        extension (list[str]): A list of valid file extensions.

    Returns:
        Path: The validated file path.

    Raises:
        ValueError: If the file extension is not in the list of valid extensions.
    """

    # validate path
    file_path = validate_path(file_path)

    if file_path.suffix not in extension:
        raise ValueError(f"The file extension must be one of {extension}.")
    return file_path


def is_valid_files_extension(
    # END: be15d9bcejpp
    file_paths: list[Path],
    extension: list[str]
    ) -> list[bool]:
    """
    Check if the file extensions of the given file paths are valid.

    Args:
        file_paths (list[Path]): A list of file paths.
        extension (list[str]): A list of valid file extensions.

    Returns:
        list[bool]: A list of boolean values indicating whether each file path
        has a valid extension.
    """

    # validate inputs
    file_paths = validate_list(file_paths, Path)
    extension = validate_list(extension, str)

    return [file_path.suffix in extension for file_path in file_paths]
