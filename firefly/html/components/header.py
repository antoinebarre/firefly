"""Collection of Header components."""

from typing import Optional
import attrs

from .html_tag import HTMLOptions
from .components import AdditionalFile
from .components import HTMLComponent
from ._render_tools import create_block
from .heading import h

class HeaderComponent

@attrs.define
class PageTitle(HTMLComponent):
    title: str = attrs.field(
        metadata={'description': 'The title of the page'},
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        kw_only=False)
    options: Optional[HTMLOptions] = attrs.field(
        default=None,
        metadata={'description': 'The options of the title'},
        validator=attrs.validators.optional(attrs.validators.instance_of(HTMLOptions)),
        kw_only=True)


    def render(self) -> str:
        return create_block(
            open_prefix="<header>",
            close_suffix="</header>",
            content=h(level=1,title=self.title).render(),
            inline=False,
            indentation_size=self._indent_value
        )

    def get_additional_files(self) -> list[AdditionalFile]:
        return []