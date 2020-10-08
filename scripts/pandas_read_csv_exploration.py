#! /usr/bin/env python3
"""
Pandas read_csv exploration
"""

from typing import Dict, List, Optional
from math import trunc

from pandas.api.types import CategoricalDtype
import datasense as ds
import pandas as pd

output_url = 'pandas_read_csv_exploration.html'
header_title = 'pandas_read_csv_exploration'
header_id = 'pandas-read-csv-exploration'


def main():
    pd.set_option(
        'display.width',
        120
    )
    pd.set_option(
        'display.max_columns',
        100
    )
    pd.set_option(
        'display.max_rows',
        100
    )
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    help(read_file)
    print()
    df = create_dataframe()
    print('Create dataframe')
    print(df.head())
    print(df.dtypes)
    print()
    save_dataframe(df=df)
    # Example 1
    # Read a csv file. There is no guarante thee column dtypes will be correct.
    data = read_file(file_name='myfile.csv')
    print('Example 1. The dtypes are not correct.')
    print(data.head())
    print(data.dtypes)
    print()
    # Example 2
    # Read a csv file. Ensure the dtypes of columns. Rename the columns.
    column_names_dict = {
        'a': 'A',
        'b': 'B',
        'c': 'C',
        'd': 'D',
        'i': 'I',
        'r': 'R',
        'r': 'R',
        's': 'S',
        't': 'T',
        'u': 'U',
        'y': 'Y',
        'x': 'X',
        'z': 'Z'
    }
    index_columns = ['Y']
    date_parser = '%Y-%m-%d %H:%M:%S'
    date_time_columns = ['T', 'U']
    time_delta_columns = ['D']
    category_columns = ['C']
    # converters = {'a': lambda x: trunc(float(x))}
    integer_columns = ['A', 'I']
    float_columns = ['X']
    boolean_columns = ['R']
    object_columns = ['Z']
    sort_columns = ['I', 'A']
    sort_columns_bool = [True, False]
    data = read_file(
        file_name='myfile.csv',
        column_names_dict=column_names_dict,
        index_columns=index_columns,
        date_time_columns=date_time_columns,
        date_parser=date_parser,
        time_delta_columns=time_delta_columns,
        category_columns=category_columns,
        # converters=converters,
        integer_columns=integer_columns,
        float_columns=float_columns,
        boolean_columns=boolean_columns,
        object_columns=object_columns,
        sort_columns=sort_columns,
        sort_columns_bool=sort_columns_bool
    )
    print(
        'Example 2. Ensure the column dtypes are correct. Rename the columns.'
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print()
    print('index', data.index.name, 'dtype:', data.index.dtype)
    print('</pre>')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


def create_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            'a': ds.random_data(
                distribution='uniform',
                size=42,
                loc=13,
                scale=70
            ),
            'b': ds.random_data(distribution='bool'),
            'c': ds.random_data(distribution='categories'),
            'd': ds.timedelta_data(),
            'i': ds.random_data(
                distribution='uniform',
                size=42,
                loc=13,
                scale=70
            ),
            'r': ds.random_data(
                distribution='strings',
                strings=['0', '1']
            ),
            's': ds.random_data(distribution='strings'),
            't': ds.datetime_data(),
            'u': ds.datetime_data(),
            'x': ds.random_data(distribution='norm'),
            'y': ds.random_data(distribution='randint'),
            'z': ds.random_data(distribution='uniform')
        }
    )
    return df


def save_dataframe(df) -> None:
    df.to_csv(
        'myfile.csv',
        index=False
    )


def read_file(
    file_name: str,
    *,
    column_names_dict: Optional[Dict[str, str]] = {},
    index_columns: Optional[List[str]] = [],
    converters: Optional[dict] = None,
    parse_dates: Optional[List[str]] = None,
    date_parser: Optional[str] = None,
    date_time_columns: Optional[List[str]] = [],
    time_delta_columns: Optional[List[str]] = [],
    category_columns: Optional[List[str]] = [],
    integer_columns: Optional[List[str]] = [],
    float_columns: Optional[List[str]] = [],
    boolean_columns: Optional[List[str]] = [],
    object_columns: Optional[List[str]] = [],
    sort_columns: Optional[List[str]] = [],
    sort_columns_bool: Optional[List[bool]] = []
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
    parse_dates : Optional[List[str]] = None,
        The columns to use to parse date and time.
    date_parser : Optional[str] = None,
        The string to use for parsing date and time.
    date_time_columns : Optional[List[str]] = [],
        The columns to change to dtype datetime.
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

    Returns
    -------
    df : pd.DataFrame
        The dataframe created from the external file.

    Examples
    --------
    Example 1
    Read a csv file. There is no guarante thee column dtypes will be correct.
    >>> data = read_file(file_name='myfile.csv')

    Example 2
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
    >>> data = read_file(
    >>>     file_name='myfile.csv',
    >>>     column_names_dict=column_names_dict,
    >>>     index_columns=index_columns,
    >>>     date_time_columns=date_time_columns,
    >>>     date_parser=date_parser,
    >>>     time_delta_columns=time_delta_columns,
    >>>     category_columns=category_columns,
    >>>     integer_columns=integer_columns
    >>> )
    """
    df = pd.read_csv(
        file_name,
        converters=converters,
        parse_dates=parse_dates,
        date_parser=date_parser
    )
    if column_names_dict:
        df = df.rename(columns=column_names_dict)
    if index_columns:
        df = df.set_index(index_columns)
    for column in category_columns:
        df[column] = df[column].astype(CategoricalDtype())
    for column in date_time_columns:
        df[column] = pd.to_datetime(
            df[column],
            format=date_parser
        )
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
    return df


if __name__ == '__main__':
    main()
