#! /usr/bin/env python3
"""
Pandas read_csv exploration
"""

from typing import Callable, Dict, List, Optional
from datetime import datetime
from math import trunc
import time

from pandas.api.types import CategoricalDtype
import datasense as ds
import pandas as pd

output_url = 'pandas_read_csv_exploration.html'
header_title = 'pandas_read_csv_exploration'
header_id = 'pandas-read-csv-exploration'
file_name='myfile.csv'


def main():
    start_time = time.time()
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
    help(ds.read_file)
    print()
    df = create_dataframe()
    print('Create dataframe')
    print(df.head())
    print(df.dtypes)
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
    parse_dates = ['t', 'u']
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
    data = ds.read_file(
        file_name=file_name,
        column_names_dict=column_names_dict,
        index_columns=index_columns,
        date_time_columns=date_time_columns,
        parse_dates=parse_dates,
        date_parser=date_parser(),
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
    stop_time = time.time()
    ds.page_break()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        read_file_names=file_name,
        save_file_names=file_name
    )
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


def date_parser() -> Callable:
    return lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    main()
