#! /usr/bin/env python3
"""
Test def probability_plot() of graphs.py.

tim e-f '%e' ./probability_plot_test.py
./probability_plot_test.py
"""

import datasense as ds

output_url = 'probability_plot_test.html'
header_title = 'probability_plot_test'
header_id = 'probability-plot-test'


def main():
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    data = ds.random_data()
    fig, ax = ds.probability_plot(
        data=data
    )
    fig.savefig(
        fname='probability_plot_test.svg',
        format='svg'
    )
    ds.html_figure(filename='probability_plot_test.svg')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


if __name__ == '__main__':
    main()
