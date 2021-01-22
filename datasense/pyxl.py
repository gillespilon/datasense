"""
openpyxl functions
"""

from typing import Optional

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


__all__ = (
    'style_header',
)
