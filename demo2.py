"""Create an html Pages based on FyreFly components."""


from firefly.html.components import Div

from firefly.html.components import TextParagraph

from firefly.html import HTMLDocument
from firefly.html.components import h

print(TextParagraph("Hello, World!",{"style":"sco"}).render())

a = Div(
    TextParagraph("Hello, World!"),
    TextParagraph("Hello, World!"))

b = Div(
    TextParagraph("Hello, World!"),
    TextParagraph("Hello, World!"))

h1 = h(level=1, title="Title Hello, World!")

md = HTMLDocument()

md.add_component(h1)
md.add_component(a)
md.add_component(b)

print(md.get_html_content())