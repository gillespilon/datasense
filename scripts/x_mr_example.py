#! /usr/bin/env python3
"""
Example of XmR control charts

time -f '%e' ./x_mr_example.py
./x_mr_example.py
"""

import time

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd

data_file = 'x_mr_example'
x_chart_title = 'Individuals Control Chart'
x_chart_ylabel = 'Measurement X (units)'
x_chart_xlabel = 'Sample'
mr_chart_title = 'Moving Range Control Chart'
mr_chart_ylabel = 'Measurement mR (units)'
mr_chart_xlabel = 'Sample'
colour1 = '#33bbee'
figsize = (8, 6)
output_url = 'x_mr_example.html'
header_title = 'x_mr_example'
header_id = 'x-mr-example'


def main():
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    data = create_data()  # use the data in this notebook
#     data = ds.read_file(
#         file_name=f'{data_file}.csv',
#         index_columns=['Sample']
#     )
#     data = ds.read_file(
#         file_name=f'{data_file}.xlsx',
#         index_columns=['Sample']
#     )
#     data = ds.read_file(
#         file_name=f'{data_file}.ods',
#         index_columns=['Sample']
#     )
    ds.page_break()
    x_chart(df=data)
    ds.page_break()
    mr_chart(df=data)
#     help(cc.X)
#     help(cc.mR)
    stop_time = time.time()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def create_data() -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function is for demonstration purposes.
    '''
    df = {
        'Sample':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'X':       [25.0, 24.0, 38.5, 22.4, 23.1, 13.9, 13.9,
                    10.0, 13.3, 10.0, 16.0, 16.0, 16.0]
    }
    df = pd.DataFrame(df)
    df = df.set_index('Sample')
    # df = {
    #     'X':       [25.0, 24.0, 38.5, 22.4, 23.1, 13.9, 13.9,
    #                 10.0, 13.3, 10.0, 16.0, 16.0, 16.0]
    # }
    # df = pd.DataFrame(df)
    return df


def x_chart(df: pd.DataFrame) -> None:
    '''
    Creates an X control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    x = cc.X(data=df)
    ax = x.ax(fig)
    ax.axhline(
        y=x.sigmas[+1],
        linestyle='--',
        dashes=(5, 5),
        color=colour1,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[-1],
        linestyle='--',
        dashes=(5, 5),
        color=colour1,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[+2],
        linestyle='--',
        dashes=(5, 5),
        color=colour1,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[-2],
        linestyle='--',
        dashes=(5, 5),
        color=colour1,
        alpha=0.5
    )
    cc.draw_rules(x, ax)
    ax.set_title(
        label=x_chart_title,
        fontweight='bold'
    )
    ax.set_ylabel(ylabel=x_chart_ylabel)
    ax.set_xlabel(xlabel=x_chart_xlabel)
    fig.savefig(fname=f'{data_file}_x.svg')
    print(
       f'X Report\n'
       f'============\n'
       f'UCL        : {x.ucl}\n'
       f'Xbarbar    : {x.mean}\n'
       f'LCL        : {x.lcl}\n'
       f'Sigma(Xbar): {x.sigma}\n'
    )
    ds.html_figure(file_name=f'{data_file}_x.svg')


def mr_chart(df: pd.DataFrame) -> None:
    '''
    Creates an mR control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    mr = cc.mR(data=df)
    ax = mr.ax(fig)
    cc.draw_rule(mr, ax, *cc.points_one(mr), '1')
    ax.set_title(
        label=mr_chart_title,
        fontweight='bold'
    )
    ax.set_ylabel(ylabel=mr_chart_ylabel)
    ax.set_xlabel(xlabel=mr_chart_xlabel)
    fig.savefig(fname=f'{data_file}_mr.svg')
    print(
       f'mR Report\n'
       f'============\n'
       f'UCL        : {mr.ucl}\n'
       f'Xbarbar    : {mr.mean}\n'
       f'LCL        : {mr.lcl}\n'
       f'Sigma(Xbar): {mr.sigma}\n'
    )
    ds.html_figure(file_name=f'{data_file}_mr.svg')


if __name__ == '__main__':
    main()
