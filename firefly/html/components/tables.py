# see https://github.com/sbi-rviot/ph_table
# https://www.youtube.com/watch?v=biI9OFH6Nmg&t=113s
# https://tympanus.net/codrops/2012/11/02/heading-set-styling-with-css/


from dataclasses import dataclass
from typing import Literal, Optional
import attrs


from firefly.tools.strings import indent
from .components import AdditionalFile, HTMLComponent, collect_additional_files
from .paragraph import Text


@dataclass
class TableColumn():
    header: str
    data: list[HTMLComponent | str]
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

    def length(self) -> int:
        return len(self.data)

    def get_data(self) -> list[HTMLComponent]:
        return [Text(data) if isinstance(data, str) else data for data in self.data]

@dataclass
class Cells():
    data : HTMLComponent
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

def _create_HTML_table_row(
     row_elements: list[Cells],
     balise: Literal["th", "td"] = "td",
     indent_value: int = 4
    ) -> str:

    elements_str = ""
    for element in row_elements:
        # create alignement attribute
        alignement_attr = f' align="{element.alignment}"' \
            if element.alignment else ""

        # create width attribute
        width_attr = f' style="width:{element.width_percent}%"' \
            if element.width_percent else ""

        # create the element
        elements_str += f"<{balise}{alignement_attr}{width_attr}>\n" \
            f"{indent(element.data.render(),indent_value)}\n" \
            f"</{balise}>\n"

    cells = "".join(elements_str)

    return f"<tr>\n{indent(cells,indent_value)}</tr>\n"

def _validate_table_columns(columns: list[TableColumn]) -> list[TableColumn]:
    if not columns:
        raise ValueError("The table must have at least one column.")
    if not all(isinstance(column, TableColumn) for column in columns):
        raise ValueError("All columns must be of type TableColumn.")

    # check if all columns have the same length
    if len({column.length() for column in columns}) > 1:
        raise ValueError("All columns must have the same length.")

    return columns

def _extract_headers(columns: list[TableColumn]) -> list[Cells]:
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
    Represents an HTML table.

    Attributes:
        columns (list[TableColumn]): The columns of the table.
        class_ (Optional[str]): The HTML class of the table for CSS.
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

    def __attrs_post_init__(self):
        self.columns = _validate_table_columns(self.columns)

    def render(self) -> str:
        """
        Renders the HTML representation of the table.

        Returns:
            str: The HTML representation of the table.
        """
        # create header of the table
        headers = _extract_headers(self.columns)
        header_row = _create_HTML_table_row(headers, balise="th")

        # create the class attribute
        class_attr = f' class="{self.class_}"' if self.class_ else ""

        # create the body of the table
        body_rows = []
        for idx in range(self.columns[0].length()):
            elements = _extract_specific_elements(self.columns, idx)
            body_rows.append(_create_HTML_table_row(elements))
        body = "".join(body_rows)
        return (f'<table{class_attr} style="width:100%">' +
                f'\n{indent(header_row,self._indent_value)}\n' +
                f"{indent(body,self._indent_value)}\n</table>")

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Gets the additional files associated with the table.

        Returns:
            list[AdditionalFile]: The additional files associated with the table.
        """
        return _get_additional_files(self.columns)
