
from firefly.html import HTMLOptions

opt = HTMLOptions(
    id="mydiv",
    class_="mydiv")

print(opt.render())  # <div id="mydiv" class="mydiv"></div>