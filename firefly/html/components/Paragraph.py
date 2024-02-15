"""Collection of function and class for HTML Paragraph"""


from typing import Optional
import attrs

from .generic_component import HTMLGenericComponent # pylint: disable=import-error
from .components import AdditionalFile, HTMLComponent
from .html_tag import HTMLOptions, HTMLTag


__all__ = ["TextParagraph", "AdvancedParagraph"]


@attrs.define
class Text(HTMLComponent):
    """
    Represents a text HTML component.

    Args:
        text (str): The text to be rendered.
    """

    text: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={'description': 'The text to be rendered'},
        kw_only=False)

    def render(self) -> str:
        """
        Renders the text HTML component.

        Returns:
            str: The rendered HTML string.
        """
        return self.text

    def get_additional_files(self) -> list[AdditionalFile]:
        # Nothing to publish
        return []

def TextParagraph(  # pylint: disable=invalid-name
    text: str,
    *,
    options: Optional[HTMLOptions] = None,
    ) -> HTMLGenericComponent:
    """
    Create a paragraph component with the given text and options.

    Args:
        text (str): The text content of the paragraph.
        options (Optional[dict[str,str]]): Optional dictionary of tag options.

    Returns:
        HTMLGenericComponent: The paragraph component.

    """
    tag = HTMLTag(
        tag_name="p",
        options=options)
    return HTMLGenericComponent(
        tag=tag,
        contents=[Text(text)])

def AdvancedParagraph(  # pylint: disable=invalid-name
    *children: HTMLComponent | str,
    options: Optional[HTMLOptions] = None) -> HTMLGenericComponent:
    """
    Create an advanced paragraph component.

    Args:
        *children (HTMLComponent | str): The child components or strings to be
            included in the paragraph.
        options (Optional[dict[str,str]]): Additional options for the paragraph.

    Returns:
        HTMLGenericComponent: The advanced paragraph component.
    """
    components = [Text(child) if isinstance(child, str) else child for child in children]

    tag = HTMLTag(
        tag_name="p",
        options=options)
    return HTMLGenericComponent(
        tag=tag,
        contents=components)
