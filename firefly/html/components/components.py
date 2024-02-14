


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import attrs

__all__ = ["AdditionalFile", "HTMLObject", "HTMLComponent"]


@attrs.define
class AdditionalFile():
    original_path: Path = attrs.field(
        validator=attrs.validators.instance_of(Path),
        metadata={'description': 'Original path of the file'},
        kw_only=True)
    published_directory: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={
            'description': 'Directory where the file will be published within the HTML report'
            },
        kw_only=True)

    def get_original_path(self) -> Path:
        """
        Returns the original path of the file.

        Returns:
            Path: The original path of the file.
        """
        return self.original_path

    def get_published_directory(self) -> str:
        """
        Returns the directory where the file will be published within the HTML report.

        Returns:
            str: The directory where the file will be published within the HTML report.
        """
        return self.published_directory

    def get_filename(self) -> str:
        """
        Returns the name of the file associated with this object.

        Returns:
            str: The name of the file.
        """
        return self.original_path.name

    @property
    def filename(self) -> str:
        """
        Returns the name of the file associated with this object.

        :return: The name of the file.
        :rtype: str
        """
        return self.original_path.name

class HTMLObject(ABC):
    """
    Base class for HTML objects.
    """
    _indent_value: int = 4

    @abstractmethod
    def render(self) -> str:
        """
        Renders the HTML object.

        Returns:
            str: The rendered HTML.
        """

    # @staticmethod
    # def _validate_non_empty_string(
    #     instance: Any,  # pylint: disable=unused-argument
    #     attribute: attrs.Attribute,  # pylint: disable=unused-argument
    #     value: str):
    #     value = validate_string(value, empty_allowed=False)
    #     if "<" in value or ">" in value:
    #         raise ValueError(
    #             "HTML Tag Value cannot contain '<' or '>' characters." +
    #             f"Got: {value}")
    #     return value

class HTMLComponent(HTMLObject, ABC):
    """
    Represents an HTML component.

    This class is an abstract base class (ABC) that provides a common interface
    for all HTML components.
    Subclasses must implement the `publish_additional_files` method to publish
    additional files required by the HTML component.

    Attributes:
        None

    Methods:
        publish_additional_files: Publishes additional files required by the HTML component.
        render: Renders the HTML component.
    """

    @abstractmethod
    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Publishes additional files required by the HTML component.

        Args:
            path (Path): The path where the additional files should be published.

        Returns:
            list[AdditionalFile]: A list of additional files published.

        """
        