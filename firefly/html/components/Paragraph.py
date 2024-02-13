

import attrs
from .HTMLComponent import HTMLComponent


@attrs.define
class TextParagraph(HTMLComponent):
    text: str = attrs.field(
        validator=attrs.validators.instance_of(str),
        metadata={'description': 'The text to be rendered in the paragraph'},
        kw_only=True)

    def __init__(self, text):
        self.text = text

    def render(self):
        return "<p>{}</p>".format(self.text