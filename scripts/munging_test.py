#! /usr/bin/env python3
"""
Test functions in munging.py
"""

from typing import Callable
from datetime import datetime
import time

import datasense as ds
import pandas as pd
import numpy as np

output_url = 'test_munging.html'
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
    print('--------------------------')
    print('test find_float_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_float = ds.find_float_columns(df=df)
    print(columns_float)
    print('--------------------------')
    print('test find_int_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_int = ds.find_int_columns(df=df)
    print(columns_int)
    print('--------------------------')
    print('test find_int_float_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_int_float = ds.find_int_float_columns(df=df)
    print(columns_int_float)
    print('--------------------------')
    print('test find_object_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_object = ds.find_object_columns(df=df)
    print(columns_object)
    print('--------------------------')
    print('test find_timedelta_columns')
    print('test example')
    df = ds.create_dataframe()
    columns_timedelta = ds.find_timedelta_columns(df=df)
    print(columns_timedelta)
    print('--------------------------')
    print('test number_empty_cells_in_columns')
    print('test example')
    df = pd.DataFrame({
        'X': [25.0, 24.0, 35.5, np.nan, 23.1],
        'Y': [27, 24, np.nan, 23, np.nan],
        'Z': ['a', 'b', np.nan, 'd', 'e']
    })
    empty_cells = ds.number_empty_cells_in_columns(df=df)
    print(empty_cells)
    print('--------------------------')
    print('test process_columns')
    print('test example')
    df = ds.create_dataframe()
    df, columns_in_count, columns_non_empty_count, columns_empty_count,\
        columns_empty_list, columns_non_empty_list, columns_bool_list,\
        columns_bool_count, columns_float_list, columns_float_count,\
        columns_integer_list, columns_integer_count,\
        columns_datetime_list, columns_datetime_count,\
        columns_object_list, columns_object_count, columns_category_list,\
        columns_category_count, columns_timedelta_list,\
        columns_timedelta_count = ds.process_columns(df=df)
    print('columns_in_count       :', columns_in_count)
    print('columns_non_empty_count:', columns_non_empty_count)
    print('columns_empty_count    :', columns_empty_count)
    print('columns_empty_list     :', columns_empty_list)
    print('columns_non_empty_list :', columns_non_empty_list)
    print('columns_bool_list      :', columns_bool_list)
    print('columns_bool_count     :', columns_bool_count)
    print('columns_float_list     :', columns_float_list)
    print('columns_float_count    :', columns_float_count)
    print('columns_integer_list   :', columns_integer_list)
    print('columns_integer_count  :', columns_integer_count)
    print('columns_datetime_list  :', columns_datetime_list)
    print('columns_datetime_count :', columns_datetime_count)
    print('columns_object_list    :', columns_object_list)
    print('columns_object_count   :', columns_object_count)
    print('columns_category_list  :', columns_category_list)
    print('columns_category_count :', columns_category_count)
    print('columns_timedelta_list :', columns_timedelta_list)
    print('columns_timedelta_count:', columns_timedelta_count)
    print('--------------------------')
    print('test process_rows')
    print('test example')
    df = ds.create_dataframe()
    df, rows_in_count, rows_out_count, rows_empty_count = ds.process_rows(df)
    print('rows_in_count   :', rows_in_count)
    print('rows_out_count  :', rows_out_count)
    print('rows_empty_count:', rows_empty_count)
    print('--------------------------')
    print('test save_file example 1')
    print('test example')
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name='x_y.csv'
    )
    print('--------------------------')
    print('test save_file example 2')
    print('test example')
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name='x_y.csv',
        index=True,
        index_label='myindex'
    )
    print('--------------------------')
    print('test save_file example 3')
    print('test example')
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name='x_y.xlsx'
    )
    print('--------------------------')
    print('test save_file example 4')
    print('test example')
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name='x_y.xlsx',
        index=True,
        index_label='myindex'
    )
    print('--------------------------')
    print('test byte_size')
    print('test example')
    df = ds.create_dataframe()
    print(
        ds.byte_size(
            num=df.memory_usage(index=True).sum()
        )
    )
    print('--------------------------')
    print('test read_file')
    print('test example 1')
    my_file = 'myfile.csv'
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name=my_file
    )
    df = ds.read_file(file_name=my_file)
    ds.dataframe_info(
        df=df,
        file_in=my_file)
    stop_time = time.time()
    print('--------------------------')
    print('test read_file')
    print('test example 2')
    file_name = 'myfile.csv'
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
    ds.dataframe_info(
        df=df,
        file_in=my_file
    )
    print('--------------------------')
    print('test read_file')
    print('test example 3')
    file_name = 'myfile.csv'
    df = ds.create_dataframe()
    ds.save_file(
        df=df,
        file_name=file_name
    )
    column_names_dict = {
        'a': 'A',
        'b': 'B',
        'c': 'C',
        'd': 'D',
        'i': 'I',
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
    df = ds.read_file(
        file_name=file_name,
        column_names_dict=column_names_dict,
        index_columns=index_columns,
        date_parser=date_parser(),
        parse_dates=parse_dates,
        time_delta_columns=time_delta_columns,
        category_columns=category_columns,
        integer_columns=integer_columns
    )
    ds.dataframe_info(
        df=df,
        file_in=file_name
    )
    print('--------------------------')
    print('test read_file')
    print('test example 4')
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
