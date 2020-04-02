#! /usr/bin/env python3


'''
Example of XbarR control charts

time -f '%e' ./xbar_r_example.py
./xbar_r_example.py
'''


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm


from datasense import control_charts as cc


data_file = 'xbar_r_example'


xbar_chart_title = 'Average Control Chart'
xbar_chart_ylabel = 'Measurement Xbar (units)'
xbar_chart_xlabel = 'Sample'


r_chart_title = 'Range Control Chart'
r_chart_ylabel = 'Measurement R (units)'
r_chart_xlabel = 'Sample'


def main():
    data = create_data()  # use the data in this notebook
#     data = read_csv(f'{data_file}.csv')  # read a csv file
#     data = read_xlsx(f'{data_file}.xlsx')  # read an xlsx file
#     data = read_ods(f'{data_file}.ods')  # read an ods file
    xbar_chart(data)
    r_chart(data)
#     help(cc.Xbar)
#     help(cc.R)


def create_data() -> pd.DataFrame:
    '''
    Create a dataframe.
    This function is for demonstration purposes.
    '''
    df = {
        'Sample':  [
                    1, 2, 3, 4, 5,
                    6, 7, 8, 9, 10,
                    11, 12, 13, 14, 15,
                    16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25
                   ],
        'X1':      [
                    96, 68, 70, 68, 85,
                    57, 86, 56, 55, 73,
                    72, 70, 89, 59, 79,
                    71, 76, 80, 68, 43,
                    39, 83, 56, 95, 47
                   ],
        'X2':      [
                    69, 51, 69, 69, 69,
                    47, 69, 59, 81, 69,
                    69, 48, 76, 59, 53,
                    97, 51, 78, 66, 71,
                    72, 74, 69, 57, 68
                   ],
        'X3':      [
                    77, 71, 70, 64, 80,
                    45, 59, 53, 49, 82,
                    36, 78, 62, 93, 57,
                    66, 62, 71, 66, 48,
                    66, 56, 75, 88, 62
                   ],
        'X4':      [
                    63, 55, 91, 71, 48,
                    65, 65, 58, 69, 77,
                    82, 69, 57, 79, 38,
                    55, 84, 73, 103, 53,
                    79, 87, 51, 66, 74
                   ]
    }
    df = pd.DataFrame(df)
    df = df.set_index('Sample')
    return df


def read_csv(filename: str) -> pd.DataFrame:
    '''
    Create a dataframe.
    This function reads a csv file.
    '''
    df = pd.read_csv(filename, index_col='Sample')
    return df


def read_xlsx(filename: str) -> pd.DataFrame:
    '''
    Create a dataframe.
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


def xbar_chart(df: pd.DataFrame) -> None:
    '''
    Creates an Xbar control chart.
    Identifies out-of-control points.
    Adds cart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    xbar = cc.Xbar(df)
    ax = xbar.ax(fig)
    ax.axhline(y=xbar.sigmas[+1], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=xbar.sigmas[-1], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=xbar.sigmas[+2], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=xbar.sigmas[-2], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
#     cc.draw_rule(xbar, ax, *cc.points_one(xbar), '1')
#     cc.draw_rule(xbar, ax, *cc.points_four(xbar), '4')
#     cc.draw_rule(xbar, ax, *cc.points_two(xbar), '2')
    cc.draw_rules(xbar, ax)
    ax.set_title(xbar_chart_title, fontweight='bold')
    ax.set_ylabel(xbar_chart_ylabel)
    ax.set_xlabel(xbar_chart_xlabel)
    ax.figure.savefig(f'{data_file}_xbar.svg')


def r_chart(df: pd.DataFrame) -> None:
    '''
    Creates an R control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    '''
    fig = plt.figure(figsize=(8, 6))
    r = cc.R(df)
    ax = r.ax(fig)
    ax.axhline(y=r.sigmas[+1], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=r.sigmas[-1], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=r.sigmas[+2], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    ax.axhline(y=r.sigmas[-2], linestyle='--', dashes=(5, 5),
               c=cm.Paired.colors[0], alpha=0.5)
    cc.draw_rule(r, ax, *cc.points_one(r), '1')
    ax.set_title(r_chart_title, fontweight='bold')
    ax.set_ylabel(r_chart_ylabel)
    ax.set_xlabel(r_chart_xlabel)
    ax.figure.savefig(f'{data_file}_r.svg')


if __name__ == '__main__':
    main()
