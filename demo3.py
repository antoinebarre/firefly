
from firefly.html.components.css_style import CSS_Style
from firefly.html.components.lists import ListOptions, OrderedList, UnorderedList
from firefly.html.components.span import Span, SpanOptions

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