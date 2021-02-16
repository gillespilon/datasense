"""
openpyxl functions
"""

from typing import List, Optional, Tuple, Union
from pathlib import Path

from openpyxl.styles import Alignment, Font, NamedStyle, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import pandas as pd
import openpyxl


def style_header(
    *,
    font_bold: Optional[bool] = True,
    align_horizontal: Optional[str] = 'center',
    align_vertical: Optional[str] = 'center',
    fill_type: Optional[str] = 'solid',
    color_foreground: Optional[str] = 'd9d9d9'
):
    """
    Define a style typically used to style the first row of a worksheet.

    Parameters
    ----------
    font_bold : Optional[bool] = True
        The boolean for making a font bold.
    align_horizontal : Optional[str] = 'center'
        The string for horizontal alignment of a cell.
    align_vertical : Optional[str] = 'center'
        The string for vertical alignment of a cell.
    fill_type : Optional[str] = 'solid'
        The string for the type of fill of a cell.
    color_foreground : Optional[str] = 'd9d9d9'
        The string for the foreground color of a cell.

    Example
    -------
    >>> import datasense as ds
    >>> ds.style_header()
    """
    header_style = NamedStyle(name='header_style')
    header_style.font = Font(bold=font_bold)
    header_style.alignment = Alignment(
        horizontal=align_horizontal,
        vertical=align_vertical
    )
    header_style.fill = PatternFill(
        fill_type=fill_type,
        fgColor=color_foreground
    )


def list_empty_worksheet_rows(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    min_row: int
) -> List[int]:
    """
    Create list of row numbers of empty worksheet rows.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.
    min_row : int
        Start row for iteration.

    Returns
    -------
    empty_rows : List[int]
        List of row numbers.

    Example
    -------
    Remove empty rows starting from row 2.
    >>> import datasense as ds
    >>> ws = wb[sheet_name]
    >>> empty_rows = ds.list_empty_worksheet_rows(
    >>>     ws=ws,
    >>>     min_row=2
    >>> )

    """
    empty_rows = []
    for row in ws.iter_rows(min_row=min_row):
        onerow = [cell.value for cell in row]
        if all(item == onerow[0] for item in onerow):
            empty_rows.append(row[0].row)
    return empty_rows


def remove_empty_worksheet_rows(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    empty_rows: List[int]
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    Delete empty worksheet rows.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.
    empty_rows : List[int]
        List of row numbers.

    Returns
    -------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.

    Example
    -------
    Remove empty rows found.
    >>> import datasense as ds
    >>> ws = ds.remove_empty_worksheet_rows(
    >>>     ws=ws,
    >>>     empty_rows=empty_rows
    >>> )
    """
    for row_idx in reversed(empty_rows):
        ws.delete_rows(
            idx=row_idx,
            amount=1
        )
    return ws


def remove_worksheet_rows(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    rows_to_remove: List[int]
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    Remove worksheet rows.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.
    rows_to_remove: List[int]
        The list of row numbers to remove.

    Returns
    -------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.

    Example
    -------
    >>> import datasense as ds
    >>> ws = ds.remove_worksheet_rows(
    >>>     ws=ws,
    >>>     rows_to_remove=rows_to_remove
    >>> )
    """
    for row in rows_to_remove:
        ws.delete_rows(
            idx=row,
            amount=1
        )
    return ws


def list_duplicate_worksheet_rows(
    ws: openpyxl.worksheet.worksheet.Worksheet
) -> List[int]:
    """
    Find duplicate rows in a worksheet.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.

    Returns
    -------
    duplicate_rows : List[int]
        A list of duplicate row numbers.

    Example
    -------
    >>> import datasense as ds
    >>> duplicate_rows = ds.list_duplicate_worksheet_rows(ws=ws)
    >>> ws = ds.remove_worksheet_rows(
    >>>     ws=ws,
    >>>     duplicate_rows=duplicate_rows
    >>> )
    """
    duplicate_rows = []
    unique_rows = []
    for row in ws.rows:
        working_list = []
        for cell in row:
            working_list.append(cell.value)
        if working_list not in unique_rows:
            unique_rows.append(working_list)
        else:
            duplicate_rows.append(cell.row)
    return duplicate_rows


def read_workbook(
    filename: Union[Path, str],
    *,
    data_only: Optional[bool] = True
) -> Tuple[openpyxl.workbook.Workbook, List[str]]:
    """
    Read a workbook, print the Path, and print the sheet names.

    Parameters
    ----------
    filename : Union[Path, str]
        The file containing the workbook.
    data_only : Optional[bool] = True
        If True, read values stored in the cells. If False, read formulae
        stored in the cells.

    Returns
    -------
    wb : openpyxl.workbook.Workbook
        A workbook.
    sheet_names : List[str]
        The sheet names in the workbook.

    Examples
    --------
    >>> import datasense as ds
    >>> wb, sheet_names = ds.read_workbook(
    >>>     filename=file,
    >>>     data_only=True
    >>> )
    """
    wb = load_workbook(
        filename=filename,
        data_only=data_only
    )
    print('File:')
    print(filename)
    print('Sheet names found:')
    sheet_names = wb.sheetnames
    print(wb.sheetnames)
    return (wb, sheet_names)


def change_case_worksheet_columns(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    min_col: int,
    max_col: int,
    min_row: int,
    max_row: int,
    case: str = 'upper'
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    Change case for one or more worksheet columns.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        The worksheet in which to change the case of column(s).
    min_col : int
        The first column in the range to change.
    max_col : int
        The last column in the range to change.
    min_row : int
        The first row in the range to change.
    max_row : int
        The last row in the range to change.
    case: str = 'upper'
        The case to change. Currently only upper or lower.

    Returns
    -------
    ws : openpyxl.worksheet.worksheet.Worksheet
        A worksheet from a workbook.

    Example
    -------
    >>> import datasense as ds
    >>> ws = ds.change_case_worksheet_columns(
    >>>     ws=ws,
    >>>     min_col=4,
    >>>     max_col=6,
    >>>     min_row=2,
    >>>     max_row=ws.max_row,
    >>>     case='upper'
    >>> )
    """
    for col in ws.iter_cols(
        min_col=min_col,
        max_col=max_col,
        min_row=min_row,
        max_row=max_row
    ):
        for cell in col:
            if case == 'upper':
                cell.value = str(cell.value).upper()
            elif case == 'lower':
                cell.value = str(cell.value).lower()
    return ws


def write_dataframe_to_worksheet(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    df: pd.DataFrame,
    index: bool = False,
    header: bool = True
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    Write a dataframe to a worksheet.

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
        The worksheet to which the dataframe will be written.
    df : pd.DataFrame
        The dataframe of data.
    index : bool = False
        Boolean to determine if dataframe index is written to worksheet.
    header : bool = True
        Boolean to determine if dataframe header is written to worksheet.

    Returns
    -------
    ws : openpyxl.worksheet.worksheet.Worksheet
        The worksheet created.

    Example
    >>> import datasense as ds
    >>> ws = ds.write_dataframe_to_worksheet(
    >>>     ws=ws,
    >>>     df=df,
    >>>     index=False,
    >>>     header=True
    >>> )
    """
    for row in dataframe_to_rows(
        df=df,
        index=index,
        header=header
    ):
        ws.append(row)
    return ws


__all__ = (
    'style_header',
    'list_empty_worksheet_rows',
    'remove_empty_worksheet_rows',
    'remove_worksheet_rows',
    'list_duplicate_worksheet_rows',
    'read_workbook',
    'change_case_worksheet_columns',
    'write_dataframe_to_worksheet',
)
