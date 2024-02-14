"""Division component for HTML."""

from .generic_component import HTMLGenericComponent # pylint: disable=import-error
from .html_tag import HTMLTag
from .components import HTMLComponent

__all__ = ["Div"]

def Div(*contents: HTMLComponent) -> HTMLGenericComponent:  # pylint: disable=invalid-name
    """
    Returns a division component for HTML.

    Args:
        *contents (HTMLComponent): The contents of the division.

    Returns:
        HTMLGenericComponent: The division component.
    """

    tag = HTMLTag("div")
    return HTMLGenericComponent(
        tag=tag,
        contents=list(contents))