""" Function to generate a span element """

from typing import Optional

from .paragraph import Text
from .generic_component import HTMLGenericComponent
from .html_tag import HTMLTag, HTMLOptions

__all__ = ["Span"]


def Span(  # pylint: disable=invalid-name
    content: str,
    *,
    options: Optional[HTMLOptions] = None) -> HTMLGenericComponent:
    """
    Create a <span> HTML element with the specified content and options.

    Args:
        content (str): The content to be placed inside the <span> element.
        options (Optional[HTMLOptions]): Additional options for the <span> element.

    Returns:
        HTMLGenericComponent: The <span> element as an HTMLGenericComponent object.
    """
    return HTMLGenericComponent(
        tag=HTMLTag(
            tag_name="span",
            options=options,
        ),
        contents=[Text(content)],
        inline=True
    )