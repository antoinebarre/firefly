"""Collections of Classes and Functions to work with HTML documents."""


from pathlib import Path
from typing import Protocol

import attrs

from firefly.tools.files import copy_file
from firefly.validation.fileIO import validate_file_extension

from .components import AdditionalFile
from .components._render_tools import create_block
from .components.title import  HTMLHeader

__all__ = ["HTMLDocument","HTMLComponent"]

# allowed file extensions
ALLOWED_HTML_EXTENSIONS = ['.html', '.htm']

class HTMLComponent(Protocol):
    """
    Represents an HTML component.

    This protocol defines the methods that a class must implement to be
    considered an HTML component.
    """
    def render(self) -> str:
        """
        Render the object and return it as a string.

        Returns:
            str: The rendered object as a string.
        """
        ... # pylint: disable=unnecessary-ellipsis

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the object.

        :return: A list of AdditionalFiles objects.
        """
        ... # pylint: disable=unnecessary-ellipsis

@attrs.define
class HTMLDocument:
    """
    Represents an HTML document.

    Attributes:
        _header (HTMLHeader): The header of the HTML document.
        _components (list[HTMLComponent]): List of HTML components to be rendered.
        _additional_files (list[AdditionalFile]): List of additional files to be published.

    Public Methods:
        add_component(component: HTMLComponent) -> None: Adds a component to the list
        of components and updates the additional files.
        add_header(header: HTMLHeader) -> None: Adds a header to the document.
        get_body_html_content() -> str: Returns the HTML content of the document's body.
        get_html() -> str: Returns the HTML content of the document.
        publish(htlm_file_path: Path, exist_ok: bool = False) -> None: Publishes the HTML
        content to the specified file path.
    """
    _header : HTMLHeader = attrs.field(
        default=None,
        metadata={'description': 'The header of the HTML document'},
        validator=attrs.validators.optional(
            attrs.validators.instance_of(HTMLHeader)),
        kw_only=True)
    _components: list[HTMLComponent] = attrs.field(
        default=[], # type: ignore
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)), # type: ignore
        kw_only=True)
    _additional_files: list[AdditionalFile] = attrs.field(
        default=[],
        metadata={'description': 'List of additional files to be published'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(AdditionalFile)),
        kw_only=True)

    def add_component(self, component: HTMLComponent):
        """
        Adds a component to the list of components and updates the additional files.

        Args:
            component (HTMLComponent): The component to be added.

        Returns:
            None
        """
        self._components.append(component)
        self._additional_files.extend(component.get_additional_files())

    def add_header(self, header: HTMLHeader):
        """
        Adds a header to the document.

        Args:
            header (HTMLHeader): The header to be added.

        Returns:
            None
        """
        self._header = header
        self._additional_files.extend(header.get_additional_files())

    def get_body_html_content(self) -> str:
        """
        Returns the HTML content of the document's body.

        Returns:
            str: The HTML content of the document.
        """
        return "".join(component.render() for component in self._components)

    def get_html(self) -> str:
        """
        Returns the HTML content of the document.

        Returns:
            str: The HTML content of the document.
        """
        header_content = self._header.render() if self._header else ""
        body_content = create_block(
            open_prefix="<body>",
            close_suffix="</body>",
            content=self.get_body_html_content()
        )
        return create_block(
            open_prefix="<html>",
            close_suffix="</html>",
            content=header_content + body_content
        )

    def publish(self, htlm_file_path: Path, exist_ok: bool = False):
        """
        Publishes the HTML content to the specified file path.

        Args:
            htlm_file_path (Path): The file path where the HTML content will be published.
            exist_ok (bool, optional): If True, allows overwriting an existing file. Defaults to False.

        Raises:
            FileExistsError: If the file already exists at the specified file path.
        """
        # validate the file path
        htlm_file_path = validate_file_extension(
            file_path=htlm_file_path,
            extension=ALLOWED_HTML_EXTENSIONS)

        # validate non existing file
        if htlm_file_path.exists() and exist_ok is False:
            raise FileExistsError(f"The file {htlm_file_path} already exists.")

        # create target directory
        target_directory = htlm_file_path.parent

        #create directory if it does not exist
        target_directory.mkdir(parents=True, exist_ok=True)

        #create the HTML block with the header and the body
        html_content = self.get_html()

        # add the doctype
        html_content = f"<!DOCTYPE html>\n{html_content}"

        # write the content to the file
        htlm_file_path.write_text(html_content, encoding='utf-8')

        # publish additional files
        for file in self._additional_files:
            published_path = target_directory / file.get_published_directory() / file.get_filename()
            # copy the file
            _  = copy_file(
                source_path=file.get_original_path(),
                destination_path=published_path)