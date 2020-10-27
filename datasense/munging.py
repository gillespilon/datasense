"""
Data munging
"""

from typing import Callable, Dict, IO, List, Optional, Tuple, Union
from shutil import rmtree
from pathlib import Path
import webbrowser
import textwrap
import sys

from pandas.api.types import CategoricalDtype
from beautifultable import BeautifulTable
import pandas as pd
import numpy as np


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
        columns_empty_list, columns_non_empty_list, columns_bool_list,\
        columns_bool_count,\
        columns_float_list, columns_float_count,\
        columns_integer_list, columns_integer_count, columns_datetime_list,\
        columns_datetime_count, columns_object_list, columns_object_count,\
        columns_category_list, columns_category_count,\
        columns_timedelta_list, columns_timedelta_count\
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
    Find all boolean columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_bool = ds.find_bool_columns(df=df)
    >>> print(columns_bool)
    ['b']
    """
    columns_bool = list(df.select_dtypes(include=['bool']).columns)
    return columns_bool


def find_category_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all category columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_category = ds.find_category_columns(df=df)
    >>> print(columns_category)
    ['c']
    """
    columns_category = list(df.select_dtypes(include=['category']).columns)
    return columns_category


def find_datetime_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all datetime columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_datetime = ds.find_datetime_columns(df=df)
    >>> print(columns_datetime)
    ['t']
    """
    columns_datetime = list(df.select_dtypes(include=['datetime64']).columns)
    return columns_datetime


def find_float_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all float columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_float = ds.find_float_columns(df=df)
    >>> print(columns_float)
    ['x', 'z']
    """
    columns_float = list(df.select_dtypes(include=['float64']).columns)
    return columns_float


def find_int_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all integer columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_int = ds.find_int_columns(df=df)
    >>> print(columns_int)
    ['y']
    """
    columns_int = list(df.select_dtypes(include=['int64']).columns)
    return columns_int


def find_int_float_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all integer and float columns in a dataframe.

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
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_int_float = ds.find_int_float_columns(df=df)
    >>> print(columns_int_float)
    ['x', 'y', 'z']
    """
    columns_int_float = list(
        df.select_dtypes(include=['int64', 'float64']).columns
    )
    return columns_int_float


def find_object_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all object columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_object = ds.find_object_columns(df=df)
    >>> print(columns_object)
    ['s']
    """
    columns_object = list(df.select_dtypes(include=['object']).columns)
    return columns_object


def find_timedelta_columns(df: pd.DataFrame) -> List[str]:
    """
    Find all timedelta columns in a dataframe.

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
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> columns_timedelta = ds.find_timedelta_columns(df=df)
    >>> print(columns_timedelta)
    ['d']
    """
    columns_timedelta = list(df.select_dtypes(include=['timedelta']).columns)
    return columns_timedelta


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
    int,
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
    df: Union[pd.DataFrame, pd.Series],
    file_name: str,
    *,
    index: Optional[bool] = False
) -> None:
    """
    Save a DataFrame or Series to a file.

    Parameters
    ---------
    df : pd.DataFrame
        The dataframe to be saved to a file.
    file_name : str
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
    >>>     file_name='x_y.csv'
    >>> )

    Example 2
    ---------
    >>> ds.save_file(
    >>>     df=df,
    >>>     file_name='x_y.csv',
    >>>     index=True
    >>> )
    """
    if '.csv' in file_name:
        df.to_csv(
            path_or_buf=file_name,
            index=index
        )


def read_file(
    file_name: str,
    *,
    column_names_dict: Optional[Dict[str, str]] = {},
    index_columns: Optional[List[str]] = [],
    converters: Optional[dict] = None,
    parse_dates: Optional[List[str]] = False,
    date_parser: Optional[Callable] = None,
    format: Optional[str] = None,
    # date_time_columns: Optional[List[str]] = [],
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
    Create a DataFrame from an external file.

    Parameters
    ----------
    file_name : str
        The name of the file to read.
    column_names_dict : Optional[List[str]]
        The new column names to replace the old column names.
    index_columns : Optional[List[str]]
        The columns to use for the dataframe index.
    converters : Optional[dict] = None,
        Dictionary of functions for converting values in certain columns.
    parse_dates : Optional[List[str]] = False,
        The columns to use to parse date and time.
    date_parser : Optional[Callable] = None,
        The function to use for parsing date and time.
    format : Optional[str] = None,
        The str to use for formatting date and time.
    # date_time_columns : Optional[List[str]] = [],
    #     The columns to change to dtype datetime.
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
    nrows : Optional[int] = None
        The number of rows to read.

    Returns
    -------
    df : pd.DataFrame
        The dataframe created from the external file.

    Examples
    --------
    Example 1
    Read a csv file. There is no guarante the column dtypes will be correct.
    >>> data = read_file(file_name='myfile.csv')

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
    >>> date_parser = '%Y-%m-%d %H:%M:%S'
    >>> date_time_columns = ['T', 'U']
    >>> time_delta_columns = ['D']
    >>> category_columns = ['C']
    >>> integer_columns = ['A', 'I']
    >>> float_columns = ['X']
    >>> boolean_columns = ['R']
    >>> object_columns = ['Z']
    >>>
    >>>
    >>> def date_parser() -> Callable:
    >>>     return lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    >>>
    >>>
    >>> data = read_file(
    >>>     file_name='myfile.csv',
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
    >>> data_ods = ds.read_file(
    >>>     file_name='my_ods_file.ods',
    >>>     parse_dates=['T', 'U']
    >>> )
    """
    if '.csv' in file_name:
        df = pd.read_csv(
            file_name,
            converters=converters,
            parse_dates=parse_dates,
            date_parser=date_parser,
            nrows=nrows
        )
        if column_names_dict:
            df = df.rename(columns=column_names_dict)
        if index_columns:
            df = df.set_index(index_columns)
        for column in category_columns:
            df[column] = df[column].astype(CategoricalDtype())
        # for column in date_time_columns:
        #     df[column] = pd.to_datetime(
        #         df[column],
        #         format=date_parser
        #     )
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
            df = df.sort_values(
                by=sort_columns,
                axis='index',
                ascending=sort_columns_bool,
                kind='mergesort'
            )
    elif '.ods' in file_name:
        df = pd.read_excel(
            file_name,
            engine='odf',
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            date_parser=date_parser
        )
        # for column in date_time_columns:
        #     df[column] = pd.to_datetime(
        #         df[column],
        #         format=format
        #     )
    elif '.xlsx' in file_name and sheet_name:
        df = pd.read_excel(
            file_name,
            engine='openpyxl',
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            date_parser=date_parser
        )
    return df


# def read_file(
#     file_name: str,
#     *,
#     sheetname: Optional[str] = None,
#     indexcol: Optional[bool] = None,
#     abscissa: Optional[str] = None,
#     datetimeparser: Optional[str] = None,
#     columnnamessort: Optional[str] = False
# ) -> pd.DataFrame:
#     """
#     Create a DataFrame from an external file.
#
#     Parameters
#     ----------
#     file_name : str
#         The name of the file to read.
#     sheetname : Optional[str] = None
#         The name of the worksheet of a workbook.
#     indexcol : Optional[bool] = None
#         If False, do not use the first column.
#     abscissa : Optional[str] = None
#         The column to use to parse dates.
#     datetimeparser : Optional[str] = None
#         The datetimeparser string.
#     columnnamessort : Optional[str] = False
#         The column on which to sort the dataframe.
#
#     Returns
#     -------
#     df : pd.DataFrame
#
#     Example
#     -------
#     >>> df = ds.read_file(file_name='file_name.csv')
#     """
#
#     if '.ods' in file_name and abscissa and datetimeparser:
#         df = pd.read_excel(
#             file_name,
#             engine='odf',
#             parse_dates=[abscissa],
#             date_parser=lambda s: datetime.strptime(s, datetimeparser),
#         )
#     elif '.ods' in file_name and abscissa and not datetimeparser:
#         df = pd.read_excel(
#             file_name,
#             engine='odf',
#             parse_dates=[abscissa]
#         )
#     elif '.ods' in file_name and not abscissa and not datetimeparser:
#         df = pd.read_excel(
#             file_name,
#             engine='odf',
#         )
#     elif '.csv' in file_name and abscissa and datetimeparser \
#             and indexcol is False:
#         df = pd.read_csv(
#             file_name,
#             index_col=indexcol,
#             parse_dates=[abscissa],
#             date_parser=lambda s: datetime.strptime(s, datetimeparser),
#         )
#     elif '.csv' in file_name and abscissa and datetimeparser:
#         df = pd.read_csv(
#             file_name,
#             parse_dates=[abscissa],
#             date_parser=lambda s: datetime.strptime(s, datetimeparser),
#         )
#     elif '.csv' in file_name and abscissa:
#         df = pd.read_csv(
#             file_name,
#             parse_dates=[abscissa]
#         )
#     elif '.csv' in file_name:
#         df = pd.read_csv(
#             file_name,
#         )
#     elif '.xlsx' in file_name and abscissa and datetimeparser:
#         df = pd.read_excel(
#             file_name,
#             parse_dates=[abscissa],
#             date_parser=lambda s: datetime.strptime(s, datetimeparser),
#         )
#     elif '.xlsx' in file_name and sheetname and indexcol is False:
#         df = pd.read_excel(
#             file_name,
#             sheet_name=sheetname,
#             index_col=indexcol
#         )
#     elif '.xlsx' in file_name and not datetimeparser:
#         df = pd.read_excel(
#             file_name,
#         )
#     if datetimeparser is not None:
#         df = df.sort_values(
#             by=abscissa,
#             axis='rows',
#             ascending=True
#         )
#     if columnnamessort is True:
#         sortedcolumnnames = sorted(df.columns)
#         df = df[sortedcolumnnames]
#     return df


def html_header(
    header_title: str = 'Report',
    header_id: str = 'report'
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
    print(f'<title>{header_title}</title>')
    print('</head>')
    print('<body>')
    print(
        f'<h1 class="title"'
        f' id="{header_id}">'
        f'{header_title}</h1>'
    )
    # print('<pre style="white-space: pre-wrap;">')


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
    output_url: str,
    *,
    header_title: Optional[str] = 'Report',
    header_id: Optional[str] = 'report',
) -> IO[str]:
    '''
    Open file to write html and set header.

    Parameters
    ----------
    output_url : str
        The file name for the html output.
    header_title : Optional[str]
        The file title.
    header_id : Optional[str]
        The id for the header_title.

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
    '''
    original_stdout = sys.stdout
    sys.stdout = open(
        file=output_url,
        mode='w'
    )
    html_header(
        header_title=header_title,
        header_id=header_id
    )
    return original_stdout


def html_end(
    original_stdout: IO[str],
    output_url: str
) -> None:
    '''
    Set footer, close html file, open html file in new tab in web browser.

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
    '''
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
    Print html tag for a figure.

    Parameters
    ----------
    file_name : str
        The file name of the image.
    caption : Optional[str]
        The figure caption.
    """
    if caption is None:
        caption = file_name
    print(
        '<figure>'
        f'<img src="{file_name}" '
        f'alt="{file_name}"/>'
        f'<figcaption>{caption}</figcaption>'
        '</figure>'
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
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'b': ds.random_data(distribution='bool'),
    >>>         'c': ds.random_data(distribution='categories'),
    >>>         'd': ds.timedelta_data(),
    >>>         's': ds.random_data(distribution='strings'),
    >>>         't': ds.datetime_data(),
    >>>         'x': ds.random_data(distribution='norm'),
    >>>         'y': ds.random_data(distribution='randint'),
    >>>         'z': ds.random_data(distribution='uniform')
    >>>     }
    >>> )
    >>> print(
    >>>     byte_size(
    >>>         num=df.memory_usage(index=True).sum()
    >>>     )
    >>> )
    1.8 KiB
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
    limit: float
) -> List[str]:
    """
    Remove features that have NaN > limit

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    columns : List[str]
        The list of columns to evaluate.
    limit : float
        The percentage empty threshold value.

    Returns
    -------
    List[str]
        The list of columns below the threshold value.

    Example
    -------
    >>> import datasense as ds

    >>> features = ds.feature_percent_empty(
    >>>     df=data,
    >>>     columns=features,
    >>>     limit=percent_empty_features
    >>> )
    """
    num_rows = df.shape[0]
    return [col for col in columns if
            ((df[col].isna().sum() / num_rows * 100) <= limit)]


def report_summary(
    start_time: float,
    stop_time: float,
    *,
    read_file_names: Optional[List[str]] = None,
    save_file_names: Optional[List[str]] = None,
    targets: List[str] = None,
    features: List[str] = None,
    number_knots: List[int] = None
) -> None:
    """
    Report summary

    Parameters
    ----------
    start_time : float
        The start time.
    stop_time : float
        The stop time.
    read_file_names : List[str]
        The list of file names read.
    save_file_names : List[str]
        The list of file names saved.
    targets : List[str]
        The list of target variables.
    features : List[str]
        Thje list of feature variables.
    number_knots : List[int]
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
    print('<h1>Report summary</h1>')
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


def set_up_graphics_directory(graphdir: str) -> None:
    """
    Create an empty directory
    """
    try:
        rmtree(graphdir)
    except Exception:
        pass
    Path(graphdir).mkdir(parents=True, exist_ok=True)


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
)
