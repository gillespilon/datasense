#! /usr/bin/env python3
'''
Test def plot_line_x_y() of graphs.py

time -f '%e' ./plot_line_x_y_test.py
./plot_line_x_y_test.py
'''

import datasense as ds

output_url = 'plot_line_x_y_test.html'
header_title = 'plot_line_x_y_test'
header_id = 'plot-line-x-y-test'


def main():
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    # Example 1
    series_x = ds.datetime_data()
    series_y = ds.random_data()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig(
        fname='plot_line_x_y_datex_test.svg',
        format='svg'
    )
    ds.html_figure(file_name='plot_line_x_y_datex_test.svg')
    # Example 2
    series_x = ds.random_data(distribution='randint').sort_values()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y,
        figsize=(8, 4.5),
        marker='o',
        markersize=8,
        linestyle=':',
        colour='#337733'
    )
    fig.savefig(
        fname='plot_line_x_y_intx_test.svg',
        format='svg'
    )
    ds.html_figure(file_name='plot_line_x_y_intx_test.svg')
    # Example 3
    series_x = ds.random_data(distribution='uniform').sort_values()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig(
        fname='plot_line_x_y_uniformx_test.svg',
        format='svg'
    )
    ds.html_figure(file_name='plot_line_x_y_uniformx_test.svg')
    # Example 4
    series_x = ds.random_data().sort_values()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    fig.savefig(
        fname='plot_line_x_y_normx_test.svg',
        format='svg'
    )
    ds.html_figure(file_name='plot_line_x_y_normx_test.svg')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
