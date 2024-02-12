
"""
Module containing tools for markdown formatting.
"""

from enum import IntEnum, StrEnum, auto
import warnings

from firefly.validation.enum import DetailledEnum
from firefly.validation.values import validate_string

class TextAlignment(StrEnum):
    """
    Enum class representing different text alignments.
    Default value is left.
    """

    right = auto() # pylint: disable=invalid-name
    left = auto() # pylint: disable=invalid-name
    center = auto()  # type: ignore # pylint: disable=invalid-name
    justify = auto() # pylint: disable=invalid-name

    @classmethod
    def _missing_(cls,value):
        warnings.warn(f"{value} is not a valid {cls.__name__}. " \
                f"Valid types: {', '.join([repr(m.value) for m in cls])}"\
                    f"Default value is used :{cls.left}")
        return cls.left


class HeaderLevel(DetailledEnum,IntEnum):
    """
    Enum class representing different header levels in markdown.
    """
    TITLE = 1          # H1 - Main title (largest and most important)
    HEADING = 2        # H2 - Section headings
    SUBHEADING = 3     # H3 - Subsection headings
    SUBSUBHEADING = 4  # H4 - Smaller subsection headings
    MINORHEADING = 5   # H5 - Even smaller headings
    LEASTHEADING = 6   # H6 - The smallest heading level


class MkFormat:
    """This class helps to create bold, italics and change color text."""

    @staticmethod
    def bold(text: str) -> str:
        """
        Applies bold formatting to the given text.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text with bold formatting applied.
        """
        # validate text
        text = validate_string(text)

        return f"**{text}**"

    @staticmethod
    def italics(text: str) -> str:
        """
        Applies italics formatting to the given text.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text with italics.

        """
        # validate text
        text = validate_string(text)

        return f"*{text}*"

    @staticmethod
    def inline_code(text: str) -> str:
        """
        Formats the given text as inline code by surrounding it with backticks.

        Args:
            text (str): The text to be formatted as inline code.

        Returns:
            str: The formatted inline code.
        """
        # validate text
        text = validate_string(text)

        return f"``{text}``"

    @staticmethod
    def center_text(text: str) -> str:
        """
        Center-aligns the given text.

        Args:
            text (str): The text to be center-aligned.

        Returns:
            str: The center-aligned text.
        """
        # validate text
        text = validate_string(text)

        return f"<center>{text}</center>"

    @staticmethod
    def text_color(
            text: str,
            color: str = "black"
            ) -> str:
        """Change text color.

        color: it is the text color: ``'orange'``, ``'blue'``, ``'red'``...
                      or a **RGB** color such as ``'#ffce00'``.
                      default is ``'black'``.
        """
        # validate text
        text = validate_string(text)

        # manage if color is empty
        if not color:
            color = "black"

        return f'<font color="{color}">{text}</font>'

    @staticmethod
    def text_external_link(
            text: str,
            link: str = ""
            ) -> str:
        """
        Returns a formatted markdown string for an external link.

        Args:
            text (str): The text to be displayed for the link.
            link (str, optional): The URL of the external link. Defaults to "".

        Returns:
            str: The formatted markdown string for the external link.
        """
        # validate text
        text = validate_string(text)

        return f"[{text}]({link})"

    @staticmethod
    def insert_code(code: str,
                    language: str = ""
                    ) -> str:
        """
        Inserts code into a markdown code block.

        Args:
            code (str): The code to be inserted.
            language (str, optional): The language of the code. Defaults to "".

        Returns:
            str: The markdown code block with the inserted code.
        """
        if not language:
            return "```\n" + code + "\n```"
        else:
            return f"```{language}" + "\n" + code + "\n```"

    @staticmethod
    def text_style(
        text: str,
        *,
        align: str = "left",  # center, right, left, or justify
        bold: bool = False,
        italic: bool = False,
        text_color: str = "",  # color name or RGB code
        background_color: str = "",  # color name or RGB code
        font_size: int = 0,  # positive integer
    ) -> str:
        """
        Applies various text styles to the given text and returns it wrapped in a paragraph tag.

        Args:
            text (str): The text to be styled.
            align (str, optional): The alignment of the text. Defaults to "left".
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            text_color (str, optional): The color of the text. Defaults to "".
            background_color (str, optional): The background color of the text. Defaults to "".
            font_size (int, optional): The font size of the text. Defaults to 0.

        Returns:
            str: The styled text wrapped in a paragraph tag.
        """
        # Dictionary to hold CSS properties
        style_options = {
            "text-align": TextAlignment(align),
            "font-weight": "bold" if bold else None,
            "font-style": "italic" if italic else None,
            "color": text_color or None,
            "background-color": background_color or None,
            "font-size": f"{font_size}px" if font_size > 0 else None,
        }

        # Filter out None values
        style_options = {k: v for k, v in style_options.items() if v is not None}

        style_str = "; ".join(f"{k}: {v}" for k, v in style_options.items())

        return f"<p style='{style_str}'>{text}</p>"


if __name__ == "__main__":
    print(TextAlignment.right)
    print(HeaderLevel.TITLE)
    print(MkFormat.bold("Hello"))
    print(MkFormat.italics("Hello"))
    print(MkFormat.inline_code("Hello"))
    print(MkFormat.center_text("Hello"))
    print(MkFormat.text_color("Hello", "blue"))
    print(MkFormat.text_external_link("Hello", "https://www.google.com"))
    print(MkFormat.insert_code("Hello"))
    print(MkFormat.text_style(
        "Hello",
        align="center",
        bold=True,
        italic=True,
        text_color="blue",
        background_color="red",
        font_size=12))

    a = HeaderLevel.HEADING
    print(int(HeaderLevel.HEADING.value))
