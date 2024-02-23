#! /usr/bin/env python3
"""
Cubic spline plot

This script has several functions:

- Estimate a cubic spline for abscissa, ordinate = integer, float
- Estimate a cubic spline for abscissa, ordinate = datetime, float
- Plot the raw data as a scatter plot
- Plot the cubic spline as a line plot

time -f '%e' ./cubic_spline_example.py
./cubic_spline_example.py
"""

from typing import NoReturn, Tuple
from matplotlib.ticker import NullFormatter, NullLocator
from matplotlib.dates import DateFormatter, DayLocator
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    file_names = ['raw_data_integer_float.csv', 'raw_data_datetime_float.csv']
    ordinate_predicted_name = ['ordinate_predicted', 'ordinate_predicted']
    graph_file_name = [
        'cubic_spline_integer_float', 'cubic_spline_datetime_float'
    ]
    abscissa_name = ['abscissa', 'abscissa']
    ordinate_name = ['ordinate', 'observed']
    column_names_sort = [False, False]
    date_time_parser = [None, parser]
    date_formatter = [None, '%m-%d']
    figure_width_height = (8, 6)
    parser = '%Y-%m-%d %H:%M:%S'
    axis_title = 'Cubic Spline'
    x_axis_label = 'Abscissa'
    y_axis_label = 'Ordinate'
    ds.style_graph()
    for (
        file_name, abscissaname, ordinatename, ordinatepredictedname,
        datetimeparser, columnnamessort, dateformatter, graphfile_name
    ) in zip(
        file_names, abscissa_name, ordinate_name, ordinate_predicted_name,
        date_time_parser, column_names_sort, date_formatter, graph_file_name
    ):
        data = ds.read_file(file_name=file_name, parse_dates=[abscissaname])
        if datetimeparser is True:
            data[abscissaname] = pd.to_numeric(data[abscissaname])
            spline = ds.cubic_spline(
                df=data, abscissa=abscissaname, ordinate=ordinatename
            )
            data[ordinatepredictedname] = spline(data[abscissaname])
            data[abscissaname] = data[abscissaname]\
                .astype(dtype='datetime64[ns]')
        else:
            spline = ds.cubic_spline(
                df=data, abscissa=abscissaname, ordinate=ordinatename
            )
            data[ordinatepredictedname] = spline(data[abscissaname])
        plot_graph(
            df=data, columnx=abscissaname, columny=ordinatename,
            columnz=ordinatepredictedname,
            figsize=figure_width_height, dateformat=dateformatter,
            graphname=graphfile_name, graphtitle=axis_title,
            xaxislabel=x_axis_label, yaxislabel=y_axis_label
        )


def plot_graph(
    df: pd.DataFrame,
    columnx: str,
    columny: str,
    columnz: str,
    figsize: Tuple[int, int],
    dateformat: str,
    graphname: str,
    graphtitle: str,
    xaxislabel: str,
    yaxislabel: str
) -> NoReturn:
    fig, ax = ds.plot_line_x_y(X=df[columnx], y=df[columnz], figsize=figsize)
    if dateformat:
        ax.xaxis.set_major_locator(DayLocator())
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_formatter(DateFormatter(dateformat))
        ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel(xlabel=xaxislabel)
    ax.set_ylabel(ylabel=yaxislabel)
    ax.set_title(label=graphtitle)
    ds.despine(ax=ax)
    fig.savefig(fname=f'{graphname}.svg', format='svg')


if __name__ == '__main__':
    main()
