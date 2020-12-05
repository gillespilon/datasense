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
#     output_url = 'create_series.html'
#     header_title = 'Create Pandas Series'
#     header_id = 'create-pandas-series'
#     original_stdout = ds.html_begin(
#         output_url=output_url,
#         header_title=header_title,
#         header_id=header_id
#     )
    my_list_1 = [1, 2, np.nan, 4, 5]
    print('my_list_1:')
    print(my_list_1)
    my_dict_1 = {'A': my_list_1}
    my_list_2 = [6.0, np.nan, 8.0, 9.0, 10.0]
    print('my_dict_1:')
    print(my_dict_1)
    print('my_list_2:')
    print(my_list_2)
    my_dict_2 = {'B': my_list_2}
    print('my_dict_2:')
    print(my_dict_2)
    my_list_3 = ['a', 'b', 'c', '', 'e']
    print('my_list_3:')
    print(my_list_3)
    my_dict_3 = {'C': my_list_3}
    print('my_dict_3:')
    print(my_dict_3)
    my_dict_4 = {**my_dict_1, **my_dict_2, **my_dict_3}
    print('my_dict_4:')
    print(my_dict_4)
    my_index = [1, 2, 3, 4, 5]
    convert_dict = {'A': 'Int64', 'B': 'float64', 'C': 'str'}
    df1 = pd.DataFrame(
        data={
            **{'A': my_list_1},
            **{'B': my_list_2},
            **{'C': my_list_3},
        }
    )
    print('df1:')
    print(df1)
    print(df1.dtypes)
    ds.save_file(
        df=df1,
        file_name='df1.csv'
    )
    df2 = pd.DataFrame(data=my_dict_4)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    ds.save_file(
        df=df2,
        file_name='df2.csv'
    )
    df2 = df2.astype(dtype=convert_dict)
    print('df2:')
    print(df2)
    print(df2.dtypes)
    ds.save_file(
        df=df2,
        file_name='df2.csv'
    )
    df3 = pd.DataFrame(data=my_dict_4).astype(dtype=convert_dict)
    print('df3:')
    print(df3)
    print(df3.dtypes)
    df4 = pd.DataFrame(
        data={
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
        }
    )
    print('df4:')
    print(df4)
    print(df4.dtypes)
    df4 = pd.DataFrame(
        data={
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
        }
    ).astype(dtype=convert_dict)
    print('df4:')
    print(df4)
    print(df4.dtypes)
    my_dict_5 = {
            'A': [1, 2, np.nan, 4, 5],
            'B': [6.0, np.nan, 8.0, 9.0, 10.0],
            'C': ['a', 'b', 'c', '', 'e']
    }
    df5 = pd.DataFrame(data=my_dict_5).astype(dtype=convert_dict)
    print('df5:')
    print(df5)
    print(df5.dtypes)
    df6 = pd.DataFrame(
        data=my_dict_5,
        index=my_index
    ).astype(dtype=convert_dict)
    print('df6:')
    print(df6)
    print(df6.dtypes)
#     ds.html_end(
#         original_stdout=original_stdout,
#         output_url=output_url
#     )


if __name__ == '__main__':
    main()
