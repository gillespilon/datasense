"""
Data munging
"""

from typing import Callable, Dict, List, NoReturn, Tuple, Union,\
    Pattern
from shutil import copytree, move, rmtree
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk
import textwrap
import psutil
import string
import os

from datasense import random_data, timedelta_data, datetime_data
from pandas.api.types import CategoricalDtype
from beautifultable import BeautifulTable
import pyarrow.feather as ft
from scipy.stats import norm
import pandas as pd
import numpy as np


def dataframe_info(
    *,
    df: pd.DataFrame,
    file_in: Union[Path, str],
    unique_bool: bool = False
) -> pd.DataFrame:
    """
    Describe a DataFrame.

    Display count of rows (rows_in_count)
    Display count of empty rows (rows_empty_count)
    Display count of non-empty rows (rows_out_count)
    Display count of columns (columns_in_count)
    Display count of empty columns (columns_empty_count)
    Display count of non-empty columns (columns_non_empty_count)
    Display table of data type, empty cell count, and empty cell percentage
        for non-empty columns (calls def number_empty_cells_in_columns())
    Display count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Display count and list of boolean columns
        (columns_bool_count, columns_bool_list)
    Display count and list of category columns
        (columns_category_count, columns_category_list)
    Display count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Display count and list of float columns
        (columns_float_count, columns_float_list)
    Display count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Display count and list of string columns
        (columns_object_count, columns_object_list)
    Display count and list of timedelta columns
        (columns_timedelta_count, columns_timedelta_list)
    Display count and list of empty columns
        (columns_empty_count, columns_empty_list)

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    file_in : Union[Path, str]
        The name of the file from which df was created.
    unique_bool : bool = False
        Print unique values of a column if True.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------
    Example 1
    ---------
    >>> df = ds.dataframe_info(
    >>>     df=df,
    >>>     file_in='df'
    >>> )

    Example 2
    ---------
    >>> df = ds.dataframe_info(
    >>>     df=df,
    >>>     file_in='df',
    >>>     unique_bool=True
    >>> )
    """
    df, rows_in_count, rows_out_count, rows_empty_count = process_rows(df=df)
    df, columns_in_count, columns_non_empty_count, columns_empty_count,\
        columns_empty_list, columns_non_empty_list, columns_bool_list,\
        columns_bool_count,\
        columns_float_list, columns_float_count,\
        columns_integer_list, columns_integer_count, columns_datetime_list,\
        columns_datetime_count, columns_object_list, columns_object_count,\
        columns_category_list, columns_category_count,\
        columns_timedelta_list, columns_timedelta_count\
        = process_columns(df=df)
    print('==========================')
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
    print_list_by_item(list=columns_non_empty_list)
    print()
    print(f'List of {columns_bool_count} bool columns:')
    print_list_by_item(list=columns_bool_list)
    print()
    print(f'List of {columns_category_count} category columns:')
    print_list_by_item(list=columns_category_list)
    print()
    print(f'List of {columns_datetime_count} datetime columns:')
    print_list_by_item(list=columns_datetime_list)
    print()
    print(f'List of {columns_float_count} float columns:')
    print_list_by_item(list=columns_float_list)
    print()
    print(f'List of {columns_integer_count} integer columns:')
    print_list_by_item(list=columns_integer_list)
    print()
    print(f'List of {columns_object_count} string columns:')
    print_list_by_item(list=columns_object_list)
    print()
    print(f'List of {columns_timedelta_count} timedelta columns:')
    print_list_by_item(list=columns_timedelta_list)
    print()
    print(f'List of {columns_empty_count} empty columns:')
    print_list_by_item(list=columns_empty_list)
    print()
    if unique_bool:
        for column in columns_non_empty_list:
            print('column:', column)
            print(df[column].unique())
            print()
    return df


def find_bool_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Create a list of boolean column names of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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
    columns_bool = list(df.select_dtypes(include=['bool', 'boolean']).columns)
    return columns_bool


def find_category_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Create list of category column names of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def find_datetime_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all datetime columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def find_float_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all float columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def find_int_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all integer columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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
    columns_int = list(df.select_dtypes(include=['int64', 'Int64']).columns)
    return columns_int


def find_int_float_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all integer and float columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def find_object_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all object columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def find_timedelta_columns(
    *,
    df: pd.DataFrame
) -> List[str]:
    """
    Find all timedelta columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

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


def number_empty_cells_in_columns(
    *,
    df: pd.DataFrame
) -> NoReturn:
    """
    Create and print a table of data type, empty-cell count, and empty-all
    percentage for non-empty columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Example
    -------
    >>> import datasense as ds
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    >>>     'X': [25.0, 24.0, 35.5, np.nan, 23.1],
    >>>     'Y': [27, 24, np.nan, 23, np.nan],
    >>>     'Z': ['a', 'b', np.nan, 'd', 'e']
    >>> })
    >>> empty_cells = ds.number_empty_cells_in_columns(df=df)
    >>> print(empty_cells)
    Information about non-empty columns
     Column   Data type   Empty cell count   Empty cell %   Unique
    -------- ----------- ------------------ -------------- --------
     X        float64                    1           20.0        4
     Y        float64                    2           40.0        3
     Z        object                     1           20.0        4
    """
    print('Information about non-empty columns')
    table = BeautifulTable(maxwidth=90)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    column_alignments = {
        'Column': BeautifulTable.ALIGN_LEFT,
        'Data type': BeautifulTable.ALIGN_LEFT,
        'Empty cell count': BeautifulTable.ALIGN_RIGHT,
        'Empty cell %': BeautifulTable.ALIGN_RIGHT,
        'Unique': BeautifulTable.ALIGN_RIGHT,
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
                 percent_nan,
                 df[column_name].nunique()]
            )
        except KeyError:
            print('Error on column:', column_name)
    print(table)
    print()


def process_columns(
    *,
    df: pd.DataFrame
) -> Tuple[
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
    Return a DataFrame without empty columns and ensure all column labels are
    strings.

    Create various counts of columns of a DataFrame.

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
        The input DataFrame.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.
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
    # ensure all column labels are strings
    df.columns = [str(column) for column in df.columns]
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


def process_rows(
    *,
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, int, int, int]:
    """
    Return a DataFrame without duplicate rows.

    Create various counts of rows of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.
    rows_in_count : int
        The count of rows of the input DataFrame.
    rows_out_count : int
        The count of rows of the output DataFrame.
    rows_empty_count : int
        The count of empty rows of the input DataFrame.

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
    *,
    df: Union[pd.DataFrame, pd.Series],
    file_name: Union[str, Path],
    index: bool = False,
    index_label: str = None,
    sheet_name: str = 'sheet_001',
) -> NoReturn:
    """
    Save a DataFrame or Series to a file.

    Parameters
    ----------
    df : Union[pd.DataFrame, pd.Series]
        The DataFrame or series to be saved to a file.
    file_name : Union[str, Path]
        The name of the file to be saved.
    index : bool = False
        If True, creates an index.
    index_label : str = None
        The index label.
    sheet_name : str = 'sheet_001'
        The name of the worksheet in the workbook.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.csv'
    >>> )

    Example 2
    ---------
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.csv',
    >>>     index=True
    >>> )

    Example 3
    ---------
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.xlsx'
    >>> )

    Example 4
    ---------
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.xlsx',
    >>>     index=True,
    >>>     sheet_name='sheet_one'
    >>> )

    Example 5
    ---------
    >>> from pathlib import Path
    >>> file_to_save = 'myfeatherfile.feather'
    >>> path = Path(file_to_save)
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name=path
    >>> )

    """
    if type(file_name).__name__ == 'str':
        file_name = Path(file_name)
    if file_name.suffix in ['.csv', '.CSV']:
        df.to_csv(
            path_or_buf=file_name,
            index=index,
            index_label=index_label
        )
    elif file_name.suffix in ['.ods', '.ODS']:
        excel_writer = pd.ExcelWriter(
            path=file_name,
            engine='odf',
        )
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            index=index,
            index_label=index_label
        )
        excel_writer.save()
    elif file_name.suffix in ['.xlsx', '.XLSX']:
        excel_writer = pd.ExcelWriter(file_name)
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            engine='openpyxl',
            index=index,
            index_label=index_label
        )
        excel_writer.save()
    # this works in Linux but not in Windows
    elif file_name.suffix in ['.xlsb', '.XLSB']:
        excel_writer = pd.ExcelWriter(file_name)
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            engine='pyxlsb',
            index=index,
            index_label=index_label
        )
        excel_writer.save()
    elif file_name.suffix in ['.feather']:
        df = ft.write_feather(
            df=df,
            dest=file_name
        )


def read_file(
    *,
    file_name: Union[str, Path],
    header: Union[int, List[int], None] = 0,
    skiprows: Union[List[int], None] = None,
    column_names_dict: Dict[str, str] = {},
    index_columns: List[str] = [],
    usecols: Union[List[str], None] = None,
    dtype: Union[dict, None] = None,
    converters: Union[dict, None] = None,
    parse_dates: List[str] = False,
    date_parser: Union[Callable, None] = None,
    datetime_format: Union[str, None] = None,
    time_delta_columns: List[str] = [],
    category_columns: List[str] = [],
    integer_columns: List[str] = [],
    float_columns: List[str] = [],
    boolean_columns: List[str] = [],
    object_columns: List[str] = [],
    sort_columns: List[str] = [],
    sort_columns_bool: List[bool] = [],
    sheet_name: str = False,
    nrows: Union[int, None] = None
) -> pd.DataFrame:
    """
    Create a DataFrame from an external file.

    Parameters
    ----------
    file_name : Union[str, Path]
        The name of the file to read.
    header : Union[int, List[int], None] = 0
        The row to use for the column labels. Use None if there is no header.
    skiprows : Union[List[int], None] = None
        The specific row indices to skip.
    column_names_dict : Dict[str, str] = {}
        The new column names to replace the old column names.
    index_columns : List[str] = []
        The columns to use for the DataFrame index.
    usecols : Union[List[str], None] = None
        The columns to read.
    dtype : Union[dict, None] = None
        A dictionary of column names and dtypes.
        NOTE: Nullable Boolean data type is experimental and does not work;
        use .astype() on df after created.
    converters : Union[dict, None] = None
        Dictionary of functions for converting values in certain columns.
    parse_dates : List[str] = False
        The columns to use to parse date and time.
    date_parser : Union[Callable, None] = None
        The function to use for parsing date and time, when pandas needs
        extra help.
    datetime_format : Union[str, None] = None
        The str to use for formatting date and time.
    time_delta_columns : List[str] = []
        The columns to change to dtype timedelta.
    category_columns : List[str] = []
        The columns to change to dtype category.
    integer_columns : List[str] = []
        The columns to change to dtype integer.
    float_columns : List[str] = []
        The columns to change to dtype float.
    boolean_columns : List[str] = []
        The columns to change to dtype boolean.
    object_columns : List[str] = []
        The columns to change to dtype object.
    sort_columns : List[str] = []
        The columns on which to sort the DataFrame.
    sort_columns_bool : List[bool] = []
        The booleans for sort_columns.
    sheet_name : str = False
        The name of the worksheet in the workbook.
    nrows : Union[int, None] = None
        The number of rows to read.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame created from the external file.

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

    Example 1
    ---------
    Read a csv file. There is no guarantee the column dtypes will be correct.
    Only [a, i, s, x, z] have the correct dtypes.
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

    Example 2
    ---------
    Read a csv file. Ensure the dtypes of datetime columns.
    >>> parse_dates = ['t', 'u']
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     parse_dates=parse_dates
    >>> )
    >>> print(df.dtypes)
    a           float64
    b              bool
    c            object
    d            object
    i           float64
    r             int64
    s            object
    t    datetime64[ns]
    u    datetime64[ns]
    x           float64
    y             int64
    z           float64
    dtype: object

    Example 3
    ---------
    Read a csv file. Ensure the dtypes of columns; not timedelta, datetime.
    >>> convert_dict = {
    >>>     'a': 'float64',
    >>>     'b': 'boolean',
    >>>     'c': 'category',
    >>>     'i': 'float64',
    >>>     'r': 'str',
    >>>     's': 'str',
    >>>     'x': 'float64',
    >>>     'y': 'Int64',
    >>>     'z': 'float64'
    >>> }
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     dtype=convert_dict
    >>> )
    >>> print(df.dtypes)
    a     float64
    b     boolean
    c    category
    d      object
    i     float64
    r      object
    s      object
    t      object
    u      object
    x     float64
    y       Int64
    z     float64
    dtype: object

    Example 4
    ---------
    Read a csv file. Ensure the dtypes of columns. Rename the columns.
    Set index with another column. Convert float column to integer.
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
    >>> sort_columns = ['I', 'A']
    >>> sort_columns_bool = [True, False]
    >>> df = ds.read_file(
    >>>     file_name='myfile.csv',
    >>>     column_names_dict=column_names_dict,
    >>>     index_columns=index_columns,
    >>>     parse_dates=parse_dates,
    >>>     date_parser=date_parser(),
    >>>     time_delta_columns=time_delta_columns,
    >>>     category_columns=category_columns,
    >>>     integer_columns=integer_columns
    >>>     float_columns=float_columns,
    >>>     boolean_columns=boolean_columns,
    >>>     object_columns=object_columns,
    >>>     sort_columns=sort_columns,
    >>>     sort_columns_bool=sort_columns_bool
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

    Example 5
    ---------
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

    Example 6
    ---------
    Read an xlsx file.
    >>> file_name = 'myfile.xlsx'
    >>> sheet_name = 'raw_data'
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     sheet_name=sheet_name
    >>> )
    >>> ds.dataframe_info(
    >>>     df=df,
    >>>     file_in=file_name
    >>> )

    Example 7
    ---------
    Read an xlsb file.
    >>> file_name = 'myfile.xlsb'
    >>> sheet_name = 'raw_data'
    >>> df = ds.read_file(
    >>>     file_name=file_name,
    >>>     sheet_name=sheet_name
    >>> )
    >>> ds.dataframe_info(
    >>>     df=df,
    >>>     file_in=file_name
    >>> )

    Example 8
    ---------
    Read a feather file.
    >>> from pathlib import Path
    >>> file_to_read = 'myfeatherfile.feather'
    >>> path = Path(file_to_read)
    >>> df = ds.read_file(file_name=path)

    Example 9
    ---------
    Read a feather file with columns list.
    >>> from pathlib import Path
    >>> file_to_read = 'myfeatherfile.feather'
    >>> usecols = ['col1', 'col2']
    >>> path = Path(file_to_read)
    >>> df = ds.read_file(
    >>>     file_name=path,
    >>>     usecols=usecols
    >>> )
    """
    if type(file_name).__name__ == 'str':
        file_name = Path(file_name)
    if file_name.suffix in ['.csv', '.CSV']:
        df = pd.read_csv(
            file_name,
            skiprows=skiprows,
            usecols=usecols,
            dtype=dtype,
            converters=converters,
            parse_dates=parse_dates,
            date_parser=date_parser,
            nrows=nrows
        )
    elif file_name.suffix in ['.ods', '.ODS']:
        df = pd.read_excel(
            io=file_name,
            skiprows=skiprows,
            usecols=usecols,
            dtype=dtype,
            engine='odf',
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            date_parser=date_parser
        )
    elif file_name.suffix in ['.xlsx', '.XLSX', '.xlsm', '.XLSM']:
        df = pd.read_excel(
            io=file_name,
            sheet_name=sheet_name,
            header=header,
            usecols=usecols,
            dtype=dtype,
            engine='openpyxl',
            skiprows=skiprows,
            nrows=nrows,
            parse_dates=parse_dates,
            date_parser=date_parser,
        )
    elif file_name.suffix in ['.xlsb', '.XLSB']:
        df = pd.read_excel(
            io=file_name,
            sheet_name=sheet_name,
            header=header,
            usecols=usecols,
            dtype=dtype,
            engine='pyxlsb',
            skiprows=skiprows,
            nrows=nrows,
            parse_dates=parse_dates,
            date_parser=date_parser,
        )
    elif file_name.suffix in ['.feather']:
        df = ft.read_feather(
            source=file_name,
            columns=usecols
        )
    if column_names_dict:
        df = rename_some_columns(
            df=df,
            column_names_dict=column_names_dict
        )
    if index_columns:
        df = df.set_index(index_columns)
    for column in category_columns:
        df[column] = df[column].astype(dtype=CategoricalDtype())
    for column in time_delta_columns:
        df[column] = pd.to_timedelta(df[column])
    for column in integer_columns:
        df[column] = df[column].astype(dtype='int64')
    for column in float_columns:
        df[column] = df[column].astype(dtype='float64')
    for column in boolean_columns:
        df[column] = df[column].astype(dtype='bool')
    for column in object_columns:
        df[column] = df[column].astype(dtype='object')
    if sort_columns and sort_columns_bool:
        df = sort_rows(
            df=df,
            sort_columns=sort_columns,
            sort_columns_bool=sort_columns_bool,
            kind='mergesort'
        )
    return df


def byte_size(
    *,
    num: np.int64,
    suffix: str = 'B'
) -> str:
    """
    Convert bytes to requested units.

    Parameters
    ----------
    num : np.int64
        The input value.
    suffix : str = 'B'
        The units.

    Returns
    -------
    memory_usage : str
        The output value.

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
    *,
    df: pd.DataFrame,
    columns: List[str],
    threshold: float
) -> List[str]:
    """
    Remove features that have NaN > threshold.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
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


def create_directory(
    *,
    directories: List[str],
    ignore_errors: bool = True
) -> NoReturn:
    """
    Create empty directories for a path.
    - Deletes existing directories, whether empty or non-empty.
    - Ignores errors such as no existing directories.

    Parameters
    ----------
    directories : List[str]
        The list of directories.
    ignore_errors : bool = True
        Boolean to deal with errors.

    Example
    -------
    >>> import datasense as ds
    >>> directory_list = ['directory_one', 'directory_two']
    >>> ds.create_directory(directories=directory_list)
    """
    for directory in directories:
        rmtree(path=directory, ignore_errors=ignore_errors)
        Path(directory).mkdir(parents=True, exist_ok=True)


def delete_directory(
    *,
    directories: List[str],
    ignore_errors: bool = True
) -> NoReturn:
    """
    Delete a list of directories.
    - Deletes existing directories, whether empty or non-empty.

    Parameters
    ----------
    directories : List[str]
        The list of directories.
    ignore_errors : bool = True
        Boolean to deal with errors.

    Example
    -------
    >>> import datasense as ds
    >>> directory_list = ['directory_one', 'directory_two']
    >>> ds.delete_directory(directories=directory_list)
    """
    for directory in directories:
        rmtree(path=directory, ignore_errors=ignore_errors)


def rename_directory(
    *,
    sources: List[str],
    destinations: List[str],
    ignore_errors: bool = True
) -> NoReturn:
    """
    Delete destination directories (if present) and rename source directories
    to the destination directories.

    Parameters
    ----------
    sources : List[str]
        The old directories.
    destinations : List[str]
        The new directories.
    ignore_errors : bool = True
        Boolean to deal with errors.

    Example
    -------
    >>> import datasense as ds
    >>> sources = ['old_directory']
    >>> destinations = ['new_directory']
    >>> ds.rename_directory(sources=sources, destinations=destinations)
    """
    for source, destination in zip(sources, destinations):
        rmtree(path=destination, ignore_errors=ignore_errors)
        move(src=source, dst=destination)


def copy_directory(
    *,
    sources: Union[Path, str],
    destinations: Union[Path, str],
    ignore_errors: bool = True
) -> NoReturn:
    """
    Delete destination directories (if present) and copy source directories
    to destination directories.

    Parameters
    ----------
    sources : Union[Path, str]
        The source directory name.
    destinations : Union[Path, str]
        The destination directory name.

    Example
    -------
    >>> import datasense as ds
    >>> sources = ['source_directory']
    >>> destinations = ['destination_directory']
    >>> ds.rename_directory(
    >>>     sources=sources,
    >>>     destinations=destinations
    >>> )
    """
    for source, destination in zip(sources, destinations):
        rmtree(path=destination, ignore_errors=ignore_errors)
        copytree(
            src=source,
            dst=destination
        )


def replace_text_numbers(
    *,
    df: pd.DataFrame,
    columns: Union[List[str], List[int], List[float], List[Pattern[str]]],
    old: Union[List[str], List[int], List[float], List[Pattern[str]]],
    new: List[int],
    regex: bool = True
) -> pd.DataFrame:
    """
    Replace text or numbers with text or numbers.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    columns: Union[List[str], List[int], List[float], List[Pattern[str]]]
        The list of columns for replacement.
    old: Union[List[str], List[int], List[float], List[Pattern[str]]]
        The list of item to replace.
    new : List[int]
        The list of replacement items.
    regex : bool = True
        Determines if the passed-in pattern is a regular expression.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    -------
    Example 1
    ---------
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
    ---------
    >>> data = ds.replace_text_numbers(
    >>>     df=data,
    >>>     columns=['Q23'],
    >>>     old=[r'\xa0'],
    >>>     new=[r' '],
    >>>     regex=True
    >>> )

    Example 3
    ---------
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


def create_dataframe(
    *,
    size: int = 42,
    fraction_nan: float = 0.13
) -> pd.DataFrame:
    # TODO: why did I create distribution "u"?
    """
    Create a Pandas DataFrame.

    Parameters
    ----------
    size : int = 42
        The number of rows to create.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Notes
    -----
    a  : float64
    b  : bool
    bn : boolean (nullable)
    c  : category
    cs : CategoricalDtype category
    d  : timedelta64[ns]
    r  : object
    s  : object
    t  : datetime64[ns]
    u  : datetime64[ns]
    x  : float64
    y  : int64
    yn : Int64
    z  : float64

    Example
    -------
    >>> df = create_dataframe()
    """
    df = pd.DataFrame(
        {
            'a': random_data(
                distribution='uniform',
                size=size,
                loc=13,
                scale=70
            ),
            'b': random_data(
                distribution='bool',
                size=size
            ),
            'bn': random_data(
                distribution='boolean',
                size=size
            ),
            'c': random_data(
                distribution='category',
                size=size,
                categories=['blue', 'white', 'red']
            ),
            'cs': random_data(
                distribution='categories',
                size=size,
                categories=['small', 'medium', 'large']
            ),
            'd': timedelta_data(time_delta_days=size-1),
            'i': random_data(
                distribution='randint',
                size=size
            ),
            'r': random_data(
                distribution='strings',
                strings=['0', '1'],
                size=size
            ),
            's': random_data(
                distribution='strings',
                size=size
                ),
            't': datetime_data(time_delta_days=size-1),
            'u': datetime_data(time_delta_days=size-1),
            'x': random_data(
                distribution='norm',
                size=size
            ),
            'y': random_data(
                distribution='randint',
                size=size
            ),
            'yn': random_data(
                distribution='randInt',
                size=size,
                fraction_nan=fraction_nan
            ),
            'z': random_data(
                distribution='uniform',
                size=size
            )
        }
    )
    return df


def create_dataframe_norm(
    *,
    row_count: int = 42,
    column_count: int = 13,
    loc: float = 69,
    scale: float = 13,
    random_state: int = None,
    column_names: List[str] = None
) -> pd.DataFrame:
    """
    Create DataFrame of random normal data.

    Parameters
    ----------
    row_count : int = 42,
        The number of rows to create.
    column_count : int = 13,
        The number of columns to create.
    loc : float = 69,
        The mean of the data.
    scale : float = 13
        The standard deviation of the data.
    random_state: int = None
        The random number seed.
    column_names: List[str]
        The column names.

    Examples
    --------
    Example 1
    ---------
    >>> df = ds.create_dataframe_norm()

    Example 2
    ---------
    >>> column_names = [f'col{item}' for item in range(column_count)]
    >>> row_count = 1000
    >>> column_count = 100
    >>> df = ds.create_dataframe_norm(
    >>>     row_count=row_count,
    >>>     column_count=column_count,
    >>>     loc=69,
    >>>     scale=13,
    >>>     random_state=42,
    >>>     column_names=column_names
    >>> )
    """
    if not column_names:
        column_names = [f'col{item}' for item in range(column_count)]
    df = pd.DataFrame(
        norm.rvs(
            size=(row_count, column_count),
            loc=loc,
            scale=scale,
            random_state=random_state
        ),
        columns=column_names
    )
    return df


def delete_rows(
    *,
    df: pd.DataFrame,
    delete_row_criteria:
        Union[Tuple[str, int], Tuple[str, float], Tuple[str, str]]
) -> pd.DataFrame:
    """
    Delete rows of a DataFrame based on a value in one column.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    delete_row_criteria : Tuple[str, int]
        A tuple of column name and criteria for the entire cell.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

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
    *,
    df: pd.DataFrame,
    columns: List[str]
) -> pd.DataFrame:
    """
    Delete columns of a DataFrame using a list.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    columns : List[str]
        A list of column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

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
    *,
    df: pd.DataFrame,
    sort_columns: List[str],
    sort_columns_bool: List[bool],
    kind: str = 'mergesort'
) -> pd.DataFrame:
    """
    Sort a DataFrame for one or more columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    sort_columns : List[str]
        The sort columns.
    sort_columns_bool : List[bool]
        The booleans for sort_columns: True = ascending, False = descending.
    kind: str = 'mergesort'
        The sort algorithm.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

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
    *,
    df: pd.DataFrame,
    labels: List[str]
) -> pd.DataFrame:
    """
    Rename all DataFrame columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    labels : List[str]
        The list of all column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

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
    *,
    df: pd.DataFrame,
    column_names_dict: Dict[str, str]
) -> pd.DataFrame:
    """
    Rename some columns with a dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    column_names_dict : Dict[str, str]
        The dictionary of old:new column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

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
    *,
    s: pd.Series,
    replace_dict: Dict[str, str],
    regex: bool = False
) -> pd.Series:
    """
    Replace values in a series using a dictionary.

    Parameters
    ----------
    s : pd.Series
        The input series.
    replace_dict : Union[Dict[str, str], Dict[int, int], Dict[float, float]]
        The dictionary of values to replace.
    regex : bool = True
        Determines if the passed-in pattern is a regular expression.

    Returns:
    s : pd.Series
        The output series.

    Examples
    --------
    >>> import datasense as ds
    >>> s = ds.replace_column_values(
    >>>     s=s
    >>>     replace_dict=replace_dict
    >>> )
    """
    # s = s.replace(
    #     to_replace=replace_dict,
    #     value=None,
    #     regex=regex
    # )
    list_from_series = s.to_list()
    list_transformed = [replace_dict.get(x, x) for x in list_from_series]
    s = pd.Series(data=list_transformed).astype(dtype='str')
    return s


def directory_file_list(
    *,
    directory: Union[str, Path],
    patterns: List[str] = None
) -> List[Path]:
    """
    Return a list of files within a directory.

    Parameters
    ----------
    path : Union[str, Path]
        The path of the directory.
    extension : List[str]
        The file extensions to use for finding files in the path.

    Returns
    -------
    files : List[Path]
        A list of paths.

    Examples
    --------
    Example 1
    ---------
    >>> patterns = ['.pdf']
    >>> import datasense as ds
    >>> files = ds.directory_file_list(
    >>>     directory=path,
    >>>     patterns=patterns
    >>> )

    Example 2
    ---------
    >>> patterns = ['.PDF']
    >>> import datasense as ds
    >>> files = ds.directory_file_list(
    >>>     directory=path,
    >>>     patterns=patterns
    >>> )

    Example 3
    ---------
    >>> patterns = ['.pdf', '.PDF']
    >>> import datasense as ds
    >>> files = ds.directory_file_list(
    >>>     directory=path,
    >>>     patterns=patterns
    >>> )

    Example 4
    ---------
    >>> # Return all files within a directory
    >>> import datasense as ds
    >>> files = ds.directory_file_list(
    >>>     directory=path
    >>> )
    """
    directory = Path(directory)
    if not patterns:
        files = [
            x for x in directory.iterdir()
        ]
    else:
        files = [
            x for x in directory.iterdir() if x.suffix in patterns
        ]
    return files


def directory_file_print(
    *,
    directory: Union[str, Path],
    text: str = 'Files in directory'
) -> NoReturn:
    """
    Print the files in a path.

    Parameters
    ----------
    path : Path
        The path of the files to print.
    text : str
        The text to print.

    Example
    -------
    >>> import datasense as ds
    >>> path = <path to a directory>
    >>> text = 'your text'
    >>> ds.directory_file_print(
    >>>     path=path,
    >>>     text=text
    >>> )
    """
    directory = Path(directory)
    if text:
        print(f'{text}', directory)
    for x in directory.iterdir():
        print(x.name)
    print()


def directory_remove_file(
    *,
    path: Path,
    file_names: List[str]
) -> List[str]:
    """
    Parameters
    ----------
    path : Path
        The path of the file to remove.
    file_names : List[str]
        The list of files from which to remove the path.

    Returns
    -------
    file_names : {list[str]
        The list of files without the removed path.

    Example
    -------
    >>> import datasense as ds
    >>> file_names = ds.directory_remove_file(
    >>>     path=path,
    >>>     file_names=file_names
    >>> )
    """
    for file in file_names:
        if path.name in file:
            os.remove(file)
            file_names.remove(file)
    return file_names


def print_list_by_item(
    *,
    list: List[str],
    title: str = None,
    width: int = 80
) -> NoReturn:
    '''
    Print each item of a list.

    Parameters
    ----------
    list : str
        The list of strings to print.
    title : str = None
        The title to print.
    width : int = 80
        The width of the output in characters.

    Example
    -------
    >>> import datasense as ds
    >>> ds.print_list_by_item(list=my_list_to_print)
    '''
    wrapper = textwrap.TextWrapper(width=width)
    string_not_list = ", ".join(list)
    new_list = wrapper.wrap(string_not_list)
    if title:
        print(title)
    for element in new_list:
        print(element)


def ask_directory_path(
    *,
    title: str = 'Select directory',
    initialdir: Path = None,
    print_bool: bool = False
) -> Path:
    """
    Ask user for directory.

    Parameters
    ----------
    title : str = 'Select directory'
        The title of the dialog window.
    initialdir : Path
        The directory in which the dialogue starts.
    print_bool : bool = True
        A boolean. Print message if True.

    Returns
    -------
    path: Path
        The path of the directory.

    Example
    -------
    >>> from tkinter import filedialog
    >>> from pathlib import Path
    >>> from tkinter import Tk
    >>> import datasense as ds
    >>> path = ds.ask_directory_path(title='your message')
    """
    rootwindow = Tk()
    path = filedialog.askdirectory(
        parent=rootwindow,
        initialdir=initialdir,
        title=title
    )
    path = Path(path)
    rootwindow.destroy()
    if print_bool:
        print(title)
        print(path)
        print()
    return path


def ask_open_file_name_path(
    *,
    title: str,
    initialdir: Union[Path, None] = None,
    filetypes: Union[List[Tuple[str]]] = [('xlsx files', '.xlsx .XLSX')]
) -> Path:
    """
    Ask user for the path of the file to open.

    Parameters
    ----------
    title : str
        The title of the dialog window.
    initialdir : Union[Path, None] = None
        The directory in which the dialogue starts.
    filetypes : List[Tuple[str]] = [('xlsx files', '.xlsx .XLSX')]
        The file types to make visible.

    Returns
    -------
    path: Path
        The path of the file to open.

    Examples
    --------
    Example 1
    ---------
    >>> from tkinter import filedialog
    >>> from pathlib import Path
    >>> from tkinter import Tk
    >>> import datasense as ds
    >>> path = ds.ask_open_file_name_path(title='your message')

    Example 2
    ---------
    >>> path = ds.ask_open_file_name_path(
    >>>     title='your message',
    >>>     filetypes=[('csv files', '.csv .CSV')]
    >>> )
    """
    rootwindow = Tk()
    path = filedialog.askopenfilename(
        parent=rootwindow,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )
    path = Path(path)
    rootwindow.destroy()
    return path


def ask_save_as_file_name_path(
    *,
    title: str,
    initialdir: Union[Path, None] = None,
    filetypes: Union[List[Tuple[str]]] = [('xlsx files', '.xlsx .XLSX')],
    print_bool: bool = True
) -> Path:
    """
    Ask user for the path of the file to save as.

    Parameters
    ----------
    title : str = 'Select file'
        The title of the dialog window.
    initialdir : Union[Path, None] = None
        The directory in which the dialogue starts.
    filetypes : List[Tuple[str]] = [('xlsx files', '.xlsx .XLSX')]
        The list of file types to show in the dialog.
    print_bool : bool = True
        A boolean. Print message if True.

    Returns
    -------
    path: Path
        The path of the file to save as.

    Example2
    --------
    Example 1
    ---------
    >>> from tkinter import filedialog
    >>> from pathlib import Path
    >>> from tkinter import Tk
    >>> import datasense as ds
    >>> path = ds.ask_save_as_file_name_path(title='your message')

    Example 2
    ---------
    >>> path = ds.ask_save_as_file_name_path(
    >>>     title='your message',
    >>>     filetypes=[('csv files', '.csv .CSV')]
    >>> )
    """
    rootwindow = Tk()
    path = filedialog.asksaveasfilename(
        parent=rootwindow,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )
    path = Path(path)
    rootwindow.destroy()
    if print_bool:
        print(title)
        print(path)
        print()
    return path


def series_replace_string(
    *,
    series: pd.Series,
    find: str,
    replace: str,
    regex: bool = True
) -> pd.Series:
    """
    Find and replace a string in a series.

    Parameters
    ----------
    series : pd.Series
        The input series of data.
    find : str
        The string to find.
    replace : str
        The replacement string.
    regex : bool = True
        Determines if the passed-in pattern is a regular expression.

    Returns
    -------
    series : pd.Series
        The output series of data.

    Example
    -------
    >>> import datasense as ds
    >>> df[column] = series_replace_string(
    >>>     series=df[column],
    >>>     find='find this text',
    >>>     replace='replace with this text'
    >>> )
    """
    series = series.str.replace(
        pat=find,
        repl=replace,
        regex=regex
    )
    return series


def list_directories_within_directory(
    *,
    path: Union[str, Path]
) -> List[str]:
    '''
    Return a list of directories found within a path.

    Parameters
    ----------
    path : Union[str, Path]
        The path of the enclosing directory.

    Returns
    -------
    directory_list : List[str]
        A list of directories.

    Example
    -------
    >>> import datasense as ds
    >>> directory_list = ds.list_directories_within_directory(
    >>>     path='directory_companies'
    >>> )
    '''
    path = Path(path)
    directory_list = [item.name for item in path.iterdir() if item.is_dir()]
    return directory_list


def remove_punctuation(
    *,
    list_dirty: List[str]
) -> List[str]:
    '''
    Remove punctuation from list items.

    Parameters
    ----------
    list_dirty : List[str]
        The list of items containing punctuation.

    Returns
    -------
    list_clean : List[str]
        The list of items without punctuation.

    Example
    -------
    >>> import datasense as ds
    >>> list_clean = ds.remove_punctuation(list_dirty=list_dirty)
    '''
    list_clean = [
        ''.join(
            character for character in item
            if character not in string.punctuation
        )
        for item in list_dirty
    ]
    return list_clean


def list_change_case(
    *,
    list_dirty: List[str],
    case: str
) -> List[str]:
    '''
    Change the case of items in a list.

    Parameters
    ----------
    list_dirty : List[str]
        The list of strings.
    case : str
        The type of case to apply.

    Returns
    -------
    list_clean : List[str]
        The list of strings with case applied.

    Example
    -------
    >>> import datasense as ds
    >>> list_clean = ds.list_change_case(
    >>>     list_dirty=list_dirty,
    >>>     case='upper'
    >>> )
    '''
    if case == 'upper':
        list_clean = [x.upper() for x in list_dirty]
    elif case == 'lower':
        list_clean = [x.lower() for x in list_dirty]
    elif case == 'title':
        list_clean = [x.title() for x in list_dirty]
    elif case == 'capitalize':
        list_clean = [x.capitalize() for x in list_dirty]
    return list_clean


def listone_contains_all_listtwo_substrings(
    *,
    listone: List[str],
    listtwo: List[str]
) -> List[str]:
    '''
    Return a list of items from one list that contain substrings of items
    from another list.

    Parameters
    ----------
    listone : List[str]
        The list of items in which there are substrings to match from listtwo.
    listwo : List[str]
        The list of items that are substrings of the items in listone.

    Returns
    -------
    matches : List[str]
        The list of items from listone that contain substrings of the items
        from listtwo.

    Example
    -------
    >>> listone = ['prefix-2020-21-CMJG-suffix', 'bobs your uncle']
    >>> listwo = [ 'CMJG', '2020-21']
    >>> matches = ds.listone_contains_all_listwo_substrings(
    >>>     listone=listone,
    >>>     listtwo=listtow
    >>> )
    >>> ['prefix-2020-21-CMJG-suffix']
    '''
    matches = [x for x in listone if all(y in x for y in listtwo)]
    return matches


def list_one_list_two_ops(
    *,
    list_one: Union[List[str], List[int], List[float]],
    list_two: Union[List[str], List[int], List[float]],
    action: str
) -> Union[List[str], List[int], List[float]]:
    '''
    Create a list of items comparing two lists:
    - Items unique to list_one
    - Items unique to list_two
    - Items common to both lists (intersection)

    Parameters
    ----------
    list_one : Union[List[str], List[int], List[float]]
        A list of items.
    list_two : Union[List[str], List[int], List[float]]
        A list of items.
    action : str
        A string of either "list_one", "list_two", or "intersection"

    Returns
    -------
    list_result : Union[List[str], List[int], List[float]]
        The list of unique items.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    >>>     list_one=list_one,
    >>>     list_two=list_two,
    >>>     action='list_one'
    >>> )
    >>> [1, 2, 3]

    Example 2
    ---------
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    >>>     list_one=list_one,
    >>>     list_two=list_two,
    >>>     action='list_two'
    >>> )
    >>> [7, 8, 9]

    Example 3
    ---------
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    >>>     list_one=list_one,
    >>>     list_two=list_two,
    >>>     action='intersection'
    >>> )
    >>> [4, 5, 6]
    '''
    if action == 'list_one':
        list_result = list(set(list_one).difference(list_two))
    elif action == 'list_two':
        list_result = list(set(list_two).difference(list_one))
    elif action == 'intersection':
        list_result = list(set(list_one).intersection(list_two))
    else:
        print('Error. Enter "list_one" or "list_two" for parameter "unique"')
    return list_result


def parameters_text_replacement(
    *,
    file_name: Path,
    sheet_name: str,
    usecols: List[str],
    case: 'str' = None
) -> Tuple[Tuple[str, str]]:
    '''
    Read Excel worksheet.
    Create tuple of text replacement tuples.

    Parameters
    ----------
    file_name : Path
        The path of the Excel file.
    sheet_name : str
        The Excel worksheet.
    usecols : List[str]
        The column names to read.
    case : 'str' = None
        Change the case of all items: None, lower, upper.

    Returns
    -------
    text_replacement : Tuple[Tuple[str, str]]

    Examples
    --------
    Example 1
    ---------
    >>> path_parameters = Path('bcp_parameters.xlsx')
    >>> usecols = ['old_text', 'new_text']
    >>> sheet_name = 'text_replacement'
    >>> text_replacement = parameters(
    >>>     file_name=path_parameters,
    >>>     sheet_name=sheet_name,
    >>>     usecols=usecols
    >>> )

    Example 2
    ---------
    >>> path_parameters = Path('bcp_parameters.xlsx')
    >>> usecols = ['old_text', 'new_text']
    >>> sheet_name = 'text_replacement'
    >>> text_replacement = parameters(
    >>>     file_name=path_parameters,
    >>>     sheet_name=sheet_name,
    >>>     usecols=usecols,
    >>>     case='upper'
    >>> )

    Example 3
    ---------
    >>> path_parameters = Path('bcp_parameters.xlsx')
    >>> usecols = ['old_text', 'new_text']
    >>> sheet_name = 'text_replacement'
    >>> text_replacement = parameters(
    >>>     file_name=path_parameters,
    >>>     sheet_name=sheet_name,
    >>>     usecols=usecols,
    >>>     case='lower'
    >>> )
    '''
    df = read_file(
        file_name=file_name,
        sheet_name=sheet_name,
        usecols=usecols
    )
    if case == 'upper':
        tuples = tuple(
            zip(df[usecols[0]].str.upper(), df[usecols[1]].str.upper())
        )
    elif case == 'lower':
        tuples = tuple(
            zip(df[usecols[0]].str.lower(), df[usecols[1]].str.lower())
        )
    else:
        tuples = tuple(
            zip(
                df[usecols[0]].astype(dtype='str'),
                df[usecols[1]].astype(dtype='str')
            )
        )
    return tuples


def parameters_dict_replacement(
    *,
    file_name: Path,
    sheet_name: str,
    usecols: List[str]
) -> Dict[str, str]:
    '''
    Read Excel worksheet.
    Create dictionary of text replacement key, value pairs.

    Parameters
    ----------
    file_name : Path
        The path of the Excel file.
    sheet_name : str
        The Excel worksheet.
    usecols : List[str]
        The column names to read.

    Returns
    -------
    text_replacement : Dict[str, str]

    Example
    -------
    >>> path_parameters = Path('parameters.xlsx')
    >>> usecols = ['old_text', 'new_text']
    >>> sheet_name = 'text_replacement'
    >>> replacement_dict = ds.parameters_dict_replacement(
    >>>     file_name=path_parameters,
    >>>     sheet_name=sheet_name,
    >>>     usecols=usecols
    >>> )
    '''
    df = read_file(
        file_name=file_name,
        sheet_name=sheet_name,
        usecols=usecols
    )
    dictionary = dict(zip(df[usecols[0]], df[usecols[1]]))
    return dictionary


def quit_sap_excel() -> NoReturn:
    '''
    Several applications, Excel in particular, need to be closed otherwise
    they may cause a function to crash.
    '''
    for proc in psutil.process_iter():
        if proc.name().lower() == "excel.exe":
            proc.kill()
        if proc.name().lower() == "saplogon.exe":
            proc.kill()


def get_mtime(path: Path) -> float:
    '''
    Get the time of last modification of a Path object.
    '''
    return path.stat().st_mtime


def file_size(path: Union[Path, str]) -> int:
    """
    Determine the file size in bytes.

    Parameters
    ----------
    path : Path
        The path of the file.

    Returns
    -------
    size : int
        The file size in bytes

    Example
    -------
    >>> path = 'myfile.feather'
    >>> size = ds.file_size(path=path)
    """
    size = Path(path).stat().st_size
    return size


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
    'byte_size',
    'feature_percent_empty',
    'create_directory',
    'delete_directory',
    'rename_directory',
    'copy_directory',
    'replace_text_numbers',
    'create_dataframe',
    'create_dataframe_norm',
    'delete_rows',
    'delete_columns',
    'sort_rows',
    'rename_all_columns',
    'rename_some_columns',
    'replace_column_values',
    'directory_file_list',
    'directory_file_print',
    'directory_remove_file',
    'print_list_by_item',
    'ask_directory_path',
    'ask_open_file_name_path',
    'ask_save_as_file_name_path',
    'series_replace_string',
    'list_directories_within_directory',
    'remove_punctuation',
    'list_change_case',
    'listone_contains_all_listtwo_substrings',
    'list_one_list_two_ops',
    'parameters_text_replacement',
    'parameters_dict_replacement',
    'quit_sap_excel',
    'get_mtime',
    'file_size',
)
