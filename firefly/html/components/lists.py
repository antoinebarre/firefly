"""Collection of list components."""


from typing import Literal, Optional
import attrs

from ._render_tools import create_block
from .paragraph import validate_HTML_children

from .components import AdditionalFile, HTMLComponent
from .html_tag import HTMLOptions, HTMLTag


__all__ = ["OrderedList", "UnorderedList", "ListOptions"]

@attrs.define
class ListOptions(HTMLOptions):
    """
    Represents the options for a list HTML element.
    """
    type_: Optional[Literal["A", "a", "I", "i", "1"]] = attrs.field(
        default=None, # type: ignore
        metadata={'description': 'The type of the HTML tag used only for list items'},
        validator=attrs.validators.in_(["A", "a", "I", "i", "1"]),
        kw_only=True)

@attrs.define
class HTMLList(HTMLComponent):
    """
    Represents a list of HTML components to be rendered.

    Attributes:
        contents (list[HTMLComponent]): List of HTML components to be rendered.
        ordered (Optional[bool]): Whether the list is ordered or not.
        options (Optional[HTMLOptions]): The options of the list.
        indentation (int): The indentation size for the content.
    """
    contents: list[HTMLComponent] = attrs.field(
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)),
        kw_only=True)
    ordered: Optional[bool] = attrs.field(
        default=False, # type: ignore
        metadata={'description': 'Whether the list is ordered or not'},
        validator=attrs.validators.instance_of(bool), # type: ignore
        kw_only=True),
    options: Optional[ListOptions] = attrs.field(
        default=None,
        metadata={'description': 'The options of the list'},
        validator=attrs.validators.optional(attrs.validators.instance_of(ListOptions)),
        kw_only=True)
    indentation: int = attrs.field(
        metadata={'description': 'The indentation size for the content'},
        validator=attrs.validators.instance_of(int),
        default=4, # type: ignore
        kw_only=True) # type: ignore

    def render(self) -> str:
        """
        Renders the component and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """
        # Create the tag
        tag = self._create_tag()

        content_str = "".join(
            create_block(
                open_prefix="<li>",
                close_suffix="</li>",
                content=content.render(),
                inline=False,
            ) for content in self.contents
        )
        return create_block(
            open_prefix=tag.create_prefix_tag(),
            content=content_str,
            close_suffix=tag.create_suffix_tag(),
            indentation_size=self.indentation,
            inline=False)


    def _get_tag(self) -> str:
        """
        Returns the tag of the component.

        Returns:
            str: The tag of the component.
        """
        return "ol" if self.ordered else "ul"

    def _create_tag(self) -> HTMLTag:
        """
        Creates the tag of the component.

        Returns:
            HTMLTag: The tag of the component.
        """
        return HTMLTag(
            tag_name=self._get_tag(),
            options=self.options)

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files required by the component.

        Returns:
            list[AdditionalFile]: The list of additional files.
        """
        additional_files: list[AdditionalFile] = []
        for component in self.contents:
            additional_files += component.get_additional_files()
        return additional_files

def OrderedList(  # pylint: disable=invalid-name
    *items: HTMLComponent | str,
    options: Optional[ListOptions] = None) -> HTMLList:
    """
    Create an ordered list with the given items.

    Args:
        *items: The items to be included in the ordered list. Each item can be an
            HTMLComponent or a string.
        options: Optional ListOptions to customize the appearance of the ordered list.

    Returns:
        HTMLList: The created ordered list.

    """
    # change all string to html component
    components = validate_HTML_children(items)

    return HTMLList(
        contents=components,
        ordered=True,
        options=options)

def UnorderedList( # pylint: disable=invalid-name
    *items: HTMLComponent | str,
    options: Optional[ListOptions] = None) -> HTMLList:
    """
    Create an unordered list with the given items.

    Args:
        *items: Variable number of HTMLComponent or str objects representing the list items.
        options: Optional HTMLOptions object specifying additional options for the list.

    Returns:
        HTMLList: An HTMLList object representing the unordered list.
    """
    # change all string to html component
    components = validate_HTML_children(items)

    return HTMLList(
        contents=components,
        ordered=False,
        options=options)
