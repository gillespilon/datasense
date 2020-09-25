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
            'x': ds.random_data(distribution='norm'),
            'y': ds.random_data(distribution='randint'),
            'z': ds.random_data(distribution='uniform'),
            't': ds.datetime_data()
        }
    )
    print('df.head()', df.head())
    print()
    print('df.shape', df.shape)
    print()
    columns_int_float = ds.find_int_float_columns(
        df=df
    )
    print('columns_int_float', columns_int_float)
    print('</pre>')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
