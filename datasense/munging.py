'''
Data munging
'''

from typing import IO, List, Optional, Tuple
from datetime import datetime
import webbrowser
import textwrap
import sys

from beautifultable import BeautifulTable
import pandas as pd


def dataframe_info(
    df: pd.DataFrame,
    filein: str
) -> pd.DataFrame:
    '''
    Describe a DataFrame.

    Display count of rows (rows_in_count)
    Display count of empty rows (rows_empty_count)
    Display count of non-empty rows (rows_out_count)
    Display count of columns (columns_in_count)
    Display count of empty columns (columns_empty_count)
    Display count of non-empty columns (columns_non_empty_count)
    Display table of data type, empty cell count, and empty cell percentage
        for non-empty columns
    Display count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Display count and list of float columns
        (columns_float_count, columns_float_list)
    Display count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Display count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Display count and list of string columns
        (columns_object_count, columns_object_list)
    Display count and list of empty columns
        (columns_empty_count, columns_empty_list)

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    filein : str
        The name of the file from which df was created.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.dataframe_info(
    >>>     df=df,
    >>>     filein='myfile.csv'
    >>> )
    '''
    df, rows_in_count, rows_out_count, rows_empty_count = process_rows(df)
    df, columns_in_count, columns_non_empty_count, columns_empty_count,\
        columns_empty_list, columns_non_empty_list, columns_float_list,\
        columns_float_count, columns_integer_list, columns_integer_count,\
        columns_datetime_list, columns_datetime_count,\
        columns_object_list, columns_object_count\
        = process_columns(df)
    wrapper = textwrap.TextWrapper(width=70)
    print('--------------------------')
    print(f'DataFrame information for: {filein}')
    print()
    print(f'Rows total        : {rows_in_count}')
    print(f'Rows empty        : {rows_empty_count} (deleted)')
    print(f'Rows not empty    : {rows_out_count}')
    print(f'Columns total     : {columns_in_count}')
    print(f'Columns empty     : {columns_empty_count} (deleted)')
    print(f'Columns not empty : {columns_non_empty_count}')
    print()
    number_empty_cells_in_columns(df)
    print(f'List of {columns_non_empty_count} non-empty columns:')
    string_not_list = ", ".join(columns_non_empty_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_float_count} float columns:')
    string_not_list = ", ".join(columns_float_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_integer_count} integer columns:')
    string_not_list = ", ".join(columns_integer_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_datetime_count} datetime columns:')
    string_not_list = ", ".join(columns_datetime_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_object_count} string columns:')
    string_not_list = ", ".join(columns_object_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_empty_count} empty columns:')
    string_not_list = ", ".join(columns_empty_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    return df


def find_int_float_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all integer and float columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_int_float : List[str]
        A list of integer and float column names.

    Example
    -------
    >>> import datasense as ds
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform'),
    >>>         't': ds.datetime_data()
    >>>     }
    >>> )
    >>> columns_int_float = ds.find_int_float_columns(df=df)
    >>> print(columns_int_float)
    ['x', 'y']
   """
    columns_int_float = sorted(
        {
            column_name for column_name in df.columns
            if df[column_name].dtype in ('int64', 'float64')
        }
    )
    return columns_int_float


def number_empty_cells_in_columns(df: pd.DataFrame) -> None:
    '''
    Create a table of data type, empty-cell count, and empty-all percentage
    for non-empty columns.
    '''

    print('Information about non-empty columns')
    table = BeautifulTable(maxwidth=90)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    column_alignments = {
        'Column': BeautifulTable.ALIGN_LEFT,
        'Data type': BeautifulTable.ALIGN_LEFT,
        'Empty cell count': BeautifulTable.ALIGN_RIGHT,
        'Empty cell percentage': BeautifulTable.ALIGN_RIGHT,
    }
    table.columns.header = list(column_alignments.keys())
    for item, (_column_name, alignment) in\
            enumerate(column_alignments.items()):
        table.columns.alignment[item] = alignment
    num_rows = df.shape[0]
    for column_name in df:
        try:
            sum_nan = sum(pd.isnull(df[column_name]))
            percent_nan = round(sum_nan / num_rows * 100, 3)
            table.rows.append(
                [column_name,
                 df[column_name].dtype,
                 sum_nan,
                 percent_nan]
            )
        except KeyError:
            print('Error on column:', column_name)
    print(table)
    print()


def process_columns(df: pd.DataFrame) -> Tuple[
    pd.DataFrame,
    int,
    int,
    int,
    List[str],
    List[str],
    List[str],
    int,
    List[str],
    int,
    List[str],
    int,
    List[str],
    int
]:
    '''
    Create various counts of columns.

    Create count of columns
        (columns_in_count)
    Create count and list of empty columns
        (columns_empty_count, columns_empty_list)
    Create count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Delete empty columns
    Create count and list of float columns
        (columns_float_count, columns_float_list)
    Create count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Create count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Create count and list of string columns
        (columns_object_count, columns_object_list)
    '''

    columns_empty_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].isnull().all()
    })
    columns_in_count = len(df.columns)
    columns_empty_count = len(columns_empty_list)
    columns_non_empty_count = columns_in_count - columns_empty_count
    df = df.drop(columns_empty_list, axis='columns')
    columns_non_empty_list = sorted(df.columns)
    columns_float_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'float'
    })
    columns_float_count = len(columns_float_list)
    columns_integer_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'int64'
    })
    columns_integer_count = len(columns_integer_list)
    columns_datetime_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'datetime64[ns]'
    })
    columns_datetime_count = len(columns_datetime_list)
    columns_object_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'object'
    })
    columns_object_count = len(columns_object_list)
    return (
        df, columns_in_count, columns_non_empty_count,
        columns_empty_count, columns_empty_list, columns_non_empty_list,
        columns_float_list, columns_float_count,
        columns_integer_list, columns_integer_count,
        columns_datetime_list, columns_datetime_count,
        columns_object_list, columns_object_count
    )


def process_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, int, int, int]:
    '''
    Create various counts of rows.

    Count number of rows (rows_in_count)
    Delete empty rows
    Count number of non-empty rows (rows_out_count)
    Count number of empty rows (rows_empty_count)
    '''

    rows_in_count = df.shape[0]
    df = df.dropna(axis='rows', how='all')
    rows_out_count = df.shape[0]
    rows_empty_count = rows_in_count - rows_out_count
    return (df, rows_in_count, rows_out_count, rows_empty_count)


def save_file(
    df: pd.DataFrame,
    filename: str,
    *,
    index: Optional[bool] = False
) -> None:
    '''
    Save a DataFrame to a csv file.

    Parameters
    ---------
    df : pd.DataFrame
        The dataframe to be saved to a file.
    filename : str
        The name of the file to be saved.
    index : bool
        If True, creates an index.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'x': ds.random_data(),
    >>>         'y': ds.random_data()
    >>>     }
    >>> )
    >>> ds.save_file(
    >>>     df=df,
    >>>     filename='x_y.csv'
    >>> )

    Example 2
    ---------
    >>> ds.save_file(
    >>>     df=df,
    >>>     filename='x_y.csv',
    >>>     index=True
    >>> )
    '''
    df.to_csv(
        path_or_buf=filename,
        index=index
    )


def read_file(
    filename: str,
    *,
    sheetname: Optional[str] = None,
    indexcol: Optional[bool] = None,
    abscissa: Optional[str] = None,
    datetimeparser: Optional[str] = None,
    columnnamessort: Optional[str] = False
) -> pd.DataFrame:
    '''
    Create a DataFrame from an external file.

    Reads an ods, csv, or xlsx file
    Sorts on abscissa if datetimeparser is True
    Sorts on columnnames if columnnamessort is True

    filename       :
    sheetname      :
    indexcol       :
    abscissa       :
    datetimeparser : str such as %Y-%m-%d %H:%M:%S
    columnnamessort:
    '''

    if '.ods' in filename and abscissa and datetimeparser:
        df = pd.read_excel(
            filename,
            engine='odf',
            parse_dates=[abscissa],
            date_parser=lambda s: datetime.strptime(s, datetimeparser),
        )
    elif '.ods' in filename and abscissa and not datetimeparser:
        df = pd.read_excel(
            filename,
            engine='odf',
            parse_dates=[abscissa]
        )
    elif '.ods' in filename and not abscissa and not datetimeparser:
        df = pd.read_excel(
            filename,
            engine='odf',
        )
    elif '.csv' in filename and abscissa and datetimeparser \
            and indexcol is False:
        df = pd.read_csv(
            filename,
            index_col=indexcol,
            parse_dates=[abscissa],
            date_parser=lambda s: datetime.strptime(s, datetimeparser),
        )
    elif '.csv' in filename and abscissa and datetimeparser:
        df = pd.read_csv(
            filename,
            parse_dates=[abscissa],
            date_parser=lambda s: datetime.strptime(s, datetimeparser),
        )
    elif '.csv' in filename and abscissa:
        df = pd.read_csv(
            filename,
            parse_dates=[abscissa]
        )
    elif '.csv' in filename:
        df = pd.read_csv(
            filename,
        )
    elif '.xlsx' in filename and abscissa and datetimeparser:
        df = pd.read_excel(
            filename,
            parse_dates=[abscissa],
            date_parser=lambda s: datetime.strptime(s, datetimeparser),
        )
    elif '.xlsx' in filename and sheetname and indexcol is False:
        df = pd.read_excel(
            filename,
            sheet_name=sheetname,
            index_col=indexcol
        )
    elif '.xlsx' in filename and not datetimeparser:
        df = pd.read_excel(
            filename,
        )
    if datetimeparser is not None:
        df = df.sort_values(
            by=abscissa,
            axis='rows',
            ascending=True
        )
    if columnnamessort is True:
        sortedcolumnnames = sorted(df.columns)
        df = df[sortedcolumnnames]
    return df


def html_header(
    headertitle: str = 'Report',
    headerid: str = 'report'
) -> None:
    '''
    Creates an html header.
    '''

    print('<!DOCTYPE html>')
    print('<html lang="" xml:lang="" xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta charset="utf-8"/>')
    print(
        '<meta content="width=device-width, initial-scale=1.0, '
        'user-scalable=yes" name="viewport"/>'
    )
    print('<style>@import url("support.css");</style>')
    print(f'<title>{headertitle}</title>')
    print('</head>')
    print('<body>')
    print(
        f'<h1 class="title"'
        f' id="{headerid}">'
        f'{headertitle}</h1>'
    )
    # print('<pre>')


def html_footer() -> None:
    '''
    Creates an html footer.
    '''

    # print('</pre>')
    print('</body>')
    print('</html>')


def page_break():
    '''
    Create a page break for html output.
    '''

    print('<p style="page-break-after:always">')
    print('<p style="page-break-before:always">')


def html_begin(
    outputurl: str,
    *,
    headertitle: Optional[str] = 'Report',
    headerid: Optional[str] = 'report',
) -> IO[str]:
    '''
    Open file to write html and set header.

    Parameters
    ----------
    outputurl : str
        The file name for the html output.
    headertitle : Optional[str]
        The file title.
    headerid : Optional[str]
        The id for the headertitle.

    Examples
    --------
    Example 1
        >>> import datasense as ds
        >>>
        >>> output_url = 'my_html_file.html'
        >>> original_stdout = ds.html_begin(outputurl=output_url)

    Example 2
        >>> header_title = 'My Report'
        >>> header_id = 'my-report'
        >>> original_stdout = ds.html_begin(
        >>>     outputurl=output_url,
        >>>     headertitle=header_title,
        >>>     headerid=header_id
        >>> )
    '''
    originalstdout = sys.stdout
    sys.stdout = open(
        file=outputurl,
        mode='w'
    )
    html_header(
        headertitle=headertitle,
        headerid=headerid
    )
    return originalstdout


def html_end(
    originalstdout: IO[str],
    outputurl: str
) -> None:
    '''
    Set footer, close html file, open html file in new tab in web browser.

    Parameters
    ----------
    originalstdout : IO[str]
        The original stdout.
    outputurl : str
        The file name for the html output.

    Example
    -------
        >>> import datasense as ds
        >>>
        >>> output_url = 'my_html_file.html'
        >>> # see original_stdout example in def html_begin()
        >>> ds.html_end(
        >>>     originalstdout=original_stdout,
        >>>     outputurl=output_url
        >>> )
    '''
    html_footer()
    sys.stdout.close()
    sys.stdout = originalstdout
    webbrowser.open_new_tab(
        url=outputurl
    )


def html_figure(
    filename: str,
    *,
    caption: Optional[str] = None
) -> None:
    """
    Print html tag for a figure.

    Parameters
    ----------
    filename : str
        The file name of the image.
    caption : Optional[str]
        The figure caption.
    """
    if caption is None:
        caption = filename
    print(
        '<figure>'
        f'<img src="{filename}" '
        f'alt="{filename}"/>'
        f'<figcaption>{caption}</figcaption>'
        '</figure>'
    )


__all__ = (
    'dataframe_info',
    'find_int_float_columns',
    'number_empty_cells_in_columns',
    'process_columns',
    'process_rows',
    'read_file',
    'save_file',
    'html_header',
    'html_footer',
    'page_break',
    'html_begin',
    'html_end',
    'html_figure',
)
