"""Collection of tools for working with HTML Tags."""

from typing import Optional
import attrs

from .css_style import CSS_Style
from .components import HTMLObject

__all__ = ["HTMLOptions", "HTMLTag"]

@attrs.define
class HTMLOptions(HTMLObject):
    """Class to represent the options of an HTML tag."""
    id: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The id of the HTML tag'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    class_: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The class of the HTML'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    style: Optional[CSS_Style] = attrs.field(
        default=None,
        metadata={'description': 'The style of the HTML tag.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(CSS_Style)),
        kw_only=True)

    type_: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The type of the HTML tag used only for list items'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)

    @staticmethod
    def _rename_attribute(attribute_name: str) -> str:
        """
        Rename the attribute name to match the HTML tag option name.

        Args:
            attribute_name (str): The attribute name.

        Returns:
            str: The renamed attribute name.
        """
        # remove the underscore if it is the last character
        if attribute_name[-1] == "_":
            attribute_name = attribute_name[:-1]
        return attribute_name.replace('_', '-')

    def render(self):
        option_components = []
        for field in attrs.fields(self.__class__):
            option_name = field.name
            # Convert field name to HTML Tag option name
            option_name_html = self._rename_attribute(option_name)
            if attribute_value := getattr(self, option_name):
                if isinstance(attribute_value, HTMLObject):
                    attribute_value = attribute_value.render()
                option_components.append(f' {option_name_html}="{attribute_value}"')
        return ''.join(option_components)


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
    options: Optional[HTMLOptions] = attrs.field(
        default=None,
        metadata={'description': 'The HTML tag options'},
        validator=attrs.validators.optional(attrs.validators.instance_of(HTMLOptions)),
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
