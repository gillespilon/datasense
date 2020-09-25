#! /usr/bin/env python3
'''
Test def plot_line_y() of graphs.py

time -f '%e' ./plot_line_y_test.py
./plot_line_y_test.py
'''

import datasense as ds

output_url = 'plot_line_y_test.html'
header_title = 'plot_line_y_test'
header_id = 'plot-scatter-x-y-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    series_y = ds.random_data()
    fig, ax = ds.plot_line_y(y=series_y)
    fig.savefig(
        fname='plot_line_y_test_1.svg',
        format='svg'
    )
    ds.html_figure(filename='plot_line_y_test_1.svg')
    fig, ax = ds.plot_line_y(
        y=series_y,
        figuresize=(8, 4.5),
        marker='o',
        markersize=4,
        linestyle=':',
        colour='#ee7733'
    )
    fig.savefig(
        fname='plot_line_y_test_2.svg',
        format='svg'
    )
    ds.html_figure(filename='plot_line_y_test_2.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
