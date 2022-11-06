#! /usr/bin/env python3
'''
Test Xbar and R of control_charts.py

time -f '%e' ./control_charts.py
./control_charts.py
'''

import time

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd

output_url = 'plot_xbar_r_test.html'
header_title = 'plot_xbar_r_test'
header_id = 'plot-xbar-r-test'
graph_xbar_file_name = 'plot_xbar_test.svg'
graph_r_file_name = 'plot_r_test.svg'
figsize = (8, 6)


def main():
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    X1 = ds.random_data(
        distribution='norm',
        size=25,
        loc=69,
        scale=13
    )
    X2 = ds.random_data(
        distribution='norm',
        size=25,
        loc=69,
        scale=13
    )
    X3 = ds.random_data(
        distribution='norm',
        size=25,
        loc=69,
        scale=13
    )
    X4 = ds.random_data(
        distribution='norm',
        size=25,
        loc=69,
        scale=13
    )
    data = pd.DataFrame(
        data={
            'X1': X1,
            'X2': X2,
            'X3': X3,
            'X4': X4,
        }
    )
    # print('dtype:', type(data).__name__)
    # print(data.head())
    # Create Xbar control chart
    ds.page_break()
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    xbar = cc.Xbar(data=data)
    # print('class:', type(x).__name__)
    ax = xbar.ax(fig)
    fig.savefig(fname=graph_xbar_file_name)
    ds.html_figure(file_name=graph_xbar_file_name)
    print(
       f'Xbar Report\n'
       f'============\n'
       f'UCL        : {xbar.ucl.round(3)}\n'
       f'Xbarbar    : {xbar.mean.round(3)}\n'
       f'LCL        : {xbar.lcl.round(3)}\n'
       f'Sigma(Xbar): {xbar.sigma.round(3)}\n'
    )
    # Create R chart
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    r = cc.R(data=data)
    # print('class:', type(x).__name__)
    ax = r.ax(fig)
    fig.savefig(fname=graph_r_file_name)
    ds.html_figure(file_name=graph_r_file_name)
    print(
       f'R Report\n'
       f'============\n'
       f'UCL        : {r.ucl.round(3)}\n'
       f'Rbar       : {r.mean.round(3)}\n'
       f'LCL        : {round(r.lcl, 3)}\n'
       f'Sigma(R)   : {r.sigma.round(3)}\n'
    )
    stop_time = time.time()
    ds.page_break()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
