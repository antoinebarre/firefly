"""Division component for HTML."""

from typing import Optional
from .generic_component import HTMLGenericComponent # pylint: disable=import-error
from .html_tag import HTMLOptions, HTMLTag
from .components import HTMLComponent

__all__ = ["Div"]

def Div(  # pylint: disable=invalid-name
    *contents: HTMLComponent,
    options : Optional[HTMLOptions] = None
    ) -> HTMLGenericComponent:  # pylint: disable=invalid-name
    """
    Returns a division component for HTML.

    Args:
        *contents (HTMLComponent): The contents of the division.

    Returns:
        HTMLGenericComponent: The division component.
    """

    tag = HTMLTag(
        tag_name="div",
        options=options)
    return HTMLGenericComponent(
        tag=tag,
        contents=list(contents))