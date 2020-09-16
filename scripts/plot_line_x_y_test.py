#! /usr/bin/env python3
'''
Test def plot_line_x_y() of graphs.py

time -f '%e' ./plot_line_x_y_test.py
./plot_line_x_y_test.py
'''

import webbrowser
import sys

from numpy.random import default_rng
import datasense as ds
import pandas as pd

output_url = 'plot_line_x_y_test.html'
header_title = 'plot_line_x_y_test'
header_id = 'plot-line-x-y-test'


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
#     df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_line_x_y(
        df['LAB_BOARD_DAT_COD'],
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        markersize=2,
        colour='#ee7733'
    )
    fig.savefig('plot_line_x_y_datex_test.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_x_y_datex_test.svg" '
        'alt="alternate text graph 1"/>'
        '<figcaption>plot_line_x_y_datex_test</figcaption>'
        '</figure>'
        '</p>'
    )

    fig, ax = ds.plot_line_x_y(
        pd.Series(range(1, df['LAB_BOARD_DAT_COD'].count() + 1)),
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        markersize=2,
        colour='#ee7733'
    )
    fig.savefig('plot_line_x_y_floatx_test.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_x_y_floatx_test.svg" '
        'alt="alternate text graph 1"/>'
        '<figcaption>plot_line_x_y_floatx_test</figcaption>'
        '</figure>'
        '</p>'
    )

    rng = default_rng()
    series_x = pd.Series(range(1, 43))
    series_y = pd.Series(rng.standard_normal(size=42))
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig('plot_line_x_y_test_1.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_x_y_test_1.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_line_x_y_test_1</figcaption>'
        '</figure>'
        '</p>'
    )

    series_x = pd.Series(range(1, 43))
    series_y = pd.Series(rng.standard_normal(size=42))
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y,
        figuresize=(8, 6),
        marker='o',
        markersize=8,
        linestyle=':',
        colour='#cc3311'
    )
    fig.savefig('plot_line_x_y_test_2.svg', format='svg')
    print(
        '<p>'
        '<figure>'
        '<img src="plot_line_x_y_test_2.svg" alt="alternate text graph 1"/>'
        '<figcaption>plot_line_x_y_test_2</figcaption>'
        '</figure>'
        '</p>'
    )
    ds.html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout
    webbrowser.open_new_tab(output_url)


if __name__ == '__main__':
    main()
