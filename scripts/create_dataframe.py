#! /usr/bin/env python3
"""
Create a Pandas dataframe.

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.

./create_dataframe.py > create_dataframe.txt
"""

import datasense as ds
import pandas as pd
import numpy as np


def main():
    print('Create Pandas dataframe')
    print()
    my_list_1 = [1, 2, np.nan, 4, 5]
    print('my_list_1:')
    print(my_list_1)
    print()
    my_dict_1 = {'A': my_list_1}
    print('my_dict_1:')
    print(my_dict_1)
    print()
    my_list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print('my_list_2:')
    print(my_list_2)
    print()
    my_dict_2 = {'B': my_list_2}
    print('my_dict_2:')
    print(my_dict_2)
    print()
    my_list_3 = ['a', 'b', 'c', '', 'e']
    print('my_list_3:')
    print(my_list_3)
    print()
    my_dict_3 = {'C': my_list_3}
    print('my_dict_3:')
    print(my_dict_3)
    print()
    my_dict_4 = {**my_dict_1, **my_dict_2, **my_dict_3}
    print('my_dict_4:')
    print(my_dict_4)
    print()
    my_index = [1, 2, 3, 4, 5]
    convert_dict = {'A': 'Int64', 'B': 'float64', 'C': 'str'}
    df1 = pd.DataFrame(
        data={
            **{'A': my_list_1},
            **{'B': my_list_2},
            **{'C': my_list_3},
        }
    ).astype(dtype=convert_dict)
    print('df1:')
    print(df1)
    print(df1.dtypes)
    print()
    df2 = pd.DataFrame(data=my_dict_4).astype(dtype=convert_dict)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    print()
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
    my_dict_4 = {
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
    }
    df4 = pd.DataFrame(data=my_dict_4).astype(dtype=convert_dict)
    print('df4:')
    print(df4)
    print(df4.dtypes)
    print()
    df5 = pd.DataFrame(
        data=my_dict_4,
        index=my_index
    ).astype(dtype=convert_dict)
    print('df5:')
    print(df5)
    print(df5.dtypes)


if __name__ == '__main__':
    main()
