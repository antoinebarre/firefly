"""Contains the HTML components for the title and CSS stylesheet of an HTML document."""

import importlib.resources as pkg_resources
from pathlib import Path
from typing import Optional
import attrs

from .components import AdditionalFile, HTMLComponent
from ._render_tools import create_block



@attrs.define
class PageTitle(HTMLComponent):
    """
    Represents the title of an HTML document in the Header.

    Attributes:
        title (str): The title of the HTML document.
    """
    title: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1),],
        metadata={'description': 'The title of the HTML document'},
        kw_only=True)

    def render(self) -> str:
        """
        Renders the title as an HTML string.

        Returns:
            str: The title as an HTML string.
        """
        return create_block(
            open_prefix="<title>",
            close_suffix="</title>",
            content=self.title.upper(),
            indentation_size=self._indent_value,
            inline=True
            ) + "\n" + create_block(
            open_prefix="<h1>",
            close_suffix="</h1>",
            content=self.title,
            inline=True)
    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the title component.

        :return: A list of AdditionalFile objects.
        """
        return []

@attrs.define
class CSSStyleSheet(HTMLComponent):
    """
    Represents a CSS stylesheet.

    Attributes:
        css_file_path (Path): The path to the CSS file.

    Methods:
        get_additional_files(): Returns a list of additional files associated
        with the CSS stylesheet.
        render(): Renders the CSS stylesheet as an HTML string.
    """

    css_file_path: Path = attrs.field(
        validator=attrs.validators.instance_of(Path),
        metadata={'description': 'The path to the CSS file'},
        kw_only=False)
    # constant
    __css_folder = "style"

    def __attrs_post_init__(self):
        """
        Checks if the stylesheet path is valid.
        Raises:
            FileNotFoundError: If the CSS file does not exist.
        """
        if not self.css_file_path.exists():
            raise FileNotFoundError(f"The CSS file {self.css_file_path} does not exist.")

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the CSS stylesheet.

        Returns:
            list[AdditionalFile]: A list of AdditionalFile objects.
        """
        return [AdditionalFile(
            original_path=self.css_file_path,
            published_directory=self.__css_folder,
            published_filename=self.css_file_path.name
        )]

    def render(self) -> str:
        """
        Renders the CSS stylesheet as an HTML string.

        Returns:
            str: The CSS stylesheet as an HTML string.
        """
        return ('<link rel="stylesheet" type="text/css"' +
            f' href="{self.__css_folder}/{self.css_file_path.name}">')

ALLOWED_COMPONENTS = (PageTitle,CSSStyleSheet)

@attrs.define
class HTMLHeader(HTMLComponent):
    """
    Represents the header component of an HTML document.

    Attributes:
        title (Optional[PageTitle]): The title of the HTML document.
        css (Optional[CSSStyleSheet]): The CSS stylesheet of the HTML document.
    """

    title : Optional[PageTitle] = attrs.field(
       default=None,
       metadata={'description': 'The title of the HTML document'},
       kw_only=True)
    css: Optional[CSSStyleSheet] = attrs.field(
        default=None,
        metadata={'description': 'The CSS stylesheet of the HTML document'},
        kw_only=True)

    def render(self) -> str:
        """
        Renders the header component.

        Returns:
            str: The rendered HTML code.
        """
        element2render = []
        for element in attrs.fields(self.__class__):
            component = getattr(self, element.name)
            if component is not None:
                element2render.append(component.render())
        return create_block(
            open_prefix="<head>",
            close_suffix="</head>",
            content="\n".join(element2render),
        )

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the header component.

        Returns:
            list[AdditionalFile]: A list of AdditionalFile objects.
        """
        additional_files = []
        for element in attrs.fields(self.__class__):
            component = getattr(self, element.name)
            if component is not None:
                additional_files.extend(component.get_additional_files())
        return additional_files


def create_header(
    *,
    title: Optional[str] = None,
    css_file_path: Optional[Path] = None,
    ) -> HTMLHeader:
    """
    Creates an HTML header component.

    Args:
        title (Optional[str], optional): The title of the HTML document. Defaults to None.
        css_file_path (Optional[Path], optional): The path to the CSS file. Defaults to None.

    Returns:
        HTMLHeader: The HTML header component.
    """
    title_component = PageTitle(title=title) if title else None
    css_component = myCSSStyleSheet()
    return HTMLHeader(title=title_component, css=css_component)


# TODO updgade this function to use the new HTMLDocument class
def myCSSStyleSheet():
    with pkg_resources.path("firefly.html.templates", "report.css") as css_path:
        # css_path is a Path object that can be used within this block
        return CSSStyleSheet(css_file_path=Path(css_path))
    
    