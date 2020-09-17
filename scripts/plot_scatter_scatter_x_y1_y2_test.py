#! /usr/bin/env python3
'''
Test def plot_scatter_scatter_x_y1_y2() of graphs.py

time -f '%e' ./plot_scatter_scatter_x_y1_y2_test.py
./plot_scatter_scatter_x_y1_y2_test.py
'''

from numpy.random import default_rng
from datetime import timedelta
from pandas import Series
from numpy import arange
import datasense as ds

output_url = 'plot_scatter_x_y1_y2_test.html'
header_title = 'plot_scatter_x_y1_y2_test'
header_id = 'plot-scatter-x-y1-y2-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    rng = default_rng()
    series_x = Series(
        arange(
            '2020-01-01T13:13:13',
            '2020-02-12T13:13:13',
            timedelta(hours=24),
            dtype='datetime64[s]'
        )
    )
    series_y1 = Series(rng.standard_normal(size=42))
    series_y2 = Series(rng.standard_normal(size=42))
    fig, ax = ds.plot_scatter_scatter_x_y1_y2(
        X=series_x,
        y1=series_y1,
        y2=series_y2
    )
    fig.savefig('plot_scatter_scatter_x_y1_y2_datex_test.svg', format='svg')
    ds.html_figure(filename='plot_scatter_scatter_x_y1_y2_datex_test.svg')
    ds.page_break()
    series_x = Series(
        rng.uniform(
            low=13,
            high=69,
            size=42
        )
    )
    fig, ax = ds.plot_scatter_scatter_x_y1_y2(
        X=series_x,
        y1=series_y1,
        y2=series_y2
    )
    fig.savefig('plot_scatter_scatter_x_y1_y2_intx_test.svg', format='svg')
    ds.html_figure(filename='plot_scatter_scatter_x_y1_y2_intx_test.svg')
    fig, ax = ds.plot_scatter_scatter_x_y1_y2(
        X=series_x,
        y1=series_y1,
        y2=series_y2,
        figuresize=(8, 5),
        marker1='o',
        marker2='+',
        markersize1=8,
        markersize2=12,
        colour1='#cc3311',
        colour2='#ee3377',
        labellegendy1='y1',
        labellegendy2='y2'
    )
    ax.legend(frameon=False)
    fig.savefig('plot_scatter_scatter_x_y1_y2_test.svg', format='svg')
    ds.html_figure(filename='plot_scatter_scatter_x_y1_y2_test.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
