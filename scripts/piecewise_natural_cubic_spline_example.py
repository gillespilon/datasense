#! /usr/bin/env python3


'''
A piecewise natural cubic spline (cubic curves in the interior segments, linear
in the exterior segments) is used to interpolate points to fit the data while
smoothing out the noise. A large number of data are fitted with low-degree
polynomials, to eliminate excessive oscillations and non-convergence.

References

[Drury, Matthew. Basis Expansions](https://github.com/madrury/basis-expansions)

[Leal, Lois Anne. Numerical Interpolation: Natural Cubic Spline]
(https://towardsdatascience.com/numerical-interpolation-natural-cubic-spline
-52c1157b98ac)

[SAS/GRAPH SYMBOL Statement (INTERPOL=SM&lt;nn&gt;&lt;P&gt;&lt;S&gt;)]
(https://documentation.sas.com/?docsetId=graphref&docsetTarget=n0c0j84n1e2jz9n
1bhkn41o3v0d6.htm&docsetVersion=9.4&locale=en#p115cutvcmx2dln1cdo96duwmxru)

[Wikipedia. Smoothing spline](https://en.wikipedia.org/wiki/Smoothing_spline)

[Wikipedia. Spline (mathematics)]
(https://en.wikipedia.org/wiki/Spline_(mathematics))

time -f '%e' ./piecewise_natural_cubic_spline.py
./piecewise_natural_cubic_spline.py

The graphs can be viewed with the view_spline_graphs.html file created.
'''


from multiprocessing import Pool
from typing import List, Tuple
from shutil import rmtree
from pathlib import Path
import itertools
import time

import matplotlib.axes as axes
import matplotlib.cm as cm
import datasense as ds
import pandas as pd


def main():
    start_time = time.time()
    global figure_width_height, c, axis_title, x_axis_label, y_axis_label,\
        graphics_directory
    file_names, targets, features, number_knots, graphics_directory, \
        figure_width_height, x_axis_label, y_axis_label, axis_title, c, \
        date_time_parser, output_url, header_title, header_id = parameters()
    set_up_graphics_directory(graphics_directory)
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    for file, target, feature in itertools.product(
        file_names, targets, features
    ):
        data = ds.read_file(
            filename=file,
            abscissa=feature
        )
        data[target] = data[target].fillna(data[target].mean())
        dates = True
        X = pd.to_numeric(data[feature])
        y = data[target]
        t = ((X, y, file, target, feature, knot, dates)
             for knot in number_knots)
        with Pool() as pool:
            for _ in pool.imap_unordered(plot_scatter_line, t):
                pass
        for knot in number_knots:
            print(
                f'<p><img src="{graphics_directory}/'
                f'spline_{file.strip(".csv")}_'
                f'{target}_{feature}_{knot}.svg"/></p>'
            )
    page_break()
    stop_time = time.time()
    elapsed_time = stop_time - start_time
    summary(
        elapsedtime=elapsed_time,
        filenames=file_names,
        targets=targets,
        features=features,
        number_knots=number_knots
    )
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


def parameters(
) -> (
    List[str],
    List[str],
    List[str],
    List[int],
    str,
    Tuple[int, int],
    str,
    str,
    str,
    Tuple[Tuple[float]],
    str,
    str
):
    '''
    Set parameters.
    '''

    parameters = ds.read_file(
        filename='piecewise_natural_cubic_spline_parameters.csv'
    )
    filenames = [x for x in parameters['File names'] if str(x) != 'nan']
    targets = [x for x in parameters['Targets'] if str(x) != 'nan']
    features = [x for x in parameters['Features'] if str(x) != 'nan']
    number_knots = [int(x) for x in parameters['Number of knots']
                if str(x) != 'nan']
    datetimeparser = parameters['Other parameter values'][0]
    graphicsdirectory = parameters['Other parameter values'][1]
    figurewidthheight = eval(parameters['Other parameter values'][2])
    xaxislabel = parameters['Other parameter values'][3]
    yaxislabel = parameters['Other parameter values'][4]
    axistitle = parameters['Other parameter values'][5]
    outputurl = parameters['Other parameter values'][6]
    headertitle = parameters['Other parameter values'][7]
    headerid = parameters['Other parameter values'][8]
    c = cm.Paired.colors
    return (
        filenames, targets, features, number_knots, graphicsdirectory,
        figurewidthheight, xaxislabel, yaxislabel, axistitle, c,
        datetimeparser, outputurl, headertitle, headerid
    )


def page_break() -> None:
    '''
    Creates a page break for html output.
    '''

    print('<p style="page-break-after: always">')
    print('<p style="page-break-before: always">')


def summary(
    elapsedtime: float,
    filenames: List[str],
    targets: List[str],
    features: List[str],
    number_knots: List[int]
) -> None:
    '''
    Print report summary.
    '''

    print('<h1>Report summary</h1>')
    print(f'Execution time : {elapsedtime:.3f} s')
    print(f'Files read     : {filenames}')
    print(f'Targets        : {targets}')
    print(f'Features       : {features}')
    print(f'Number of knots: {number_knots}')


def set_up_graphics_directory(graphdir: str) -> None:
    '''
    Create an empty directory
    '''
    try:
        rmtree(graphdir)
    except Exception:
        pass
    Path(graphdir).mkdir(parents=True, exist_ok=True)


def plot_scatter_line(
        t: Tuple[pd.Series, pd.Series, int, int, str, str, str, int, bool]
) -> None:
    X, y, file, target, feature, number_knots, dates = t
    model = ds.natural_cubic_spline(
        X=X,
        y=y,
        number_knots=number_knots
    )
    if dates:
        XX = X.astype('datetime64[ns]')
    else:
        XX = X
    fig, ax = ds.plot_scatter_line_x_y1_y2(
        X=XX,
        y1=y,
        y2=model.predict(X),
        figuresize=figure_width_height,
        labellegendy2=f'number knots = {number_knots}'
    )
    ax.legend(frameon=False, loc='best')
    ax.set_title(
        f'{axis_title}\n'
        f'file: {file} '
        f'column: {target}'
    )
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    despine(ax)
    fig.savefig(
        f'{graphics_directory}'
        f'/spline_'
        f'{file.strip(".csv")}_'
        f'{target}_{feature}_'
        f'{number_knots}.svg',
        format='svg'
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
