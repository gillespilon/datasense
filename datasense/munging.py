"""
Data munging
"""

from shutil import copytree, move, rmtree
from tkinter import filedialog
from typing import Pattern
from pathlib import Path
from tkinter import Tk
import psutil
import string
import sys

from datasense import random_data, timedelta_data, datetime_data
from pandas.api.types import CategoricalDtype
from beautifultable import BeautifulTable
import pyarrow.feather as ft
from scipy.stats import norm
import pandas as pd
import numpy as np


def dataframe_info(
    *, df: pd.DataFrame, file_in: Path | str, unique_bool: bool = False
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
    file_in : Path | str
        The name of the file from which df was created.
    unique_bool : bool = False
        Print unique values of a column if True.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.dataframe_info(
    ...     df=df,
    ...     file_in='df'
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> df = ds.dataframe_info(
    ...     df=df,
    ...     file_in='df',
    ...     unique_bool=True
    ... ) # doctest: +SKIP
    """
    df, rows_in_count, rows_out_count, rows_empty_count = process_rows(df=df)
    (
        df,
        columns_in_count,
        columns_non_empty_count,
        columns_empty_count,
        columns_empty_list,
        columns_non_empty_list,
        columns_bool_list,
        columns_bool_count,
        columns_float_list,
        columns_float_count,
        columns_integer_list,
        columns_integer_count,
        columns_datetime_list,
        columns_datetime_count,
        columns_object_list,
        columns_object_count,
        columns_category_list,
        columns_category_count,
        columns_timedelta_list,
        columns_timedelta_count,
    ) = process_columns(df=df)
    print("==========================")
    print(f"DataFrame information for: {file_in}")
    print()
    print(f"Rows total        : {rows_in_count}")
    print(f"Rows empty        : {rows_empty_count} (deleted)")
    print(f"Rows not empty    : {rows_out_count}")
    print(f"Columns total     : {columns_in_count}")
    print(f"Columns empty     : {columns_empty_count} (deleted)")
    print(f"Columns not empty : {columns_non_empty_count}")
    print()
    number_empty_cells_in_columns(df=df)
    print(f"List of {columns_non_empty_count} non-empty columns:")
    print_list_by_item(list_to_print=columns_non_empty_list)
    print()
    print(f"List of {columns_bool_count} bool columns:")
    print_list_by_item(list_to_print=columns_bool_list)
    print()
    print(f"List of {columns_category_count} category columns:")
    print_list_by_item(list_to_print=columns_category_list)
    print()
    print(f"List of {columns_datetime_count} datetime columns:")
    print_list_by_item(list_to_print=columns_datetime_list)
    print()
    print(f"List of {columns_float_count} float columns:")
    print_list_by_item(list_to_print=columns_float_list)
    print()
    print(f"List of {columns_integer_count} integer columns:")
    print_list_by_item(list_to_print=columns_integer_list)
    print()
    print(f"List of {columns_object_count} string columns:")
    print_list_by_item(list_to_print=columns_object_list)
    print()
    print(f"List of {columns_timedelta_count} timedelta columns:")
    print_list_by_item(list_to_print=columns_timedelta_list)
    print()
    print(f"List of {columns_empty_count} empty columns:")
    print_list_by_item(list_to_print=columns_empty_list)
    print()
    if unique_bool:
        for column in columns_non_empty_list:
            print("column:", column)
            print(df[column].unique())
            print()
    return df


def find_bool_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Create a list of boolean column names of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    columns_bool : list[str]
        A list of boolean column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_bool = ds.find_bool_columns(df=df)
    >>> columns_bool
    ['b', 'bn']
    """
    columns_bool = list(df.select_dtypes(include=["bool", "boolean"]).columns)
    return columns_bool


def find_category_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Create list of category column names of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    columns_category : list[str]
        A list of category column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_category = ds.find_category_columns(df=df)
    >>> columns_category
    ['c', 'cs']
    """
    columns_category = list(df.select_dtypes(include=["category"]).columns)
    return columns_category


def find_datetime_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all datetime columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    datetime_columns : list[str]
        A list of datetime column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_datetime = ds.find_datetime_columns(df=df)
    >>> columns_datetime
    ['t', 'u']
    """
    datetime_columns = list(df.select_dtypes(include=["datetime64"]).columns)
    return datetime_columns


def find_float_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all float columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    float_columns : list[str]
        A list of float column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_float = ds.find_float_columns(df=df)
    >>> columns_float
    ['a', 'x', 'z']
    """
    float_columns = df.select_dtypes(include=["float64"]).columns.tolist()
    return float_columns


def find_integer_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all integer columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    integer_columns : list[str]
        A list of integer column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_int = ds.find_integer_columns(df=df)
    >>> columns_int
    ['i', 'y', 'yn']
    """
    integer_columns = df.select_dtypes(
        include=["int64", "Int64"]
    ).columns.tolist()
    return integer_columns


def find_int_float_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all integer and float columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    columns_int_float : list[str]
        A list of integer and float column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_int_float = ds.find_int_float_columns(df=df)
    >>> columns_int_float
    ['a', 'i', 'x', 'y', 'yn', 'z']
    """
    columns_int_float = list(
        df.select_dtypes(include=["int64", "float64"]).columns
    )
    return columns_int_float


def find_object_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all object columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    object_columns : list[str]
        A list of object column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_object = ds.find_object_columns(df=df)
    >>> columns_object
    ['r', 's']
    """
    object_columns = df.select_dtypes(include=["object"]).columns.tolist()
    return object_columns


def find_timedelta_columns(*, df: pd.DataFrame) -> list[str]:
    """
    Find all timedelta columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    columns_timedelta : list[str]
        A list of timedelta column names.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> columns_timedelta = ds.find_timedelta_columns(df=df)
    >>> columns_timedelta
    ['d']
    """
    columns_timedelta = list(df.select_dtypes(include=["timedelta"]).columns)
    return columns_timedelta


def number_empty_cells_in_columns(*, df: pd.DataFrame) -> None:
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
    >>> df = pd.DataFrame(data={
    ...     'X': [25.0, 24.0, 35.5, np.nan, 23.1],
    ...     'Y': [27, 24, np.nan, 23, np.nan],
    ...     'Z': ['a', 'b', np.nan, 'd', 'e']
    ... })
    >>> ds.number_empty_cells_in_columns(df=df) # doctest:+NORMALIZE_WHITESPACE
    Information about non-empty columns
     Column   Data type   Empty cell count   Empty cell %   Unique
    -------- ----------- ------------------ -------------- --------
     X        float64                    1           20.0        4
     Y        float64                    2           40.0        3
     Z        object                     1           20.0        4
    """
    print("Information about non-empty columns")
    table = BeautifulTable(maxwidth=90)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    column_alignments = {
        "Column": BeautifulTable.ALIGN_LEFT,
        "Data type": BeautifulTable.ALIGN_LEFT,
        "Empty cell count": BeautifulTable.ALIGN_RIGHT,
        "Empty cell %": BeautifulTable.ALIGN_RIGHT,
        "Unique": BeautifulTable.ALIGN_RIGHT,
    }
    table.columns.header = list(column_alignments.keys())
    for item, (_column_name, alignment) in enumerate(
        column_alignments.items()
    ):
        table.columns.alignment[item] = alignment
    num_rows = df.shape[0]
    for column_name in df:
        try:
            sum_nan = sum(pd.isna(df[column_name]))
            percent_nan = round(sum_nan / num_rows * 100, 1)
            table.rows.append(
                [
                    column_name,
                    df[column_name].dtype,
                    sum_nan,
                    percent_nan,
                    df[column_name].nunique(),
                ]
            )
        except KeyError:
            print("Error on column:", column_name)
    print(table)


def process_columns(
    *, df: pd.DataFrame
) -> tuple[
    pd.DataFrame,
    int,
    int,
    int,
    list[str],
    list[str],
    list[str],
    int,
    list[str],
    int,
    list[str],
    int,
    list[str],
    int,
    list[str],
    int,
    list[str],
    int,
    list[str],
    int,
]:
    """
    Return a DataFrame without empty columns and ensure all column labels are
    strings.

    Create various counts of columns of a DataFrame.
    Create count of columns (columns_in_count)
    Create count and list of empty columns (columns_empty_count, columns_empty_list)
    Create count and list of non-empty columns (columns_non_empty_count, columns_non_empty_list)
    Delete empty columns
    Create count and list of boolean columns (columns_bool_count, columns_bool_list)
    Create count and list of category columns (columns_category_count, columns_category_list)
    Create count and list of datetime columns (columns_datetime_count, columns_datetime_list)
    Create count and list of float columns (columns_float_count, columns_float_list)
    Create count and list of integer columns (columns_integer_count, columns_integer_list)
    Create count and list of string columns (columns_object_count, columns_object_list)
    Create count of timedelta columns (columns_timedelta_count, columns_timedelta_list)

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
    columns_empty_list : list[str]
        The list of empty columns.
    columns_non_empty_list : list[str]
        The list of non-empty columns.
    columns_bool_list : list[str]
        The list of boolean columns.
    columns_bool_count : int
        The count of boolean columns.
    columns_float_list : list[str]
        The list of float columns.
    columns_float_count : int
        The count of float columns.
    columns_integer_list : list[str]
        The list of integer columns.
    columns_integer_count : int
        The count of integer columns
    columns_datetime_list : list[str]
        The list of datetime columns.
    columns_datetime_count : int
        The count of datetime columns.
    columns_object_list : list[str]
        The list of object columns.
    columns_object_count : int
        The count of object columns.
    columns_category_list : list[str]
        The list of category columns.
    columns_category_count : int
        The count of category columns.
    columns_timedelta_list : list[str]
        The list of timedelta columns.
    columns_timedelta_count : int
        The count of timedelta columns.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> df, columns_in_count, columns_non_empty_count, columns_empty_count,\
    ...     columns_empty_list, columns_non_empty_list, columns_bool_list,\
    ...     columns_bool_count, columns_float_list, columns_float_count,\
    ...     columns_integer_list, columns_integer_count,\
    ...     columns_datetime_list, columns_datetime_count,\
    ...     columns_object_list, columns_object_count, columns_category_list,\
    ...     columns_category_count, columns_timedelta_list,\
    ...     columns_timedelta_count = ds.process_columns(df=df) # doctest:+SKIP
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
    columns_empty_list = sorted(
        {
            column_name
            for column_name in df.columns
            if df[column_name].isna().all()
        }
    )
    columns_in_count = len(df.columns)
    columns_empty_count = len(columns_empty_list)
    columns_non_empty_count = columns_in_count - columns_empty_count
    # df = df.drop(
    #     labels=columns_empty_list,
    #     axis="columns"
    # )
    df = delete_empty_columns(df=df, list_empty_columns=columns_empty_list)
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
    columns_integer_list = find_integer_columns(df=df)
    columns_integer_count = len(columns_integer_list)
    columns_object_list = find_object_columns(df=df)
    columns_object_count = len(columns_object_list)
    columns_timedelta_list = find_timedelta_columns(df=df)
    columns_timedelta_count = len(columns_timedelta_list)
    return (
        df,
        columns_in_count,
        columns_non_empty_count,
        columns_empty_count,
        columns_empty_list,
        columns_non_empty_list,
        columns_bool_list,
        columns_bool_count,
        columns_float_list,
        columns_float_count,
        columns_integer_list,
        columns_integer_count,
        columns_datetime_list,
        columns_datetime_count,
        columns_object_list,
        columns_object_count,
        columns_category_list,
        columns_category_count,
        columns_timedelta_list,
        columns_timedelta_count,
    )


def process_rows(*, df: pd.DataFrame) -> tuple[pd.DataFrame, int, int, int]:
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
    >>> df, rows_in_count, rows_out_count, rows_empty_count = \
    ...     ds.process_rows(df=df) # doctest: +SKIP
    rows_in_count   : 42
    rows_out_count  : 42
    rows_empty_count: 0
    """
    rows_in_count = df.shape[0]
    df = delete_empty_rows(df=df).drop_duplicates()
    rows_out_count = df.shape[0]
    rows_empty_count = rows_in_count - rows_out_count
    return (df, rows_in_count, rows_out_count, rows_empty_count)


def save_file(
    *,
    df: pd.DataFrame | pd.Series,
    file_name: str | Path,
    index: bool = False,
    index_label: str = None,
    sheet_name: str = "sheet_001",
    encoding: str = "utf-8",
) -> None:
    """
    Save a DataFrame or Series to a file.

    Parameters
    ----------
    df : pd.DataFrame | pd.Series
        The DataFrame or Series to be saved to a file.
    file_name : str | Path
        The name of the file to be saved.
    index : bool = False
        If True, creates an index.
    index_label : str = None
        The index label.
    sheet_name : str = 'sheet_001'
        The name of the worksheet in the workbook.
    encoding : str = "utf-8"
        Encoding to use for UTF when writing.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    ...     df=df,
    ...     file_name='x_y.csv'
    ... )

    >>> import datasense as ds
    >>> ds.save_file(
    ...     df=df,
    ...     file_name='x_y.csv',
    ...     index=True
    ... )

    >>> import datasense as ds
    >>> ds.save_file(
    ...     df=df,
    ...     file_name='x_y.xlsx'
    ... )

    >>> import datasense as ds
    >>> ds.save_file(
    ...     df=df,
    ...     file_name='x_y.xlsx',
    ...     index=True,
    ...     sheet_name='sheet_one'
    ... )

    >>> import datasense as ds
    >>> from pathlib import Path
    >>> file_to_save = 'myfeatherfile.feather'
    >>> path = Path(file_to_save)
    >>> ds.save_file(
    ...     df=df,
    ...     file_name=path
    ... )

    """
    if isinstance(type(file_name).__name__, str):
        file_name = Path(file_name)
    if file_name.suffix in [".csv", ".CSV"]:
        df.to_csv(
            path_or_buf=file_name,
            index=index,
            index_label=index_label,
            encoding=encoding,
        )
    elif file_name.suffix in [".ods", ".ODS"]:
        excel_writer = pd.ExcelWriter(
            path=file_name,
            engine="odf",
        )
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            index=index,
            index_label=index_label,
        )
        excel_writer.close()
    elif file_name.suffix in [".xlsx", ".XLSX"]:
        excel_writer = pd.ExcelWriter(file_name)
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            engine="openpyxl",
            index=index,
            index_label=index_label,
        )
        excel_writer.close()
    # Removed xlsb XLSB support because Arch Linux does not support
    # elif file_name.suffix in ['.xlsb', '.XLSB']:
    #     excel_writer = pd.ExcelWriter(file_name)
    #     df.to_excel(
    #         excel_writer=excel_writer,
    #         sheet_name=sheet_name,
    #         engine='pyxlsb',
    #         index=index,
    #         index_label=index_label
    #     )
    #     excel_writer.save()
    elif file_name.suffix in [".feather"]:
        ft.write_feather(df=df, dest=file_name)


def read_file(
    *,
    file_name: str | Path,
    header: int | list[int] | None = 0,
    skiprows: list[int] | None = None,
    column_names_dict: dict[str, str] = {},
    index_columns: list[str] = [],
    usecols: list[str] | None = None,
    dtype: dict | None = None,
    converters: dict | None = None,
    parse_dates: list[str | int] | dict | bool = False,
    # date_format: str | dict = None,
    datetime_format: str | None = None,
    time_delta_columns: list[str] = [],
    category_columns: list[str] = [],
    integer_columns: list[str] = [],
    float_columns: list[str] = [],
    boolean_columns: list[str] = [],
    object_columns: list[str] = [],
    sort_columns: list[str] = [],
    sort_columns_bool: list[bool] = [],
    sheet_name: str = False,
    nrows: int | None = None,
    skip_blank_lines: bool = True,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Create a DataFrame from an external file.

    - read csv | read CSV
    - read ods | read ODS
    - read Excel: read xlsx | read XLSX | read xlsm | read XLSM
    - read feather

    Parameters
    ----------
    file_name : str | Path
        The name of the file to read.
    header : int | list[int] | None = 0
        The row to use for the column labels. Use None if there is no header.
    skiprows : list[int] | None = None
        The specific row indices to skip.
    column_names_dict : dict[str, str] = {}
        The new column names to replace the old column names.
    index_columns : list[str] = []
        The columns to use for the DataFrame index.
    usecols : list[str] | None = None
        The columns to read.
    dtype : dict | None = None
        A dictionary of column names and dtypes.
        NOTE: Nullable Boolean data type is experimental and does not work;
        use .astype() on df after created.
    converters : dict | None = None
        Dictionary of functions for converting values in certain columns.
    parse_dates : list[str] = False
        The columns to use to parse date and time.
    date_format : str | dict = None
        If used in conjunction with parse_dates, will parse dates according to
        this format.
    datetime_format : str | None = None
        The str to use for formatting date and time.
    time_delta_columns : list[str] = []
        The columns to change to dtype timedelta.
    category_columns : list[str] = []
        The columns to change to dtype category.
    integer_columns : list[str] = []
        The columns to change to dtype integer.
    float_columns : list[str] = []
        The columns to change to dtype float.
    boolean_columns : list[str] = []
        The columns to change to dtype boolean.
    object_columns : list[str] = []
        The columns to change to dtype object.
    sort_columns : list[str] = []
        The columns on which to sort the DataFrame.
    sort_columns_bool : list[bool] = []
        The booleans for sort_columns.
    sheet_name : str = False
        The name of the worksheet in the workbook.
    nrows : int | None = None
        The number of rows to read.
    skip_blank_lines : bool = True
        If True, skip over blank lines rather than interpreting as NaN values.
    encoding : str = "utf-8"
        Encoding to use for UTF when reading.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame created from the external file.

    Examples
    --------

    Create a data file for the examples.

    >>> import datasense as ds
    >>> file_name='myfile.csv'
    >>> df = ds.create_dataframe()
    >>> df.columns # doctest: +SKIP
    >>> df.dtypes  # doctest: +SKIP
    >>> df.save_file(
    ...     df=df,
    ...     file_name=file_name
    ... ) # doctest: +SKIP
    Index(['a', 'b', 'c', 'd', 'i', 'r', 's', 't', 'u', 'x', 'y', 'z'],dtype='object')
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

    Read a csv file. There is no guarantee the column dtypes will be correct.
    Only [a, i, s, x, z] have the correct dtypes.

    >>> import datasense as ds
    >>> file_name = "file.csv"
    >>> df = ds.read_file(file_name=file_name) # doctest: +SKIP
    >>> df.dtypes # doctest: +SKIP
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

    Read a csv file. Ensure the dtypes of datetime columns.

    >>> import datasense as ds
    >>> parse_dates = ['t', 'u']
    >>> file_name = "file.csv"
    >>> df = ds.read_file(
    ...     file_name=file_name,
    ...     parse_dates=parse_dates
    ... ) # doctest: +SKIP
    >>> df.dtypes# doctest: +NORMALIZE_WHITESPACE
    a           float64
    b              bool
    bn          boolean
    c          category
    cs         category
    d   timedelta64[ns]
    i             int64
    r            object
    s            object
    t    datetime64[ns]
    u    datetime64[ns]
    x           float64
    y             int64
    yn            Int64
    z           float64
    dtype: object

    Read a csv file. Ensure the dtypes of columns; not timedelta, datetime.

    >>> import datasense as ds
    >>> convert_dict = {
    ...     'a': 'float64',
    ...     'b': 'boolean',
    ...     'c': 'category',
    ...     'i': 'float64',
    ...     'r': 'str',
    ...     's': 'str',
    ...     'x': 'float64',
    ...     'y': 'Int64',
    ...     'z': 'float64'
    ... }
    >>> df = ds.read_file(
    ...     file_name=file_name,
    ...     dtype=convert_dict
    ... ) # doctest: +SKIP
    >>> df.dtypes
    a             float64
    b                bool
    bn            boolean
    c            category
    cs           category
    d     timedelta64[ns]
    i               int64
    r              object
    s              object
    t      datetime64[ns]
    u      datetime64[ns]
    x             float64
    y               int64
    yn              Int64
    z             float64
    dtype: object

    Read a csv file. Ensure the dtypes of columns. Rename the columns.
    Set index with another column. Convert float column to integer.

    >>> import datasense as ds
    >>> column_names_dict = {
    ...     'a': 'A',
    ...     'b': 'B',
    ...     'c': 'C',
    ...     'd': 'D',
    ...     'i': 'I',
    ...     'r': 'R',
    ...     's': 'S',
    ...     't': 'T',
    ...     'u': 'U',
    ...     'y': 'Y',
    ...     'x': 'X',
    ...     'z': 'Z'
    ... }
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
    ...     file_name='myfile.csv',
    ...     column_names_dict=column_names_dict,
    ...     index_columns=index_columns,
    ...     parse_dates=parse_dates,
    ...     # date_format=date_format,
    ...     time_delta_columns=time_delta_columns,
    ...     category_columns=category_columns,
    ...     integer_columns=integer_columns,
    ...     float_columns=float_columns,
    ...     boolean_columns=boolean_columns,
    ...     object_columns=object_columns,
    ...     sort_columns=sort_columns,
    ...     sort_columns_bool=sort_columns_bool
    ... ) # doctest: +SKIP
    >>> data = ds.read_file(
    ...     file_name=file_name,
    ...     column_names_dict=column_names_dict,
    ...     index_columns=index_columns,
    ...     date_time_columns=date_time_columns,
    ...     # date_format=date_format,
    ...     parse_dates=date_time_columns,
    ...     time_delta_columns=time_delta_columns,
    ...     category_columns=category_columns,
    ...     integer_columns=integer_columns
    ... ) # doctest: +SKIP

    Read an ods file.

    >>> import datasense as ds
    >>> file_name = 'myfile.ods'
    >>> df = ds.create_dataframe()
    >>> ds.save_file(
    ...     df=df,
    ...     file_name=file_name
    ... )
    >>> parse_dates = ['t', 'u']
    >>> df = ds.read_file(
    ...     file_name=file_name,
    ...     parse_dates=parse_dates
    ... ) # doctest: +SKIP
    >>> ds.dataframe_info(
    ...     df=df,
    ...     file_in=file_name
    ... ) # doctest: +SKIP

    Read an xlsx file.

    >>> import datasense as ds
    >>> file_name = 'myfile.xlsx'
    >>> sheet_name = 'raw_data'
    >>> df = ds.read_file(
    ...     file_name=file_name,
    ...     sheet_name=sheet_name
    ... ) # doctest: +SKIP
    >>> ds.dataframe_info(
    ...     df=df,
    ...     file_in=file_name
    ... ) # doctest: +SKIP

    Read a feather file.

    >>> import datasense as ds
    >>> from pathlib import Path
    >>> file_to_read = 'myfeatherfile.feather'
    >>> path = Path(file_to_read)
    >>> df = ds.read_file(file_name=path)

    Read a feather file with columns list.

    >>> import datasense as ds
    >>> from pathlib import Path
    >>> file_to_read = 'myfeatherfile.feather'
    >>> usecols = ['col1', 'col2']
    >>> path = Path(file_to_read)
    >>> df = ds.read_file(
    ...     file_name=path,
    ...     usecols=usecols
    ... ) # doctest: +SKIP

    Removed xlsb XLSB support because Arch Linux does not support. The
    following example is retained for historical purposes and in case
    Arch Linux supports it in future.

    Read an xlsb file.

    >>> import datasense as ds
    >>> file_name = 'myfile.xlsb'
    >>> sheet_name = 'raw_data'
    >>> df = ds.read_file(
    ...     file_name=file_name,
    ...     sheet_name=sheet_name
    ... )
    >>> ds.dataframe_info(
    ...     df=df,
    ...     file_in=file_name
    ... )
    """
    if isinstance(type(file_name).__name__, str):
        file_name = Path(file_name)
    if file_name.suffix in [".csv", ".CSV"]:
        df = pd.read_csv(
            file_name,
            skiprows=skiprows,
            usecols=usecols,
            dtype=dtype,
            converters=converters,
            parse_dates=parse_dates,
            # date_format=date_format,
            nrows=nrows,
            skip_blank_lines=skip_blank_lines,
            encoding=encoding,
        )
    elif file_name.suffix in [".ods", ".ODS"]:
        df = pd.read_excel(
            io=file_name,
            skiprows=skiprows,
            usecols=usecols,
            dtype=dtype,
            engine="odf",
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            # date_format=date_format,
        )
    elif file_name.suffix in [".xlsx", ".XLSX", ".xlsm", ".XLSM"]:
        df = pd.read_excel(
            io=file_name,
            sheet_name=sheet_name,
            header=header,
            usecols=usecols,
            dtype=dtype,
            engine="openpyxl",
            skiprows=skiprows,
            nrows=nrows,
            parse_dates=parse_dates,
            # date_format=date_format,
        )
    # Removed xlsb XLSB support because Arch Linux does not support
    # elif file_name.suffix in ['.xlsb', '.XLSB']:
    #     df = pd.read_excel(
    #         io=file_name,
    #         sheet_name=sheet_name,
    #         header=header,
    #         usecols=usecols,
    #         dtype=dtype,
    #         engine='pyxlsb',
    #         skiprows=skiprows,
    #         nrows=nrows,
    #         parse_dates=parse_dates,
    #         # date_format=date_format,
    #     )
    elif file_name.suffix in [".feather"]:
        df = ft.read_feather(source=file_name, columns=usecols)
    if column_names_dict:
        df = rename_some_columns(df=df, column_names_dict=column_names_dict)
    if index_columns:
        df = df.set_index(index_columns)
    for column in category_columns:
        df[column] = df[column].astype(dtype=CategoricalDtype())
    for column in time_delta_columns:
        df[column] = pd.to_timedelta(df[column])
    for column in integer_columns:
        df[column] = df[column].astype(dtype="int64")
    for column in float_columns:
        df[column] = df[column].astype(dtype="float64")
    for column in boolean_columns:
        df[column] = df[column].astype(dtype="bool")
    for column in object_columns:
        df[column] = df[column].astype(dtype="object")
    if sort_columns and sort_columns_bool:
        df = sort_rows(
            df=df,
            sort_columns=sort_columns,
            sort_columns_bool=sort_columns_bool,
            kind="mergesort",
        )
    return df


def byte_size(*, num: np.int64, suffix: str = "B") -> str:
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
    ...     ds.byte_size(
    ...         num=df.memory_usage(index=True).sum()
    ...     )
    ... )
    4.2 KiB
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    memory_usage = "%.1f %s%s" % (num, "Yi", suffix)
    return memory_usage


def feature_percent_empty(
    *, df: pd.DataFrame, columns: list[str], threshold: float
) -> list[str]:
    """
    Remove features that have NaN > threshold.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    columns : list[str]
        The list of columns to evaluate.
    threshold : float
        The percentage empty threshold value.

    Returns
    -------
    list_columns : list[str]
        The list of columns below the threshold value.

    Example
    -------

    >>> import datasense as ds
    >>> features = ds.feature_percent_empty(
    ...     df=data,
    ...     columns=features,
    ...     threshold=percent_empty_features
    ... ) # doctest: +SKIP
    """
    num_rows = df.shape[0]
    list_columns = [
        col
        for col in columns
        if ((df[col].isna().sum() / num_rows * 100) <= threshold)
    ]
    return list_columns


def create_directory(
    *, directories: list[str], ignore_errors: bool = True
) -> None:
    """
    Create empty directories for a path.
    - Deletes existing directories, whether empty or non-empty.
    - Ignores errors such as no existing directories.

    Parameters
    ----------
    directories : list[str]
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
    *, directories: list[str], ignore_errors: bool = True
) -> None:
    """
    Delete a list of directories.
    - Deletes existing directories, whether empty or non-empty.

    Parameters
    ----------
    directories : list[str]
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
    *, sources: list[str], destinations: list[str], ignore_errors: bool = True
) -> None:
    """
    Delete destination directories (if present) and rename source directories
    to the destination directories.

    Parameters
    ----------
    sources : list[str]
        The old directories.
    destinations : list[str]
        The new directories.
    ignore_errors : bool = True
        Boolean to deal with errors.

    Example
    -------

    >>> import datasense as ds
    >>> sources = ['old_directory']
    >>> destinations = ['new_directory']
    >>> ds.rename_directory(sources=sources, destinations=destinations) \
    ...     # doctest: +SKIP
    """
    for source, destination in zip(sources, destinations):
        rmtree(path=destination, ignore_errors=ignore_errors)
        move(src=source, dst=destination)


def copy_directory(
    *,
    sources: Path | str,
    destinations: Path | str,
    ignore_errors: bool = True,
) -> None:
    """
    Delete destination directories (if present) and copy source directories
    to destination directories.

    Parameters
    ----------
    sources : Path | str
        The source directory name.
    destinations : Path | str
        The destination directory name.
    ignore_errors : bool = True
        Boolean to deal with errors.

    Example
    -------

    >>> import datasense as ds
    >>> sources = ['source_directory']
    >>> destinations = ['destination_directory']
    >>> ds.rename_directory(
    ...     sources=sources,
    ...     destinations=destinations
    ... ) # doctest: +SKIP
    """
    for source, destination in zip(sources, destinations):
        rmtree(path=destination, ignore_errors=ignore_errors)
        copytree(src=source, dst=destination)


def replace_text_numbers(
    *,
    df: pd.DataFrame,
    columns: list[str] | list[int] | list[float] | list[Pattern[str]],
    old: list[str] | list[int] | list[float] | list[Pattern[str]],
    new: list[int],
    regex: bool = True,
) -> pd.DataFrame:
    """
    Replace text or numbers with text or numbers.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    columns: list[str] | list[int] | list[float] | list[Pattern[str]]
        The list of columns for replacement.
    old: list[str] | list[int] | list[float] | list[Pattern[str]]
        The list of item to replace.
    new : list[int]
        The list of replacement items.
    regex : bool = True
        Determines if the passed-in pattern is a regular expression.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------

    >>> import datasense as ds
    >>> list_y_1_n_5 = [
    ...     'Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q06', 'Q10', 'Q17', 'Q18',
    ...     'Q19', 'Q20', 'Q21', 'Q23', 'Q24', 'Q25'
    ... ]
    >>> list_y_5_n_1 = [
    ...     'Q07', 'Q11', 'Q12', 'Q13', 'Q15', 'Q16'
    ... ]
    >>> data = ds.replace_text_numbers(
    ...     df=data,
    ...     columns=list_y_1_n_5,
    ...     old=['Yes', 'No'],
    ...     new=[1, 5],
    ...     regex=False
    ... ) # doctest: +SKIP
    >>> data = ds.replace_text_numbers(
    ...     df=data,
    ...     columns=list_y_5_n_1,
    ...     old=['Yes', 'No'],
    ...     new=[5, 1],
    ...     regex=False
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> data = ds.replace_text_numbers(
    ...     df=data,
    ...     columns=['Q23'],
    ...     old=[r'\xa0'],
    ...     new=[r' '],
    ...     regex=True
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> data = ds.replace_text_numbers(
    ...     df=data,
    ...     columns=['address_country'],
    ...     old=[
    ...         'AD', 'AE', 'AF', 'AG',
    ...         'AI', 'AL', 'AM', 'AN',
    ...         'AO', 'AQ', 'AR', 'AS',
    ...         'AT', 'AU', 'AW', 'AZ',
    ...     ]
    ...     new=[
    ...         'Andorra', 'Unit.Arab Emir.', 'Afghanistan', 'Antigua/Barbuda',
    ...         'Anguilla', 'Albania', 'Armenia', 'Niederl.Antill.',
    ...         'Angola', 'Antarctica', 'Argentina', 'Samoa,American',
    ...         'Austria', 'Australia', 'Aruba', 'Azerbaijan',
    ...     ],
    ...     regex=False
    ... ) # doctest: +SKIP
    """
    dfnew = df.copy(deep=True)
    for column in columns:
        dfnew[column] = dfnew[column].replace(
            to_replace=old, value=new, regex=regex
        )
    return dfnew


def create_dataframe(
    *, size: int = 42, fraction_nan: float = 0.13
) -> pd.DataFrame:
    # TODO: why did I create distribution "u"?
    """
    Create a Pandas DataFrame.

    Parameters
    ----------
    size : int = 42
        The number of rows to create.
    fraction_nan : float = 0.13
        The fraction of the DataFrame rows to contain NaN.

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

    >>> import datasense as ds
    >>> df = create_dataframe()
    """
    df = pd.DataFrame(
        {
            "a": random_data(
                distribution="uniform", size=size, loc=13, scale=70
            ),
            "b": random_data(distribution="bool", size=size),
            "bn": random_data(distribution="boolean", size=size),
            "c": random_data(
                distribution="category",
                size=size,
                categories=["blue", "white", "red"],
            ),
            "cs": random_data(
                distribution="categories",
                size=size,
                categories=["small", "medium", "large"],
            ),
            "d": timedelta_data(time_delta_days=size - 1),
            "i": random_data(distribution="randint", size=size),
            "r": random_data(
                distribution="strings", strings=["0", "1"], size=size
            ),
            "s": random_data(distribution="strings", size=size),
            "t": datetime_data(time_delta_days=size - 1),
            "u": datetime_data(time_delta_days=size - 1),
            "x": random_data(distribution="norm", size=size),
            "y": random_data(distribution="randint", size=size),
            "yn": random_data(
                distribution="randInt", size=size, fraction_nan=fraction_nan
            ),
            "z": random_data(distribution="uniform", size=size),
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
    column_names: list[str] = None,
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
    column_names: list[str]
        The column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.create_dataframe_norm()

    >>> import datasense as ds
    >>> column_count = 100
    >>> row_count = 1000
    >>> column_names = [f'col{item}' for item in range(column_count)]
    >>> df = ds.create_dataframe_norm(
    ...     row_count=row_count,
    ...     column_count=column_count,
    ...     loc=69,
    ...     scale=13,
    ...     random_state=42,
    ...     column_names=column_names
    ... )
    """
    if not column_names:
        column_names = [f"col{item}" for item in range(column_count)]
    df = pd.DataFrame(
        norm.rvs(
            size=(row_count, column_count),
            loc=loc,
            scale=scale,
            random_state=random_state,
        ),
        columns=column_names,
    )
    return df


def delete_rows(
    *,
    df: pd.DataFrame,
    delete_row_criteria: tuple[str, int] | tuple[str, float] | tuple[str, str],
) -> pd.DataFrame:
    """
    Delete rows of a DataFrame based on a value in one column.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    delete_row_criteria:
        tuple[str, int] | tuple[str, float] | tuple[str, str]
        A tuple of column name and criteria for the entire cell.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.delete_rows(
    ...     df=df,
    ...     delete_row_criteria=['Batch Acceptance', 1]
    ... ) # doctest: +SKIP
    """

    if delete_row_criteria:
        df = df.loc[~(df[delete_row_criteria[0]] == delete_row_criteria[1])]
    return df


def delete_columns(*, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Delete columns of a DataFrame using a list.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    columns : list[str]
        A list of column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.delete_columns(
    ...     df=df,
    ...     columns=columns
    ... ) # doctest: +SKIP
    """
    df = df.drop(columns=columns)
    return df


def sort_rows(
    *,
    df: pd.DataFrame,
    sort_columns: list[str],
    sort_columns_bool: list[bool],
    kind: str = "mergesort",
) -> pd.DataFrame:
    """
    Sort a DataFrame for one or more columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    sort_columns : list[str]
        The sort columns.
    sort_columns_bool : list[bool]
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
    ...     df=df,
    ...     sort_columns=sort_columns,
    ...     sort_columns_bool=sort_columns_bool,
    ...     kind='mergesort'
    ... ) # doctest: +SKIP
    """

    df = df.sort_values(
        by=sort_columns, axis="index", ascending=sort_columns_bool, kind=kind
    )
    return df


def rename_all_columns(*, df: pd.DataFrame, labels: list[str]) -> pd.DataFrame:
    """
    Rename all DataFrame columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    labels : list[str]
        The list of all column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.rename_all_columns(
    ...     df=df,
    ...     labels=labels
    ... ) # doctest: +SKIP
    """
    df = df.set_axis(labels=labels, axis="columns")
    return df


def rename_some_columns(
    *, df: pd.DataFrame, column_names_dict: dict[str, str]
) -> pd.DataFrame:
    """
    Rename some columns with a dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    column_names_dict : dict[str, str]
        The dictionary of old:new column names.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Example
    -------

    >>> import datasense as ds
    >>> df = ds.rename_some_columns(
    ...     df=df,
    ...     column_names_dict=column_names_dict
    ... ) # doctest: +SKIP
    """
    df = df.rename(columns=column_names_dict)
    return df


def replace_column_values(
    *,
    s: pd.Series,
    replace_dict: dict[str, str] | dict[int, int] | dict[float, float],
    regex: bool = False,
) -> pd.Series:
    """
    Replace values in a series using a dictionary.

    Parameters
    ----------
    s : pd.Series
        The input series.
    replace_dict : dict[str, str] | dict[int, int] | dict[float, float]
        The dictionary of values to replace.
    regex : bool = True
        Determines if the passed-in pattern is a regular expression.

    Returns:
    --------
    s : pd.Series
        The output series.

    Example
    -------

    >>> import datasense as ds
    >>> s = ds.replace_column_values(
    ...     s=s,
    ...     replace_dict=replace_dict
    ... ) # doctest: +SKIP
    """
    # s = s.replace(
    #     to_replace=replace_dict,
    #     value=None,
    #     regex=regex
    # )
    list_from_series = s.to_list()
    list_transformed = [replace_dict.get(x, x) for x in list_from_series]
    s = pd.Series(data=list_transformed).astype(dtype="object")
    return s


def list_files(
    *,
    directory: str | Path,
    pattern_startswith: list[str] | tuple[str] | None = None,
    pattern_extension: list[str] | tuple[str] | None = None,
) -> list[Path]:
    """
    Return a list of files within a directory.

    Parameters
    ----------
    directory : str | Path
        The path of the directory.
    pattern_startswith : list[str] | tuple[str] | None = None
        The string for determining if a file starts with this string.
    pattern_extension : list[str] | tuple[str] | None = None
        The file extensions to use for finding files in the path.

    Returns
    -------
    files : list[Path]
        A list of paths.

    Examples
    --------

    >>> import datasense as ds
    >>> files = ds.list_files(directory=path) # doctest: +SKIP

    >>> import datasense as ds
    >>> pattern_extension = [".html", ".HTML"]
    >>> path = "path"
    >>> files = ds.list_files(
    ...     directory=path,
    ...     pattern_extension=pattern_extension
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> pattern_extension = [".html", ".HTML"]
    >>> pattern_startswith = ["job_aid"]
    >>> files = ds.list_files(
    ...     directory=path,
    ...     pattern_extension=pattern_extension,
    ...     pattern_startswith=pattern_startswith
    ... ) # doctest: +SKIP
    """
    directory = Path(directory)
    files = list(directory.iterdir())
    if pattern_extension:
        files = [f for f in files if f.suffix in pattern_extension]
    if pattern_startswith:
        pattern_startswith = tuple(pattern_startswith)
        files = [f for f in files if f.name.startswith(pattern_startswith)]
    return files


def directory_file_print(
    *, directory: str | Path, text: str = "Files in directory"
) -> None:
    """
    Print the files in a path.

    Parameters
    ----------
    directory : str | Path
        The path of the files to print.
    text : str = 'Files in directory'
        The text to print.

    Example
    -------

    >>> import datasense as ds
    >>> path = "path to a directory"
    >>> text = 'your text'
    >>> ds.directory_file_print(
    ...     directory=path,
    ...     text=text
    ... ) # doctest: +SKIP
    """
    directory = Path(directory)
    if text:
        print(f"{text}", directory)
    for x in directory.iterdir():
        print(x.name)
    print()


def delete_list_files(*, files: list[Path] | list[str]) -> None:
    """
    Delete a list of files

    Parameters
    ----------
    files : list[Path] | list[str]
        The list of files from which to remove the path.

    Example
    -------

    >>> import datasense as ds
    >>> ds.delete_list_files(
    ...     files=files,
    ... ) # doctest: +SKIP
    """
    paths = [Path(file) for file in files]
    for path in paths:
        path.unlink()


def print_list_by_item(*, list_to_print: list[str], title: str = None) -> None:
    """
    Print each item of a list.

    Parameters
    ----------
    list_to_print : list[str]
        The list of strings to print.
    title : str = None
        The title to print.

    Example
    -------

    >>> import datasense as ds
    >>> ds.print_list_by_item(list_to_print=my_list_to_print) # doctest: +SKIP
    """
    if title:
        print(title)
    print(*list_to_print, sep="\n")


def ask_directory_path(
    *,
    title: str = "Select directory",
    initialdir: Path = None,
    print_bool: bool = False,
) -> Path:
    """
    Ask user for directory.

    Parameters
    ----------
    title : str = 'Select directory'
        The title of the dialog window.
    initialdir : Path = None
        The directory in which the dialogue starts.
    print_bool : bool = False
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
    >>> path = ds.ask_directory_path(title='your message') # doctest: +SKIP
    """
    rootwindow = Tk()
    path = filedialog.askdirectory(
        parent=rootwindow, initialdir=initialdir, title=title
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
    initialdir: Path | None = None,
    filetypes: list[tuple[str]] = [("xlsx files", ".xlsx .XLSX")],
) -> Path:
    """
    Ask user for the path of the file to open.

    Parameters
    ----------
    title : str
        The title of the dialog window.
    initialdir : Path | None = None
        The directory in which the dialogue starts.
    filetypes : list[tuple[str]] = [('xlsx files', '.xlsx .XLSX')]
        The file types to make visible.

    Returns
    -------
    path: Path
        The path of the file to open.

    Examples
    --------

    >>> from tkinter import filedialog
    >>> from pathlib import Path
    >>> from tkinter import Tk
    >>> import datasense as ds
    >>> path = ds.ask_open_file_name_path(title='message') # doctest: +SKIP

    >>> import datasense as ds
    >>> path = ds.ask_open_file_name_path(
    ...     title='your message',
    ...     filetypes=[('csv files', '.csv .CSV')]
    ... ) # doctest: +SKIP
    """
    rootwindow = Tk()
    rootwindow.withdraw()  # Hide the main window
    path = filedialog.askopenfilename(
        parent=rootwindow,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes,
    )
    path = Path(path)
    rootwindow.destroy()
    return path


def ask_save_as_file_name_path(
    *,
    title: str = "Select file",
    initialdir: Path | None = None,
    filetypes: list[tuple[str]] = [("xlsx files", ".xlsx .XLSX")],
    print_bool: bool = True,
) -> Path:
    """
    Ask user for the path of the file to save as.

    Parameters
    ----------
    title : str = 'Select file'
        The title of the dialog window.
    initialdir : Path | None = None
        The directory in which the dialogue starts.
    filetypes : list[tuple[str]] = [('xlsx files', '.xlsx .XLSX')]
        The list of file types to show in the dialog.
    print_bool : bool = True
        A boolean. Print message if True.

    Returns
    -------
    path: Path
        The path of the file to save as.

    Examples
    --------

    >>> from tkinter import filedialog
    >>> from pathlib import Path
    >>> from tkinter import Tk
    >>> import datasense as ds
    >>> path = ds.ask_save_as_file_name_path(title='message') # doctest: +SKIP

    >>> import datasense as ds
    >>> path = ds.ask_save_as_file_name_path(
    ...     title='your message',
    ...     filetypes=[('csv files', '.csv .CSV')]
    ... ) # doctest: +SKIP
    """
    rootwindow = Tk()
    path = filedialog.asksaveasfilename(
        parent=rootwindow,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes,
    )
    path = Path(path)
    rootwindow.destroy()
    if print_bool:
        print(title)
        print(path)
        print()
    return path


def series_replace_string(
    *, series: pd.Series, find: str, replace: str, regex: bool = True
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
    ...     series=df[column],
    ...     find='find this text',
    ...     replace='replace with this text'
    ... ) # doctest: +SKIP
    """
    series = series.str.replace(pat=find, repl=replace, regex=regex)
    return series


def list_directories(
    *,
    path: str | Path,
    pattern_startswith: list[str] | tuple[str] | None = None,
) -> list[str]:
    """
    Return a list of directories found within a path.

    Parameters
    ----------
    path : str | Path
        The path of the enclosing directory.
    pattern_startswith : list[str] | tuple[str] | None = None
        The string for determining if a directory start with this string.

    Returns
    -------
    directory_list : list[str]
        A list of directories.

    Examples
    --------

    >>> import datasense as ds
    >>> path = "path"
    >>> directory_list = ds.list_directories(path=path) # doctest: +SKIP

    >>> import datasense as ds
    >>> path = "path"
    >>> pattern_startswith = ["job aids"]
    >>> directory_list = ds.list_directories(
    ...     path=path,
    ...     pattern_startswith=pattern_startswith
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> path = "path"
    >>> pattern_startswith = ["job aids", "cheatsheet"]
    >>> directory_list = ds.list_directories(
    ...     path=path,
    ...     pattern_startswith=pattern_startswith
    ... ) # doctest: +SKIP
    """
    path = Path(path)
    directories = [d.name for d in path.iterdir() if d.is_dir()]
    if pattern_startswith:
        pattern_startswith = tuple(pattern_startswith)
        directories = [
            d for d in directories if d.startswith(pattern_startswith)
        ]
    return directories


def remove_punctuation(*, list_dirty: list[str]) -> list[str]:
    """
    Remove punctuation from list items.

    Parameters
    ----------
    list_dirty : list[str]
        The list of items containing punctuation.

    Returns
    -------
    list_clean : list[str]
        The list of items without punctuation.

    Example
    -------

    >>> import datasense as ds
    >>> list_clean = ds.remove_punctuation(list_dirty=list_dirty) \
    ...     # doctest: +SKIP
    """
    list_clean = [
        "".join(
            character
            for character in item
            if character not in string.punctuation
        )
        for item in list_dirty
    ]
    return list_clean


def list_change_case(*, list_dirty: list[str], case: str) -> list[str]:
    """
    Change the case of items in a list.

    Parameters
    ----------
    list_dirty : list[str]
        The list of strings.
    case : str
        The type of case to apply.

    Returns
    -------
    list_clean : list[str]
        The list of strings with case applied.

    Example
    -------

    >>> import datasense as ds
    >>> list_clean = ds.list_change_case(
    ...     list_dirty=list_dirty,
    ...     case='upper'
    ... ) # doctest: +SKIP
    """
    if case == "upper":
        list_clean = [x.upper() for x in list_dirty]
    elif case == "lower":
        list_clean = [x.lower() for x in list_dirty]
    elif case == "title":
        list_clean = [x.title() for x in list_dirty]
    elif case == "capitalize":
        list_clean = [x.capitalize() for x in list_dirty]
    return list_clean


def listone_contains_all_listtwo_substrings(
    *, listone: list[str], listtwo: list[str]
) -> list[str]:
    """
    Return a list of items from one list that contain substrings of items
    from another list.

    Parameters
    ----------
    listone : list[str]
        The list of items in which there are substrings to match from listtwo.
    listwo : list[str]
        The list of items that are substrings of the items in listone.

    Returns
    -------
    matches : list[str]
        The list of items from listone that contain substrings of the items
        from listtwo.

    Example
    -------

    >>> import datasense as ds
    >>> listone = ['prefix-2020-21-CMJG-suffix', 'bobs your uncle']
    >>> listwo = [ 'CMJG', '2020-21']
    >>> matches = ds.listone_contains_all_listtwo_substrings(
    ...     listone=listone,
    ...     listtwo=listtow
    ... ) # doctest: +SKIP
    ['prefix-2020-21-CMJG-suffix']
    """
    matches = [x for x in listone if all(y in x for y in listtwo)]
    return matches


def list_one_list_two_ops(
    *,
    list_one: list[str] | list[int] | list[float],
    list_two: list[str] | list[int] | list[float],
    action: str,
) -> list[str] | list[int] | list[float]:
    """
    Create a list of items comparing two lists:
    - Items unique to list_one
    - Items unique to list_two
    - Items common to both lists (intersection)
    Duplicate items are removed.

    Parameters
    ----------
    list_one : list[str] | list[int] | list[float]
        A list of items.
    list_two : list[str] | list[int] | list[float]
        A list of items.
    action : str
        A string of either "list_one", "list_two", or "intersection".

    Returns
    -------
    list_result : list[str] | list[int] | list[float]
        The list of unique items.

    Examples
    --------

    >>> import datasense as ds
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    ...     list_one=list_one,
    ...     list_two=list_two,
    ...     action="list_one"
    ... ) # doctest: +SKIP
    [1, 2, 3]

    >>> import datasense as ds
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    ...     list_one=list_one,
    ...     list_two=list_two,
    ...     action="list_two"
    ... ) # doctest: +SKIP
    [7, 8, 9]

    >>> import datasense as ds
    >>> list_one = [1, 2, 3, 4, 5, 6]
    >>> list_two = [4, 5, 6, 7, 8, 9]
    >>> list_one_unique = ds.list_one_list_two_ops(
    ...     list_one=list_one,
    ...     list_two=list_two,
    ...     action="intersection"
    ... ) # doctest: +SKIP
    [4, 5, 6]
    """
    match action:
        case "list_one":
            list_result_integers = [
                x
                for x in list_one
                if isinstance(x, int)
                and x not in [y for y in list_two if isinstance(y, int)]
            ]
            list_result_floats = [
                x
                for x in list_one
                if isinstance(x, float)
                and x not in [y for y in list_two if isinstance(y, float)]
            ]
            list_result_strings = [
                x
                for x in list_one
                if isinstance(x, str)
                and x not in [y for y in list_two if isinstance(y, str)]
            ]
            list_result = [
                *list_result_integers,
                *list_result_floats,
                *list_result_strings,
            ]
        case "list_two":
            list_result_integers = [
                x
                for x in list_two
                if isinstance(x, int)
                and x not in [y for y in list_one if isinstance(y, int)]
            ]
            list_result_floats = [
                x
                for x in list_two
                if isinstance(x, float)
                and x not in [y for y in list_one if isinstance(y, float)]
            ]
            list_result_strings = [
                x
                for x in list_two
                if isinstance(x, str)
                and x not in [y for y in list_one if isinstance(y, str)]
            ]
            list_result = [
                *list_result_integers,
                *list_result_floats,
                *list_result_strings,
            ]
        case "intersection":
            list_result_integers = [
                x
                for x in list_one
                if isinstance(x, int)
                and x in [y for y in list_two if isinstance(y, int)]
            ]
            list_result_floats = [
                x
                for x in list_one
                if isinstance(x, float)
                and x in [y for y in list_two if isinstance(y, float)]
            ]
            list_result_strings = [
                x
                for x in list_one
                if isinstance(x, str)
                and x in [y for y in list_two if isinstance(y, str)]
            ]
            list_result = [
                *list_result_integers,
                *list_result_floats,
                *list_result_strings,
            ]
        case _:
            print(
                'Error. Enter "list_one", "list_two", or "intersection" '
                'for parameter "action".'
            )
    return list_result


def parameters_text_replacement(
    *,
    file_name: Path,
    sheet_name: str,
    usecols: list[str],
    text_case: "str" = None,
) -> tuple[tuple[str, str]]:
    """
    Read Excel worksheet.
    Create tuple of text replacement tuples.

    Parameters
    ----------
    file_name : Path
        The path of the Excel file.
    sheet_name : str
        The Excel worksheet.
    usecols : list[str]
        The column names to read.
    case : "str" = None
        Change the case of all items: None, lower, upper.

    Returns
    -------
    text_replacement : tuple[tuple[str, str]]

    Examples
    --------

    >>> import datasense as ds
    >>> path_parameters = Path("bcp_parameters.xlsx")
    >>> usecols = ["old_text", "new_text"]
    >>> sheet_name = "text_replacement"
    >>> text_replacement = parameters(
    ...     file_name=path_parameters,
    ...     sheet_name=sheet_name,
    ...     usecols=usecols
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> path_parameters = Path("bcp_parameters.xlsx")
    >>> usecols = ["old_text", "new_text"]
    >>> sheet_name = "text_replacement"
    >>> text_replacement = parameters(
    ...     file_name=path_parameters,
    ...     sheet_name=sheet_name,
    ...     usecols=usecols,
    ...     case="upper"
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> path_parameters = Path("bcp_parameters.xlsx")
    >>> usecols = ["old_text", "new_text"]
    >>> sheet_name = "text_replacement"
    >>> text_replacement = parameters(
    ...     file_name=path_parameters,
    ...     sheet_name=sheet_name,
    ...     usecols=usecols,
    ...     case="lower"
    ... ) # doctest: +SKIP
    """
    df = read_file(file_name=file_name, sheet_name=sheet_name, usecols=usecols)
    match text_case:
        case "upper":
            tuples = tuple(
                zip(df[usecols[0]].str.upper(), df[usecols[1]].str.upper())
            )
        case "lower":
            tuples = tuple(
                zip(df[usecols[0]].str.lower(), df[usecols[1]].str.lower())
            )
        case _:
            tuples = tuple(
                zip(
                    df[usecols[0]].astype(dtype="object"),
                    df[usecols[1]].astype(dtype="object"),
                )
            )
    # introduced before Python 3.10
    # if text_case == "upper":
    #     tuples = tuple(
    #         zip(df[usecols[0]].str.upper(), df[usecols[1]].str.upper())
    #     )
    # elif text_case == "lower":
    #     tuples = tuple(
    #         zip(df[usecols[0]].str.lower(), df[usecols[1]].str.lower())
    #     )
    # else:
    #     tuples = tuple(
    #         zip(
    #             df[usecols[0]].astype(dtype="object"),
    #             df[usecols[1]].astype(dtype="object")
    #         )
    #     )
    return tuples


def parameters_dict_replacement(
    *, file_name: Path, sheet_name: str, usecols: list[str]
) -> dict[str, str]:
    """
    Read Excel worksheet.
    Create dictionary of text replacement key, value pairs.

    Parameters
    ----------
    file_name : Path
        The path of the Excel file.
    sheet_name : str
        The Excel worksheet.
    usecols : list[str]
        The column names to read.

    Returns
    -------
    text_replacement : dict[str, str]

    Example
    -------

    >>> import datasense as ds
    >>> path_parameters = Path('parameters.xlsx')
    >>> usecols = ['old_text', 'new_text']
    >>> sheet_name = 'text_replacement'
    >>> replacement_dict = ds.parameters_dict_replacement(
    ...     file_name=path_parameters,
    ...     sheet_name=sheet_name,
    ...     usecols=usecols
    ... ) # doctest: +SKIP
    """
    df = read_file(file_name=file_name, sheet_name=sheet_name, usecols=usecols)
    dictionary = dict(zip(df[usecols[0]], df[usecols[1]]))
    return dictionary


def quit_sap_excel() -> None:
    """
    Several applications, Excel in particular, need to be closed otherwise
    they may cause a function to crash.
    """
    for proc in psutil.process_iter():
        if proc.name().lower() == "excel.exe":
            proc.kill()
        if proc.name().lower() == "saplogon.exe":
            proc.kill()


def get_mtime(path: Path) -> float:
    """
    Get the time of last modification of a Path object.

    Parameters
    ----------
    path : Path
        The path of the object.

    Returns:
    --------
    modified_time : float
    """
    modified_time = path.stat().st_mtime
    return modified_time


def file_size(path: Path | str) -> int:
    """
    Determine the file size in bytes.

    Parameters
    ----------
    path : Path | str
        The path of the file.

    Returns
    -------
    size : int
        The file size in bytes

    Example
    -------

    >>> import datasense as ds
    >>> path = "myfile.feather"
    >>> size = ds.file_size(path=path) # doctest: +SKIP
    """
    size = Path(path).stat().st_size
    return size


def mask_outliers(
    df: pd.DataFrame, mask: list[tuple[str, float, float]]
) -> pd.DataFrame:
    """
    Mask outliers within a scikit-learn pipeline.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    mask : list[tuple[str, float, float]]
        The list of mask values.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Example
    -------

    Create a transformer to be used in a scikit-learn pipeline.

    >>> from sklearn.preprocessing import FunctionTransformer
    >>> from sklearn.compose import make_column_transformer
    >>> from sklearn.pipeline import make_pipeline
    >>> from sklearn.impute import SimpleImputer
    >>> import datasense as ds
    >>> mask = [
    ...     ("X1", -10, 10),
    ...     ("X2", -25, 25),
    ...     ("X3", -5, 5),
    ...     ("X4", -7, 7),
    ...     ("X5", -3, 3),
    ...     ("X6", -2, 2),
    ...     ("X7", -13, 13),
    ...     ("X8", -8, 8),
    ...     ("X9", -9, 9),
    ...     ("X10", -10, 10),
    ...     ("X11", -9, 9),
    ...     ("X12", -16, 17),
    ...     ("X13", -20, 23)
    ... ]
    >>> mask = FunctionTransformer(
    ...     mask_outliers,
    ...     kw_args={"mask": mask}
    ... )
    >>> imputer = SimpleImputer()
    >>> imputer_pipeline = make_pipeline(mask, imputer)
    >>> transformer = make_column_transformer(
    ...     (imputer_pipeline, features),
    ...     remainder="drop"
    ... ) # doctest: +SKIP
    """
    for column, lowvalue, highvalue in mask:
        df[column] = df[column].mask(
            cond=(df[column] <= lowvalue) | (df[column] >= highvalue),
            other=pd.NA,
        )
    return pd.DataFrame(data=df)


def delete_empty_rows(
    df: pd.DataFrame, list_columns: list[str] | None = None
) -> pd.DataFrame:
    """
    Delete empty rows

    Notes
    -----
    The following code also works, should dropna not work.

    Delete rows where all elements are missing in all columns.
    df.loc[~(df.shape[1] == df.isna().sum(axis=1)), :]

    Delete rows where all elements are missing, in specific columns.
    df.dropna(how="all", subset=specific_columns)

    Delete rows where all elements are missing, in specific columns.
    df.loc[~((df[look_in_columns].isna().sum(axis=1)) == (len(specific_columns))), :]

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    list_columns : list[str] | None = None
        A list of columns to use to determine if row elements are empty.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.delete_empty_rows(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> list_columns = ["column_x", "column_y", "column_z"]
    >>> df = ds.delete_empty_rows(
    ...     df=df,
    ...     list_columns=list_columns
    ... ) # doctest: +SKIP
    """
    df = df.replace(r"^\s*$", np.NaN, regex=True).replace(
        "", np.NaN, regex=True
    )
    if list_columns:
        df = df.dropna(axis="index", subset=list_columns)
    else:
        df = df.dropna(axis="index", how="all")
    return df


def delete_empty_columns(
    *, df: pd.DataFrame, list_empty_columns: list[str] | None = None
) -> pd.DataFrame:
    """
    Delete empty columns

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    list_empty_columns : list[str] | None = None
        A list of empty columns to delete. The code does not check if these
        columns are empty, but assumes they are.

    TODO: Check that the columns in list_empty_columns are empty.

    Returns
    -------
    df : pd.DataFrame
        The output DataFrame.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.delete_empty_columns(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> list_empty_columns = ["mixed", "nan_none"]
    >>> df = ds.delete_empty_columns(
    ...    df=df,
    ...    list_empty_columns=list_empty_columns
    ... ) # doctest: +SKIP

    Notes
    -----
    The following code also works, should dropna not work.

    Delete columns where all elements are missing.
    df.loc[:, ~df.isna().all()]
    """
    df = df.replace(r"^\s*$", np.NaN, regex=True).replace(
        "", np.NaN, regex=True
    )
    if list_empty_columns:
        if (
            len(list_empty_columns) * df.shape[0]
            == df[list_empty_columns].isna().sum().sum()
        ):
            df = df.drop(labels=list_empty_columns, axis="columns")
        else:
            print(
                "One or more of the columns in the submitted list were not "
                "empty. None of the columns in the submitted list were "
                "deleted."
            )
            print()
    else:
        df = df.dropna(axis="columns", how="all")
    return df


def optimize_float_columns(
    df: pd.DataFrame, float_columns: list[str] = None
) -> pd.DataFrame:
    """
    Downcast float columns

    Parameter
    ---------
    df : pd.DataFrame
        The DataFrame that contains one or more float columns.
    float_columns : list[str] | None = None
        A list of float columns to downcast.

    Returns
    ------
    df : pd.DataFrame
        The DataFrame with all float columns downcast and other columns
        unchanged.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.optimize_float_columns(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> float_columns = ["column A", "column B"]
    >>> df = ds.optimize_float_columns(
    ...     df=df,
    ...     float_columns=float_columns
    ... ) # doctest: +SKIP
    """
    if not float_columns:
        float_columns = find_float_columns(df=df)
    df[float_columns] = df[float_columns].apply(
        pd.to_numeric, downcast="float"
    )
    return df


def optimize_integer_columns(
    df: pd.DataFrame, integer_columns: list[str] | None = None
) -> pd.DataFrame:
    """
    Downcast integer columns

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame that contains one or more integer columns.
    integer_columns : list[str] | None = None
        A list of integer columns to downcast.

    Returns
    ------
    df : pd.DataFrame
        The DataFrame with all integer columns downcast and other columns
        unchanged.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.optimize_integer_columns(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> integer_columns = ["column A", "column B"]
    >>> df = ds.optimize_integer_columns(
    ...     df=df,
    ...     integer_columns=integer_columns
    ... ) # doctest: +SKIP
    """
    if not integer_columns:
        integer_columns = find_integer_columns(df=df)
    df[integer_columns] = df[integer_columns].apply(
        pd.to_numeric, downcast="integer"
    )
    return df


def optimize_object_columns(
    df: pd.DataFrame,
    object_columns: list[str] | None = None,
    fraction_categories: int | None = 0.5,
) -> pd.DataFrame:
    """
    Downcast object columns

    Parameter
    ---------
    df : pd.DataFrame
        The DataFrame that contains one or more integer columns.
    object_columns : list[str] | None = None
        A list of object columns to downcast.
    fraction_categories : int | None = 0.5
        The fraction of categories in an object column.

    Returns
    ------
    df : pd.DataFrame
        The DataFrame with all object columns downcast and other columns
        unchanged.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.optimize_integer_columns(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> fraction_categories = 0.25
    >>> df = ds.optimize_integer_columns(
    ...     df=df,
    ...     fraction_categories = fraction_categories
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> object_columns = ["column A", "column B"]
    >>> df = df.optimize_object_columns(
    ...     df=df,
    ...     object_columns=object_columns
    ... ) # doctest: +SKIP
    """
    if not object_columns:
        object_columns = find_object_columns(df=df)
    for column in object_columns:
        num_unique_values = len(df[column].unique())
        num_total_values = len(df[column])
        if float(num_unique_values) / num_total_values < fraction_categories:
            df[column] = df[column].astype(
                CategoricalDtype(categories=None, ordered=False)
            )
    return df


def optimize_datetime_columns(
    df: pd.DataFrame, datetime_columns: list[str] = None
) -> pd.DataFrame:
    """
    Cast object and datetime columns to pandas datetime. It does not reduce
    memory usage, but enables time-based operations.

    Parameter
    ---------
    df : pd.DataFrame
        The DataFrame that contains one or more datetime columns.
    datetime_columns : list[str] | None = None
        A list of datetime columns to cast.

    Returns
    ------
    df : pd.DataFrame
        The DataFrame with all datetime columns cast and other columns
        unchanged.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.optimize_integer_columns(df=df) # doctest: +SKIP

    >>> import datasense as ds
    >>> integer_columns = ["column A", "column B"]
    >>> df = ds.optimize_integer_columns(
    ...     df=df,
    ...     datetime_columns=datetime_columns
    ... ) # doctest: +SKIP
    """
    if not datetime_columns:
        datetime_columns = find_datetime_columns(df=df)
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])
    return df


def optimize_columns(
    df: pd.DataFrame,
    float_columns: list[str] = None,
    integer_columns: list[str] | None = None,
    datetime_columns: list[str] | None = None,
    object_columns: list[str] | None = None,
    fraction_categories: int | None = 0.5,
) -> pd.DataFrame:
    """
    Downcast float columns

    Parameter
    ----------
    df : pd.DataFrame
        The DataFrame.
    float_columns : list[str] | None = None
        A list of float columns to downcast.
    integer_columns : list[str] | None = None
        A list of integer columns to downcast.
    object_columns : list[str] | None = None
        A list of object columns to downcast.
    fraction_categories : int | None = 0.5
        The fraction of categories in an object column.

    Returns
    ------
    df : pd.DataFrame
        The DataFrame with all columns downcast where possible or requested.

    Examples
    --------

    >>> import datasense as ds
    >>> df = ds.optimize_columns(df=df) # doctest: +SKIP

    If using the default values, it is important to identify object columns
    that should be datetime columns in order to get the correct answer.
    >>> import datasense as ds
    >>> df = ds.optimize_columns(
    ...     df=df,
    ...     datetime_columns=datetime_columns,
    ... ) # doctest: +SKIP

    >>> import datasense as ds
    >>> float_columns = ["column_A", "column_B"]
    >>> integer_columns = ["column_C", "column_D"]
    >>> object_columns = ["column_E", "column_F"]
    >>> df = ds.optimize_columns(
    ...     df=df,
    ...     float_columns=float_columns,
    ...     integer_columns=integer_columns,
    ...     datetime_columns=datetime_columns,
    ...     object_columns=object_columns,
    ...     fraction_categories=0.2
    ... ) # doctest: +SKIP
    """
    df = optimize_float_columns(df=df, float_columns=float_columns)
    df = optimize_integer_columns(df=df, integer_columns=integer_columns)
    df = optimize_datetime_columns(df=df, datetime_columns=datetime_columns)
    df = optimize_object_columns(
        df=df,
        fraction_categories=fraction_categories,
        object_columns=object_columns,
    )
    return df


def series_memory_usage(s: pd.Series, suffix: str = "B") -> str:
    """
    Determine memory usage of a pandas Series

    Parameters
    ----------
    s : pd.Series
        A pandas Series.
    suffix : str = "B"
        The units of the memory usage.

    Returns
    -------
    memory_usage : str
        A string with the value and units of memory usage.

    Example
    -------

    >>> import datasense as ds
    >>> memory_usage = ds.series_memory_usage(
    ...     s=s,
    ...     suffix="B"
    ... ) # doctest: +SKIP
    """
    memory_usage = byte_size(num=s.memory_usage(index=False), suffix="B")
    return memory_usage


def convert_csv_to_feather(
    paths_in: list[str] | Path, paths_out: list[str] | Path
) -> None:
    """
    Convert list of csv files to feather files

    Parameters
    ----------
    paths_in : list[str] | Path
        List of csv file names or paths.
    paths_out : list[str] | Path
        Liat of feather file names or paths.

    Note
    ----
    paths_in and paths_out must be of the same length

    Example
    -------

    One way to create paths_in.

    >>> import datasense as ds
    >>> extension_in = [".csv"]
    >>> paths_in = ds.list_files(
    ...     directory=path_csv,
    ...     pattern_extension=extension_in
    ... ) # doctest: +SKIP

    One way to create paths_out.

    >>> extension_out = ".feather"
    >>> paths_out = [
    ...     Path(
    ...         directory_feather_files,
    ...         paths_in[count].name
    ...     ).with_suffix(extension_out)
    ...     for count, element in enumerate(paths_in)
    ... ] # doctest: +SKIP

    Convert csv to feather.

    >>> import datasense as ds
    >>> ds.convert_csv_to_feather(
    ...     paths_in=paths_in,
    ...     paths_out=paths_out
    ... ) # doctest: +SKIP
    """
    try:
        if len(paths_in) == len(paths_out):
            pass
    except Exception:
        print("Length of paths_in != length of paths_out.")
        sys.exit()
    for path_in, path_out in zip(paths_in, paths_out):
        df = read_file(file_name=path_in)
        save_file(df=df, file_name=path_out)


def print_dictionary_by_key(
    *, dictionary_to_print: dict[str, list[str]], title: str = None
) -> None:
    """
    Print each key, value of a dictionary, one key per line.

    Parameters
    ----------
    dictionary_to_print : dict[str, list[str]]
        The dictionary to print.
    title : str = None
        The title to print.

    Example
    -------

    >>> import datasense as ds
    >>> ds.print_dictionary_by_key(dictionary_to_print=mydict) # doctest: +SKIP
    """
    if title:
        print(title)

    for key, value in dictionary_to_print.items():
        print(str(key) + " : " + str(value))


def convert_seconds_to_hh_mm_ss(
    *, seconds: int = None
) -> tuple[int, int, int]:
    """
    Convert seconds to hours, minutes and seconds.

    Parameters
    ----------
    seconds : int = None
        Time in seconds

    Returns
    -------
        Tuple of (hours, minutes, seconds).

    Example
    ------

    >>> import datasense as ds
    >>> hours_minutes_seconds = ds.convert_seconds_to_hh_mm_ss(seconds=251)
    >>> hours_minutes_seconds
    (0, 4, 11)
    """
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    seconds = int(seconds)
    return (hours, minutes, seconds)


__all__ = (
    "listone_contains_all_listtwo_substrings",
    "number_empty_cells_in_columns",
    "convert_seconds_to_hh_mm_ss",
    "parameters_dict_replacement",
    "parameters_text_replacement",
    "ask_save_as_file_name_path",
    "optimize_datetime_columns",
    "optimize_integer_columns",
    "print_dictionary_by_key",
    "optimize_object_columns",
    "ask_open_file_name_path",
    "convert_csv_to_feather",
    "find_int_float_columns",
    "find_timedelta_columns",
    "optimize_float_columns",
    "create_dataframe_norm",
    "replace_column_values",
    "feature_percent_empty",
    "find_category_columns",
    "find_datetime_columns",
    "list_one_list_two_ops",
    "series_replace_string",
    "delete_empty_columns",
    "directory_file_print",
    "replace_text_numbers",
    "find_integer_columns",
    "find_object_columns",
    "rename_some_columns",
    "series_memory_usage",
    "ask_directory_path",
    "rename_all_columns",
    "find_float_columns",
    "remove_punctuation",
    "print_list_by_item",
    "delete_empty_rows",
    "delete_list_files",
    "find_bool_columns",
    "create_dataframe",
    "create_directory",
    "delete_directory",
    "list_change_case",
    "list_directories",
    "optimize_columns",
    "rename_directory",
    "process_columns",
    "copy_directory",
    "dataframe_info",
    "delete_columns",
    "quit_sap_excel",
    "mask_outliers",
    "process_rows",
    "delete_rows",
    "list_files",
    "byte_size",
    "get_mtime",
    "file_size",
    "read_file",
    "save_file",
    "sort_rows",
)
