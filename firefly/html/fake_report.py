

from pathlib import Path
import tempfile
from firefly.html.components.header import create_header
from firefly.html.components.images import Image
from firefly.html.components.lists import UnorderedList, ListOptions, OrderedList
from firefly.html.components.tables import Table, TableColumn
from firefly.tools.images import create_random_png
from firefly.tools.strings import LoremIpsum
from firefly.html.base import HTMLDocument
from .components.link import Link
from .components.structure import Article



def create_fake_report(
    html_file_path: Path,
    ) -> HTMLDocument:
    
    # create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)
    
    

    # create the HTML document
    md = HTMLDocument()

    # create the header
    md.add_header( create_header(
        title="Fake Report",
        css_file_path=Path("firefly/html/templates/report.css")))

    # create the body based on article
    intro = Article(
        title="Introduction")

    intro.add_paragraph(
        "This is a fake report created with Firefly.")

    md.add_component(intro)

    # create sections
    section1 = Article(
        title="Section 1")
    section1.add_paragraph(LoremIpsum.generate_paragraph())
    
    section11 = Article(
        title="Section 1.1")
    section11.add_paragraph(LoremIpsum.generate_paragraph())
    
    # create a table
    tt = Table(
        legend="The Beatles",
        columns=[
            TableColumn(
            header= "Name",
            data=["John","Paul","George","Ringo"]),
            TableColumn(
            header= "Instrument",
            data=["Guitar","Bass","Guitar","Drums"]),
            TableColumn(
            header= "Vocals",
            data=["Yes","Yes","Yes","Yes"]),
        ]
        )
    section11.add_components(tt)
    
    section1.add_components(section11)
    
    
    
    section12 = Article(
        title="Section 1.2")
    section12.add_paragraph(LoremIpsum.generate_paragraph())
    
    # create a fake image png
    image_path = create_random_png(temp_dir_path / "fake_image.png")
    
    im = Image(
        image_path=image_path,
        alt_text="Fake Image",
        width=400,
        height=300,
        legend="This is a fake image.",
        )
    
    section12.add_components(im)
    
    section1.add_components(section12)
    
    section2 = Article(
        title="Section 2")
    section2.add_paragraph(LoremIpsum.generate_paragraph())
    
    section21 = Article(
        title="Section 2.1")
    section21.add_paragraph(LoremIpsum.generate_paragraph())
    
    l = UnorderedList(
    "Hello, World!",
    "Hello, World!",
    "Hello, World!",
    )

    l2 = UnorderedList(
        "titi",
        "sdfsdfsdfsdf",
        "dflkdlfkdlfk",
        "dlsfjldsfjk")

    l3 = OrderedList(
        "Hello, World!1",
        "Hello, World!2",
        "Hello, World!3",
        options=ListOptions(type_="A"))
    section21.add_components(l,l2,l3)

    section2.add_components(section21)

    section22 = Article(
        title="Section 2.2")
    section22.add_paragraph(LoremIpsum.generate_paragraph())
    section22.add_components(Link("GO TO GOOGLE",link="https://www.google.com"))
    
    section2.add_components(section22)
    
    md.add_component(section1,section2)
    
    
    # publish the HTML document
    md.publish(html_file_path, exist_ok=True)
    
    temp_dir.cleanup()
    
    return md
    