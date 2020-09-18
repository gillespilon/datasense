#! /usr/bin/env python3
'''
Test def plot_scatter_x_y() of graphs.py

time -f '%e' ./plot_scatter_x_y_test.py
./plot_scatter_x_y_test.py
'''

from numpy.random import default_rng
from datetime import timedelta
from numpy import arange
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
    rng = default_rng()
    series_x = pd.Series(
        arange(
            '2020-01-01T13:13:13',
            '2020-02-12T13:13:13',
            timedelta(hours=24),
            dtype='datetime64[s]'
        )
    )
    series_y = pd.Series(rng.standard_normal(size=42))
    fig, ax = ds.plot_scatter_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig('plot_scatter_x_y_datex_test.svg', format='svg')
    ds.html_figure(filename='plot_scatter_x_y_datex_test.svg')
    series_x = pd.Series(
        rng.uniform(
            low=13,
            high=69,
            size=42
        )
    )
    fig, ax = ds.plot_scatter_x_y(
        X=series_x,
        y=series_y,
        figuresize=(8, 4.5),
        marker='o',
        markersize=8,
        colour='#cc3311'
    )
    fig.savefig('plot_scatter_x_y_intx_test.svg', format='svg')
    ds.html_figure(filename='plot_scatter_x_y_intx_test.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
