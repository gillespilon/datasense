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
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    # Example 1
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
    ds.html_figure(file_name='plot_scatter_scatter_x1_x2_y1_y2_datex_test.svg')
    # Example 2
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
        y1=series_y1,
        y2=series_y2,
        smoothing='natural_cubic_spline',
        number_knots=7
    )
    fig.savefig(
        fname=(
            'plot_scatter_scatter_x1_x2_y1_y2_'
            'datex_smoothing_y1_y2_test.svg'
        ),
        format='svg'
    )
    ds.html_figure(
        file_name=(
            'plot_scatter_scatter_x1_x2_y1_y2_datex_smoothing_y1_y2_test.svg'
            )
    )
    # Example 3
    series_x1 = ds.random_data(distribution='uniform').sort_values()
    series_x2 = ds.random_data(distribution='uniform').sort_values()
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
        y1=series_y1,
        y2=series_y2,
        figsize=(8, 5),
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
    ds.html_figure(file_name='plot_scatter_scatter_x1_x2_y1_y2_test.svg')
    # Example 4
    fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
        X1=series_x1,
        X2=series_x2,
        y1=series_y1,
        y2=series_y2,
        figsize=(8, 5),
        marker1='o',
        marker2='+',
        markersize1=8,
        markersize2=12,
        colour1='#cc3311',
        colour2='#ee3377',
        labellegendy1='y1',
        labellegendy2='y2',
        smoothing='natural_cubic_spline',
        number_knots=7
    )
    ax.legend(frameon=False)
    fig.savefig(
        fname='plot_scatter_scatter_x1_x2_y1_y2_smoothing_y1_y2_test.svg',
        format='svg'
    )
    ds.html_figure(
        file_name='plot_scatter_scatter_x1_x2_y1_y2_smoothing_y1_y2_test.svg'
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
