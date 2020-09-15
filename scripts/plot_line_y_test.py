#! /usr/bin/env python3
'''
Test def plot_line_y() of graphs.py

time -f '%e' ./plot_line_y_test.py
./plot_line_y_test.py
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
    original_stdout = sys.stdout
    sys.stdout = open(output_url, 'w')
    ds.html_header(
        headertitle=header_title,
        headerid=header_id
    )
    df = ds.read_file(
        filename='norfolk.csv',
        abscissa='LAB_BOARD_DAT_COD',
        datetimeparser='%d%b%Y:%H:%M:%S'
    )
    df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_line_y(
        y=df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_line_y_test_1.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_y_test_1.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_line_y_test_1</figcaption>'
        '</figure>'
        '</p>'
    )

    rng = default_rng()
    data = rng.standard_normal(size=42)
    series = pd.Series(data)
    fig, ax = ds.plot_line_y(y=series)
    fig.savefig('plot_line_y_test_2.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_y_test_2.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_line_y_test_2</figcaption>'
        '</figure>'
        '</p>'
    )

    data = rng.standard_normal(size=42)
    series = pd.Series(data)
    fig, ax = ds.plot_line_y(
        y=series,
        figuresize=(8, 6),
        marker='o',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_line_y_test_3.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_y_test_3.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_line_y_test_3</figcaption>'
        '</figure>'
        '</p>'
    )
    ds.html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout
    webbrowser.open_new_tab(output_url)


if __name__ == '__main__':
    main()
