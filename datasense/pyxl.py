"""
openpyxl functions
"""

from typing import IO, List, Optional, Tuple, Union
from pathlib import Path
import time
import sys
import io

from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill,\
    Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from datasense import report_summary, html_end
from openpyxl import load_workbook
import pandas as pd
import numpy as np
import openpyxl


def cell_fill_down(
    ws: Worksheet,
    min_row: int,
    max_row: int,
    min_col: int,
    max_col: int
) -> Worksheet:
    """
    Fill empty cell with the value from the cell above

    Parameters
    ----------
    ws : Worksheet
        The worksheet in which to change the case of column(s).
    min_row : int
        The first row in the range to change.
    max_row : int
        The last row in the range to change.
    min_col : int
        The first column in the range to change.
    max_col : int
        The last column in the range to change.

    Returns
    -------
    ws : Worksheet

    Example
    -------
    >>> for column in fill_down_columns:
    >>>     ws = ds.cell_fill_down(
    >>>         ws=ws,
    >>>         min_row=row_below_labels,
    >>>         max_row=ws.max_row,
    >>>         min_col=column_names_numbers[column],
    >>>         max_col=column_names_numbers[column]
    >>>     )
    """
    row_count = 0
    for row in ws.iter_rows(
        min_col=min_col,
        max_col=max_col
    ):
        for cell in row:
            if cell.value:
                row_count += 1
    if row_count > 0:
        for row in ws.iter_rows(
            min_row=min_row + 1,  # start one row below the 'start' row
            max_row=max_row,
            min_col=min_col,
            max_col=max_col
        ):
            for cell in row:
                if not cell.value:
                    cell.value = ws[cell.row - 1][min_col - 1].value
    return ws


def cell_style(
    wb: Workbook,
    style_name: str = 'cell_style',
    *,
    font_name: Optional[str] = 'Calibri',
    font_size: Optional[int] = 11,
    font_bold: Optional[bool] = True,
    font_colour: Optional[str] = '000000',
    horizontal_alignment: Optional[str] = 'center',
    vertical_alignment: Optional[str] = 'center',
    wrap_text: Union[str, bool] = None,
    fill_type: Union[str, bool] = 'solid',
    foreground_colour: Union[str, bool] = 'd9d9d9',
    border_style: Union[str, bool] = None,
    border_colour: Union[str, bool] = None,
) -> NamedStyle:
    """
    Define a cell style
    ----------
    style_name : str = 'cell_style'
        The name for the cell style.
    font_name : Optional[str] = 'Calibri'
        The font name for the style.
    font_size : Optional[int] = 11
        The font size for the style.
    font_bold : Optional[bool] = True
        A boolean to apply bold style.
    font_colour : Optional[str] = 'ffffff'
        The string for the font colour.
    horizontal_alignment : Optional[str] = 'center'
        The string for horizontal alignment.
    vertical_alignment : Optional[str] = 'center'
        The string for vertical alignment.
    fill_type : Optional[str] = 'solid'
        The string for the fill type.
    foreground_colour : Optional[str] = 'd9d9d9'
        The string for the foreground colour.

    Returns
    -------
    row_style : NamedStyle
        The named style.

    Example
    -------
    >>> red_cell_style = ds.cell_style(
    >>>     style_name='red_cell_style',
    >>>     font_colour='ffffff',
    >>>     foreground_colour='c00000'
    >>> )
    >>> wb.add_named_style(red_cell_style)
    >>> for cell in ['C1', 'D1', 'E1']:
    >>>     ws[cell].style = red_cell_style
    """
    cell_style = NamedStyle(name=style_name)
    cell_style.font = Font(
        name=font_name,
        size=font_size,
        bold=font_bold,
        color=font_colour
    )
    cell_style.alignment = Alignment(
        horizontal=horizontal_alignment,
        vertical=vertical_alignment,
        wrap_text=wrap_text
    )
    cell_style.fill = PatternFill(
        fill_type=fill_type,
        fgColor=foreground_colour
    )
    cell_style.border = Border(
        bottom=Side(
            border_style=border_style,
            color=border_colour
        )
    )
    wb.add_named_style(cell_style)
    return (wb, cell_style)


def change_case_worksheet_columns(
    ws: Worksheet,
    min_col: int,
    max_col: int,
    min_row: int,
    max_row: int,
    case: str = 'upper'
) -> Worksheet:
    """
    Change case for one or more worksheet columns.

    Parameters
    ----------
    ws : Worksheet
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
    ws : Worksheet
        A worksheet from a workbook.

    Example
    -------
    >>> import datasense as ds
    >>> ws = ds.change_case_worksheet_columns(
    >>>     ws=ws,
    >>>     min_col=4,
    >>>     max_col=6,
    >>>     min_row=1,
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


def exit_script(
    original_stdout: IO[str],
    output_url: str
):
    """
    Exit from a script and complete the html file.

    Parameters
    ----------
    original_stdout : IO[str]
        The original stdout.
    output_url : str
        The output url.

    Example
    -------
    exit_script(
        original_stdout=original_stdout,
        output_url=output_url
    )
    """
    html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )
    sys.exit()


def list_duplicate_worksheet_rows(
    ws: Worksheet,
    *,
    columns_to_ignore: Optional[List[int]] = []
) -> List[int]:
    """
    Find duplicate rows in a worksheet.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    columns_to_ignore : Optional[List[int]] = None
        A list of column numbers to not use in determining duplicate rows.

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
            if cell.column not in columns_to_ignore:
                working_list.append(cell.value)
        if working_list not in unique_rows:
            unique_rows.append(working_list)
        else:
            duplicate_rows.append(cell.row)
    return duplicate_rows


def list_empty_and_nan_worksheet_rows(
    ws: Worksheet,
    min_row: int
) -> List[int]:
    """
    Create list of row numbers of blank worksheet rows.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    min_row : int
        Start row for iteration.

    Returns
    -------
    blank_rows : List[int]
        List of row numbers.

    Example
    -------
    >>> import datasense as ds
    >>> ws = wb[sheetname]
    >>> blank_rows = ds.list_nan_worksheet_rows(
    >>>     ws=ws,
    >>>     min_row=2
    >>> )
    """
    blank_rows = []
    for row in ws.iter_rows(min_row=min_row):
        onerow = [cell.value for cell in row]
        if all(item in [
            None, 'None', 'NONE', '', np.nan
        ] for item in onerow):
            blank_rows.append(row[0].row)
    return blank_rows


def list_empty_except_nan_worksheet_rows(
    ws: Worksheet,
    min_row: int
) -> List[int]:
    """
    Create list of row numbers of empty worksheet rows, except those
    with np.nan.

    Parameters
    ----------
    ws : Worksheet
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
    >>> empty_rows = ds.list_empty_except_nan_worksheet_rows(
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


def list_nan_worksheet_rows(
    ws: Worksheet,
    min_row: int
) -> List[int]:
    """
    Create list of row numbers of blank worksheet rows.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    min_row : int
        Start row for iteration.

    Returns
    -------
    blank_rows : List[int]
        List of row numbers.

    Example
    -------
    >>> import datasense as ds
    >>> ws = wb[sheetname]
    >>> blank_rows = ds.list_nan_worksheet_rows(
    >>>     ws=ws,
    >>>     min_row=2
    >>> )
    """
    blank_rows = []
    for row in ws.iter_rows(min_row=min_row):
        onerow = [cell.value for cell in row]
        if all(item != item for item in onerow):
            blank_rows.append(row[0].row)
    return blank_rows


def list_rows_with_content(
    ws: Worksheet,
    min_row: int,
    column: int,
    text: str
) -> List[int]:
    '''
    List rows that contain specific text in a specified column.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    min_row : int
        Start row for iteration.
    column : int
        The column to search.
    text : str
        The text to search.

    Returns
    -------
    List[int]
        A list of row numbers.

    Example
    -------
    >>> rows_with_text = ds.list_rows_with_content(
    >>>     ws=ws,
    >>>     min_row=2,
    >>>     column=11,
    >>>     text='ETA'
    >>> )
    '''
    rows_with_text = []
    for row in ws.iter_rows(
        min_row=min_row,
        min_col=column,
        max_col=column
    ):
        for cell in row:
            if cell.value == text:
                rows_with_text.append(row[0].row)
    return rows_with_text


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
    wb : Workbook
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
    sheet_names = wb.sheetnames
    return (wb, sheet_names)


def remove_empty_worksheet_rows(
    ws: Worksheet,
    empty_rows: List[int]
) -> Worksheet:
    """
    Delete empty worksheet rows.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    empty_rows : List[int]
        List of row numbers.

    Returns
    -------
    ws : Worksheet
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
    ws: Worksheet,
    rows_to_remove: List[int]
) -> Worksheet:
    """
    Remove worksheet rows.

    Parameters
    ----------
    ws : Worksheet
        A worksheet from a workbook.
    rows_to_remove: List[int]
        The list of row numbers to remove.

    Returns
    -------
    ws : Worksheet
        A worksheet from a workbook.

    Example
    -------
    >>> import datasense as ds
    >>> ws = ds.remove_worksheet_rows(
    >>>     ws=ws,
    >>>     rows_to_remove=rows_to_remove
    >>> )
    """
    for row in reversed(rows_to_remove):
        ws.delete_rows(
            idx=row,
            amount=1
        )
    return ws


def row_style(
    wb: Workbook,
    style_name: str = 'row_style',
    *,
    font_name: Optional[str] = 'Calibri',
    font_size: Optional[int] = 11,
    font_bold: Optional[bool] = True,
    font_colour: Optional[str] = '000000',
    horizontal_alignment: Optional[str] = 'center',
    vertical_alignment: Optional[str] = 'center',
    fill_type: Optional[str] = 'solid',
    foreground_colour: Optional[str] = 'd9d9d9'
) -> NamedStyle:
    """
    Define a row style

    Parameters
    ----------
    style_name : str = 'row_style'
        The name for the row style.
    font_name : Optional[str] = 'Calibri'
        The font name for the style.
    font_size : Optional[int] = 11
        The font size for the style.
    font_bold : Optional[bool] = True
        A boolean to apply bold style.
    font_colour : Optional[Optional[str]] = '000000'
        The string for the font colour.
    horizontal_alignment : Optional[str] = 'center'
        The string for horizontal alignment.
    vertical_alignment : Optional[str] = 'center'
        The string for vertical alignment.
    fill_type : Optional[str] = 'solid'
        The string for the fill type.
    foreground_colour : Optional[str] = 'd9d9d9'
        The string for the foreground colour.

    Returns
    -------
    row_style : NamedStyle,
        The named style.

    Example
    -------
    >>> header_row_style = ds.row_style(
    >>>     style_name='header_row_style'
    >>> )
    >>> wb.add_named_style(header_row_style)
    >>> for row in label_row_numbers:
    >>>     for cell in ws[row]:
    >>>         cell.style = header_row_style
    """
    row_style = NamedStyle(name=style_name)
    row_style.font = Font(
        name=font_name,
        size=font_size,
        bold=font_bold
    )
    row_style.alignment = Alignment(
        horizontal=horizontal_alignment,
        vertical=vertical_alignment
    )
    row_style.fill = PatternFill(
        fill_type=fill_type,
        fgColor=foreground_colour
    )
    wb.add_named_style(row_style)
    return (wb, row_style)


def validate_column_labels(
    ws: Worksheet,
    column_labels: List[str],
    first_column: int,
    last_column: int,
    row_of_labels: int,
    *,
    start_time: Optional[float] = None,
    stop_time: Optional[float] = None,
    original_stdout: Optional[IO[str]] = None,
    output_url: Optional[str] = None

) -> Worksheet:
    """
    Validate the labels of a worksheet with a desired list of labels

    Parameters
    ----------
    ws : Worksheet
        The worksheet to analyze.
    column_labels : List[str]
        The list of desired column labels.
    first_column : int
        The first column of the label range in the worksheet.
    last_column : int
        The last column of the label range in the worksheet.
    row_of_labels : int
        The row number of the labels in the worksheet.
    start_time : Optional[float] = None
        The start time of the script.
    stop_time : Optional[float] = None
        The stop time of the script.
    original_stdout : Optional[IO[str]] = None
        The original stdout.
    output_url : Optional[str] = None
        The output url.

    Returns
    -------
    ws : Worksheet,
        The worksheet to analyze.

    Example
    -------
    >>> ws = ds.validate_column_labels(
    >>>     ws=ws,
    >>>     column_labels=column_labels,
    >>>     first_column=first_column,
    >>>     last_column=last_column,
    >>>     row_of_labels=row_of_labels,
    >>>     start_time=start_time,
    >>>     stop_time=time.time(),
    >>>     original_stdout=original_stdout,
    >>>     output_url=output_url
    >>> )
    """
    labels_found = []
    for col in range(first_column, last_column + 1):
        labels_found.append(ws.cell(row=row_of_labels, column=col).value)
    if len(labels_found) == len(column_labels) and \
            labels_found[-1] == column_labels[-1]:
        for col, label in zip(
            range(first_column, last_column + 1),
            column_labels
        ):
            ws.cell(
                row=1,
                column=col
            ).value = label
    elif stop_time:
        print('Column labels incorrect. Fix. Re-run script.')
        print('XXX File NOT OK XXX')
        stop_time = stop_time
        report_summary(
            start_time=start_time,
            stop_time=stop_time
        )
        exit_script(
            original_stdout=original_stdout,
            output_url=output_url
        )
    return ws


def validate_sheet_names(
    wb: openpyxl.workbook.Workbook,
    file: Union[Path, str],
    sheet_name: str,
    sheet_names: List[str],
    start_time: float,
    original_stdout: io.TextIOWrapper,
    output_url: str
) -> openpyxl.workbook.Workbook:
    """
    Parameters
    ----------
    wb : Workbook,
        A workbook.
    file : Union[Path, str],
        The file containing the workbook.
    sheet_name : str,
        A sheet name in the workbook.
    sheet_names : List[str],
        The sheet names in the workbook.
    start_time : float,
        The start time of the script.
    original_stdout : io.TextIOWrapper,
        The buffered text stream for the html output.
    output_url : str
        The html file name.

    Returns
    -------
    wb : Workbook

    Example
    -------
    >>> import datasense as ds
    >>> wb = validate_sheet_names(
    >>>     wb=wb,
    >>>     file=file,
    >>>     sheet_name=sheet_name,
    >>>     sheet_names=sheet_names,
    >>>     start_time=start_time,
    >>>     original_stdout=original_stdout,
    >>>     output_url=output_url
    >>> )
    """
    if sheet_name not in sheet_names and len(sheet_names) != 1:
        print('Manually rename one of these sheets:')
        print(wb.sheetnames)
        print('Then re-run script')
        print('XXX File NOT OK XXX')
        stop_time = time.time()
        report_summary(
            start_time=start_time,
            stop_time=stop_time
        )
        exit_script(
            original_stdout=original_stdout,
            output_url=output_url
        )
    elif sheet_name not in sheet_names and len(sheet_names) == 1:
        print('One sheet found and it was re-named.')
        ws = wb.active
        ws.title = sheet_name
        wb.save(filename=file)
    elif sheet_name in sheet_names and len(sheet_names) != 1:
        sheet_names_removed = [x for x in sheet_names if x != sheet_name]
        for sheet in sheet_names_removed:
            wb.remove(worksheet=wb[sheet])
        print('Sheet names removed:')
        print(sheet_names_removed)
        wb.save(filename=file)
    return wb


def write_dataframe_to_worksheet(
    ws: Worksheet,
    df: pd.DataFrame,
    index: bool = False,
    header: bool = True
) -> Worksheet:
    """
    Write a dataframe to a worksheet.

    Parameters
    ----------
    ws : Worksheet
        The worksheet to which the dataframe will be written.
    df : pd.DataFrame
        The dataframe of data.
    index : bool = False
        Boolean to determine if dataframe index is written to worksheet.
    header : bool = True
        Boolean to determine if dataframe header is written to worksheet.

    Returns
    -------
    ws : Worksheet
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

    # TODO:
    # Read comments into list
    # for col in ws_out.iter_cols(
    #     min_col=column_names_numbers['Molex PN'],
    #     max_col=column_names_numbers['Molex PN']
    # ):
    #     comments = [c.comment.text for c in col]
    # print(comments)


__all__ = (
    'cell_fill_down',
    'cell_style',
    'change_case_worksheet_columns',
    'exit_script',
    'list_duplicate_worksheet_rows',
    'list_empty_and_nan_worksheet_rows',
    'list_empty_except_nan_worksheet_rows',
    'list_nan_worksheet_rows',
    'list_rows_with_content',
    'read_workbook',
    'remove_empty_worksheet_rows',
    'remove_worksheet_rows',
    'row_style',
    'validate_sheet_names',
    'validate_column_labels',
    'write_dataframe_to_worksheet',
)
