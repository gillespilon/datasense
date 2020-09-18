#! /usr/bin/env python3
'''
Test def plot_scatter_y() of graphs.py

time -f '%e' ./plot_scatter_y_test.py
./plot_scatter_y_test.py
'''

from numpy.random import default_rng
import datasense as ds
import pandas as pd

output_url = 'plot_scatter_y_test.html'
header_title = 'plot_scatter_y_test'
header_id = 'plot-scatter-y-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    rng = default_rng()
    series_y = pd.Series(rng.standard_normal(size=42))
    fig, ax = ds.plot_scatter_y(y=series_y)
    fig.savefig('plot_scatter_y_test_1.svg', format='svg')
    ds.html_figure(filename='plot_scatter_y_test_1.svg')
    fig, ax = ds.plot_scatter_y(
        y=series_y,
        figuresize=(8, 4.5),
        marker='o',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_y_test_2.svg', format='svg')
    ds.html_figure(filename='plot_scatter_y_test_2.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
