"""Collection of tools for working with HTML Tags."""

from typing import Optional
import attrs
from pydantic import BaseModel, field_validator

from .components import HTMLObject


# List of allowed keys for the options dictionary
ALLOWED_KEYS = ["id", "class", "style"]

class TagOptions(HTMLObject,BaseModel):
    """Class to represent the options of an HTML tag."""

    options: Optional[dict[str,str]] = None

    @field_validator("options")
    @classmethod
    def validate_options(cls, v : Optional[dict[str,str]] = None):
        """
        Validates the options dictionary.

        Args:
            v (Optional[dict[str,str]]): The options dictionary to validate.

        Returns:
            Optional[dict[str,str]]: The validated options dictionary.

        Raises:
            ValueError: If any key in the dictionary is not in the list of allowed keys.
        """
        if v is None:
            return v
        if any(key not in ALLOWED_KEYS for key in v.keys()):
            raise ValueError(
                "Dictionary keys must be in the list of allowed keys. " +
                f"Got: {v}. " +
                f"Allowed: {ALLOWED_KEYS}")
        return v

    def __init__(
        self, options: Optional[dict[str,str]] = None,
        ):
        """
        Initializes a TagOptions object.

        Args:
            options (Optional[dict[str,str]]): The options dictionary.
            **kwargs: Additional keyword arguments.
        """
        super(TagOptions, self).__init__(options=options)

    def __str__(self) -> str:
        """
        Returns a string representation of the TagOptions object.

        Returns:
            str: The string representation of the TagOptions object.
        """
        value = ""
        if self.options:
            for key, val in self.options.items():
                value += f' {key}="{val}"'
        return value

    def render(self):
        return str(self)

@attrs.define
class HTMLTag():
    """
    Represents an HTML tag.

    Attributes:
        tag_name (str): The HTML tag name. Cannot be empty.
        options (Optional[TagOptions]): The HTML tag options.
    """

    tag_name: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={'description': 'The HTML tag name'},
        kw_only=False)
    options: Optional[TagOptions] = attrs.field(
        default=None,
        metadata={'description': 'The HTML tag options'},
        validator=attrs.validators.optional(attrs.validators.instance_of(TagOptions)),
        kw_only=True)

    def create_prefix_tag(self) -> str:
        """
        Create the opening tag for the HTML element.

        Returns:
            str: The opening tag for the HTML element.
        """
        if self.options:
            return f"<{self.tag_name}{self.options.render()}>"
        return f"<{self.tag_name}>"

    def create_suffix_tag(self) -> str:
        """
        Create the closing tag for the HTML element.

        Returns:
            str: The closing tag for the HTML element.
        """
        return f"</{self.tag_name}>"
