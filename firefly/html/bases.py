

from abc import ABC, abstractmethod
from pathlib import Path
import attrs



@attrs.define
class HTMLReporter():
    title: str = attrs.field(
        validator=attrs.validators.instance_of(str),
        metadata={'description': 'Title of the HTML page'},
        kw_only=True)
    content: list[HTMLComponent] = attrs.field(default=[],
        metadata={'description': 'List of HTML components to be rendered'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)),
        kw_only=True)
    additional_files: list[Path] = attrs.field(default=[],
        metadata={'description': 'List of additional files to be published'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(AdditionalFile)),
        kw_only=True)
    
    def render(self) -> str:
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.title.upper()}</title>
</head>
<body>
"""
        for component in self.content:
            html += component.render()
        html += """</body>
</html>"""


