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
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    print('<pre>')
    df = pd.DataFrame(
        {
            'b': ds.random_data(
                distribution='randint',
                low=0,
                high=2
            ).astype(dtype='bool'),
            'x': ds.random_data(distribution='norm'),
            'y': ds.random_data(distribution='randint'),
            'z': ds.random_data(distribution='uniform'),
            't': ds.datetime_data()
        }
    )
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
    df = ds.dataframe_info(
        df=df,
        filein='test'
    )
    print('</pre>')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
