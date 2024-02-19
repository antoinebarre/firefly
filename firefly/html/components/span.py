""" Function to generate a span element """

from typing import Optional

import attrs

from .css_style import CSS_Style

from .paragraph import Text
from .generic_component import HTMLGenericComponent
from .html_tag import HTMLTag, HTMLOptions

__all__ = ["Span"]

@attrs.define
class SpanOptions(HTMLOptions):
    """
    Represents the options for a <span> HTML element.
    """
    style: Optional[CSS_Style] = attrs.field(
        default=None,
        metadata={'description': 'The style of the HTML tag.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(CSS_Style)),
        kw_only=True)

def Span(  # pylint: disable=invalid-name
    content: str,
    *,
    options: Optional[SpanOptions] = None) -> HTMLGenericComponent:
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