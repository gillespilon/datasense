#! /usr/bin/env python3
"""
Pandas read file exploration
"""

from datetime import datetime
from typing import Callable
import time

import datasense as ds
import pandas as pd

output_url = 'pandas_read_file_exploration.html'
header_title = 'pandas_read_file_exploration'
header_id = 'pandas-read-file-exploration'
file_name = 'myfile.csv'


def main():
    start_time = time.time()
    pd.options.display.max_columns = 100
    pd.options.display.max_rows = 100
    pd.options.display.width = 120
    file_name = 'myfile.csv'
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    help(ds.read_file)
    print()
    print('Create dataframe')
    df = ds.create_dataframe()
    print(df.head())
    print(df.columns)
    print(df.dtypes)
    ds.dataframe_info(
        df=df,
        file_in=file_name
    )
    help(ds.save_file)
    print()
    ds.save_file(
        df=df,
        file_name=file_name
    )
    # Example 1
    # Read a csv file. There is no guarantee the column dtypes will be correct.
    print('Example 1. Only [a, i, s, x, z] have the correct dtypes.')
    df = ds.read_file(file_name=file_name)
    print(df.dtypes)
    print()
    # Example 2
    # Read a csv file. Ensure the dtypes of datetime columns.
    print('Example 2. Ensure the dtypes of datetime columns.')
    parse_dates = ['t', 'u']
    df = ds.read_file(
        file_name=file_name,
        parse_dates=parse_dates
    )
    print(df.dtypes)
    print()
    # Example 3
    # Read a csv file. Ensure the dtypes of columns; not timedelta, datetime.
    print('Example 3. Ensure the dtypes of cols; not timedelta, datetime.')
    convert_dict = {
        'a': 'float64',
        'b': 'boolean',
        'c': 'category',
        'i': 'float64',
        'r': 'str',
        's': 'str',
        'x': 'float64',
        'y': 'Int64',
        'z': 'float64'
    }
    df = ds.read_file(
        file_name=file_name,
        dtype=convert_dict
    )
    print(df.dtypes)
    print()
    # Example 4
    # Read a csv file. Ensure the dtypes of columns. Rename the columns.
    print(
        'Example 4. Ensure the column dtypes are correct. Rename the columns.'
    )
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
        'x': 'X',
        'y': 'Y',
        'z': 'Z'
    }
    index_columns = ['Y']
    parse_dates = ['t', 'u']
    time_delta_columns = ['D']
    category_columns = ['C']
    integer_columns = ['A', 'I']
    float_columns = ['X']
    boolean_columns = ['R']
    object_columns = ['Z']
    sort_columns = ['I', 'A']
    sort_columns_bool = [True, False]
    data = ds.read_file(
        file_name=file_name,
        column_names_dict=column_names_dict,
        index_columns=index_columns,
        parse_dates=parse_dates,
        date_parser=date_parser(),
        time_delta_columns=time_delta_columns,
        category_columns=category_columns,
        integer_columns=integer_columns,
        float_columns=float_columns,
        boolean_columns=boolean_columns,
        object_columns=object_columns,
        sort_columns=sort_columns,
        sort_columns_bool=sort_columns_bool
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print(data.info(verbose=True))
    print()
    print('index', data.index.name, 'dtype:', data.index.dtype)
    print()
    ds.dataframe_info(
        df=data,
        file_in=file_name
    )
    # Example 5
    # Read an ods file.
    file_name = 'myfile.ods'
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name=file_name
    )
    parse_dates = ['t', 'u']
    df = ds.read_file(
        file_name=file_name,
        parse_dates=parse_dates
    )
    print(
        'Example 5. Read an ods file.'
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print(data.info(verbose=True))
    print()
    ds.dataframe_info(
        df=data,
        file_in=file_name
    )
    # Example 6
    # Read an xlsx file.
    df = ds.read_file(file_name=file_name)
    file_name = 'myfile.xlsx'
    sheet_name = 'raw_data'
    ds.save_file(
        df=df,
        file_name=file_name,
        sheet_name=sheet_name
    )
    df = ds.read_file(
        file_name=file_name,
        sheet_name=sheet_name
    )
    ds.dataframe_info(
        df=df,
        file_in=file_name
    )
    stop_time = time.time()
    ds.page_break()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        read_file_names=file_name,
        save_file_names=file_name
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def date_parser() -> Callable:
    """
    Date parser callable function

    Returns
    -------
    Parsed date and time.

    Example
    >>> date_parser=date_parser()
    """
    return lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    main()
