"""
Data munging
"""

from typing import Callable, Dict, IO, List, Optional, Tuple, Union,\
    Pattern
from shutil import rmtree
from pathlib import Path
import webbrowser
import textwrap
import sys

from datasense import random_data, timedelta_data, datetime_data
from pandas.api.types import CategoricalDtype
from beautifultable import BeautifulTable
import pandas as pd
import numpy as np


def dataframe_info(
    df: pd.DataFrame,
    file_in: str
) -> pd.DataFrame:
    """
    Describe a dataframe.

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
    Display count and list of boolean columns
        (columns_bool_count, columns_bool_list)
    Display count and list of float columns
        (columns_float_count, columns_float_list)
    Display count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Display count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Display count and list of string columns
        (columns_object_count, columns_object_list)
    Display count and list of timedelta columns
        (columns_timedelta_count, columns_timedelta_list)
    Display count and list of empty columns
        (columns_empty_count, columns_empty_list)

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    file_in : str
        The name of the file from which df was created.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> my_file = 'myfile.csv'
    >>> df = ds.read_file(my_file)
    >>> df = ds.dataframe_info(
    >>>     df=df,
    >>>     file_in=my_file
    >>> )

    Example 2
    >>> df = ds.create_dataframe()
    >>> df = ds.dataframe_info(
    >>>     df=df,
    >>>     file_in='df'
    >>> )
    """
    df, rows_in_count, rows_out_count, rows_empty_count = process_rows(df)
    df, columns_in_count, columns_non_empty_count, columns_empty_count,\
        columns_empty_list, columns_non_empty_list, columns_bool_list,\
        columns_bool_count,\
        columns_float_list, columns_float_count,\
        columns_integer_list, columns_integer_count, columns_datetime_list,\
        columns_datetime_count, columns_object_list, columns_object_count,\
        columns_category_list, columns_category_count,\
        columns_timedelta_list, columns_timedelta_count\
        = process_columns(df=df)
    wrapper = textwrap.TextWrapper(width=70)
    print('--------------------------')
    print(f'DataFrame information for: {file_in}')
    print()
    print(f'Rows total        : {rows_in_count}')
    print(f'Rows empty        : {rows_empty_count} (deleted)')
    print(f'Rows not empty    : {rows_out_count}')
    print(f'Columns total     : {columns_in_count}')
    print(f'Columns empty     : {columns_empty_count} (deleted)')
    print(f'Columns not empty : {columns_non_empty_count}')
    print()
    number_empty_cells_in_columns(df=df)
    print(f'List of {columns_non_empty_count} non-empty columns:')
    string_not_list = ", ".join(columns_non_empty_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_bool_count} bool columns:')
    string_not_list = ", ".join(columns_bool_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_category_count} category columns:')
    string_not_list = ", ".join(columns_category_list)
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
    print(f'List of {columns_object_count} string columns:')
    string_not_list = ", ".join(columns_object_list)
    new_list = wrapper.wrap(string_not_list)
    for element in new_list:
        print(element)
    print()
    print(f'List of {columns_timedelta_count} timedelta columns:')
    string_not_list = ", ".join(columns_timedelta_list)
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


def find_bool_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all boolean columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_bool : List[str]
        A list of boolean column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_bool = ds.find_bool_columns(df=df)
    >>> print(columns_bool)
    ['b']
    """
    columns_bool = list(df.select_dtypes(include=['bool']).columns)
    return columns_bool


def find_category_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all category columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_category : List[str]
        A list of category column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_category = ds.find_category_columns(df=df)
    >>> print(columns_category)
    ['c']
    """
    columns_category = list(df.select_dtypes(include=['category']).columns)
    return columns_category


def find_datetime_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all datetime columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_datetime : List[str]
        A list of datetime column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_datetime = ds.find_datetime_columns(df=df)
    >>> print(columns_datetime)
    ['t', 'u']
    """
    columns_datetime = list(df.select_dtypes(include=['datetime64']).columns)
    return columns_datetime


def find_float_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all float columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_float : List[str]
        A list of float column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_float = ds.find_float_columns(df=df)
    >>> print(columns_float)
    ['a', 'i', 'x', 'z']
    """
    columns_float = list(df.select_dtypes(include=['float64']).columns)
    return columns_float


def find_int_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all integer columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_int : List[str]
        A list of integer column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_int = ds.find_int_columns(df=df)
    >>> print(columns_int)
    ['y']
    """
    columns_int = list(df.select_dtypes(include=['int64']).columns)
    return columns_int


def find_int_float_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all integer and float columns of a dataframe.

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
    >>> df = ds.create_dataframe()
    >>> columns_int_float = ds.find_int_float_columns(df=df)
    >>> print(columns_int_float)
    ['a', 'i', 'x', 'y', 'z']
    """
    columns_int_float = list(
        df.select_dtypes(include=['int64', 'float64']).columns
    )
    return columns_int_float


def find_object_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all object columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_object : List[str]
        A list of object column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_object = ds.find_object_columns(df=df)
    >>> print(columns_object)
    ['r', 's']
    """
    columns_object = list(df.select_dtypes(include=['object']).columns)
    return columns_object


def find_timedelta_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all timedelta columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    columns_timedelta : List[str]
        A list of timedelta column names.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_timedelta = ds.find_timedelta_columns(df=df)
    >>> print(columns_timedelta)
    ['d']
    """
    columns_timedelta = list(df.select_dtypes(include=['timedelta']).columns)
    return columns_timedelta


def number_empty_cells_in_columns(df: pd.DataFrame) -> None:
    """
    Create a table of data type, empty-cell count, and empty-all percentage
    for non-empty columns of a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> number_empty_cells_in_columns(df=df)
    >>> df = pd.DataFrame({
    >>>     'X': [25.0, 24.0, 35.5, np.nan, 23.1],
    >>>     'Y': [27, 24, np.nan, 23, np.nan],
    >>>     'Z': ['a', 'b', np.nan, 'd', 'e']
    >>> })
    >>> empty_cells = ds.number_empty_cells_in_columns(df=df)
    >>> print(empty_cells)
    Information about non-empty columns
     Column   Data type   Empty cell count   Empty cell %
    -------- ----------- ------------------ -------------
     X        float64                    1           20.0
     Y        float64                    2           40.0
     Z        object                     1           20.0
    """
    print('Information about non-empty columns')
    table = BeautifulTable(maxwidth=90)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    column_alignments = {
        'Column': BeautifulTable.ALIGN_LEFT,
        'Data type': BeautifulTable.ALIGN_LEFT,
        'Empty cell count': BeautifulTable.ALIGN_RIGHT,
        'Empty cell %': BeautifulTable.ALIGN_RIGHT,
    }
    table.columns.header = list(column_alignments.keys())
    for item, (_column_name, alignment) in\
            enumerate(column_alignments.items()):
        table.columns.alignment[item] = alignment
    num_rows = df.shape[0]
    for column_name in df:
        try:
            sum_nan = sum(pd.isnull(df[column_name]))
            percent_nan = round(sum_nan / num_rows * 100, 1)
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
    int,
    List[str],
    int,
    List[str],
    int,
    List[str],
    int,
]:
    """
    Create various counts of columns of a dataframe.

    Create count of columns
        (columns_in_count)
    Create count and list of empty columns
        (columns_empty_count, columns_empty_list)
    Create count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Delete empty columns
    Create count and list of boolean columns
        (columns_bool_count, columns_bool_list)
    Create count and list of category columns
        (columns_category_count, columns_category_list)
    Create count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Create count and list of float columns
        (columns_float_count, columns_float_list)
    Create count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Create count and list of string columns
        (columns_object_count, columns_object_list)
    Create count of timedelta columns
        (columns_timedelta_count, columns_timedelta_list)

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.
    columns_in_count : int
        The count of columns.
    columns_non_empty_count : int
        The count of non-empty columns.
    columns_empty_count: int
        The count of empty columns.
    columns_empty_list : List[str]
        The list of empty columns.
    columns_non_empty_list : List[str]
        The list of non-empty columns.
    columns_bool_list : List[str]
        The list of boolean columns.
    columns_bool_count : int
        The count of boolean columns.
    columns_float_list : List[str]
        The list of float columns.
    columns_float_count : int
        The count of float columns.
    columns_integer_list : List[str]
        The list of integer columns.
    columns_integer_count : int
        The count of integer columns
    columns_datetime_list : List[str]
        The list of datetime columns.
    columns_datetime_count : int
        The count of datetime columns.
    columns_object_list : List[str]
        The list of object columns.
    columns_object_count : int
        The count of object columns.
    columns_category_list : List[str]
        The list of category columns.
    columns_category_count : int
        The count of category columns.
    columns_timedelta_list : List[str]
        The list of timedelta columns.
    columns_timedelta_count : int
        The count of timedelta columns.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> df, columns_in_count, columns_non_empty_count, columns_empty_count,\
    >>>     columns_empty_list, columns_non_empty_list, columns_bool_list,\
    >>>     columns_bool_count, columns_float_list, columns_float_count,\
    >>>     columns_integer_list, columns_integer_count,\
    >>>     columns_datetime_list, columns_datetime_count,\
    >>>     columns_object_list, columns_object_count, columns_category_list,\
    >>>     columns_category_count, columns_timedelta_list,\
    >>>     columns_timedelta_count = ds.process_columns(df=df)
    columns_in_count       : 12
    columns_non_empty_count: 12
    columns_empty_count    : 0
    columns_empty_list     : []
    columns_non_empty_list :
        ['a', 'b', 'c', 'd', 'i', 'r', 's', 't', 'u', 'x', 'y', 'z']
    columns_bool_list      : ['b']
    columns_bool_count     : 1
    columns_float_list     : ['a', 'i', 'x', 'z']
    columns_float_count    : 4
    columns_integer_list   : ['y']
    columns_integer_count  : 1
    columns_datetime_list  : ['t', 'u']
    columns_datetime_count : 2
    columns_object_list    : ['r', 's']
    columns_object_count   : 2
    columns_category_list  : ['c']
    columns_category_count : 1
    columns_timedelta_list : ['d']
    columns_timedelta_count: 1
    """
    columns_empty_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].isnull().all()
    })
    columns_in_count = len(df.columns)
    columns_empty_count = len(columns_empty_list)
    columns_non_empty_count = columns_in_count - columns_empty_count
    df = df.drop(columns_empty_list, axis='columns')
    columns_non_empty_list = sorted(df.columns)
    columns_bool_list = find_bool_columns(df=df)
    columns_bool_count = len(columns_bool_list)
    columns_category_list = find_category_columns(df=df)
    columns_category_count = len(columns_category_list)
    columns_datetime_list = find_datetime_columns(df=df)
    columns_datetime_count = len(columns_datetime_list)
    columns_float_list = find_float_columns(df=df)
    columns_float_count = len(columns_float_list)
    columns_integer_list = find_int_columns(df=df)
    columns_integer_count = len(columns_integer_list)
    columns_object_list = find_object_columns(df=df)
    columns_object_count = len(columns_object_list)
    columns_timedelta_list = find_timedelta_columns(df=df)
    columns_timedelta_count = len(columns_timedelta_list)
    return (
        df, columns_in_count, columns_non_empty_count,
        columns_empty_count, columns_empty_list, columns_non_empty_list,
        columns_bool_list, columns_bool_count,
        columns_float_list, columns_float_count,
        columns_integer_list, columns_integer_count,
        columns_datetime_list, columns_datetime_count,
        columns_object_list, columns_object_count,
        columns_category_list, columns_category_count,
        columns_timedelta_list, columns_timedelta_count
    )


def process_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, int, int, int]:
    """
    Create various counts of rows of a dataframe.
    Drop duplicate rows.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.
    rows_in_count : int
        The count of rows of the input dataframe.
    rows_out_count : int
        The count of rows of the output dataframe.
    rows_empty_count : int
        The count of empty rows of the input dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> df, rows_in_count, rows_out_count, rows_empty_count =\
    >>>     ds.process_rows(df)
    rows_in_count   : 42
    rows_out_count  : 42
    rows_empty_count: 0
    """
    rows_in_count = df.shape[0]
    df = df.dropna(axis='rows', how='all').drop_duplicates()
    rows_out_count = df.shape[0]
    rows_empty_count = rows_in_count - rows_out_count
    return (df, rows_in_count, rows_out_count, rows_empty_count)


def save_file(
    df: Union[pd.DataFrame, pd.Series],
    file_name: str,
    *,
    index: Optional[bool] = False,
    index_label: Optional[str] = None,
    sheet_name: Optional[str] = 'sheet_001',
) -> None:
    """
    Save a DataFrame or Series to a file.

    Parameters
    ----------
    df : Union[pd.DataFrame, pd.Series]
        The dataframe or series to be saved to a file.
    file_name : str
        The name of the file to be saved.
    index : Optional[bool]
        If True, creates an index.
    index_label : Optional[str]
        The index label.
    sheet_name : Optional[str]
        The name of the worksheet in the workbook.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.csv'
    >>> )

    Example 2
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.csv',
    >>>     index=True
    >>> )

    Example 3
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.xlsx'
    >>> )

    Example 4
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.xlsx',
    >>>     index=True,
    >>>     sheet_name='sheet_one'
    >>> )
    """
    if '.csv' in file_name:
        df.to_csv(
            path_or_buf=file_name,
            index=index,
            index_label=index_label
        )
    elif 'ods' in file_name:
        excel_writer = pd.ExcelWriter(file_name)
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            engine='odf',
            index=index,
            index_label=index_label
        )
        excel_writer.save()
    elif 'xlsx' in file_name:
        excel_writer = pd.ExcelWriter(file_name)
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            engine='openpyxl',
            index=index,
            index_label=index_label
        )
        excel_writer.save()


def read_file(
    file_name: str,
    *,
    skiprows: Optional[List[int]] = None,
    column_names_dict: Optional[Dict[str, str]] = {},
    index_columns: Optional[List[str]] = [],
    usecols: Optional[List[str]] = None,
    converters: Optional[dict] = None,
    parse_dates: Optional[List[str]] = False,
    date_parser: Optional[Callable] = None,
    format: Optional[str] = None,
    time_delta_columns: Optional[List[str]] = [],
    category_columns: Optional[List[str]] = [],
    integer_columns: Optional[List[str]] = [],
    float_columns: Optional[List[str]] = [],
    boolean_columns: Optional[List[str]] = [],
    object_columns: Optional[List[str]] = [],
    sort_columns: Optional[List[str]] = [],
    sort_columns_bool: Optional[List[bool]] = [],
    sheet_name: Optional[str] = False,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Create a dataframe from an external file.

    Parameters
    ----------
    file_name : str
        The name of the file to read.
    skiprows : Optional[List[int]]
        The specific row indices to skip.
    column_names_dict : Optional[List[str]]
        The new column names to replace the old column names.
    index_columns : Optional[List[str]]
        The columns to use for the dataframe index.
    usecols : Optional[List[str]] = None,
        The columns to read.
    converters : Optional[dict] = None,
        Dictionary of functions for converting values in certain columns.
    parse_dates : Optional[List[str]] = False,
        The columns to use to parse date and time.
    date_parser : Optional[Callable] = None,
        The function to use for parsing date and time, when pandas needs
        extra help.
    format : Optional[str] = None,
        The str to use for formatting date and time.
    time_delta_columns : Optional[List[str]] = [],
        The columns to change to dtype timedelta.
    category_columns : Optional[List[str]] = []
        The columns to change to dtype category.
    integer_columns : Optional[List[str]] = []
        The columns to change to dtype integer.
    float_columns : Optional[List[str]] = []
        The columns to change to dtype float.
    boolean_columns : Optional[List[str]] = []
        The columns to change to dtype boolean.
    object_columns : Optional[List[str]] = []
        The columns to change to dtype object.
    sort_columns : Optional[List[str]] = []
        The columns on which to sort the dataframe.
    sort_columns_bool : Optional[List[bool]] = []
        The booleans for sort_columns.
    sheet_name : Optional[str] = False
        The name of the worksheet in the workbook.
    nrows : Optional[int] = None
        The number of rows to read.

    Returns
    -------
    df : pd.DataFrame
        The dataframe created from the external file.

    Examples
    --------
    Create a data file for the examples.
    >>> import datsense as ds
    >>> file_name='myfile.csv'
    >>> df = ds.create_dataframe()
    >>> print(df.columns)
    >>> print(df.dtypes)
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name=file_name
    >>> )
    Index(
        ['a', 'b', 'c', 'd', 'i', 'r', 's', 't', 'u', 'x', 'y', 'z'],
        dtype='object'
    )
    a            float64
    b            boolean
    c           category
    d    timedelta64[ns]
    i            float64
    r             object
    s             object
    t     datetime64[ns]
    u     datetime64[ns]
    x            float64
    y              Int64
    z            float64
    dtype: object

    # Example 1
    # Read a csv file. There is no guarantee the column dtypes will be correct.
    # Only [a, i, s, x, y, z] have the correct dtypes.
    >>> df = ds.read_file(file_name=file_name)
    >>> print(df.dtypes)
    a    float64
    b       bool
    c     object
    d     object
    i    float64
    r      int64
    s     object
    t     object
    u     object
    x    float64
    y      int64
    z    float64
    dtype: object

    # Example 2
    # Read a csv file. Ensure the dtypes of datetime columns.
    >>> parse_dates = ['t', 'u']
    >>> data = ds.read_file(
    >>>     file_name=file_name,
    >>>     parse_dates=parse_dates
    >>> )

    Example 3
    Read a csv file. Ensure the dtypes of columns. Rename the columns.
    Set index with another column. Convert float column to integer.
    >>> file_name = 'myfile.csv'
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name=file_name
    >>> )
    >>> column_names_dict = {
    >>>     'a': 'A',
    >>>     'b': 'B',
    >>>     'c': 'C',
    >>>     'd': 'D',
    >>>     'i': 'I',
    >>>     'r': 'R',
    >>>     's': 'S',
    >>>     't': 'T',
    >>>     'u': 'U',
    >>>     'y': 'Y',
    >>>     'x': 'X',
    >>>     'z': 'Z'
    >>> }
    >>> index_columns = ['Y']
    >>> parse_dates = ['t', 'u']
    >>> time_delta_columns = ['D']
    >>> category_columns = ['C']
    >>> integer_columns = ['A', 'I']
    >>> float_columns = ['X']
    >>> boolean_columns = ['R']
    >>> object_columns = ['Z']
    >>> df = ds.read_file(
    >>>     file_name='myfile.csv',
    >>>     column_names_dict=column_names_dict,
    >>>     index_columns=index_columns,
    >>>     date_parser=date_parser(),
    >>>     parse_dates=parse_dates,
    >>>     time_delta_columns=time_delta_columns,
    >>>     category_columns=category_columns,
    >>>     integer_columns=integer_columns
    >>> )
    >>>
    >>>
    >>> def date_parser() -> Callable:
    >>>     return lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    >>>
    >>>
    >>> data = ds.read_file(
    >>>     file_name=file_name,
    >>>     column_names_dict=column_names_dict,
    >>>     index_columns=index_columns,
    >>>     date_time_columns=date_time_columns,
    >>>     date_parser=date_parser,
    >>>     parse_dates=date_time_columns,
    >>>     time_delta_columns=time_delta_columns,
    >>>     category_columns=category_columns,
    >>>     integer_columns=integer_columns
    >>> )

    Example 4
    Read an ods file.
    >>> file_name = 'myfile.ods'
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name=file_name
    >>> )
    >>> parse_dates = ['t', 'u']
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     parse_dates=parse_dates
    >>> )
    >>> ds.dataframe_info(
    >>>     df=df,
    >>>     file_in=file_name
    >>> )

    Example 5
    >>> Read an xlsx file.
    >>> file_name = 'mfile.xlsx'
    >>> sheet_name = 'raw_data'
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     sheet_name=sheet_name
    >>> )
    >>> ds.dataframe_info(
    >>>     df=df,
    >>>     file_in=file_name
    >>> )
    """
    if '.csv' in file_name:
        df = pd.read_csv(
            file_name,
            skiprows=skiprows,
            usecols=usecols,
            converters=converters,
            parse_dates=parse_dates,
            date_parser=date_parser,
            nrows=nrows
        )
    elif '.ods' in file_name:
        df = pd.read_excel(
            file_name,
            skiprows=skiprows,
            usecols=usecols,
            engine='odf',
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            date_parser=date_parser
        )
    elif '.xlsx' in file_name:
        df = pd.read_excel(
            file_name,
            skiprows=skiprows,
            usecols=usecols,
            engine='openpyxl',
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            date_parser=date_parser
        )
    if column_names_dict:
        df = rename_some_columns(
            df=df,
            column_names_dict=column_names_dict
        )
    if index_columns:
        df = df.set_index(index_columns)
    for column in category_columns:
        df[column] = df[column].astype(CategoricalDtype())
    for column in time_delta_columns:
        df[column] = pd.to_timedelta(df[column])
    for column in integer_columns:
        df[column] = df[column].astype('int64')
    for column in float_columns:
        df[column] = df[column].astype('float64')
    for column in boolean_columns:
        df[column] = df[column].astype('bool')
    for column in object_columns:
        df[column] = df[column].astype('object')
    if sort_columns and sort_columns_bool:
        df = sort_rows(
            df=df,
            sort_columns=sort_columns,
            sort_columns_bool=sort_columns_bool,
            kind='mergesort'
        )
    return df


def html_header(
    *,
    header_title: Optional[str] = 'Report',
    header_id: str = 'report'
) -> None:
    """
    Create an html header.

    Parameters
    ----------
    header_title : str = 'Report'
        The header title.
    header_id : str = 'report'
        The header ID.

    Example
    -------
    >>> import datasense as ds
    >>> ds.html_header(
    >>>     header_title=header_title,
    >>>     header_id=header_id
    >>> )
    """
    print('<!DOCTYPE html>')
    print('<html lang="" xml:lang="" xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta charset="utf-8"/>')
    print(
        '<meta content="width=device-width, initial-scale=1.0, '
        'user-scalable=yes" name="viewport"/>'
    )
    print('<style>@import url("support.css");</style>')
    print(f'<title>{header_title}</title>')
    print('</head>')
    print('<body>')
    print(
        f'<h1 class="title"'
        f' id="{header_id}">'
        f'{header_title}</h1>'
    )


def html_footer() -> None:
    """
    Create an html footer.

    Example
    -------
    >>> import datasense as ds
    >>> ds.html_footer()
    """
    print('</body>')
    print('</html>')


def page_break() -> None:
    """
    Create an html page break.

    Example
    -------
    >>> import datasense as ds
    >>> ds.page_break()
    """
    print('</pre>')
    print('<p style="page-break-after:always"></p>')
    print('<p style="page-break-before:always"></p>')
    print('<pre style="white-space: pre-wrap;">')


def html_begin(
    output_url: str,
    *,
    header_title: Optional[str] = 'Report',
    header_id: Optional[str] = 'report',
) -> IO[str]:
    """
    Open a file to write html and set an hmtl header.

    Parameters
    ----------
    output_url : str
        The file name for the html output.
    header_title : Optional[str] = 'Report'
        The file title.
    header_id : Optional[str] = 'report'
        The id for the header_title.

    Returns
    -------
    original_stdout : IO[str]
        A file object for the output of print().
    Examples
    --------
    Example 1
        >>> import datasense as ds
        >>>
        >>> output_url = 'my_html_file.html'
        >>> original_stdout = ds.html_begin(output_url=output_url)

    Example 2
        >>> header_title = 'My Report'
        >>> header_id = 'my-report'
        >>> original_stdout = ds.html_begin(
        >>>     output_url=output_url,
        >>>     header_title=header_title,
        >>>     header_id=header_id
        >>> )
    """
    original_stdout = sys.stdout
    sys.stdout = open(
        file=output_url,
        mode='w'
    )
    html_header(
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    return original_stdout


def html_end(
    original_stdout: IO[str],
    output_url: str
) -> None:
    """
    Create an html footer, close an html file, and open an html file in
    a new tab in a web browser.

    Parameters
    ----------
    original_stdout : IO[str]
        The original stdout.
    output_url : str
        The file name for the html output.

    Example
    -------
        >>> import datasense as ds
        >>>
        >>> output_url = 'my_html_file.html'
        >>> # see original_stdout example in def html_begin()
        >>> ds.html_end(
        >>>     original_stdout=original_stdout,
        >>>     output_url=output_url
        >>> )
    """
    print('</pre>')
    html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout
    webbrowser.open_new_tab(
        url=output_url
    )


def html_figure(
    file_name: str,
    *,
    caption: Optional[str] = None
) -> None:
    """
    Print an html tag for a figure.

    Parameters
    ----------
    file_name : str
        The file name of the image.
    caption : Optional[str]
        The figure caption.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> graph_file = 'my_graph_file.svg'
    >>> fig.savefig(graph_file)
    >>> ds.html_figure(file_name=graph_file)

    Example 2
    >>> ds.html_figure(
    >>>     file_name=graph_file,
    >>>     caption='my graph file caption'
    >>> )
    """
    if caption is None:
        caption = file_name
    print(
        '</pre>'
        '<figure>'
        f'<img src="{file_name}" '
        f'alt="{file_name}"/>'
        f'<figcaption>{caption}</figcaption>'
        '</figure>'
        '<pre style="white-space: pre-wrap;">'
    )


def byte_size(
    num: np.int64,
    suffix: str = 'B'
) -> str:
    """
    Convert bytes to requested units.

    Parameters
    ----------
    num : np.int64
    suffix : str = 'B'

    Returns
    -------
    memory_usage : str

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> print(
    >>>     ds.byte_size(
    >>>         num=df.memory_usage(index=True).sum()
    >>>     )
    >>> )
    3.6 KiB
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    memory_usage = "%.1f %s%s" % (num, 'Yi', suffix)
    return memory_usage


def feature_percent_empty(
    df: pd.DataFrame,
    columns: List[str],
    threshold: float
) -> List[str]:
    """
    Remove features that have NaN > threshold.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    columns : List[str]
        The list of columns to evaluate.
    threshold : float
        The percentage empty threshold value.

    Returns
    -------
    list_columns : List[str]
        The list of columns below the threshold value.

    Example
    -------
    >>> import datasense as ds

    >>> features = ds.feature_percent_empty(
    >>>     df=data,
    >>>     columns=features,
    >>>     threshold=percent_empty_features
    >>> )
    """
    num_rows = df.shape[0]
    list_columns = [col for col in columns if
                    ((df[col].isna().sum() / num_rows * 100) <= threshold)]
    return list_columns


def report_summary(
    start_time: float,
    stop_time: float,
    *,
    read_file_names: Optional[List[str]] = None,
    save_file_names: Optional[List[str]] = None,
    targets: Optional[List[str]] = None,
    features: Optional[List[str]] = None,
    number_knots: Optional[List[int]] = None
) -> None:
    """
    Create a report summary.

    Parameters
    ----------
    start_time : float
        The start time.
    stop_time : float
        The stop time.
    read_file_names : Optional[List[str]] = None
        The list of file names read.
    save_file_names : Optional[List[str]] = None
        The list of file names saved.
    targets : Optional[List[str]] = None
        The list of target variables.
    features : Optional[List[str]] = None
        Thje list of feature variables.
    number_knots : Optional[List[str]] = None
        The number of spline knots.

    Example
    -------
    >>> import datasense as ds

    >>> ds.report_summary(
    >>>     start_time=start_time,
    >>>     stop_time=stop_time
    >>> )
    """
    elapsed_time = stop_time - start_time
    print('</pre>')
    print('<h1>Report summary</h1>')
    print('<pre style="white-space: pre-wrap;">')
    print(f'Execution time : {round(elapsed_time, 3)} s')
    if read_file_names:
        print(f'Files read     : {read_file_names}')
    if save_file_names:
        print(f'Files saved    : {save_file_names}')
    if targets:
        print(f'Targets        : {targets}')
    if features:
        print(f'Features       : {features}')
    if number_knots:
        print(f'Number of knots: {number_knots}')


def set_up_graphics_directory(graphics_directory: List[str]) -> None:
    """
    Create empty directories for a path.

    Parameters
    ----------
    graphics_directory : List[str]
        The list of graphics directories.

    Example
    -------
    >>> import datasense as ds
    >>> directory_list = ['directory_one', 'directory_two']
    >>> ds.set_up_graphics_directory(graphics_directory=directory_list)
    """
    for directory in graphics_directory:
        try:
            rmtree(directory)
        except Exception:
            pass
        Path(directory).mkdir(parents=True, exist_ok=True)


def replace_text_numbers(
    df: pd.DataFrame,
    columns: Union[List[str], List[int], List[float], List[Pattern[str]]],
    old: Union[List[str], List[int], List[float], List[Pattern[str]]],
    new: List[int],
    *,
    regex: Optional[bool] = True
) -> pd.DataFrame:
    """
    Replace text or numbers with text or numbers.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    columns: Union[List[str], List[int], List[float], List[Pattern[str]]]
        The list of columns for replacement.
    old: Union[List[str], List[int], List[float], List[Pattern[str]]]
        The list of item to replace.
    new : List[int]
        The list of replacement items.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Examples
    -------
    Example 1
    >>> import datasense as ds
    >>> list_y_1_n_5 = [
    >>>     'Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q06', 'Q10', 'Q17', 'Q18',
    >>>     'Q19', 'Q20', 'Q21', 'Q23', 'Q24', 'Q25'
    >>> ]
    >>> list_y_5_n_1 = [
    >>>     'Q07', 'Q11', 'Q12', 'Q13', 'Q15', 'Q16'
    >>> ]
    >>> data = ds.replace_text_numbers(
    >>>     df=data,
    >>>     columns=list_y_1_n_5,
    >>>     old=['Yes', 'No'],
    >>>     new=[1, 5],
    >>>     regex=False
    >>> )
    >>> data = ds.replace_text_numbers(
    >>>     df=data,
    >>>     columns=list_y_5_n_1,
    >>>     old=['Yes', 'No'],
    >>>     new=[5, 1],
    >>>     regex=False
    >>> )

    Example 2
    >>> data = ds.replace_text_numbers(
    >>>     df=data,
    >>>     columns=['Q23'],
    >>>     old=[r'\xa0'],
    >>>     new=[r' '],
    >>>     regex=True
    >>> )

    Example 3
    >>> data = ds.replace_text_numbers(
    >>>     df=data,
    >>>     columns=['address_country'],
    >>>     old=[
    >>>         'AD', 'AE', 'AF', 'AG',
    >>>         'AI', 'AL', 'AM', 'AN',
    >>>         'AO', 'AQ', 'AR', 'AS',
    >>>         'AT', 'AU', 'AW', 'AZ',
    >>>     ]
    >>>     new=[
    >>>         'Andorra', 'Unit.Arab Emir.', 'Afghanistan', 'Antigua/Barbuda',
    >>>         'Anguilla', 'Albania', 'Armenia', 'Niederl.Antill.',
    >>>         'Angola', 'Antarctica', 'Argentina', 'Samoa,American',
    >>>         'Austria', 'Australia', 'Aruba', 'Azerbaijan',
    >>>     ],
    >>>     regex=False
    >>> )
    """
    dfnew = df.copy(deep=True)
    for column in columns:
        dfnew[column] = dfnew[column].replace(
            to_replace=old,
            value=new,
            regex=regex
        )
    return dfnew


def create_dataframe() -> pd.DataFrame:
    """
    Create a Pandas dataframe.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> df = create_dataframe()
    """
    df = pd.DataFrame(
        {
            'a': random_data(
                distribution='uniform',
                size=42,
                loc=13,
                scale=70
            ),
            'b': random_data(distribution='bool'),
            'c': random_data(distribution='categories'),
            'd': timedelta_data(),
            'i': random_data(
                distribution='uniform',
                size=42,
                loc=13,
                scale=70
            ),
            'r': random_data(
                distribution='strings',
                strings=['0', '1']
            ),
            's': random_data(distribution='strings'),
            't': datetime_data(),
            'u': datetime_data(),
            'x': random_data(distribution='norm'),
            'y': random_data(distribution='randint'),
            'z': random_data(distribution='uniform')
        }
    )
    return df


def delete_rows(
    df: pd.DataFrame,
    delete_row_criteria: Tuple[str, int]
) -> pd.DataFrame:
    """
    Delete rows of a dataframe based on a value in one column.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    delete_row_criteria : Tuple[str, int]
        A tuple of the column name containing an integer for deletion code.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.delete_rows(
    >>>     df=df,
    >>>     delete_row_criteria=['Batch Acceptance', 1]
    >>> )
    """

    if delete_row_criteria:
        df = df.loc[~(df[delete_row_criteria[0]] == delete_row_criteria[1])]
    return df


def delete_columns(
    df: pd.DataFrame,
    columns: List[str]
) -> pd.DataFrame:
    """
    Delete columns of a dataframe using a list.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    columns : List[str]
        A list of column names.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.delete_columns(
    >>>     df=df,
    >>>     columns=columns
    >>> )
    """
    df = df.drop(columns=columns)
    return df


def sort_rows(
    df: pd.DataFrame,
    sort_columns: List[str],
    sort_columns_bool: List[bool],
    kind: str = 'mergesort'
) -> pd.DataFrame:
    """
    Sort a dataframe in time-ascending order for one column.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    sort_columns : List[str]
        The sort columns.
    sort_columns_bool : List[bool]
        The booleans for sort_columns: True = ascending, False = descending.
    kind: str = 'mergesort'
        The sort algorithm.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.sort_rows(
    >>>     df=df,
    >>>     sort_columns=sort_columns,
    >>>     sort_columns_bool=sort_columns_bool,
    >>>     kind='mergesort'
    >>> )
    """

    df = df.sort_values(
        by=sort_columns,
        axis='index',
        ascending=sort_columns_bool,
        kind=kind
    )
    return df


def rename_all_columns(
    df: pd.DataFrame,
    labels: List[str]
) -> pd.DataFrame:
    """
    Rename all dataframe columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    labels : List[str]
        The list of all column names.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.rename_all_columns(
    >>>     df=df,
    >>>     labels=labels
    >>> )
    """
    df = df.set_axis(
        labels=labels,
        axis='columns'
    )
    return df


def rename_some_columns(
    df: pd.DataFrame,
    column_names_dict: Dict[str, str]
) -> pd.DataFrame:
    """
    Rename some columns with a dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    column_names_dict : Dict[str, str]
        The dictionary of old:new column names.

    Returns
    -------
    df : pd.DataFrame
        The output dataframe.

    Example
    -------
    >>> import datasense as ds
    >>> df = ds.rename_some_columns(
    >>>     df=df,
    >>>     column_names_dict=column_names_dict
    >>> )
    """
    df = df.rename(columns=column_names_dict)
    return df


def replace_column_values(
    s: pd.Series,
    replace_dict: Dict[str, str]
) -> pd.Series:
    """
    Replace values in a series using a dictionary.

    Parameters
    ----------
    s : pd.Series
        The input series.
    replace_dict : Union[Dict[str, str], Dict[int, int], Dict[float, float]]
        The dictionary of values to replace.

    Returns:
    s : pd.Series
        The output series.

    Examples
    -------=
    >>> import datasense as ds
    >>> df = ds.replace_column_values(
    >>>     df=df,
    >>>     column=column,
    >>>     replace_dict=replace_dict
    >>> )
    """
    s = s.replace(
        to_replace=replace_dict,
        regex=True,
        value=None
    )
    return s


__all__ = (
    'dataframe_info',
    'find_bool_columns',
    'find_category_columns',
    'find_datetime_columns',
    'find_float_columns',
    'find_int_columns',
    'find_int_float_columns',
    'find_object_columns',
    'find_timedelta_columns',
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
    'byte_size',
    'feature_percent_empty',
    'report_summary',
    'set_up_graphics_directory',
    'replace_text_numbers',
    'create_dataframe',
    'delete_rows',
    'delete_columns',
    'sort_rows',
    'rename_all_columns',
    'rename_some_columns',
    'replace_column_values',
)
