#! /usr/bin/env python3
'''
Test def plot_scatter_scatter_x1_x2_y1_y2() of graphs.py

time -f '%e' ./plot_scatter_scatter_x1_x2_y1_y2_test.py
./plot_scatter_scatter_x1_x2_y1_y2_test.py
'''

import datasense as ds

output_url = 'plot_scatter_x1_x2_y1_y2_test.html'
header_title = 'plot_scatter_x1_x2_y1_y2_test'
header_id = 'plot-scatter-x1-x2-y1-y2-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    series_x1 = ds.datetime_data()
    series_x2 = ds.datetime_data()
    series_y1 = ds.random_data()
    series_y2 = ds.random_data()
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
        y1=series_y1,
        y2=series_y2
    )
    fig.savefig(
        fname='plot_scatter_scatter_x1_x2_y1_y2_datex_test.svg',
        format='svg'
    )
    ds.html_figure(filename='plot_scatter_scatter_x1_x2_y1_y2_datex_test.svg')
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
        y1=series_y1,
        y2=series_y2,
        smoothing='natural_cubic_spline',
        numknots=7
    )
    fig.savefig(
            fname=
                'plot_scatter_scatter_x1_x2_y1_y2_datex_\
                 smoothing_y1_y2_test.svg',
        format='svg'
    )
    ds.html_figure(
        filename=
            'plot_scatter_scatter_x1_x2_y1_y2_datex_smoothing_y1_y2_test.svg'
    )
    series_x = ds.random_data(distribution='uniform')
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
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
    fig.savefig(
        fname='plot_scatter_scatter_x1_x2_y1_y2_test.svg',
        format='svg'
    )
    ds.html_figure(filename='plot_scatter_scatter_x1_x2_y1_y2_test.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
