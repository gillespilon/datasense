#! /usr/bin/env python3
"""
Pandas read file exploration
"""

from typing import Callable
from datetime import datetime
import time

import datasense as ds
import pandas as pd

output_url = 'pandas_read_file_exploration.html'
header_title = 'pandas_read_file_exploration'
header_id = 'pandas-read-file-exploration'
file_name = 'myfile.csv'


def main():
    start_time = time.time()
    pd.options.display.width = 120
    pd.options.display.max_columns = 100
    pd.options.display.max_rows = 100
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    help(ds.read_file)
    print()
    df = ds.create_dataframe()
    print('Create dataframe')
    print(df.head())
    print(df.dtypes)
    print()
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
    # Read a csv file. There is no guarante thee column dtypes will be correct.
    data = ds.read_file(file_name=file_name)
    print('Example 1. The dtypes are not correct.')
    print(data.head())
    print(data.dtypes)
    print()
    ds.dataframe_info(
        df=data,
        file_in=file_name
    )
    # Example 2
    # Read a csv file. Ensure the dtypes of datetime columns.
    parse_dates = ['t', 'u']
    data = ds.read_file(
        file_name=file_name,
        parse_dates=parse_dates
    )
    print(
        'Example 2. Ensure the dtypes of datetime columns.'
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print()
    ds.dataframe_info(
        df=data,
        file_in=file_name
    )
    # Example 3
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
    print(
        'Example 3. Ensure the column dtypes are correct. Rename the columns.'
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print()
    print('index', data.index.name, 'dtype:', data.index.dtype)
    print()
    ds.dataframe_info(
        df=data,
        file_in=file_name
    )
    # Example 4
    # Read an ods file.
    data = ds.read_file(
        file_name='test_file.ods',
        parse_dates=['dates', 'dateandtimes']
    )
    print(
        'Example 4. Read an ods file.'
    )
    print(data.head(10))
    print()
    print('column dtypes')
    print(data.dtypes)
    print()
    ds.dataframe_info(
        df=data,
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
