#! /usr/bin/env python3
"""
Create a Pandas series.

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.

./create_seriese.py > create_seriese.txt
"""

import datasense as ds
import pandas as pd
import numpy as np


def main():
    output_url = 'create_series.html'
    header_title = 'Create Pandas Series'
    header_id = 'create-pandas-series'
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    my_list_1 = [1, 2, np.nan, 4, 5]
    print('my_list_1:')
    print(my_list_1)
    my_list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print('my_list_2:')
    print(my_list_2)
    my_list_3 = ['a', 'b', 'c', '', 'e']
    print('my_list_3:')
    print(my_list_3)
    my_index = [1, 2, 3, 4, 5]
    s1 = pd.Series(data=my_list_1)
    print('s1:')
    print(s1)
    s2 = pd.Series(
        data=my_list_1,
        name='A'
    )
    print('s2:')
    print(s2)
    s3 = pd.Series(
        data=my_list_1,
        index=my_index,
        dtype='Int64',
        name='A'
    )
    print('s3:')
    print(s3)
    s4 = pd.Series(
        data=my_list_2,
        index=my_index,
        dtype='float64',
        name='B'
    )
    print('s4:')
    print(s4)
    s5 = pd.Series(
        data=my_list_3,
        index=my_index,
        dtype='str',
        name='C'
    )
    print('s5:')
    print(s5)
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
