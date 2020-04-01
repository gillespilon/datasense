#! /usr/bin/env python3


'''
Example of XmR control charts

time -f '%e' ./x_mr_example.py
./x_mr_example.py
'''


import pandas as pd
import matplotlib.pyplot as plt


from datasense import control_charts as cc


data_file = 'x_mr_example'


x_chart_title = 'Individuals Control Chart'
x_chart_ylabel = 'Measurement X (units)'
x_chart_xlabel = 'Sample'


mr_chart_title = 'Moving Range Control Chart'
mr_chart_ylabel = 'Measurement mR (units)'
mr_chart_xlabel = 'Sample'


def main():
    data = create_data()  # use the data in this notebook
#     data = read_csv(f'{data_file}.csv')  # read a csv file
#     data = read_excel(f'{data_file}.xlsx')  # read an xlsx file
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
        'X':       [25.0, 24.0, 35.5, 19.4, 20.1, 13.9, 13.9,
                    10.0, 13.3, 10.0, 16.0, 16.0, 16.0]
    }
    df = pd.DataFrame(df)
    df = df.set_index('Sample')
    return df


def read_csv(filename: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads a csv file.
    '''
    df = pd.read_csv(filename, index_col='Sample')
    return df


def read_xlsx(filename: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads an xlsx file.
    '''
    df = pd.read_excel(filename, index_col='Sample')
    return df


def read_ods(filename: str) -> pd.DataFrame:
    '''
    Creates a dataframe.
    This function reads an ods file.
    '''
    df = pd.read_excel(filename, index_col='Sample', engine='odf')
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
    cc.draw_rule(x, ax, *cc.points_one(x), '1')
    cc.draw_rule(x, ax, *cc.points_four(x), '4')
    cc.draw_rule(x, ax, *cc.points_two(x), '2')
    ax.set_title(x_chart_title)
    ax.set_ylabel(x_chart_ylabel)
    ax.set_xlabel(x_chart_xlabel)
    ax.figure.savefig(f'{data_file}_x.svg')


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
    ax.set_title(mr_chart_title)
    ax.set_ylabel(mr_chart_ylabel)
    ax.set_xlabel(mr_chart_xlabel)
    ax.figure.savefig(f'{data_file}_mr.svg')


if __name__ == '__main__':
    main()
