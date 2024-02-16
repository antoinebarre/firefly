"""Create an html Pages based on FyreFly components."""


from firefly.html.components import Div



from firefly.html import HTMLDocument
from firefly.html.components import h
from firefly.html.components.css_style import CSS_Style
from firefly.html.components.html_tag import HTMLOptions
from firefly.html.components.paragraph import Paragraph, Text
from firefly.html.components.span import Span
from firefly.html.components.lists import HTMLList, OrderedList, UnorderedList

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
    ),
    type_="A"
)

print(Paragraph("Hello, World!",options=opt).render())

a = Div(
    Paragraph("Hello, World!"),
    Paragraph("Hello, World!"))

b = Div(
    Paragraph("Hello, World!"),
    Paragraph("Hello, World!"))

c = Paragraph(
    "Hello, World!", Span(
        "Hello, World! POUET POUET", options=opt2),
    options=opt
    )

h1 = h(level=1, title="Title Hello, World!")

l = UnorderedList(
    "Hello, World!",
    "Hello, World!",
    "Hello, World!",
    options=opt
    )

l2 = UnorderedList(
    "titi",
    Text("toto:",l),
    "dflkdlfkdlfk",
    "dlsfjldsfjk")

l3 = OrderedList(
    "Hello, World!1",
    "Hello, World!2",
    "Hello, World!3",
    options=HTMLOptions(type_="A"))

md = HTMLDocument()

md.add_component(h1)
md.add_component(a)
md.add_component(b)
md.add_component(c)
md.add_component(l2)
md.add_component(l3)

print(md.get_html_content())

from pathlib import Path

md.publish(Path("index.html"), exist_ok=True)
