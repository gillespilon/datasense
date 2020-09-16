#! /usr/bin/env python3
'''
Test def plot_scatter_x_y() of graphs.py

time -f '%e' ./plot_scatter_x_y_test.py
./plot_scatter_x_y_test.py
'''

import webbrowser
import sys

from numpy.random import default_rng
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd

output_url = 'plot_scatter_x_y_test.html'
header_title = 'plot_scatter_x_y_test'
header_id = 'plot-scatter-x-y-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    df = ds.read_file(
        filename='norfolk.csv',
        abscissa='LAB_BOARD_DAT_COD',
        datetimeparser='%d%b%Y:%H:%M:%S'
    )
#     df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_scatter_x_y(
        df['LAB_BOARD_DAT_COD'],
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_x_y_datex_test.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_scatter_x_y_datex_test.svg" '
        'alt="alternate text graph 1"/>'
        '<figcaption>plot_scatter_x_y_datex_test</figcaption>'
        '</figure>'
        '</p>'
    )

    fig, ax = ds.plot_scatter_x_y(
        df['BOARD_MIXER_MANIFOLD_PRESS'],
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_x_y_floatx_test.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_scatter_x_y_floatx_test.svg" '
        'alt="alternate text graph 1"/>'
        '<figcaption>plot_scatter_x_y_floatx_test</figcaption>'
        '</figure>'
        '</p>'
    )

    rng = default_rng()
    data_x = rng.uniform(
        low=13,
        high=69,
        size=42
    )
    series_x = pd.Series(data_x)
    data_y = rng.standard_normal(size=42)
    series_y = pd.Series(data_y)
    fig, ax = ds.plot_scatter_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig('plot_scatter_x_y_test_1.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_scatter_x_y_test_1.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_scatter_x_y_test_1</figcaption>'
        '</figure>'
        '</p>'
    )

    data_x = rng.uniform(
        low=13,
        high=69,
        size=42
    )
    series_x = pd.Series(data_x)
    data_y = rng.standard_normal(size=42)
    series_y = pd.Series(data_y)
    fig, ax = ds.plot_scatter_x_y(
        X=series_x,
        y=series_y,
        figuresize=(8, 6),
        marker='o',
        markersize=8,
        colour='#cc3311'
    )
    fig.savefig('plot_scatter_x_y_test_2.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_scatter_x_y_test_2.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_scatter_x_y_test_2</figcaption>'
        '</figure>'
        '</p>'
    )
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
