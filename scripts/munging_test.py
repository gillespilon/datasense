#! /usr/bin/env python3
"""
Test functions in munging.py
"""

from typing import Callable
from datetime import datetime
import time

import datasense as ds
import pandas as pd

output_url = 'test munging.html'
header_title = 'test_munging'
header_id = 'test-munging'
file_name = 'test_munging.csv'


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
    print('--------------------------')
    print('test dataframe_info')
    print('test example 1')
    my_file = 'myfile.csv'
    df = ds.read_file(my_file)
    df = ds.dataframe_info(
        df=df,
        file_in=my_file
    )
    print('--------------------------')
    print('test dataframe_info')
    print('test example 2')
    df = ds.create_dataframe()
    df = ds.dataframe_info(
        df=df,
        file_in='df'
    )
    print('--------------------------')
    print('test find_bool_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_bool = ds.find_bool_columns(df=df)
    print(columns_bool)
    print('--------------------------')
    print('test find_category_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_category = ds.find_category_columns(df=df)
    print(columns_category)
    print('--------------------------')
    print('test find_datetime_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_datetime = ds.find_datetime_columns(df=df)
    print(columns_datetime)
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
