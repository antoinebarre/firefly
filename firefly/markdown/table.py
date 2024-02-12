"""Markdown table generator."""


from dataclasses import KW_ONLY
from pathlib import Path
from typing import Literal
from pydantic import BaseModel

from firefly.markdown.elements import MarkdownContent, MarkdownElement


class MarkdownColumnTable(BaseModel):
    """
    Represents a column-based table in Markdown format.

    Args:
        name (str): The name of the column.
        values (list[str]): The values in the column.
        align (Literal["left", "center", "right"], optional): The alignment of
            the column. Defaults to "left".
    """
    _: KW_ONLY
    name: str
    values: list[str]
    align: Literal["left", "center", "right"] = "left"


def create_markdown_table(table_columns: list[MarkdownColumnTable]) -> str:
    """
    Create a Markdown table based on the provided table columns.

    Args:
        table_columns (list[MarkdownColumnTable]): The list of table columns.

    Returns:
        str: The generated Markdown table.

    """
    # Define the alignment symbols for Markdown
    align_symbols = {
        "left": ":--",
        "center": ":-:",
        "right": "--:"
    }

    # Construct the header row
    header_row = "| " + " | ".join(column.name for column in table_columns) + " |"

    # Construct the alignment row
    alignment_row = "| " + " | ".join(align_symbols[column.align] \
        for column in table_columns) + " |"

    data_rows = [
        "| " + " | ".join(row_values) + " |"
        for row_values in zip(*[column.values for column in table_columns])
    ]
    return "\n".join([header_row, alignment_row] + data_rows)



class MarkdownTable(MarkdownElement, BaseModel):
    """
    Represents a Markdown table.

    Attributes:
        columns (list[MarkdownColumnTable]): The list of table columns.

    Methods:
        publish(directory_path: Path) -> MarkdownContent:
            Publishes the Markdown table.
    """
    columns: list[MarkdownColumnTable]

    def publish(self) -> MarkdownContent:
        """
        Publishes the Markdown table.

        Args:
            directory_path (Path): The directory path where the table will be published.

        Returns:
            MarkdownContent: The content of the published table.
        """
        return MarkdownContent(
            content=f"  \n\n{create_markdown_table(self.columns)}  \n")

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        return []

if __name__ == "__main__":
    columns = [
        MarkdownColumnTable(name="Name", values=["Alice", "Bob", "Charlie"]),
        MarkdownColumnTable(name="Age", values=["25", "30", "35"], align="center"),
        MarkdownColumnTable(name="City", values=["New York", "Los Angeles", "Chicago"])
    ]
    print(create_markdown_table(columns))
