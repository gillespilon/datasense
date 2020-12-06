#! /usr/bin/env python3
"""
Create a Pandas series.

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.

./create_seriese.py > create_seriese.txt
"""

import pandas as pd
import numpy as np


def main():
    print('Create Pandas series')
    print()
    my_list_1 = [1, 2, np.nan, 4, 5]
    print('my_list_1:')
    print(my_list_1)
    print()
    my_list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print('my_list_2:')
    print(my_list_2)
    print()
    my_list_1 = [1, 2, np.nan, 4, 5]
    my_list_3 = ['a', 'b', 'c', '', 'e']
    print('my_list_3:')
    print(my_list_3)
    print()
    my_list_1 = [1, 2, np.nan, 4, 5]
    my_index = [1, 2, 3, 4, 5]
    s1 = pd.Series(
        data=my_list_1,
        name='A'
    ).astype(dtype='Int64')
    print('s1:')
    print(s1)
    print()
    s2 = pd.Series(
        data=my_list_2,
        index=my_index,
        dtype='float64',
        name='B'
    ).astype(dtype='float64')
    print('s2:')
    print(s2)
    print()
    s3 = pd.Series(
        data=my_list_3,
        index=my_index,
        dtype='str',
        name='C'
    ).astype(dtype='str')
    print('s3:')
    print(s3)


if __name__ == '__main__':
    main()
