#! /usr/bin/env python3
"""
Example of XmR control charts

time -f '%e' ./x_mr_example.py
./x_mr_example.py
"""

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import pandas as pd

data_file = 'x_mr_example'
x_chart_title = 'Individuals Control Chart'
x_chart_ylabel = 'Measurement X (units)'
x_chart_xlabel = 'Sample'
mr_chart_title = 'Moving Range Control Chart'
mr_chart_ylabel = 'Measurement mR (units)'
mr_chart_xlabel = 'Sample'
colour1 = '#33bbee'


def main():
    data = create_data()  # use the data in this notebook
#     data = read_csv(f'{data_file}.csv')  # read a csv file
#     data = read_xlsx(f'{data_file}.xlsx')  # read an xlsx file
#     data = read_ods(f'{data_file}.ods')  # read an ods file
    x_chart(data)
    mr_chart(data)
#     help(cc.X)
#     help(cc.mR)


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
    return df


def read_csv(file_name: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads a csv file.
    '''
    df = pd.read_csv(file_name, index_col='Sample')
    return df


def read_xlsx(file_name: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads an xlsx file.
    '''
    df = pd.read_excel(file_name, index_col='Sample')
    return df


def read_ods(file_name: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads an ods file.
    '''
    df = pd.read_excel(file_name, index_col='Sample', engine='odf')
    return df


def x_chart(df: pd.DataFrame) -> None:
    '''
    Creates an X control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    x = cc.X(df)
    ax = x.ax(fig)
    ax.axhline(y=x.sigmas[+1], linestyle='--', dashes=(5, 5),
               color=colour1, alpha=0.5)
    ax.axhline(y=x.sigmas[-1], linestyle='--', dashes=(5, 5),
               color=colour1, alpha=0.5)
    ax.axhline(y=x.sigmas[+2], linestyle='--', dashes=(5, 5),
               color=colour1, alpha=0.5)
    ax.axhline(y=x.sigmas[-2], linestyle='--', dashes=(5, 5),
               color=colour1, alpha=0.5)
#     cc.draw_rule(x, ax, *cc.points_one(x), '1')
#     cc.draw_rule(x, ax, *cc.points_four(x), '4')
#     cc.draw_rule(x, ax, *cc.points_two(x), '2')
#     cc.draw_rule(x, ax, *cc.points_three(x), '3')
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


def mr_chart(df: pd.DataFrame) -> None:
    '''
    Creates an mR control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    mr = cc.mR(df)
    ax = mr.ax(fig)
    cc.draw_rule(mr, ax, *cc.points_one(mr), '1')
    ax.set_title(
        label=mr_chart_title,
        fontweight='bold'
    )
    ax.set_ylabel(ylabel=mr_chart_ylabel)
    ax.set_xlabel(xlabel=mr_chart_xlabel)
    fig.savefig(fname=f'{data_file}_mr.svg')


if __name__ == '__main__':
    main()
