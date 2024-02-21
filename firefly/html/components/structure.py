"""Collection of structure components for HTML"""

from dataclasses import dataclass, field
from typing import Optional
import warnings

from firefly.html.components.components import AdditionalFile, HTMLComponent
from firefly.html.components.paragraph import validate_HTML_children
from firefly.tools.strings import indent
from ._render_tools import create_block


@dataclass
class Article(HTMLComponent):
    """
    Represents an article component in HTML structure.

    Attributes:
        title (str): The title of the article.
        class_ (Optional[str]): The optional CSS class for the article.
        _content (list[HTMLComponent]): The list of child components.
        _level (int): The level of the article heading.

    Methods:
        set_level(level: int) -> None: Sets the level of the article heading.
        get_additional_files() -> list[AdditionalFile]: Returns the additional files
            required by the article.
        add_components(*component: HTMLComponent | str) -> None: Adds components to the article.
        render() -> str: Renders the article as HTML string.
        __set_children_level() -> None: Sets the level of the child articles.
        __get_title() -> str: Returns the HTML title tag for the article.
    """
    title: str
    _content: list[HTMLComponent] = field(default_factory=list, init=False)
    _level: int = field(init=False, default=1)
    class_: Optional[str] = field(default=None, init=True)

    def set_level(self, level: int) -> None:
        """
        Set the level of the structure.

        Args:
            level (int): The level to set.

        Returns:
            None
        """
        self._level = level

    def __set_children_level(self) -> None:
        if self._content:
            for component in self._content:
                if isinstance(component, Article):
                    # check maximum level
                    if self._level < 6:
                        component.set_level(self._level + 1)
                    else:
                        component.set_level(6)
                        warnings.warn(
                            "The maximum level of heading is 6.")

    def __get_title(self) -> str:
        return f"<h{self._level}>{self.title}</h{self._level}>\n"

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files required by the structure and its components.

        Returns:
            list[AdditionalFile]: A list of AdditionalFile objects representing
                the additional files.
        """
        additional_files = []
        if self._content:
            for component in self._content:
                additional_files.extend(component.get_additional_files())
        return additional_files

    def add_components(
                self,
                *component: HTMLComponent | str,
                ) -> None :
        """
        Add HTML or string components to the structure.

        Args:
            *component (HTMLComponent | str): The HTML components or strings to be added.

        Returns:
            None
        """
        # change all strings to Text components
        components = validate_HTML_children(component)

        self._content += components


    def render(self) -> str:
        """
        Render the structure component as an HTML article.

        Returns:
            str: The rendered HTML article.
        """
        # set the children article level to the current level + 1
        self.__set_children_level()

        if self._content:
            content_str =  (self.__get_title() +
                            "".join([component.render() for component in self._content]))
        else:
            content_str = self.__get_title()

        # create the class attribute
        class_attr = f' class="{self.class_}"' if self.class_ else ''

        return create_block(
            open_prefix=f"<article{class_attr}>",
            close_suffix="</article>",
            content = indent(content_str, self._indent_value),
            inline=False
        )
