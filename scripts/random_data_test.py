#! /usr/bin/env python3
"""
Test for random data
"""

import datasense as ds
import pandas as pd

output_url = 'random_data_test.html'
header_title = 'random_data_test'
header_id = 'random-data-test'


def main():
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    df = ds.create_dataframe()
    print('df.shape')
    print(df.shape)
    print()
    print('df.head()')
    print(df.head())
    print()
    print('df.dtypes')
    print(df.dtypes)
    print()
    print('df.columns')
    print(df.columns)
    print()
    print(help(ds.find_bool_columns))
    print()
    columns_bool = ds.find_bool_columns(df=df)
    print('bool columns')
    print(columns_bool)
    print()
    print(help(ds.find_category_columns))
    print()
    columns_category = ds.find_category_columns(df=df)
    print('category columns')
    print(columns_category)
    print()
    print(help(ds.find_datetime_columns))
    print()
    columns_datetime = ds.find_datetime_columns(df=df)
    print('datetime columns')
    print(columns_datetime)
    print()
    print(help(ds.find_float_columns))
    print()
    columns_float = ds.find_float_columns(df=df)
    print('float columns')
    print(columns_float)
    print()
    print(help(ds.find_int_columns))
    print()
    columns_int = ds.find_int_columns(df=df)
    print('integer columns')
    print(columns_int)
    print()
    print(help(ds.find_int_float_columns))
    print()
    columns_int_float = ds.find_int_float_columns(df=df)
    print('integer, float columns')
    print(columns_int_float)
    print()
    print(help(ds.find_object_columns))
    print()
    columns_object = ds.find_object_columns(df=df)
    print('object columns')
    print(columns_object)
    print()
    print(help(ds.find_timedelta_columns))
    print()
    columns_timedelta = ds.find_timedelta_columns(df=df)
    print('timedelta columns')
    print(columns_timedelta)
    print()
    df = ds.dataframe_info(
        df=df,
        file_in='test'
    )
    print()
    print('df memory usage: ')
    print(
        ds.byte_size(
            num=df.memory_usage(index=True).sum()
        )
    )
    print('</pre>')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
