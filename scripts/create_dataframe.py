#! /usr/bin/env python3
"""
Create a pandas dataframe in different ways

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.
"""

import datasense as ds
import pandas as pd
import numpy as np


def main():
    header_title = 'Create dataframe'
    header_id = 'create-dataframe'
    output_url = 'create_dataframe.html'
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('Create a pandas dataframe in different ways')
    print()
    print('Create lists and dictionaries to use in the dataframe')
    print()
    list_1 = [1, 2, np.nan, 4, 5]
    print('list_1 of Int64')
    print(list_1)
    dict_1 = {'A': list_1}
    print('dict_1')
    print(dict_1)
    list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print()
    print('list_2 of float64')
    print(list_2)
    dict_2 = {'B': list_2}
    print('dict_2:')
    print(dict_2)
    list_3 = ['a', 'b', 'c', '', 'e']
    print()
    print('list_3 of str')
    print(list_3)
    dict_3 = {'C': list_3}
    print('dict_3:')
    print(dict_3)
    list_of_lists = [list_1, list_2, list_3]
    print()
    print('list of lists:')
    print(list_of_lists)
    dict_of_lists = {**dict_1, **dict_2, **dict_3}
    print()
    print('dict_of_lists:')
    print(dict_of_lists)
    print()
    dict_types = {'A': 'Int64', 'B': 'float64', 'C': 'str'}
    # Method one
    df1 = pd.DataFrame(
        data={
            **{'A': list_1},
            **{'B': list_2},
            **{'C': list_3},
        }
    ).astype(dtype=dict_types)
    print('Method one')
    print(df1)
    print(df1.dtypes)
    print()
    # Method two
    df2 = pd.DataFrame(data=dict_of_lists).astype(dtype=dict_types)
    print('Method two')
    print(df2)
    print(df2.dtypes)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    print()
    # Method three
    df3 = pd.DataFrame(
        data={
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
        }
    ).astype(dtype=dict_types)
    print('Method three')
    print(df3)
    print(df3.dtypes)
    print()
    # Method four
    dict_of_lists = {
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
    }
    df4 = pd.DataFrame(data=dict_of_lists).astype(dtype=dict_types)
    print('Method four')
    print(df4)
    print(df4.dtypes)
    print()
    # Method five
    df5 = pd.DataFrame(
        data=dict_of_lists,
    ).astype(dtype=dict_types)
    print('Method five')
    print(df5)
    print(df5.dtypes)
    print()
    # Method six
    dict_of_lists = {
        'A': list_1,
        'B': list_2,
        'C': list_3
    }
    df6 = pd.DataFrame(data=dict_of_lists).astype(dtype=dict_types)
    print('Method six')
    print(df6)
    print(df6.dtypes)
    print()
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
