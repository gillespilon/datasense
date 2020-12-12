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
    # ).rename('B')
    list_b = [False, True, np.nan, False, True, True, False]
    print(list_b)
    series_b = pd.Series(
        data=list_b,
        name='B'
    ).astype(dtype='boolean')
    print(series_b)
    print()
    print('category distribution, dtype: category, list_c:')
    # series_c = ds.random_data(
    #     distribution='categories,
    #     size=7'
    # ).rename('C')
    # print(series_c.head())
    list_c = ['small', 'medium', '', 'medium', 'large', 'large', 'small']
    print(list_c)
    series_c = pd.Series(
        data=list_c,
        name='C'
    ).astype(dtype='category')
    print(series_c)
    print()
    print('timedelta distribution, dtype: timedelta64[ns], series_d')
    # series_d = ds.random_data(
    #     distribution='timedelta',
    #     size=7
    # ).rename('D')
    list_d = [0, 0, pd.NaT, 0, 0, 0, 0 ]
    print(list_d)
    series_d = pd.Series(
        data=list_d,
        name='D'
    ).astype(dtype='timedelta64[ns]')
    print(series_d)
    print()
    print('strings distribution, dtype:str, list_s:')
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
    print('datetime distribution, dtype: datetime64[ns], series_t')
    # series_t = ds.random_data(
    #     distribution='datetime',
    #     size=7
    # ).rename('T')
    list_t = [
        '2020-12-12 16:33:48', '2020-12-13 16:33:48', pd.NaT,
        '2020-12-15 16:33:48', '2020-12-16 16:33:48', '2020-12-17 16:33:48',
        '2020-12-18 16:33:48'
    ]
    print(list_t)
    series_t = pd.Series(
        data=list_t,
        name='T'
    ).astype(dtype='datetime64[ns]')
    print(series_t)
    print()
    print('normal distribution, dtype: float64, series_x:')
    # series_x = ds.random_data(
    #     distribution='norm',
    #     size=7,
    #     loc=69,
    #     scale=13
    # ).rename('X')
    list_x = [42.195, 82.630, np.nan, 86.738, 85.656, 79.281, 50.015]
    print(list_x)
    series_x = pd.Series(
        data=list_x,
        dtype='float64',
        name='X'
    ).astype(dtype='float64')
    print(series_x)
    print()
    print('integer distribution, dtype: Int64 (nullable), series_y:')
    # series_y = ds.random_data(
    #     distribution='randint',
    #     size=7,
    #     low=0,
    #     high=2
    # ).rename('Y')
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
