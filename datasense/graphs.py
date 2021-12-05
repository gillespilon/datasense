'''
Graphical analysis

Colours used are colour-blind friendly.
    blue    '#0077bb'
    cyan    '#33bbee'
    teal    '#009988'
    orange  '#ee7733'
    red     '#cc3311'
    magenta '#ee3377'
    grey    '#bbbbbb'
'''

from typing import List, Optional, Tuple, Union
from datetime import datetime
import math

from matplotlib.ticker import FormatStrFormatter
from datasense import natural_cubic_spline
from scipy.stats import norm, probplot
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import pandas as pd
import numpy as np


def plot_scatter_y(
    y: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y. Optional smoothing applied to y.

    The abscissa is a series of integers 1 to the size of y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    y : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_y(y=series_y)
    >>> plt.show()

    Example 2
    >>> fig, ax = ds.plot_scatter_y(
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=4,
    >>>     colour='#ee7733'
    >>> )
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    X = pd.Series(range(1, y.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle='None',
            color=colour
        )
    elif smoothing == 'natural_cubic_spline':
        model = natural_cubic_spline(
            X=X,
            y=y,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model.predict(X),
            marker=marker,
            markersize=markersize,
            linestyle='None',
            color=colour
        )
    return (fig, ax)


def plot_scatter_x_y(
    X: pd.Series,
    y: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y versus X.  Optional smoothing applied to y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    ----------
    Parameters
    x : pd.Series
        The data to plot on the abscissa.
    y : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_x = ds.datatime_data()
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()

    Example 2
    >>> series_x = ds.random_data(distribution='randint').sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=8,
    >>>     colour='#cc3311'
    >>> )
    >>> plt.show()

    Example 3
    >>> series_x = ds.random_data(distribution='uniform').sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()

    Example 4
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle='None',
            color=colour
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(
            X=XX,
            y=y,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model.predict(XX),
            marker=marker,
            markersize=markersize,
            linestyle='None',
            color=colour
        )
    return (fig, ax)


def plot_line_y(
    y: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    linestyle: Optional[str] = '-',
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Line plot of y. Optional smoothing applied to y.

    The abscissa is a series of integers 1 to the size of y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    y : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_line_y(y=series_y)
    >>> plt.show()

    Example 2
    >>> fig, ax = ds.plot_line_y(
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=4,
    >>>     colour='#ee7733'
    >>> )
    >>> )
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    X = pd.Series(range(1, y.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            color=colour
        )
    elif smoothing == 'natural_cubic_spline':
        model = natural_cubic_spline(
            X=X,
            y=y,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model.predict(X),
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            color=colour
        )
    return (fig, ax)


def plot_line_x_y(
    X: pd.Series,
    y: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    linestyle: Optional[str] = '-',
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y versus X. Optional smoothing applied to y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    x : pd.Series
        The data to plot on the abscissa.
    y : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    linestyle : Optional[str] = '-'
        The style of the line joining the points.
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    series_x = ds.datetime_data()
    series_y = ds.random_data()
    fig, ax = ds.plot_line_x_y(
        X=series_x,
        y=series_y
    )
    >>> plt.show()

    Example 2
    >>> series_x = ds.random_data(distribution='randint').sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=8,
    >>>     linestyle=':',
    >>>     colour='#337733'
    >>> )
    >>> plt.show()

    Example 3
    >>> series_x = ds.random_data(distribution='uniform').sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()

    Example 4
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            color='#0077bb'
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            # TODO: is this necessary?
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(
            X=XX,
            y=y,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model.predict(XX),
            marker=marker,
            markersize=markersize,
            linestyle=linestyle, color='#0077bb')
    return (fig, ax)


def plot_scatter_scatter_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker1: Optional[str] = '.',
    marker2: Optional[str] = '.',
    markersize1: Optional[int] = 8,
    markersize2: Optional[int] = 8,
    linestyle1: Optional[str] = 'None',
    linestyle2: Optional[str] = 'None',
    linewidth1: Optional[float] = 1,
    linewidth2: Optional[float] = 1,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y1 versus X.
    Scatter plot of y2 versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker1 : Optional[str] = '.'
        The type of plot point for y1.
    marker2 : Optional[str] = '.'
        The type of plot point for y2.
    markersize1 : Optional[int] = 8
        The size of the plot point for y1.
    markersize2 : Optional[int] = 8
        The size of the plot point for y2.
    linestyle1 : Optional[str] = 'None'
        The style of the line for y1.
    linestyle2 : Optional[str] = 'None'
        The style of the line for y2.
    linewidth1 : Optional[float] = 0
        The width of the line for y1.
    linewidth2 : Optional[float] = 0
        The width of the line for y2.
    colour1 : Optional[str] = '#0077bb'
        The colour of the line for y1.
    colour2 : Optional[str] = '#33bbee'
        The colour of the line for y2.
    labellegendy1 : Optional[str] = None
        The legend label of the line y1.
    labellegendy2 : Optional[str] = None
        The legend label of the line y2.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_x = ds.datetime_data()
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    >>>     X=series_x,
    >>>     y1=series_y1,
    >>>     y2=series_y2
    >>> )
    >>> plt.show()

    Example 2
    >>> series_x = ds.random_data(distribution='uniform')
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    >>>     X=series_x,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1='o',
    >>>     marker2='+',
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1='#cc3311',
    >>>     colour2='#ee3377',
    >>>     labellegendy1='y1',
    >>>     labellegendy2='y2'
    >>> )
    >>> ax.legend(frameon=False)
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model1.predict(X),
            marker=marker1,
            markersize=markersize1,
            linestyle='None',
            linewidth=linewidth1,
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(X),
            marker=marker2,
            markersize=markersize2,
            linestyle='None',
            linewidth=linewidth2,
            color=colour2
        )
        ax.plot(
            X,
            model1.predict(XX),
            marker='.',
            linestyle='',
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker='.',
            linestyle='',
            color=colour2
        )
    return (fig, ax)


def plot_scatter_scatter_x1_x2_y1_y2(
    X1: pd.Series,
    X2: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker1: Optional[str] = '.',
    marker2: Optional[str] = '.',
    markersize1: Optional[int] = 8,
    markersize2: Optional[int] = 8,
    linestyle1: Optional[str] = 'None',
    linestyle2: Optional[str] = 'None',
    linewidth1: Optional[float] = 1,
    linewidth2: Optional[float] = 1,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y1 versus X1.
    Scatter plot of y2 versus X2.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X1 : pd.Series
        The data to plot on the abscissa.
    X2 : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker1 : Optional[str] = '.'
        The type of plot point for y1.
    marker2 : Optional[str] = '.'
        The type of plot point for y2.
    markersize1 : Optional[int] = 8
        The size of the plot point for y1.
    markersize2 : Optional[int] = 8
        The size of the plot point for y2.
    linestyle1 : Optional[str] = 'None'
        The style of the line for y1.
    linestyle2 : Optional[str] = 'None'
        The style of the line for y2.
    linewidth1 : Optional[float] = 0
        The width of the line for y1.
    linewidth2 : Optional[float] = 0
        The width of the line for y2.
    colour1 : Optional[str] = '#0077bb'
        The colour of the line for y1.
    colour2 : Optional[str] = '#33bbee'
        The colour of the line for y2.
    labellegendy1 : Optional[str] = None
        The legend label of the line y1.
    labellegendy2 : Optional[str] = None
        The legend label of the line y2.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_x1 = ds.datetime_data()
    >>> series_x2 = ds.datetime_data()
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2
    >>> )
    >>> plt.show()

    Example 2
    >>> plt.show()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     smoothing='natural_cubic_spline',
    >>>     number_knots=7
    >>> )
    >>> plt.show()

    Example 3
    >>> series_x1 = ds.random_data(distribution='uniform').sort_values()
    >>> series_x2 = ds.random_data(distribution='uniform').sort_values()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1='o',
    >>>     marker2='+',
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1='#cc3311',
    >>>     colour2='#ee3377',
    >>>     labellegendy1='y1',
    >>>     labellegendy2='y2'
    >>> )
    >>> ax.legend(frameon=False)
    >>> plt.show()

    Example 4
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1='o',
    >>>     marker2='+',
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1='#cc3311',
    >>>     colour2='#ee3377',
    >>>     labellegendy1='y1',
    >>>     labellegendy2='y2',
    >>>     smoothing='natural_cubic_spline',
    >>>     number_knots=7
    >>> )
    >>> ax.legend(frameon=False)
    >>> plt.show()
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if (X1.dtype and X2.dtype) in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X1,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X2,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == 'natural_cubic_spline':
        if (X1.dtype and X2.dtype) in ['datetime64[ns]']:
            XX1 = pd.to_numeric(X1)
            XX2 = pd.to_numeric(X2)
            fig.autofmt_xdate()
        else:
            XX1 = X1
            XX2 = X2
        model1 = natural_cubic_spline(
            X=XX1,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX2,
            y=y2,
            number_knots=number_knots
        )
        ax.plot(
            X1,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X2,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2
        )
        ax.plot(
            X1,
            model1.predict(XX1),
            marker=marker1,
            markersize=0,
            linestyle='-',
            linewidth=linewidth1,
            color=colour1
        )
        ax.plot(
            X2,
            model2.predict(XX2),
            marker=marker2,
            markersize=0,
            linestyle='-',
            linewidth=linewidth2,
            color=colour2
        )
    return (fig, ax)


def plot_scatter_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Scatter plot of y1 versus X.
    Line plot of y2 versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    X:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y1,
            marker='.',
            linestyle='',
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=None,
            linestyle='-',
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model1.predict(XX),
            marker='.',
            linestyle='',
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=None,
            linestyle='-',
            color=colour2
        )
    return (fig, ax)


def plot_line_line_y1_y2(
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker1: Optional[str] = '.',
    marker2: Optional[str] = '.',
    markersize1: Optional[int] = 8,
    markersize2: Optional[int] = 8,
    linestyle1: Optional[str] = '-',
    linestyle2: Optional[str] = '-',
    linewidth1: Optional[float] = 1,
    linewidth2: Optional[float] = 1,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Line plot of y1 and y2.

    Optional smoothing applied to y1 and y2.
    y1 and y2 are of the same length.
    y1 and y2 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    number_knots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker1 : Optional[str] = '.'
        The type of plot point for y1.
    marker2 : Optional[str] = '.'
        The type of plot point for y2.
    markersize1 : Optional[int] = 8
        The size of the plot point for y1.
    markersize2 : Optional[int] = 8
        The size of the plot point for y2.
    linestyle1 : Optional[str] = 'None'
        The style of the line for y1.
    linestyle2 : Optional[str] = 'None'
        The style of the line for y2.
    linewidth1 : Optional[float] = 0
        The width of the line for y1.
    linewidth2 : Optional[float] = 0
        The width of the line for y2.
    colour1 : Optional[str] = '#0077bb'
        The colour of the line for y1.
    colour2 : Optional[str] = '#33bbee'
        The colour of the line for y2.
    labellegendy1 : Optional[str] = None
        The legend label of the line y1.
    labellegendy2 : Optional[str] = None
        The legend label of the line y2.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_line_line_y1_y2(
    >>>     y1=series_y1,
    >>>     y2=series_y2
    >>> )
    >>> plt.show()
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    X = pd.Series(range(1, y1.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == 'natural_cubic_spline':
        model1 = natural_cubic_spline(
            X=X,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=X,
            y=y2,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model1.predict(X),
            marker=None,
            linestyle='-',
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(X),
            marker=None,
            linestyle='-',
            color=colour2
            )
    return (fig, ax)


def plot_line_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    marker1: Optional[str] = '.',
    marker2: Optional[str] = '.',
    markersize1: Optional[int] = 8,
    markersize2: Optional[int] = 8,
    linestyle1: Optional[str] = '-',
    linestyle2: Optional[str] = '-',
    linewidth1: Optional[float] = 1,
    linewidth2: Optional[float] = 1,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Line plot of y1 versus X.
    Line plot of y2 versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    X:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model1.predict(XX),
            marker=None,
            linestyle='-',
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=None,
            linestyle='-',
            color=colour2
            )
    return (fig, ax)


def plot_line_line_line_x_y1_y2_y3(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    y3: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    colour3: Optional[str] = '#009988',
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None,
    labellegendy3: Optional[str] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Line plot of y1 versus X.
    Line plot of y2 versus X.
    Line plot of y3 versus X.
    Optional smoothing applied to y1, y2, y3.

    This graph is useful if y1, y2, and y3 have the same units.

    X:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis
    y3: series for y3 to plot on vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X,
            y1,
            marker=None,
            linestyle='-',
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=None,
            linestyle='-',
            color=colour2,
            label=labellegendy2
        )
        ax.plot(
            X,
            y3,
            marker=None,
            linestyle='-',
            color=colour3,
            label=labellegendy3
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        model3 = natural_cubic_spline(
            X=XX,
            y=y3,
            number_knots=number_knots
        )
        ax.plot(
            X,
            model1.predict(XX),
            marker=None,
            linestyle='-',
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=None,
            linestyle='-',
            color=colour2
        )
        ax.plot(
            X,
            model3.predict(XX),
            marker=None,
            linestyle='-',
            color=colour3
        )
    return (fig, ax)


def plot_scatterleft_scatterright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    linestyle1: Optional[str] = 'None',
    linestyle2: Optional[str] = 'None'
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
    '''
    Scatter plot of y1 left vertical axis versus X.
    Scatter plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  series for horizontal axis
    y1: series for y1 to plot using left vertical axis
    y2: series for y2 to plot using right vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.
    linestyle1 : Optional[str] = 'None'
        The style of the line joining the points.
    linestyle2 : Optional[str] = 'None'
        The style of the line joining the points.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax1)
        ax1.plot(
            X,
            y1,
            marker='.',
            linestyle=linestyle1,
            color=colour1
        )
        ax2.plot(
            X,
            y2,
            marker='.',
            linestyle=linestyle2,
            color=colour2
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax1.plot(
            X,
            model1.predict(XX),
            marker='.',
            linestyle=linestyle1,
            color=colour1
        )
        ax2.plot(
            X,
            model2.predict(XX),
            marker='.',
            linestyle=linestyle2,
            color=colour2
        )
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    return (fig, ax1, ax2)


def plot_lineleft_lineright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    linestyle1: Optional[str] = '-',
    linestyle2: Optional[str] = '-',
    marker1: Optional[str] = '.',
    marker1size: Optional[float] = 8,
    marker2: Optional[str] = '.',
    marker2size: Optional[float] = 8,
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
    '''
    Line plot of y1 left vertical axis versus X.
    Line plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  series for horizontal axis
    y1: series for y1 to plot using left vertical axis
    y2: series for y2 to plot using right vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.
    linestyle1: Optional[str] = '-'
        The style of the line joining the points.
    linestyle2: Optional[str] = '-'
        The style of the line joining the points.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax1)
        ax1.plot(
            X,
            y1,
            color=colour1,
            marker=marker1,
            markersize=marker1size
        )
        ax2.plot(
            X,
            y2,
            color=colour2,
            marker=marker2,
            markersize=marker2size
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax1.plot(
            X,
            model1.predict(XX),
            color=colour1,
            linestyle=linestyle1
        )
        ax2.plot(
            X,
            model2.predict(XX),
            color=colour2,
            linestyle=linestyle2
        )
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    return (fig, ax1, ax2)


def plot_barleft_lineright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    number_knots: Optional[int] = None,
    barwidth: Optional[float] = 10,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    linestyle1: Optional[str] = '-',
    linestyle2: Optional[str] = '-',
    marker2: Optional[str] = 'o'
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
    '''
    Bar plot of y1 left vertical axis versus X.
    Line plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  series for horizontal axis
    y1: series for y1 to plot using left vertical axis
    y2: series for y2 to plot using right vertical axis
    smoothing: str
        Optional: natural_cubic_spline
    number_knots: positive integer
        The number of knots to create.
    linestyle1: Optional[str] = '-'
        The style of the line joining the points.
    linestyle2: Optional[str] = '-'
        The style of the line joining the points.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax1)
        ax1.bar(
            X,
            y1,
            barwidth,
            color=colour1
        )
        ax2.plot(
            X,
            y2,
            color=colour2,
            marker=marker2
        )
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            number_knots=number_knots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            number_knots=number_knots
        )
        ax1.plot(
            X,
            model1.predict(XX),
            color=colour1,
            linestyle=linestyle1
        )
        ax2.plot(
            X,
            model2.predict(XX),
            color=colour2,
            linestyle=linestyle2
        )
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    return (fig, ax1, ax2)


def plot_pareto(
    X: pd.Series,
    y: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    width: Optional[float] = 0.8,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee',
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    linestyle: Optional[str] = '-',
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    X : pd.Series
        The data to plot on the ordinate.
    y : pd.Series
        The data to plot on the abscissa.
    figsize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    width : Optional[float] = 0.8
        The width of the bars (in).
    colour1 : Optional[str] = '#0077bb'
        The colour of the line for y1.
    colour2 : Optional[str] = '#33bbee'
        The colour of the line for y2.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    linestyle : Optional[str] = '-'
        The style of the line joining the points.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> data = pd.DataFrame(
    >>>     {
    >>>         'ordinate': ['Mo', 'Larry', 'Curly', 'Shemp', 'Joe'],
    >>>         'abscissa': [21, 2, 10, 4, 16]
    >>>     }
    >>> )
    >>> fig, ax1, ax2 = ds.plot_pareto(
    >>>     X=data['ordinate'],
    >>>     y=data['abscissa']
    >>> )
    >>> plt.show()
    """
    df = pd.concat(
        [X, y],
        axis=1
    ).sort_values(
        by=y.name,
        axis=0,
        ascending=False,
        kind='mergesort'
    )
    total_y = df[y.name].sum()
    df['percentage'] = df[y.name] / total_y * 100
    df['cumulative_percentage'] = df['percentage'].cumsum(skipna=True)
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    ax1.bar(
        x=df[X.name],
        height=df[y.name],
        width=width,
        color=colour1
    )
    ax2.plot(
        df[X.name],
        df['cumulative_percentage'],
        marker=marker,
        markersize=markersize,
        linestyle=linestyle,
        color=colour2
    )
    return (fig, ax1, ax2)


def format_dates(
    fig: plt.figure,
    ax: axes.Axes
) -> None:
    '''
    Format dates and ticks for plotting.
    '''
    loc = mdates.AutoDateLocator()
    fmt = mdates.AutoDateFormatter(loc)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()


def probability_plot(
    data: pd.Series,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    distribution: Optional[object] = norm,
    fit: Optional[bool] = True,
    plot: Optional[object] = None,
    colour1: Optional[str] = '#0077bb',
    colour2: Optional[str] = '#33bbee'
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Plot a probability plot of data against the quantiles of a specified
    theoretical distribution.

    Parameters
    ----------
    data : pd.Series
        A pandas Series.
    figsize : Optional[Tuple[flot, float]]
        The (width, height) of the figure (in, in).
    distribution : Optional[object] = norm
        Fit a normal distribution by default.
    fit : Optional[bool] = True
        Fit a least-squares regression line to the data if True.
    plot : Optional[object] = None
        If given, plot the quantiles and least-squares fit.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>>
    >>> data = ds.random_data()
    >>> fig, ax = ds.probability_plot(data=data)
    >>> plt.show()
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    (osm, osr), (slope, intercept, r) = probplot(
        x=data,
        dist=distribution,
        fit=True,
        plot=ax
    )
    ax.get_lines()[0].set_markerfacecolor(colour1)
    ax.get_lines()[0].set_markeredgecolor(colour1)
    ax.get_lines()[1].set_color(colour2)
    return (fig, ax)


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


def plot_histogram(
    s: pd.Series,
    *,
    number_bins: Optional[int] = None,
    bin_range: Union[Tuple[int, int], Tuple[int, int]] = None,
    figsize: Optional[Tuple[int, int]] = (8, 6),
    bin_width: Optional[int] = None,
    edgecolor: Optional[str] = '#ffffff',
    linewidth: Optional[int] = 1,
    bin_label_bool: Optional[bool] = False,
    color: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    s : pd.Series
        The input series.
    number_bins : Optional[int] = None
        The number of equal-width bins in the range s.max() - s.min().
    bin_range : Union[Tuple[int, int],Tuple[int, int]] = None,
        The lower and upper range of the bins. If not provided, range is
        (s.min(), s.max()).
    figsize : Optional[Tuple[int, int]] = (8, 6),
        The figure size width, height (inch).
    bin_width : Optional[int] = None,
        The width of the bin in same units as the series s.
    edgecolor : Optional[str] = '#ffffff',
        The hexadecimal color value for the bar edges.
    linewidth : Optional[int] = 1,
        The bar edges line width (point).
    bin_label_bool : Optional[bool] = False
        If True, label the bars with count and percentage of total.
    color : Optional[str] = '#0077bb'
        The color of the bar faces.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    # Create a series of random floats, normal distribution,
    # with the default parameters.
    >>> import datasense as ds
    >>> s = ds.random_data()
    >>> fig, ax = ds.plot_histogram(s=s)

    Example 2
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, max = 13.
    >>> import datasense as ds
    >>> s = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     low=0,
    >>>     high=14
    >>> )
    >>> fig, ax = ds.plot_histogram(s=s)

    Example 3
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, max = 13.
    # Set histogram parameters to control bin width.
    >>> s = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     low=0,
    >>>     high=14
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     s=s,
    >>>     bin_width=1
)

    Example 4
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, hight = 14,
    # Set histogram parameters to control bin width and plotting range.
    >>> s = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     low=0,
    >>>     high=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     s=s,
    >>>     bin_width=1,
    >>>     bin_range=(0, 10)
    >>> )

    Example 5
    # Create a series of random floats, size = 113,
    # average = 69, standard deviation = 13.
    # Set histogram parameters to control bin width and plotting range.
    >>> s = ds.random_data(
    >>>     distribution='norm',
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     s=s,
    >>>     bin_width=5,
    >>>     bin_range=(30, 110)
    >>> )

    Example 6
    # Create a series of random floats, size = 113,
    # average = 69, standard deviation = 13.
    # Set histogram parameters to control bin width, plotting range, labels.
    # Set colour of the bars.
    >>> s = ds.random_data(
    >>>     distribution='norm',
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     s=s,
    >>>     bin_width=5,
    >>>     bin_range=(30, 110),
    >>>     figsize=(10,8),
    >>>     bin_label_bool=True,
    >>>     color='#33bbee'
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if bin_width and not bin_range:
        x = (s.max() - s.min()) / bin_width
        number_bins = math.ceil(x)
    elif bin_width and bin_range:
        number_bins = int((bin_range[1] - bin_range[0]) / bin_width)
        bin_range = bin_range
    counts, bins, patches = ax.hist(
        x=s,
        bins=number_bins,
        range=bin_range,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color
    )
    if bin_label_bool:
        ax.set_xticks(bins)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
        bin_centers = 0.5 * np.diff(bins) + bins[:-1]
        for count, x in zip(counts, bin_centers):
            ax.annotate(
                text=f'{str(int(count))}',
                xy=(x, 0),
                xytext=(0, -18),
                xycoords=(
                    'data',
                    'axes fraction'
                ),
                textcoords='offset points',
                va='top',
                ha='center'
            )
            percent = f'{(100 * float(count) / counts.sum()):0.0f} %'
            ax.annotate(
                text=percent,
                xy=(x, 0),
                xytext=(0, -32),
                xycoords=(
                    'data',
                    'axes fraction'
                ),
                textcoords='offset points',
                va='top',
                ha='center'
            )
    return (fig, ax)


def plot_horizontal_bars(
    y: Union[List[int], List[float], List[str]],
    width: Union[List[int], List[float]],
    *,
    height: Optional[float] = 0.8,
    figsize: Optional[Tuple[int, int]] = (8, 6),
    edgecolor: Optional[str] = '#ffffff',
    linewidth: Optional[int] = 1,
    color: Optional[str] = '#0077bb',
    left: Union[datetime, int, float] = None
) -> Tuple[plt.Figure, axes.Axes]:
    '''
    Parameters
    ----------
    y : Union[List[int], List[float], List[str]],
        The y coordinates of the bars.
    width : Union[List[int], List[float]],
        The width(s) of the bars.
    height : Optional[float] = 0.8,
        The height of the bars.
    figsize : Optional[Tuple[int, int]] = (8, 6),
        The figure size width, height (inch).
    edgecolor : Optional[str] = '#ffffff',
        The hexadecimal color value for the bar edges.
    linewidth : Optional[int] = 1,
        The bar edges line width (point).
    color : Optional[str] = '#0077bb'
        The color of the bar faces.
    left : Union[datetime, int, float] = None
        The x coordinates of the left sides of the bars.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> y = ['Yes', 'No']
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    >>>     y=y,
    >>>     width=width
    >>> )

    Example 2
    ---------
    >>> y = ['Yes', 'No']
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    >>>     y=y,
    >>>     width=width,
    >>>>    height=0.4
    >>> )

    Example 3
    ---------
    Create Gantt chart
    >>> data = {
    >>>     'start': ['2021-11-01', '2021-11-03', '2021-11-04', '2021-11-08'],
    >>>     'end': ['2021-11-08', '2021-11-16', '2021-11-11', '2021-11-13'],
    >>>     'task': ['task 1', 'task 2', 'task 3', 'task 4']
    >>> }
    >>> columns = ['task', 'start', 'end', 'duration', 'start_relative']
    >>> data_types = {
    >>>     'start': 'datetime64[ns]',
    >>>     'end': 'datetime64[ns]',
    >>>     'task': 'str'
    >>> }
    >>> df = (pd.DataFrame(data=data)).astype(dtype=data_types)
    >>> df[columns[3]] = (df[columns[2]] - df[columns[1]]).dt.days + 1
    >>> df = df.sort_values(
    >>>     by=[columns[1]],
    >>>     axis=0,
    >>>     ascending=[True]
    >>> )
    >>> start = df[columns[1]].min()
    >>> x_ticks = [x for x in range(duration + 1)]
    >>> x_labels = [
    >>>     (start + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
    >>>     for x in x_ticks
    >>> ]
    >>> df[columns[4]] = (df[columns[1]] - start).dt.days
    >>> fig, ax = ds.plot_horizontal_bars(
    >>>     y=df[columns[0]],
    >>>     width=df[columns[3]],
    >>>     left=df[columns[4]]
    >>> )
    >>> ax.invert_yaxis()
    >>> ax.set_xticks(
    >>>     ticks=x_ticks
    >>> )
    >>> ax.set_xticklabels(labels=x_labels, rotation=45)
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.barh(
        y=y,
        width=width,
        height=height,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color,
        left=left
    )
    return (fig, ax)


def plot_vertical_bars(
    x: Union[List[int], List[float], List[str]],
    height: Union[List[int], List[float]],
    *,
    width: Optional[float] = 0.8,
    figsize: Optional[Tuple[int, int]] = (8, 6),
    edgecolor: Optional[str] = '#ffffff',
    linewidth: Optional[int] = 1,
    color: Optional[str] = '#0077bb'
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x : Union[List[int], List[float], List[str]],
        The x coordinates of the bars.
    height : Union[List[int], List[float]],
        The height(s) of the bars.
    width : Optional[float] = 0.8,
        The width of the bars.
    figsize : Optional[Tuple[int, int]] = (8, 6),
        The figure size width, height (inch).
    edgecolor : Optional[str] = '#ffffff',
        The hexadecimal color value for the bar edges.
    linewidth : Optional[int] = 1,
        The bar edges line width (point).
    color : Optional[str] = '#0077bb'
        The color of the bar faces.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> x = ['Yes', 'No']
    >>> height = [69, 31]
    >>> fig, ax = ds.plot_vertical_bars(
    >>>     x=x,
    >>>     height=height
    >>> )

    Example 2
    >>> x = ['Yes', 'No']
    >>> height = [69, 31]
    >>> fig, ax = ds.plot_vertical_bars(
    >>>     x=x,
    >>>     height=height,
    >>>>    width=0.4
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.bar(
        x=x,
        height=height,
        width=width,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color
    )
    return (fig, ax)


def plot_pie(
    x: Union[List[int], List[float]],
    labels: Union[List[int], List[float], List[str]],
    *,
    figsize: Optional[Tuple[int, int]] = (8, 6),
    startangle: Optional[float] = 0,
    colors: Optional[List[str]] = None,
    autopct: Optional[str] = '%1.1f%%'
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x : Union[List[int], List[float]],
        The wedge sizes.
    labels : Union[List[int], List[float], List[str]],
        The labels of the wedges.
    startangle : Optional[float] = 0,
        The start angle of the pie, counterclockwise from the x axis.
    colors : Optional[List[str]] = None
        The color of the wedges.
    autopct : str
        Label the wedges with their numeric value. If None, no label.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> x = [69, 31]
    >>> labels = ['Yes', 'No']
    >>> fig, ax = ds.plot_pie(
    >>>     x=x,
    >>>     labels=labels
    >>> )

    Example 2
    >>> x = [69, 31]
    >>> labels = ['Yes', 'No']
    >>> fig, ax = ds.plot_pie(
    >>>     x=x,
    >>>     labels=labels,
    >>>     startangle=90,
    >>>     colors=[
    >>>         '#0077bb', '#33bbee', '#009988', '#ee7733', '#cc3311',
    >>>         '#ee3377', '#bbbbbb'
    >>>     ]
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.pie(
        x=x,
        labels=labels,
        startangle=startangle,
        colors=colors,
        autopct=autopct
    )
    return (fig, ax)


def plot_stacked_bars(
    x: Union[List[int], List[float], List[str]],
    height1: Union[List[int], List[float]],
    label1: Optional[str] = None,
    *,
    height2: Union[List[int], List[float]] = None,
    label2: Optional[str] = None,
    height3: Union[List[int], List[float]] = None,
    label3: Optional[str] = None,
    height4: Union[List[int], List[float]] = None,
    label4: Optional[str] = None,
    height5: Union[List[int], List[float]] = None,
    label5: Optional[str] = None,
    height6: Union[List[int], List[float]] = None,
    label6: Optional[str] = None,
    height7: Union[List[int], List[float]] = None,
    label7: Optional[str] = None,
    width: Optional[float] = 0.8,
    figsize: Optional[Tuple[int, int]] = (8, 6),
    color: Union[List[str]] = [
        '#0077bb', '#33bbee', '#009988', '#ee7733', '#cc3311',
        '#ee3377', '#bbbbbb'
    ]
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Stacked vertical bar plot of up to seven levels per bar.

    Parameters
    ----------
    x : Union[List[int], List[float], List[str]],
        The x coordinates of the bars.
    height1 : Union[List[int], List[float]],
        The height of the level 1 bars.
    label1: Optional[str] = None,
        The label of the level 1 bars.
    height2 : Union[List[int], List[float]],
        The height of the level 2 bars.
    label2: Optional[str] = None,
        The label of the level 2 bars.
    height3 : Union[List[int], List[float]],
        The height of the level 3 bars.
    label3: Optional[str] = None,
        The label of the level 3 bars.
    height4 : Union[List[int], List[float]],
        The height of the level 4 bars.
    label4: Optional[str] = None,
        The label of the level 4 bars.
    height5 : Union[List[int], List[float]],
        The height of the level 5 bars.
    label5: Optional[str] = None,
        The label of the level 5 bars.
    height6 : Union[List[int], List[float]],
        The height of the level 6 bars.
    label6: Optional[str] = None,
        The label of the level 6 bars.
    height7 : Union[List[int], List[float]],
        The height of the level 7 bars.
    label7: Optional[str] = None,
        The label of the level 7 bars.
    width : Optional[float] = 0.8,
        The width of the bars.
    figsize : Optional[Tuple[int, int]] = (8, 6),
        The figure size width, height (inch).
    color: Optional[str] = [
        '#0077bb', '#33bbee', '#009988', '#ee7733', '#cc3311',
        '#ee3377', '#bbbbbb'
    ]
        The color of the bar faces, up to seven levels.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> x = ['G1', 'G2', 'G3', 'G4', 'G5']
    >>> height1 = [20, 35, 30, 35, 27]
    >>> label1 = 'A'
    >>> width = 0.35
    >>> height2 = [25, 32, 34, 20, 25]
    >>> label2 = 'B'
    >>> fig, ax = ds.plot_stacked_bars(
    >>>     x=x,
    >>>     height1=height1,
    >>>     label1=label1,
    >>>     height2=height2,
    >>>     label2=label2
    >>> )
    >>> fig.legend(frameon=False, loc='upper right')

    Example 2
    >>> x = ['G1', 'G2', 'G3', 'G4', 'G5']
    >>> height1 = [20, 35, 30, 35, 27]
    >>> label1 = 'A'
    >>> width = 0.35
    >>> height2 = [25, 32, 34, 20, 25]
    >>> label2 = 'B'
    >>> height3 = [30, 34, 23, 27, 32]
    >>> label3 = 'C'
    >>> height4 = [30, 34, 23, 27, 32]
    >>> label4 = 'D'
    >>> height5 = [30, 34, 23, 27, 32]
    >>> label5 = 'E'
    >>> height6 = [30, 34, 23, 27, 32]
    >>> label6 = 'F'
    >>> height7 = [30, 34, 23, 27, 32]
    >>> label7 = 'G'
    >>> fig, ax = ds.plot_stacked_bars(
    >>>     x=x,
    >>>     height1=height1,
    >>>     label1=label1,
    >>>     width=width,
    >>>     figsize=(9, 6),
    >>>     height2=height2,
    >>>     label2=label2,
    >>>     height3=height3,
    >>>     label3=label3,
    >>>     height4=height4,
    >>>     label4=label4,
    >>>     height5=height5,
    >>>     label5=label5,
    >>>     height6=height6,
    >>>     label6=label6,
    >>>     height7=height7,
    >>>     label7=label7,
    >>> )
    >>> fig.legend(frameon=False, loc='upper right')
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.bar(
        x=x,
        height=height1,
        label=label1,
        width=width,
        color=color[0]
    )
    if label2:
        ax.bar(
            x=x,
            height=height2,
            label=label2,
            width=width,
            bottom=height1,
            color=color[1]
        )
    if label3:
        bottom = np.add(
                height1, height2
        ).tolist()
        ax.bar(
            x=x,
            height=height3,
            label=label3,
            width=width,
            bottom=bottom,
            color=color[2]
        )
    if label4:
        bottom = np.add(
            bottom, height3
        ).tolist()
        ax.bar(
            x=x,
            height=height4,
            label=label4,
            width=width,
            bottom=bottom,
            color=color[3]
        )
    if label5:
        bottom = np.add(
            bottom, height4
        ).tolist()
        ax.bar(
            x=x,
            height=height5,
            label=label5,
            width=width,
            bottom=bottom,
            color=color[4]
        )
    if label6:
        bottom = np.add(
            bottom, height5
        ).tolist()
        ax.bar(
            x=x,
            height=height6,
            label=label6,
            width=width,
            bottom=bottom,
            color=color[5]
        )
    if label7:
        bottom = np.add(
            bottom, height6
        ).tolist()
        ax.bar(
            x=x,
            height=height7,
            label=label7,
            width=width,
            bottom=bottom,
            color=color[6]
        )
    return (fig, ax)


__all__ = (
    'plot_scatter_y',
    'plot_scatter_x_y',
    'plot_line_y',
    'plot_line_x_y',
    'plot_scatter_scatter_x_y1_y2',
    'plot_scatter_scatter_x1_x2_y1_y2',
    'plot_scatter_line_x_y1_y2',
    'plot_line_line_y1_y2',
    'plot_line_line_x_y1_y2',
    'plot_line_line_line_x_y1_y2_y3',
    'plot_scatterleft_scatterright_x_y1_y2',
    'plot_lineleft_lineright_x_y1_y2',
    'plot_barleft_lineright_x_y1_y2',
    'plot_pareto',
    'format_dates',
    'probability_plot',
    'despine',
    'plot_histogram',
    'plot_horizontal_bars',
    'plot_vertical_bars',
    'plot_pie',
    'plot_stacked_bars',
)
