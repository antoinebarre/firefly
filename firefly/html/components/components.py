"""Basic classes for HTML components."""


from abc import ABC, abstractmethod
from pathlib import Path


import attrs

__all__ = ["AdditionalFile", "HTMLObject", "HTMLComponent"]


@attrs.define
class AdditionalFile():
    """
    Represents an additional file to be included in an HTML report.

    Attributes:
        original_path (Path): The original path of the file.
        published_directory (str): The directory where the file will be published
            within the HTML report.
    """

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
    published_filename: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={
            'description': 'The name of the file within the HTML report'
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

def render_HTML_components(components: list[HTMLComponent]) -> list[str]: # pylint: disable=invalid-name
    """
    Renders a list of HTML components.

    Args:
        components (list[HTMLComponent]): The list of HTML components to be rendered.

    Returns:
        list[str]: The rendered HTML components.
    """
    return [component.render() for component in components]

def collect_additional_files(components: list[HTMLComponent]) -> list[AdditionalFile]:
    """
    Collects additional files required by a list of HTML components.

    Args:
        components (list[HTMLComponent]): The list of HTML components.

    Returns:
        list[AdditionalFile]: A list of additional files required by the components.
    """
    additional_files = []
    for component in components:
        additional_files += component.get_additional_files()
    return additional_files
