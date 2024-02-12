""" Collection of markdown elements."""


from abc import ABC, abstractmethod
from dataclasses import KW_ONLY
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field, field_validator
from firefly.tools.files import copy_file

from firefly.validation.fileIO import validate_file_extension

__all__ = [
    "AcronymMarkdown",
    "ImageMarkdown",
    "MarkdownContent",
    "MarkdownElement",
    "MarkdownText",
    "MarkdownParagraph",
    "MarkdownTitle",
    "MarkdownPageTitle"
]


class MarkdownContent(BaseModel):
    """
    Represents a piece of Markdown content with a header, content, and footer.
    """

    header: str = ""
    content: str = ""
    footer: str = ""

    def __str__(self) -> str:
        """
        Returns a string representation of the MarkdownContent object.
        """
        return f"{self.header}\n\n{self.content}\n\n{self.footer}"

    def __add__(self, other: Any) -> "MarkdownContent":
        """
        Adds two MarkdownContent objects together, concatenating their content and footer.
        If the other object is not a MarkdownContent, raises a TypeError.
        """
        if isinstance(other, MarkdownContent):
            return MarkdownContent(
                header=other.header if other.header != "" else self.header,
                content=self.content + other.content,
                footer=self.footer + other.footer
            )
        raise TypeError(f"Cannot add {type(other)} to MarkdownContent.")

class MarkdownElement(ABC,BaseModel):
    """
    Represents a base class for Markdown elements.
    """

    @abstractmethod
    def publish(self) -> MarkdownContent:
        """
        Publishes the Markdown element, and copy if necessary the additional files (e.g image)
        to the specified directory path.

        Args:
            directory_path (Path): The directory path where the Markdown element will be published.

        Returns:
            MarkdownContent: The published Markdown content.
        """

    @abstractmethod
    def export_additional_files(self, directory_path: Path) -> list[Path]:
        """
        Export additional files to the specified directory.

        Args:
            directory_path (Path): The directory path to export the files to.

        Returns:
            list[Path]: A list of paths to the exported files.
        """

class AcronymMarkdown(MarkdownElement,BaseModel):
    """
    Represents an acronym in Markdown format.

    Attributes:
        title (str): The title of the acronym.
        definition (str): The definition of the acronym.
    """
    _: KW_ONLY
    title: str
    definition: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        """
        Validate the title.

        Args:
            value (str): The title to be validated.

        Raises:
            ValueError: If the title is empty.

        Returns:
            str: The validated title.
        """
        if not value:
            raise ValueError("The title cannot be empty.")
        return value

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, value: str):
        """
        Validates the definition of an element.

        Args:
            value (str): The definition to be validated.

        Raises:
            ValueError: If the definition is empty.

        Returns:
            str: The validated definition.
        """
        if not value:
            raise ValueError("The definition cannot be empty.")
        return value

    def publish(self) -> MarkdownContent:
        return MarkdownContent(
            footer=f"*[{self.title}]: {self.definition}\n"
        )

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []

class ImageMarkdown(MarkdownElement,BaseModel):
    """
    Represents an image markdown element.

    Attributes:
        original_path (Path): The path to the original image file.
        replacement_text (str): The replacement text for the image.
    Methods:
        validate_original_path(cls, value: Path) -> Path: Validates the original image path.
        copy_image(directory_path: Path) -> Path: Copies the original image to
            the specified directory.
        publish(directory_path: Path) -> MarkdownContent: Publishes the image markdown content.
    """
    _: KW_ONLY
    original_path: Path
    replacement_text: str = ""
    _imageFolderName: str = "images"

    @field_validator("original_path")
    @classmethod
    def validate_original_path(cls, value:Path):
        """
        Validates the original path of an image.

        Args:
            value (Path): The path to the image file.

        Raises:
            FileNotFoundError: If the image file does not exist.

        Returns:
            Path: The validated path to the image file.
        """
        if not value.is_file():
            raise FileNotFoundError(f"The Image {value} does not exist.")
        value = validate_file_extension(value, [".png", ".jpg", ".jpeg", ".gif", ".svg"])
        return value

    def copy_image(self, directory_path: Path) -> Path:
        """
        Copy the original image to the specified directory.

        Args:
            directory_path (Path): The path to the target directory.

        Returns:
            Path: The path to the copied image file.
        """
        # create the target directory if it does not exist
        target_path = directory_path / self._imageFolderName

        # get the filename and extension of the original image
        new_file_path = target_path / self.original_path.name

        # copy the file to the target directory
        new_file_path = copy_file(
            source_path=self.original_path,
            destination_path=new_file_path,
        )
        return new_file_path

    def publish(self) -> MarkdownContent:
        return MarkdownContent(
            content=f"![{self.replacement_text}]({self._imageFolderName}/{self.original_path.name})"
        )

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return [self.copy_image(directory_path)]

class MarkdownNewLine(MarkdownElement):
    """
    Represents a new line in Markdown format.
    """
    def publish(self) -> MarkdownContent:
        return MarkdownContent(content="  \n")

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []


class MarkdownText(MarkdownElement,BaseModel):
    """
    Represents a Markdown text equivalent to a sentence.

    Attributes:
        content (str): The Markdown content.
    """
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str):
        """
        Validate the content of an element.

        Args:
            value (str): The content to be validated.

        Raises:
            ValueError: If the content is empty.

        Returns:
            str: The validated content.
        """
        if not value:
            raise ValueError("The content cannot be empty.")
        return value

    def publish(self) -> MarkdownContent:
        return MarkdownContent(content=self.content)

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []

class MarkdownParagraph(MarkdownElement,BaseModel):
    """
    Represents a Markdown paragraph.

    Attributes:
        content (str): The Markdown content.
    """
    _: KW_ONLY
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str):
        """
        Validates the content of an element.

        Args:
            value (str): The content to be validated.

        Raises:
            ValueError: If the content is empty.

        Returns:
            str: The validated content.
        """
        if not value:
            raise ValueError("The content cannot be empty.")
        return value

    def publish(self) -> MarkdownContent:
        return MarkdownContent(content="\n\n" + self.content + "\n")

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []

class MarkdownTitle(MarkdownElement,BaseModel):
    """
    Represents a markdown title element.

    Attributes:
        level (int): The level of the title, ranging from 1 to 6.
        title (str): The text of the title.

    Methods:
        validate_title(cls, value: str): Validates the title value.
        publish(directory_path: Path) -> MarkdownContent: Publishes the markdown content.

    Example:
        title = MarkdownTitle(level=1, title="Hello World")
        title.publish(directory_path)
    """
    _: KW_ONLY
    level: int = Field(1, ge=1, le=6)
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        """
        Validate the title.

        Args:
            value (str): The title to be validated.

        Raises:
            ValueError: If the title is empty.

        Returns:
            str: The validated title.
        """
        if not value:
            raise ValueError("The title cannot be empty.")
        return value

    def publish(self) -> MarkdownContent:
        return MarkdownContent(
            content=f"\n{'#' * self.level} {self.title.capitalize()}\n")

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []

class MarkdownPageTitle(MarkdownElement,BaseModel):
    """
    Represents a title for a Markdown page.

    Attributes:
        title (str): The title of the page.
    """
    _: KW_ONLY
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        """
        Validates the title value.

        Args:
            value (str): The title value to validate.

        Raises:
            ValueError: If the title is empty.

        Returns:
            str: The validated title value.
        """
        if not value:
            raise ValueError("The title cannot be empty.")
        return value

    def publish(self) -> MarkdownContent:
        """
        Publishes the Markdown page title.

        Args:
            directory_path (Path): The directory path where the Markdown page will be published.

        Returns:
            MarkdownContent: The published Markdown content.
        """
        return MarkdownContent(header=f"# {self.title.upper()}\n")

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []
