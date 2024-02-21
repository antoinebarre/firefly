"""Collections of Classes and Functions to work with HTML documents."""

from pathlib import Path
from typing import Protocol

import attrs
from firefly.tools.files import copy_file

from firefly.validation.fileIO import validate_file_extension

from .components import AdditionalFile

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
        components (list[HTMLComponent]): List of HTML components to be rendered.
        additional_files (list[AdditionalFile]): List of additional files to be published.

    Methods:
        add_component(component: HTMLComponent) -> None: Adds a component to the list o
            components and updates the additional files.
        get_html_content() -> str: Returns the HTML content of the document.
        publish(htlm_file_path: Path) -> None: Publishes the HTML content to the
            specified file path.
    """

    
    components: list[HTMLComponent] = attrs.field(
        default=[],
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)), # type: ignore
        kw_only=True)
    additional_files: list[AdditionalFile] = attrs.field(
        default=[],
        metadata={'description': 'List of additional files to be published'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(AdditionalFile)), # type: ignore
        kw_only=True)

    def add_component(self, component: HTMLComponent):
        """
        Adds a component to the list of components and updates the additional files.

        Args:
            component (HTMLComponent): The component to be added.

        Returns:
            None
        """
        self.components.append(component)
        self.additional_files.extend(component.get_additional_files())

    def get_html_content(self) -> str:
        """
        Returns the HTML content of the document.

        Returns:
            str: The HTML content of the document.
        """
        return "".join(component.render() for component in self.components)

    def publish(self, htlm_file_path: Path, exist_ok: bool = False):
        """
        Publishes the HTML content to the specified file path.

        Args:
            htlm_file_path (Path): The file path where the HTML content will be published.

        Raises:
            FileExistsError: If the file already exists at the specified file path.
        """
        # validate the file path
        htlm_file_path = validate_file_extension(
            file_path=htlm_file_path,
            extension=ALLOWED_HTML_EXTENSIONS)

        # validate non existing file
        if htlm_file_path.exists() and not exist_ok:
            raise FileExistsError(f"The file {htlm_file_path} already exists.")

        # create target directory
        target_directory = htlm_file_path.parent

        html_content = self.get_html_content()
        # write the content to the file
        htlm_file_path.write_text(html_content, encoding='utf-8')

        # publish additional files
        for file in self.additional_files:
            published_path = target_directory / file.get_published_directory() / file.get_filename()
            # copy the file
            _  = copy_file(
                source_path=file.get_original_path(),
                destination_path=published_path)


#         # render the HTML document
#         html = f"""<!DOCTYPE html>

# # @attrs.define
# # class HTMLReporter():
# #     title: str = attrs.field(
# #         validator=attrs.validators.instance_of(str),
# #         metadata={'description': 'Title of the HTML page'},
# #         kw_only=True)
# #     content: list[HTMLComponent] = attrs.field(default=[],
# #         metadata={'description': 'List of HTML components to be rendered'},
# #         validator=attrs.validators.deep_iterable(
# #             member_validator=attrs.validators.instance_of(HTMLComponent)),
# #         kw_only=True)
# #     additional_files: list[Path] = attrs.field(default=[],
# #         metadata={'description': 'List of additional files to be published'},
# #         validator=attrs.validators.deep_iterable(
# #             member_validator=attrs.validators.instance_of(AdditionalFile)),
# #         kw_only=True)
# #     def render(self) -> str:
# #         html = f"""<!DOCTYPE html>
# # <html>
# # <head>
# #     <title>{self.title.upper()}</title>
# # </head>
# # <body>
# # """
# #         for component in self.content:
# #             html += component.render()
# #         html += """</body>
# # </html>"""
