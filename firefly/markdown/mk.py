"""
This module provides a MarkdownText class for working with Markdown content.
"""

# to export the class Markdown see:
# https://python-markdown.github.io/


from pathlib import Path
import markdown
from pydantic import BaseModel

from firefly.markdown.elements import (MarkdownElement, MarkdownContent, AcronymMarkdown,
                                       ImageMarkdown, MarkdownPageTitle, MarkdownTitle,
                                       MarkdownText,MarkdownNewLine)
from firefly.tools.files import delete_folder, write_string_to_file
from firefly.validation.fileIO import validate_file_extension


class MarkdownDocument(BaseModel):
    """
    Represents a Markdown document.

    Attributes:
        elements (list[MarkdownElement]): The list of Markdown elements in the document.

    Methods:
        add_element(element: MarkdownElement) -> None:
            Adds a Markdown element to the document.

        publish_md_file(file_path: Path) -> MarkdownContent:
            Publishes the Markdown document to a Markdown file.

        publish_html_file(file_path: Path) -> str:
            Publishes the Markdown document to an HTML file.

        extract_abbreviation() -> list[AcronymMarkdown]:
            Extracts the AcronymMarkdown elements from the document.
    """
    elements:list[MarkdownElement] = []

    def __add__(self, other: "MarkdownDocument") -> "MarkdownDocument":
        if not isinstance(other, MarkdownDocument):
            raise TypeError("Only a MarkdownDocument can be added to another MarkdownDocument.")
        self.elements.extend(other.elements)
        return self

    def add_element(self, element: MarkdownElement) -> None:
        """
        Adds a MarkdownElement to the list of elements.

        Args:
            element (MarkdownElement): The MarkdownElement to be added.

        Returns:
            None
        """
        self.elements.append(element)

    def to_md(self) -> str:
        """
        Converts the Markdown document to a Markdown string.

        Returns:
            str: The Markdown string.
        """
        content = MarkdownContent()
        for element in self.elements:
            element_content = element.publish()
            content += element_content
        return str(content)

    def to_html(self) -> str:
        """
        Converts the Markdown document to an HTML string.

        Returns:
            str: The HTML string.
        """
        md_data = self.to_md()
        return markdown.markdown(md_data, extensions=["abbr", "tables"])

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        """
        Exports the additional files in the Markdown document.

        Args:
            directory_path (Path): The directory path where the additional files will be exported.

        Returns:
            list[Path]: The list of exported file paths.
        """
        file_paths : list[Path] = []
        for element in self.elements:
            file_paths += element.export_additional_files(directory_path)
        return file_paths

    def publish_md_file(
            self,
            *,
            file_path: Path,
            exist_ok: bool = False) -> None:
        """
        Publishes the markdown file.

        Args:
            file_path (Path): The path to the markdown file.
            exist_ok (bool, optional): If True, overwrite the file if it already
                exists. Defaults to False.
        """
        # validate file_path
        file_path = validate_file_extension(
            file_path=file_path,
            extension=[".md"])

        # collect the content
        md_data = self.to_md()

        # write the content to the file
        _ = write_string_to_file(
            file_path=file_path,
            content=md_data,
            exist_ok=exist_ok)

        # export additional files
        _ = self.export_additional_files(file_path.parent)


    def publish_html_file(
            self,
            *,
            file_path: Path,
            exist_ok:bool = False) -> None:
        """
        Publishes the HTML file by converting the markdown data to HTML and writing
        it to the specified file path.

        Args:
            file_path (Path): The path where the HTML file will be written.
            exist_ok (bool, optional): If True, allows overwriting an existing file.
                Defaults to False.
        """
        # validate file_path
        file_path = validate_file_extension(
            file_path=file_path,
            extension=[".html"])

        # get md data and export to html
        html_data = self.to_html()

        # write the content to the file
        _ = write_string_to_file(
            file_path=file_path,
            content=html_data,
            exist_ok=exist_ok)

        # export additional files
        _ = self.export_additional_files(file_path.parent)


    def extract_abbreviation(self) -> list[AcronymMarkdown]:
        """
        Extracts the AcronymMarkdown elements from the document.

        Returns:
            list[AcronymMarkdown]: The list of AcronymMarkdown elements.
        """
        return [element for element in self.elements if isinstance(element, AcronymMarkdown)]


if __name__ == "__main__":

    md = MarkdownDocument()
    md.add_element(MarkdownPageTitle(title="My First Markdown Document"))
    md.add_element(MarkdownTitle(title="Introduction", level=1))
    md.add_element(MarkdownText(content="This is the introduction to my first markdown document."))
    md.add_element(MarkdownTitle(title="Section 1", level=2))
    md.add_element(MarkdownText(content="This is the HTML first section of my markdown document."))
    md.add_element(MarkdownTitle(title="Section 2", level=2))
    md.add_element(MarkdownText(content="This is the JS second section of my markdown document."))
    md.add_element(MarkdownTitle(title="Conclusion", level=1))
    md.add_element(MarkdownText(content="This is the conclusion of my first markdown document."))
    md.add_element(AcronymMarkdown(title="MD", definition="Markdown"))
    md.add_element(AcronymMarkdown(title="HTML", definition="Hyper Text Markup Language"))
    md.add_element(AcronymMarkdown(title="CSS", definition="Cascading Style Sheets"))
    md.add_element(AcronymMarkdown(title="JS", definition="JavaScript"))
    md.add_element(AcronymMarkdown(title="API", definition="Application Programming Interface"))
    md.add_element(MarkdownNewLine())
    im1 = ImageMarkdown(original_path=Path("work/toto.png"), replacement_text="Image 1")
    md.add_element(im1)

    # create a table
    import firefly.markdown.table as table
    columns = [
        table.MarkdownColumnTable(
            name="Name", align="left", values=["John", "Jane", "Doe"]),
        table.MarkdownColumnTable(
            name="Age", align="center", values=["25", "30", "35"]),
        table.MarkdownColumnTable(
            name="City", align="right", values=["Paris", "London", "New York"])
    ]
    table1 = table.MarkdownTable(columns=columns)
    md.add_element(table1)

    # create a plot
    from firefly.markdown.plot import PlotMarkdown

    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='x', ylabel='y', title='My first plot')
    ax.grid()

    plt1 = PlotMarkdown(figure=fig, description="My first plot")
    md.add_element(plt1)


    myDir = Path("work/titi")
    my_file = myDir /"first_md.html"
    if myDir.exists():
        delete_folder(folder_path=myDir)
    myDir.mkdir(parents=True, exist_ok=True)

    md.publish_html_file(file_path=my_file)
