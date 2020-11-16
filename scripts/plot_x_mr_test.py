#! /usr/bin/env python3
'''
Test X() of control_charts.py

time -f '%e' ./control_charts.py
./control_charts.py
'''

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd

output_url = 'plot_x_mr_test.html'
header_title = 'plot_x_mr_test'
header_id = 'plot-x-mr-test'
graph_x_file_name = 'plot_x_test.svg'
graph_mr_file_name = 'plot_mr_test.svg'


def main():
    figsize = (8, 6)
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    data = ds.random_data(
        distribution='norm',
        size=42,
        loc=69,
        scale=13
    )
    data = pd.DataFrame(
        data=data,
        columns=['X']
    )
    print(data.describe())
    print('dtype:', type(data).__name__)
    print(data.head())
    # Create x control chart
    fig = plt.figure(figsize=figsize)
    x = cc.X(data=data)
    print('class:', type(x).__name__)
    ax = x.ax(fig)
    fig.savefig(fname=graph_x_file_name)
    ds.html_figure(file_name=graph_x_file_name)
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
