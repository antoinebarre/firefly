"""Tools for creating a table of contents (TOC) for a web page."""

from dataclasses import dataclass, field
import importlib.resources as pkg_resources
from bs4 import BeautifulSoup, Tag
from firefly.html.components.components import AdditionalFile

from firefly.tools.strings import generate_unique_id
from .components import HTMLComponent


@dataclass
class TableofContent(HTMLComponent):
    """A table of contents (TOC) for a web page."""
    content: str
    soup: BeautifulSoup = field(init=False)

    def __post_init__(self):
        """Initialize the table of contents."""
        self.soup = BeautifulSoup(self.content, "html.parser")

    def _get_body(self):
        """Return the body of the document."""
        return self.soup.body

    def _get_all_headings(self):
        if self._get_body() is None:
            return []
        # search for all headings in the body
        heading_tags = ["h2", "h3"]

        return self._get_body().find_all(heading_tags)

    def render(self) -> str:
        """Render the table of contents as an HTML string."""

        # get all headings
        headings = self._get_all_headings()

        # Create the main <ul> for the ToC
        toc_ul = self.soup.new_tag('ul')

        # Keep track of the current <ul> for nested <h3> elements
        current_ul = toc_ul
        for heading in headings:
            # Assign an ID to each heading if it doesn't already have one
            if not heading.has_attr('id'):
                heading_id = generate_unique_id()
                heading['id'] = heading_id

            # Create a list item <li> with a link <a> for the heading
            li = self.soup.new_tag('li')
            a = self.soup.new_tag(
                'a',
                href=f"#{heading['id']}",
                class_='menu__item2' if heading.name == 'h2' else 'menu__item3')
            a.string = heading.text
            li.append(a)

            if heading.name == 'h2':
                # For h2 headings, append the list item to the main ToC <ul>
                toc_ul.append(li)
                # Reset the current <ul> to the main ToC <ul>
                current_ul = li
            elif heading.name == 'h3':
                # For h3 headings, check if the current list item has a nested <ul>
                if not current_ul.find('ul'):
                    # If not, create a new nested <ul>
                    nested_ul = self.soup.new_tag('ul')
                    current_ul.append(nested_ul)
                # Append the <h3> list item to the nested <ul>
                current_ul.find('ul').append(li)

        # Create a <div> for the ToC
        toc_div = self.soup.new_tag('div', class_="hamburger-menu")
        toc_menu = self.soup.new_tag('input', id="menu__toggle", type="checkbox")
        toc_label = self.soup.new_tag('label', class_="menu__btn", for_="menu__toggle")
        toc_span = self.soup.new_tag('span')
        toc_label.append(toc_span)
        toc_div.append(toc_menu)
        toc_div.append(toc_label)
        toc_div.append(toc_ul)

        # Insert the ToC at the beginning of the body
        self.soup.body.insert(0, toc_div)
        
        # add css to the head
        css_link = self.soup.new_tag('link', rel='stylesheet', href='style/toc.css', type='text/css')
        
        # add the css link to the head
        self.soup.head.append(css_link)
        
        return self.soup.prettify()

    def get_additional_files(self) -> list[AdditionalFile]:
        with pkg_resources.path("firefly.html.templates", "toc.css") as css_path:
        # css_path is a Path object that can be used within this block
            return [
                AdditionalFile(
                    original_path=css_path,
                    published_directory="style",
                    published_filename="toc.css"
                )]