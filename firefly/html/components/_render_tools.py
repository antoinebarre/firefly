"""Collection of tools to render HTML components"""

from firefly.tools.strings import indent
from firefly.validation.string import validate_string

__all__ = ["create_block"]

def create_block(*,
                  open_prefix: str,
                  content: str,
                  close_suffix: str,
                  inline: bool = False,
                  indentation_size:int = 4) -> str:
    """
    Renders a string between an opening and closing balise
    (e.g. HTML tags as <div>...</div>)

    Args:
        open_prefix (str): The opening HTML tag prefix.
        content (str): The content to be wrapped with ags.
        close_suffix (str): The closing tag suffix.
        inline (bool, optional): Whether to render the content inline or not. Defaults to False.
        indentation_size (int, optional): The size of indentation for the content. Defaults to 4.

    Returns:
        str: The rendered string with HTML tags.
    """

    # validate the content
    content = validate_string(content, empty_allowed=False)


    # create the HTML tags
    prefix_tag = open_prefix
    suffix_tag = close_suffix

    if inline:
        return f"{prefix_tag}{content}{suffix_tag}"

    return f"\n{prefix_tag}\n{indent(content,indentation_size)}\n{suffix_tag}\n"
