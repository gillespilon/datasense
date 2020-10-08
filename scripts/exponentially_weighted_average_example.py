#! /usr/bin/env python3
"""
Exponentially weighted average plot

This script has several functions:

- Estimate an exponentially weighted average for
    abscissa, ordinate = integer, float
- Estimate an exponentially weighted average for
    abscissa, ordinate = datetime, float
- Plot the raw data as a scatter plot
- Plot the exponentially weighted average as a line plot

time -f '%e' ./exponentially_weighted_average.py
./exponentially_weighted_average.py
"""

from typing import List, Tuple

import matplotlib.axes as axes
import datasense as ds


def main():
    global figure_width_height, date_time_parser
    file_names, graph_file_names, abscissa_names, ordinate_names,\
        ordinate_predicted_names, x_axis_label, y_axis_label, axis_title,\
        figure_width_height, column_names_sort, date_time_parser,\
        date_formatter, alpha_value, function, output_url,\
        header_title, header_id, parser = parameters()
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    for (
        filename,
        abscissaname,
        ordinatename,
        ordinatepredictedname,
        datetimeparser,
        columnnamessort,
        dateformatter,
        graphfilename
    ) in zip(
        file_names,
        abscissa_names,
        ordinate_names,
        ordinate_predicted_names,
        date_time_parser,
        column_names_sort,
        date_formatter,
        graph_file_names
    ):
        if datetimeparser == 'None':
            data = ds.read_file(
                filename=filename,
                abscissa=abscissaname,
                columnnamessort=columnnamessort
            )
        else:
            data = ds.read_file(
                filename=filename,
                abscissa=abscissaname,
                datetimeparser=parser,
                columnnamessort=columnnamessort
            )
        data[ordinatepredictedname] = data[ordinatename]\
            .ewm(alpha=alpha_value).mean()
        fig, ax = ds.plot_scatter_line_x_y1_y2(
            X=data[abscissaname],
            y1=data[ordinatename],
            y2=data[ordinatepredictedname],
            figuresize=figure_width_height
        )
        ax.set_title(axis_title, fontweight='bold')
        ax.set_xlabel(x_axis_label, fontweight='bold')
        ax.set_ylabel(y_axis_label, fontweight='bold')
        despine(ax)
        fig.savefig(f'{graphfilename}.svg', format='svg')
        print(f'<p><img src="{graphfilename}.svg"/></p>')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


def parameters() -> (
    List[str],
    List[str],
    List[str],
    List[str],
    List[str],
    str,
    str,
    str,
    Tuple[float],
    List[bool],
    List[str],
    List[str],
    str,
    float,
    str,
    str,
    str,
    str,
    str
):
    '''
    Set parameters.
    '''

    parameters = ds.read_file(
        filename='exponentially_weighted_average_parameters.ods'
    )
    filenames = [x for x in parameters['File names'] if str(x) != 'nan']
    graphfilenames = [x for x in parameters['Graph file names']
                      if str(x) != 'nan']
    abscissanames = [x for x in parameters['Abscissa names']
                     if str(x) != 'nan']
    ordinatenames = [x for x in parameters['Ordinate names']
                     if str(x) != 'nan']
    ordinatepredictednames = [x for x in parameters['Ordinate predicted names']
                              if str(x) != 'nan']
    xaxislabel = parameters['Other parameter values'][0]
    yaxislabel = parameters['Other parameter values'][1]
    axistitle = parameters['Other parameter values'][2]
    figurewidthheight = eval(parameters['Other parameter values'][3])
    columnnamessort = [x for x in parameters['Column names sort']
                       if str(x) != 'nan']
    datetimeparser = [x for x in parameters['Date time parser']
                      if str(x) != 'nan']
    parser = parameters['Other parameter values'][4]
    dateformatter = [None
                     if split.strip() == 'None' else
                     split.strip()
                     for unsplit
                     in parameters['Date formatter']
                     if str(unsplit) != 'nan'
                     for split
                     in unsplit.split(',')]
    alphavalue = parameters['Other parameter values'][6]
    function = parameters['Other parameter values'][7]
    outputurl = parameters['Other parameter values'][8]
    headertitle = parameters['Other parameter values'][9]
    headerid = parameters['Other parameter values'][10]
    return (
        filenames, graphfilenames, abscissanames, ordinatenames,
        ordinatepredictednames, xaxislabel, yaxislabel, axistitle,
        figurewidthheight, columnnamessort, datetimeparser, dateformatter,
        alphavalue, function, outputurl, headertitle, headerid, parser
    )


def despine(ax: axes.Axes) -> None:
    """
    Remove the top and right spines of a graph.

    Parameters
    ----------
    ax : axes.Axes

    Example
    -------
    >>> despine(ax)
    """
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


if __name__ == '__main__':
    main()
