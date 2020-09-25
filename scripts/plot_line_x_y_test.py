#! /usr/bin/env python3
'''
Test def plot_line_x_y() of graphs.py

time -f '%e' ./plot_line_x_y_test.py
./plot_line_x_y_test.py
'''

from numpy.random import default_rng
import datasense as ds
import pandas as pd

output_url = 'plot_line_x_y_test.html'
header_title = 'plot_line_x_y_test'
header_id = 'plot-line-x-y-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    rng = default_rng()
    series_x = ds.datetime_data()
    series_y = pd.Series(ds.random_data())
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig('plot_line_x_y_datex_test.svg', format='svg')
    ds.html_figure(filename='plot_line_x_y_datex_test.svg')
    series_x = pd.Series(
        rng.uniform(
            low=13,
            high=69,
            size=42
        )
    ).sort_values()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y,
        figuresize=(8, 4.5),
        marker='o',
        markersize=8,
        linestyle=':',
        colour='#337733'
    )
    fig.savefig('plot_line_x_y_intx_test.svg', format='svg')
    ds.html_figure(filename='plot_line_x_y_intx_test.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
