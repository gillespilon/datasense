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
    print('Create Pandas dataframe')
    print()
    list_1 = [1, 2, np.nan, 4, 5]
    print('list_1:')
    print(list_1)
    print()
    dict_1 = {'A': list_1}
    print('dict_1:')
    print(dict_1)
    print()
    list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print('list_2:')
    print(list_2)
    print()
    dict_2 = {'B': list_2}
    print('dict_2:')
    print(dict_2)
    print()
    list_3 = ['a', 'b', 'c', '', 'e']
    print('list_3:')
    print(list_3)
    print()
    dict_3 = {'C': list_3}
    print('dict_3:')
    print(dict_3)
    print()
    dict_of_lists = {**dict_1, **dict_2, **dict_3}
    print('dict_of_lists:')
    print(dict_of_lists)
    print()
    convert_dict = {'A': 'Int64', 'B': 'float64', 'C': 'str'}
    df1 = pd.DataFrame(
        data={
            **{'A': list_1},
            **{'B': list_2},
            **{'C': list_3},
        }
    ).astype(dtype=convert_dict)
    print('df1:')
    print(df1)
    print(df1.dtypes)
    print()
    df2 = pd.DataFrame(data=dict_of_lists).astype(dtype=convert_dict)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    print()
    # This is my preferred way.
    df3 = pd.DataFrame(
        data={
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
        }
    ).astype(dtype=convert_dict)
    print('df3:')
    print(df3)
    print(df3.dtypes)
    print()
    dict_of_lists = {
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
    }
    df4 = pd.DataFrame(data=dict_of_lists).astype(dtype=convert_dict)
    print('df4:')
    print(df4)
    print(df4.dtypes)
    print()
    df5 = pd.DataFrame(
        data=dict_of_lists,
    ).astype(dtype=convert_dict)
    print('df5:')
    print(df5)
    print(df5.dtypes)
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
