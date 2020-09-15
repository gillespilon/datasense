#! /usr/bin/env python3
'''
Test def plot_scatter_y() of graphs.py

time -f '%e' ./plot_scatter_y_test.py
./plot_scatter_y_test.py
'''

from numpy.random import default_rng
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    df = ds.read_file(
        filename='norfolk.csv',
        abscissa='LAB_BOARD_DAT_COD',
        datetimeparser='%d%b%Y:%H:%M:%S'
    )
    df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_scatter_y(
        y=df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_y_test_1.svg', format='svg')

    rng = default_rng()
    data = rng.standard_normal(size=42)
    series = pd.Series(data)
    fig, ax = ds.plot_scatter_y(y=series)
    fig.savefig('plot_scatter_y_test_2.svg', format='svg')

    data = rng.standard_normal(size=42)
    series = pd.Series(data)
    fig, ax = ds.plot_scatter_y(
        y=series,
        figuresize=(8, 6),
        marker='o',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_y_test_3.svg', format='svg')

rng = default_rng()
data = rng.standard_normal(size=42)
series = pd.Series(data)
fig, ax = ds.plot_scatter_y(y=series)


if __name__ == '__main__':
    main()
