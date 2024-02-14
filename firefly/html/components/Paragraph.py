"""Collection of function and class for HTML Paragraph"""


from typing import Optional
import attrs

from firefly.validation.list import validate_list

from .generic_component import HTMLGenericComponent # pylint: disable=import-error
from .components import AdditionalFile, HTMLComponent
from .html_tag import HTMLTag, TagOptions


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
    options: Optional[dict[str,str]] = None,
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
        options=TagOptions(options=options))
    return HTMLGenericComponent(
        tag=tag,
        contents=[Text(text)])

def AdvancedParagraph(  # pylint: disable=invalid-name
    children: list[HTMLComponent] = None, # type: ignore
    options: Optional[dict[str,str]] = None) -> HTMLGenericComponent:
    """
    Create an advanced paragraph component.

    Args:
        children (list[HTMLComponent], optional): List of child components. Defaults to None.
        options (Optional[dict[str,str]], optional): Options for the paragraph
            component. Defaults to None.

    Returns:
        HTMLGenericComponent: The advanced paragraph component.
    """
    if children is None:
        children = []
    # validate children
    children = validate_list(children, HTMLComponent)

    tag = HTMLTag(
        tag_name="p",
        options=TagOptions(options=options))
    return HTMLGenericComponent(
        tag=tag,
        contents=children)
