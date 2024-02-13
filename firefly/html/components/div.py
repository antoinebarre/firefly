

import attrs

from firefly.tools.string import indent

from .HTMLComponent import HTMLComponent

@attrs.define
class Div(HTMLComponent):
    """
    Represents a <div> HTML component.

    Args:
        children (list[HTMLComponent], optional): List of HTML components to be rendered.
        style (str, optional): CSS style for the div.
        id (str, optional): ID of the div.
    """

    children: list[HTMLComponent] = attrs.field(
        default=[],
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)),
        kw_only=True)
    style: str = attrs.field(
        default=None,
        metadata={'description': 'CSS style for the div'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    id: str = attrs.field(
        default=None,
        metadata={'description': 'ID of the div'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    
    myclass: str = attrs.field(
        default=None,
        metadata={'description': 'Class of the div'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)

    def render(self):
        """
        Renders the <div> HTML component.

        Returns:
            str: The rendered HTML string.
        """
        # initialize children string
        children = ""

        # if there are children, render them
        if self.children:
            children = ''.join([child.render() for child in self.children])

        # generate div tag if necessary
        style = f' style="{self.style}"' if self.style else ''
        id_msg = f' id="{self.id}"' if self.id else ''
        myclass = f' class="{self.myclass}"' if self.myclass else ''
        
        return render_string(
            open_prefix="".join(["div",myclass,id_msg]),
            content=children,
            close_suffix="/div",
            inline=False,
            indentation_size=self._indent_value)

        return (
              f"<div{id_msg}{style}>\n"
            + f"{indent(children,self._indent_value)}\n"
            + "</div>\n"
        )

    def __str__(self):
        return self.render()

