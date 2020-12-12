#! /usr/bin/env python3
"""
Create a Pandas series.

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.

./create_series.py > create_series.txt
"""

import pandas as pd
import numpy as np

import datasense as ds


def main():
    print('Create Pandas series')
    print()
    print('uniform distribution, dtype: float, series_a')
    # series_a = ds.random_data(
    #     distribution='uniform',
    #     size=7,
    #     loc=13,
    #     scale=70
    # ).rename('A')
    list_a = [14.758, 78.956, np.nan, 57.361, 39.018, 75.764, 65.869]
    print(list_a)
    series_a = pd.Series(
        data=list_a,
        name='A'
    ).astype(dtype='float64')
    print(series_a)
    print()
    print('boolean distribution, dtype: boolean (nullable), list_b:')
    # series_b = ds.random_data(
    #     distribution='bool',
    #     size=7
    # )
    list_b = [False, True, np.nan, False, True, True, False]
    print(list_b)
    series_b = pd.Series(
        data=list_b,
        name='B'
    ).astype(dtype='boolean')
    print(series_b)
    print()
    print('category, dtype: category, list_c:')
    # series_c = ds.random_data(
    #     distribution='categories,
    #     size=7'
    # )
    # print(series_c.head())
    list_c = ['small', 'medium', '', 'medium', 'large', 'large', 'small']
    series_c = pd.Series(
        data=list_c,
        name='C'
    ).astype(dtype='category')
    print(series_c)
    print()
    print('timedelta distribution, dtype: timedelta64[ns], series_d')
    series_d = ds.random_data(
        distribution='timedelta',
        size=7
    ).rename('D')
    print(series_d)
    print()
    print('strings, str, list_s:')
    # series_s = ds.random_data(
    #     distribution='strings',
    #     size=7
    # ).rename('S')
    list_s = ['male', 'female', '', 'male', 'female', 'female', 'male']
    print(list_s)
    series_s = pd.Series(
        data=list_s,
        dtype='str',
        name='S'
    ).astype(dtype='str')
    print('series_s:')
    print(series_s)
    print()
    print('normal distribution, float64, series_x:')
    # series_x = ds.random_data(
    #     distribution='norm',
    #     size=7,
    #     loc=69,
    #     scale=13
    # )
    list_x = [42.195, 82.630, np.nan, 86.738, 85.656, 79.281, 50.015]
    print(list_x)
    series_x = pd.Series(
        data=list_x,
        dtype='float64',
        name='X'
    ).astype(dtype='float64')
    print(series_x)
    print()
    print('integer distribution, Int64 (nullable), series_y:')
    # series_y = ds.random_data(
    #     distribution='randint',
    #     size=7,
    #     low=0,
    #     high=2
    # ).astype(dtype='Int64')
    list_y = [1, 0, 1, np.nan, 1, 0, 0]
    print(list_y)
    series_y = pd.Series(
        data=list_y,
        name='Y'
    ).astype(dtype='Int64')
    print(series_y)
    print()


if __name__ == '__main__':
    main()
