"""Generic HTML component that can be used to render any HTML tag with any content"""

import attrs

from ._render_tools import create_block

from .components import AdditionalFile, HTMLComponent
from .html_tag import HTMLTag


@attrs.define
class HTMLGenericComponent(HTMLComponent):
    """
    Represents a generic HTML component.

    Attributes:
        tag (HTMLTag): The HTML tag to be rendered.
        contents (list[HTMLComponent]): List of HTML components to be rendered.
        indentation (int): The indentation size for the content.
    """

    tag: HTMLTag = attrs.field(
        validator=attrs.validators.instance_of(HTMLTag),
        metadata={'description': 'The HTML tag to be rendered'},
        kw_only=True)

    contents: list[HTMLComponent] = attrs.field(
        default=[],
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)),
        kw_only=True)

    indentation: int = attrs.field(
        metadata={'description': 'The indentation size for the content'},
        validator=attrs.validators.instance_of(int),
        default=4, # type: ignore
        kw_only=True) # type: ignore

    inline: bool = attrs.field(
        metadata={'description': 'Whether to render the content inline or not'},
        validator=attrs.validators.instance_of(bool),
        default=False, # type: ignore
        kw_only=True)

    def render(self) -> str:
        """
        Renders the component and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """
        content_str = ''.join([child.render() for child in self.contents])
        return create_block(
            open_prefix=self.tag.create_prefix_tag(),
            content=content_str,
            close_suffix=self.tag.create_suffix_tag(),
            indentation_size=self.indentation,
            inline=self.inline)

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files required by the component.

        Returns:
            list[AdditionalFile]: A list of AdditionalFile objects.
        """
        additional_files: list[AdditionalFile] = []
        for component in self.contents:
            additional_files += component.get_additional_files()

        return additional_files
