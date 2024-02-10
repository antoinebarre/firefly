""" File and directory I/O tools."""

from pathlib import Path
import shutil

from firefly.validation.fileIO import validate_path

def copy_file(*,
    source_path: Path,
    destination_path: Path) -> Path:
    """
    Copy a file from the source path to the destination path.

    Args:
        source_path (Path): The path of the source file.
        destination_path (Path): The path of the destination file.

    Returns:
        Path: The path of the copied file.

    Raises:
        FileNotFoundError: If the source file does not exist.
        FileExistsError: If the destination file already exists.
    """
    # Validate the file paths
    source_path = validate_path(source_path)
    destination_path = validate_path(destination_path)

    # Check if the source file exists
    if not source_path.exists():
        raise FileNotFoundError(f"The file {source_path} does not exist.")

    # Check if the destination file exists
    if destination_path.exists():
        raise FileExistsError(f"The file {destination_path} already exists.")

    # Create the destination directory if it does not exist
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy the file
    shutil.copyfile(source_path, destination_path)

    return destination_path

def delete_folder(*,
    folder_path: Path) -> None:
    """
    Delete a folder and its contents.

    Args:
        folder_path (Path): The path of the folder to be deleted.

    Returns:
        None

    Raises:
        FileNotFoundError: If the folder does not exist.
    """
    # Validate the folder path
    folder_path = validate_path(folder_path)

    # Check if the folder exists
    if not folder_path.exists() and not folder_path.is_dir():
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")

    # Delete the folder and its contents
    shutil.rmtree(folder_path)


def write_string_to_file(*,
    file_path: Path,
    content: str,
    exist_ok:bool = False,
    ) -> Path:
    """
    Write a string to a file.

    Args:
        file_path (Path): The path of the file.
        content (str): The content to be written to the file.
        exist_ok (bool, optional): If True, allows overwriting an existing file. Defaults to False.

    Returns:
        Path: The path of the written file.

    Raises:
        FileExistsError: If the file already exists.
    """
    # Validate the file path
    file_path = validate_path(file_path)

    # Check if the file already exists
    if file_path.exists() and not exist_ok:
        raise FileExistsError(f"The file {file_path} already exists.")

    # Create the file directory if it does not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path