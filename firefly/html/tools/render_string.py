
from typing import Optional
from firefly.tools.string import indent
from firefly.validation.string import validate_string
from firefly.html.tools.HTMLTag import HTMLTag

def render_string(*,
                  open_prefix: str,
                  content: str,
                  close_suffix: str,
                  inline: bool = False,
                  indentation_size:int = 4) -> str:
    """
    Renders a string with HTML tags.

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

    return f"{prefix_tag}\n{indent(content,indentation_size)}\n{suffix_tag}\n"


def render_html_tag(
    *,
    tag: str,
    options: Optional[list[str]] = None,
    content: str, inline: bool = False, indentation_size: int = 4) -> str:
    """
    Renders an HTML tag with the specified options and content.

    Args:
        tag (str): The HTML tag name.
        options (list[str], optional): The list of options for the tag.
            Defaults to an empty list.
        content (str): The content to be placed inside the tag.
        inline (bool, optional): Specifies whether the tag should be rendered
            inline. Defaults to False.
        indentation_size (int, optional): The number of spaces for indentation. Defaults to 4.

    Returns:
        str: The rendered HTML tag as a string.
    """

    if options is None:
        options = []
    # validate the options list
    for option in options:
        option = validate_string(option, empty_allowed=False)
        if option[0] != " ":
            raise ValueError("The option must start with a ' ' character.")

    # create the prefix tag
    tag_with_options = tag + "".join(options)
    prefix_tag = HTMLTag(tag_with_options)

    # create the suffix tag
    suffix_tag = HTMLTag(f"/{tag}")

    return render_string(
        open_prefix=prefix_tag,
        content=content,
        close_suffix=suffix_tag,
        inline=inline,
        indentation_size=indentation_size)

if __name__ == "__main__":
    print(render_string(open_prefix="div", content="Hello, World!", close_suffix="/div"))
    # "<div>
    #     Hello, World!
    # </div>

    print(render_string(open_prefix="div", content="Hello, World!", close_suffix="/div", inline=True))

    # "<div>Hello, World!</div>"

    print(render_html_tag(tag="div", content="Hello, World!"))
    # "<div>
    #     Hello, World!
    # </div>"

    print(render_html_tag(tag="div", content="Hello, World!", inline=True))
    # "<div>Hello, World!</div>"

    print(render_html_tag(tag="div", options=[" id='myid'", " class='myclass'"], content="Hello, World!"))
