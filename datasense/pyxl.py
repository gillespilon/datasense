"""
openpyxl functions
"""

from typing import List, Optional

from openpyxl.styles import Alignment, Font, NamedStyle, PatternFill


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
    >>> import datasense as ds.
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
    ws,
    min_row: int
) -> List[int]:
    """
    Create list of row numbers of empty worksheet rows

    Parameters
    ----------
    ws : openpyxl worksheet
    min_row : int
        Start row for iteration

    Returns
    -------
    ws : List[int]
        List of row numbers

    Example
    -------
    Remove empty rows starting from row 2
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
    ws,
    empty_rows: List[int]
):
    """
    Delete empty worksheet rows

    Parameters
    ----------
    ws : openpyxl worksheet
    empty_rows : List[int]
        List of row numbers

    Returns
    -------
    ws : openpyxl worksheet

    Example
    -------
    Remove empty rows found
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


__all__ = (
    'style_header',
    'list_empty_worksheet_rows',
    'remove_empty_worksheet_rows',
)
