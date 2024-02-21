"""Collection of tools to create HTML table"""
# see https://github.com/sbi-rviot/ph_table
# https://www.youtube.com/watch?v=biI9OFH6Nmg&t=113s
# https://tympanus.net/codrops/2012/11/02/heading-set-styling-with-css/


from dataclasses import dataclass
from typing import Literal, Optional
import attrs


from firefly.tools.strings import indent

from .components import AdditionalFile, HTMLComponent, collect_additional_files
from .paragraph import Text
from ._render_tools import create_block

# ============================ TABLE COMPONENTS ============================ #
@dataclass
class TableColumn():
    """
    Represents a column in a table.

    Attributes:
        header (str): The header text of the column.
        data (list[HTMLComponent | str]): The data elements in the column.
        alignment (Optional[Literal["left", "center", "right"]]): The alignment of
            the column (left, center, or right).
        width_percent (Optional[int]): The width of the column as a percentage.

    Methods:
        length() -> int: Returns the number of data elements in the column.
        get_data() -> list[HTMLComponent]: Returns the data elements in the column
            as a list of HTMLComponents.
    """
    header: str
    data: list[HTMLComponent | str]
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

    # TODO : change this class to ATTRS

    def length(self) -> int:
        """
        Returns the length of the data in the table.

        Returns:
            int: The length of the data.
        """
        return len(self.data)

    def get_data(self) -> list[HTMLComponent]:
        """
        Returns the data of the table as a list of HTMLComponent objects.
        If the data is a string, it is converted to a Text object before being added to the list.
        """
        return [Text(data) if isinstance(data, str) else data for data in self.data]

@dataclass
class Cells():
    """
    Represents a collection of cells in a table.

    Attributes:
        data (HTMLComponent): The HTML component representing the data in the cells.
        alignment (Optional[Literal["left", "center", "right"]]): The alignment of
            the cells (left, center, or right).
        width_percent (Optional[int]): The width of the cells as a percentage.
    """
    data: HTMLComponent
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

def _create_HTML_table_row( # pylint: disable=invalid-name
    row_elements: list[Cells],
    balise: Literal["th", "td"] = "td",
    indent_value: int = 4
) -> str:
    """
    Creates an HTML table row with the given row elements.

    Args:
        row_elements (list[Cells]): The list of Cells objects representing the
        elements of the row.

        balise (Literal["th", "td"], optional): The HTML tag to be used for each
        element (default is "td").

        indent_value (int, optional): The number of spaces to be used for
        indentation (default is 4).

    Returns:
        str: The HTML representation of the table row.

    """
    elements_str = ""
    for element in row_elements:
        # create alignment attribute
        alignment_attr = f' align="{element.alignment}"' \
            if element.alignment else ""

        # create width attribute
        width_attr = f' style="width:{element.width_percent}%"' \
            if element.width_percent else ""

        # create the element
        elements_str += create_block(
            open_prefix=f"<{balise}{alignment_attr}{width_attr}>",
            close_suffix=f"</{balise}>",
            content=element.data.render(),
            inline=False,
            indentation_size=Table._indent_value # pylint: disable=protected-access
        )

    cells = "".join(elements_str)

    return f"<tr>\n{indent(cells, indent_value)}</tr>\n"

def _validate_table_columns(columns: list[TableColumn]) -> list[TableColumn]:
    """
    Validate the table columns.

    Args:
        columns (list[TableColumn]): The list of table columns to validate.

    Returns:
        list[TableColumn]: The validated list of table columns.

    Raises:
        ValueError: If the table has no columns, if any column is not of type TableColumn,
        or if the columns have different lengths.
    """
    if not columns:
        raise ValueError("The table must have at least one column.")
    if not all(isinstance(column, TableColumn) for column in columns):
        raise ValueError("All columns must be of type TableColumn.")

    # check if all columns have the same length
    if len({column.length() for column in columns}) > 1:
        raise ValueError("All columns must have the same length.")

    return columns

def _extract_headers(columns: list[TableColumn]) -> list[Cells]:
    """
    Extracts the headers from the given list of TableColumn objects and returns
    a list of Cells objects.

    Args:
        columns (list[TableColumn]): The list of TableColumn objects.

    Returns:
        list[Cells]: The list of Cells objects representing the extracted headers.
    """
    return [Cells(
        data=column.header if isinstance(column.header, HTMLComponent) else Text(column.header),
        alignment= column.alignment,
        width_percent= column.width_percent
        )
            for column in columns]

def _extract_specific_elements(
    columns: list[TableColumn],
    index: int
) -> list[Cells]:
    """
    Extracts specific elements from the given columns at the specified index.

    Args:
        columns (list[TableColumn]): The list of TableColumn objects.
        index (int): The index of the specific element to extract.

    Returns:
        list[Cells]: The list of extracted Cells objects.
    """
    return [Cells(
        data= column.get_data()[index]
            if isinstance(column.get_data()[index], HTMLComponent)
            else Text(column.get_data()[index]),
        alignment= column.alignment) for column in columns]

def _get_additional_files(columns: list[TableColumn]) -> list[AdditionalFile]:
    return sum((collect_additional_files(column.get_data()) for column in columns), [])


@attrs.define
class Table(HTMLComponent):
    """
    Represents an vertical HTML table.

    Attributes:
        columns (list[TableColumn]): The columns of the table.

        class_ (Optional[str]): The HTML class of the table for CSS.

        width_percent (Optional[int]): The width of the table as a percentage
        of page width.
    """
    columns: list[TableColumn] = attrs.field(
        metadata={'description': 'The columns of the table'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(TableColumn)),
        kw_only=True)
    class_ : Optional[str] = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        metadata={'description': 'The class of the table'},
        kw_only=True)

    width_percent: Optional[int] = attrs.field(
        default=80, # type: ignore
        validator=[attrs.validators.optional(attrs.validators.instance_of(int)), # type: ignore
                   attrs.validators.optional(attrs.validators.in_(range(1, 101)))], # type: ignore
        metadata={'description': 'The width of the table as a percentage of page width'},
        kw_only=True)

    center: Optional[bool] = attrs.field(
        default=True,
        metadata={'description': 'Center the table'},
        kw_only=True)

    legend: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The legend of the table'},
        kw_only=True)

    def __attrs_post_init__(self):
        self.columns = _validate_table_columns(self.columns)

    def render(self) -> str:
        """
        Renders the HTML representation of the table.

        Returns:
            str: The HTML representation of the table.
        """
        # create the class attribute
        class_attr = f' class="{self.class_}"' if self.class_ else ""

        #manage style
        style_attribute = ""

        if self.center:
            style_attribute += "margin-left:auto;margin-right:auto;"

        if self.width_percent:
            style_attribute += f"width:{self.width_percent}%;"

        if style_attribute:
            style_attribute = f' style="{style_attribute}"'

        # create the legend
        legend = create_block(
            open_prefix="<caption>",
            close_suffix="</caption>",
            content=self.legend,
            inline=False,
            indentation_size=self._indent_value
        ) if self.legend else ""


        # create header of the table
        headers = _extract_headers(self.columns)
        header_row = _create_HTML_table_row(headers, balise="th")

        header_row = create_block(
            open_prefix="<thead>",
            close_suffix="</thead>",
            content=header_row,
            inline=False,
            indentation_size=self._indent_value
        )

        # create the body of the table
        body_rows = []
        for idx in range(self.columns[0].length()):
            elements = _extract_specific_elements(self.columns, idx)
            body_rows.append(_create_HTML_table_row(elements))

        body = create_block(
            open_prefix="<tbody>",
            close_suffix="</tbody>",
            content="\n".join(body_rows),
            inline=False,
            indentation_size=self._indent_value
        )

        return create_block(
            open_prefix=f"<table{class_attr}{style_attribute}>",
            close_suffix="</table>",
            content=f"{legend}{header_row}\n{body}",
            inline=False,
            indentation_size=self._indent_value
        )

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Gets the additional files associated with the table.

        Returns:
            list[AdditionalFile]: The additional files associated with the table.
        """
        return _get_additional_files(self.columns)
