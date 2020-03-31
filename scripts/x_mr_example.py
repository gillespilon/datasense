#! /usr/bin/env python3


'''
Shewhart X and mR control charts example
'''


import pandas as pd
import matplotlib.pyplot as plt


from datasense import control_charts as cc


x_chart_title = 'Individuals Control Chart'
x_chart_ylabel = 'Measurement X (units)'
x_chart_xlabel = 'Sample'


mr_chart_title = 'Moving Range Control Chart'
mr_chart_ylabel = 'Measurement mR (units)'
mr_chart_xlabel = 'Sample'


def main():
    data = create_data()  # use the data in this notebook
#     data = read_data('x_mr_example.csv')  # read a csv file
#     data = read_excel('x_mr_example.xlsx')  # read an xlsx file
    x_chart(data)
    mr_chart(data)


def create_data() -> pd.DataFrame:
    '''
    Create a dataframe.
    This function is for demonstration purposes.
    In a production environment, replace this with reading data from a file.
    These data will show one point for rule one. Need to create same for
    other rules.
    '''
    df = {
        'Sample':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'X':       [25.0, 24.0, 35.5, 19.4, 20.1, 13.9, 13.9,
                    10.0, 13.3, 10.0, 16.0, 16.0, 16.0]
    }
    df = pd.DataFrame(df)
    return df


def read_data(filename: str) -> pd.DataFrame:
    '''
    Create a dataframe.
    This function reads a csv file.
    These data will show one point for rule one.
    '''
    df = pd.read_csv(filename, index_col='Sample')
    return df


def read_excel(filename: str) -> pd.DataFrame:
    '''
    Create a dataframe.
    This function reads a csv file.
    These data will show one point for rule one.
    '''
    df = pd.read_excel(filename, index_col='Sample')
    return df


def x_chart(df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(8, 6))
    x = cc.X(df[['X']], subgroup_size=2)
    ax = x.ax(fig)
    cc.draw_rule(x, ax, *cc.points_one(x), '1')
    cc.draw_rule(x, ax, *cc.points_four(x), '4')
    cc.draw_rule(x, ax, *cc.points_two(x), '2')
    ax.set_title(x_chart_title)
    ax.set_ylabel(x_chart_ylabel)
    ax.set_xlabel(x_chart_xlabel)
    ax.figure.savefig('x.svg')


def mr_chart(df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(8, 6))
    mr = cc.mR(df[['X']], subgroup_size=2)
    ax = mr.ax(fig)
    cc.draw_rule(mr, ax, *cc.points_one(mr), '1')
    ax.set_title(mr_chart_title)
    ax.set_ylabel(mr_chart_ylabel)
    ax.set_xlabel(mr_chart_xlabel)
    ax.figure.savefig('mr.svg')


if __name__ == '__main__':
    main()
