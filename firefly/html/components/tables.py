# see https://github.com/sbi-rviot/ph_table
# https://www.youtube.com/watch?v=biI9OFH6Nmg&t=113s
# https://tympanus.net/codrops/2012/11/02/heading-set-styling-with-css/


from dataclasses import dataclass
from typing import Literal
import attrs


from firefly.tools.strings import indent
from .components import AdditionalFile, HTMLComponent, collect_additional_files
from .paragraph import Text


@dataclass
class TableColumn():
    header: str
    data: list[HTMLComponent | str]
    #TODO : add alignement parameters for the column (https://tympanus.net/codrops/2012/11/02/heading-set-styling-with-css/)

    def length(self) -> int:
        return len(self.data)

    def get_data(self) -> list[HTMLComponent]:

        return [Text(data) if isinstance(data, str) else data for data in self.data]

def _create_HTML_table_row(
     row_elements: list[str],
     balise: Literal["th", "td"] = "td",
     indent_value: int = 4
    ) -> str:

    cells = "".join(
        f"<{balise}>\n{indent(element,indent_value)}\n</{balise}>\n"
        for element in row_elements)
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

def _extract_headers(columns: list[TableColumn]) -> list[str]:
    return [column.header for column in columns]

def _extract_specific_elements(
    columns: list[TableColumn],
    index: int
) -> list[str]:
    return [column.get_data()[index].render() for column in columns]

def _get_additional_files(columns: list[TableColumn]) -> list[AdditionalFile]:
    return sum((collect_additional_files(column.get_data()) for column in columns), [])


@attrs.define
class Table(HTMLComponent):
    columns: list[TableColumn] = attrs.field(
        metadata={'description': 'The columns of the table'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(TableColumn)),
        kw_only=True)

    indentation: int = attrs.field(
        metadata={'description': 'The indentation size for the content'},
        validator=attrs.validators.instance_of(int),
        default=4, # type: ignore
        kw_only=True) # type: ignore
    
    def __attrs_post_init__(self):
        self.columns = _validate_table_columns(self.columns)


    def render(self) -> str:

        # create header of the table
        headers = _extract_headers(self.columns)
        header_row = _create_HTML_table_row(headers, balise="th")

        # create the body of the table
        body_rows = []
        for idx in range(self.columns[0].length()):
            elements = _extract_specific_elements(self.columns, idx)
            body_rows.append(_create_HTML_table_row(elements))
        body = "".join(body_rows)
        return (f"<table>\n{indent(header_row,self.indentation)}\n" +
                f"{indent(body,self.indentation)}\n</table>")

    def get_additional_files(self) -> list[AdditionalFile]:
        return _get_additional_files(self.columns)
