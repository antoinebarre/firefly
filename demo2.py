"""Create an html Pages based on FyreFly components."""


from firefly.html.components import Div, AdvancedParagraph

from firefly.html.components import TextParagraph

from firefly.html import HTMLDocument
from firefly.html.components import h
from firefly.html.components.css_style import CSS_Style
from firefly.html.components.html_tag import HTMLOptions
from firefly.html.components.paragraph import Text
from firefly.html.components.span import Span

opt = HTMLOptions(
    id="mydiv",
    class_="mydiv")

opt2 = HTMLOptions(
    id="mydiv",
    class_="mydiv",
    style=CSS_Style(
        color="red",
        font_family="Arial",
        font_size="40px",
        font_weight="bold",
        font_style="italic"
    )
)

print(TextParagraph("Hello, World!",options=opt).render())

a = Div(
    TextParagraph("Hello, World!"),
    TextParagraph("Hello, World!"))

b = Div(
    TextParagraph("Hello, World!"),
    TextParagraph("Hello, World!"))

c = AdvancedParagraph(
    "Hello, World!", Span(
        "Hello, World! POUET POUET", options=opt2),
    options=opt
    )

h1 = h(level=1, title="Title Hello, World!")

md = HTMLDocument()

md.add_component(h1)
md.add_component(a)
md.add_component(b)
md.add_component(c)

print(md.get_html_content())

from pathlib import Path

md.publish(Path("index.html"), exist_ok=True)