"""Heading component for HTML."""

from typing import Optional
from .paragraph import Text
from .generic_component import HTMLGenericComponent  # pylint: disable=import-error
from .html_tag import HTMLOptions, HTMLTag

__all__ = ["h"]

def h(
    *,
    level:int,
    title:str,
    options:Optional[HTMLOptions] = None,
    ) -> HTMLGenericComponent:
    """
    Create an HTML heading component.

    Args:
        level (int): The level of the heading (1 to 6).
        title (str): The title of the heading.
        options (Optional[HTMLOptions]): Optional HTML options for the heading.

    Returns:
        HTMLGenericComponent: The HTML heading component.
    """

    # validate the level
    if not isinstance(level, int) and ( level < 1 or level > 6):
        raise TypeError("The level must be an integer between 1 and 6.")

    return HTMLGenericComponent(
        tag=HTMLTag(
            tag_name=f"h{level}",
            options=options,),
        contents=[Text(title)],
        inline=True
    )
