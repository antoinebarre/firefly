
from pathlib import Path
from firefly.html.components.css_style import CSS_Style
from firefly.html.components.link import Link
from firefly.html.components.lists import ListOptions, OrderedList, UnorderedList
from firefly.html.components.paragraph import Paragraph
from firefly.html.components.span import Span, SpanOptions
from firefly.tools.images import create_random_png

# test of span
sp = Span("Hello, World!", options=SpanOptions(
        style=CSS_Style(
            color="red",
            font_family="Arial",
            font_size="40px",
            font_weight="bold",
            font_style="italic"
        )
    ))

print(sp.render())

# test list

l1 = UnorderedList(
    "Hello, World!",
    "Hello, World!",
    "Hello, World!",
    options=ListOptions(
        id="mydiv",
        class_="mydiv",
        type_="a",
    )
    )
print(l1.render())

l2 = OrderedList(
    "Hello, World!",
    "Hello, World!",
    "Hello, World!",
    options=ListOptions(
        id="mydiv",
        class_="mydiv",
        type_="a",
    )
    )

print(l2.render())

# test image
from firefly.html.components.images import Image

# create a random image
filename = create_random_png(filename=Path("work/toto.png"))

# create an image component
im = Image(
    image_path=filename,
    alt_text="Random Image",
    width=256,
    height=256
)

print(im.render())

# test link
lk = Link(
    "Click me!",
    link="http://www.google.com",
)

print(lk.render())


# test article
from firefly.html.components.structure import Article

a1 = Article(
    title="My first article",
    class_="forecast")
a1.add_components(
    Paragraph("Hello, World!"))
a1.add_components(
    Paragraph("Hello, World!"))

a2 = Article(
    title="My second article",class_="day-forecast")
a2.add_components(
    Paragraph("Hello, World!"))
a2.add_components(
    Paragraph("Hello, World!"))
a2.add_components("sedfsflkjlsfjlksjflsjkfl\n")

a3 = Article(
    title="My third article")
a3.add_components(
    Paragraph("Hello, World!"))
a3.add_components(
    Paragraph("Hello, World!"))

a2.add_components(a3)

a1.add_components(a2)
a1.add_components(
    Paragraph("Hello, World!"))
a1.add_components(
    Paragraph("Hello, World!"))

print(a1.render())