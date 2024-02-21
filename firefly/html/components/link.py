


from typing import Literal, Optional
import attrs

from firefly.tools.strings import indent

from .paragraph import Text
from .components import AdditionalFile, HTMLComponent


@attrs.define
class LinkComponent(HTMLComponent):
    """
    Represents a link component that can be rendered as an HTML anchor tag.
    """
    component: HTMLComponent = attrs.field(
        metadata={'description': 'The component to be linked'},
        validator=attrs.validators.instance_of(HTMLComponent),
        kw_only=True)
    link: str = attrs.field(
        metadata={'description': 'The link to be used'},
        validator=attrs.validators.instance_of(str),
        kw_only=True)
    target: Optional[Literal['_blank', '_self', '_parent', '_top']] = attrs.field(
        default= None, # type: ignore
        metadata={'description': 'The target of the link'},
        validator=attrs.validators.optional(
            attrs.validators.in_(['_blank', '_self', '_parent', '_top'])),
        kw_only=True)

    inline: bool = attrs.field(
        default=True, # type: ignore
        metadata={'description': 'Whether the component should be rendered inline or not'},
        validator=attrs.validators.instance_of(bool), # type: ignore
        kw_only=True)

    def render(self) -> str:
        """
        Renders the component and returns the generated HTML string.
        """
        target = f' target="{self.target}"' if self.target else ''
        if self.inline:
            return f'<a href="{self.link}"{target}>{self.component.render()}</a>'
        return f'<a href="{self.link}"{target}>\n{indent(
                                                    text=self.component.render(),
                                                    amount=self._indent_value)}\n</a>'

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the component.
        """
        return self.component.get_additional_files()

def Link(component: HTMLComponent | str,*,  # pylint: disable=invalid-name
         link: str,
         target: Optional[Literal['_blank', '_self', '_parent', '_top']] = None,
         inline: bool = True) -> LinkComponent:
    """
    Creates a link component.

    Args:
        component (HTMLComponent | str): The component to be linked.
        link (str): The link to be used.
        target (Optional[Literal['_blank', '_self', '_parent', '_top']]): The target of the link.
        inline (bool): Whether the component should be rendered inline or not. default is True.

    Returns:
        LinkComponent: The created link component.
    """
    if isinstance(component, str):
        component = Text(component)
    return LinkComponent(
        component=component,
        link=link,
        target=target,
        inline=inline)
