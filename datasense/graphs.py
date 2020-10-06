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

from typing import Optional, Tuple

from datasense import natural_cubic_spline
from scipy.stats import norm, probplot
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.cm as cm
import pandas as pd

c = cm.Paired.colors


def plot_scatter_y(
    y: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.figure, axes.Axes]:
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
    figuresize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    numknots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.figure, axes.Axes]
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
    >>>     figuresize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=4,
    >>>     colour='#ee7733'
    >>> )
    >>> plt.show()
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
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
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    colour: Optional[str] = '#0077bb'
) -> (plt.figure, axes.Axes):
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
    figuresize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    numknots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.figure, axes.Axes]
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
    >>>     figuresize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=8,
    >>>     colour='#cc3311'
    >>> )
    >>> plt.show()

    # Example 3
    >>> series_x = ds.random_data(distribution='uniform').sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()

    # Example 4
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    >>> plt.show()
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
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
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    linestyle: Optional[str] = '-',
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.figure, axes.Axes]:
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
    figuresize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    numknots : Optional[int] = None
        The number of knots for natural cubic spline smoothing.
    marker : Optional[str] = '.'
        The type of plot point.
    markersize : Optional[float] = 8
        The size of the plot point (pt).
    colour : Optional[str] = '#0077bb'
        The colour of the plot point (hexadecimal triplet string).

    Returns
    -------
    Tuple[plt.figure, axes.Axes]
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
    >>>     figuresize=(8, 4.5),
    >>>     marker='o',
    >>>     markersize=4,
    >>>     colour='#ee7733'
    >>> )
    >>> )
    >>> plt.show()
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
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
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    marker: Optional[str] = '.',
    markersize: Optional[float] = 8,
    linestyle: Optional[str] = '-',
    colour: Optional[str] = '#0077bb'
) -> Tuple[plt.figure, axes.Axes]:
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
    figuresize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    numknots : Optional[int] = None
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
    Tuple[plt.figure, axes.Axes]
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
    >>>     figuresize=(8, 4.5),
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
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
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
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
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
) -> Tuple[plt.figure, axes.Axes]:
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
    figuresize : Optional[Tuple[float, float]] = None
        The (width, height) of the figure (in, in).
    smoothing : Optional[str] = None
        The type of smoothing to apply.
    numknots : Optional[int] = None
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
    Tuple[plt.figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> from numpy.random import default_rng
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> import pandas as pd
    >>>
    >>> rng = default_rng()
    >>> series_x = Series(
    >>>     arange(
    >>>         '2020-01-01T13:13:13',
    >>>         '2020-02-12T13:13:13',
    >>>         timedelta(hours=24),
    >>>         dtype='datetime64[s]'
    >>>     )
    >>> )
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
    >>>     figuresize=(8, 5),
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
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
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
        ax.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax.plot(X, model2.predict(XX), marker='.', linestyle='', color=c[5])
    return (fig, ax)


def plot_scatter_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None
) -> (plt.figure, axes.Axes):
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
    numknots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X, y1, marker='.', linestyle='', color=c[1], label=labellegendy1
        )
        ax.plot(
            X, y2, marker=None, linestyle='-', color=c[5], label=labellegendy2
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
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
        )
        ax.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax.plot(X, model2.predict(XX), marker=None, linestyle='-', color=c[5])
    return (fig, ax)


def plot_line_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
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
) -> Tuple[plt.figure, axes.Axes]:
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
    numknots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
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
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
        )
        ax.plot(X, model1.predict(XX), marker=None, linestyle='-', color=c[1])
        ax.plot(X, model2.predict(XX), marker=None, linestyle='-', color=c[5])
    return (fig, ax)


def plot_line_line_line_x_y1_y2_y3(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    y3: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None,
    labellegendy1: Optional[str] = None,
    labellegendy2: Optional[str] = None,
    labellegendy3: Optional[str] = None
) -> (plt.figure, axes.Axes):
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
    numknots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax)
        ax.plot(
            X, y1, marker=None, linestyle='-', color=c[0], label=labellegendy1
        )
        ax.plot(
            X, y2, marker=None, linestyle='-', color=c[1], label=labellegendy2
        )
        ax.plot(
            X, y3, marker=None, linestyle='-', color=c[2], label=labellegendy3
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
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
        )
        model3 = natural_cubic_spline(
            X=XX,
            y=y3,
            numberknots=numknots
        )
        ax.plot(X, model1.predict(XX), marker=None, linestyle='-', color=c[0])
        ax.plot(X, model2.predict(XX), marker=None, linestyle='-', color=c[1])
        ax.plot(X, model3.predict(XX), marker=None, linestyle='-', color=c[2])
    return (fig, ax)


def plot_scatterleft_scatterright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None
) -> Tuple[plt.figure, axes.Axes, axes.Axes]:
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
    numknots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax1)
        ax1.plot(X, y1, marker='.', linestyle='', color=c[1])
        ax2.plot(X, y2, marker='.', linestyle='', color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
        )
        ax1.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax2.plot(X, model2.predict(XX), marker='.', linestyle='', color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (fig, ax1, ax2)


def plot_lineleft_lineright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    *,
    figuresize: Optional[Tuple[float, float]] = None,
    smoothing: Optional[str] = None,
    numknots: Optional[int] = None
) -> Tuple[plt.figure, axes.Axes, axes.Axes]:
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
    numknots: positive integer
        The number of knots to create.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.
    '''
    fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            format_dates(fig, ax1)
        ax1.plot(X, y1, color=c[1])
        ax2.plot(X, y2, color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(
            X=XX,
            y=y1,
            numberknots=numknots
        )
        model2 = natural_cubic_spline(
            X=XX,
            y=y2,
            numberknots=numknots
        )
        ax1.plot(X, model1.predict(XX), color=c[1])
        ax2.plot(X, model2.predict(XX), color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
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
    figuresize: Optional[Tuple[float, float]] = None,
    distribution: Optional[object] = norm,
    fit: Optional[bool] = True,
    plot: Optional[object] = None
) -> Tuple[plt.figure, axes.Axes]:
    """
    Plot a probability plot of data against the quantiles of a specified
    theoretical distribution.

    Parameters
    ----------
    data : pd.Series
        A pandas Series.
    figuresize : Optional[Tuple[flot, float]]
        The (width, height) of the figure (in, in).
    distribution : Optional[object] = norm
        Fit a normal distribution by default.
    fit : Optional[bool] = True
        Fit a least-squares regression line to the data if True.
    plot : Optional[object] = None
        If given, plot the quantiles and least-squares fit.

    Returns
    -------
    Tuple[plt.figure, axes.Axes]
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
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    (osm, osr), (slope, intercept, r) = probplot(
        x=data,
        dist=distribution,
        fit=True,
        plot=ax
    )
    return (fig, ax)


__all__ = (
    'plot_scatter_y',
    'plot_scatter_x_y',
    'plot_line_y',
    'plot_line_x_y',
    'plot_scatter_scatter_x_y1_y2',
    'plot_scatter_line_x_y1_y2',
    'plot_line_line_x_y1_y2',
    'plot_line_line_line_x_y1_y2_y3',
    'plot_scatterleft_scatterright_x_y1_y2',
    'plot_lineleft_lineright_x_y1_y2',
    'format_dates',
    'probability_plot',
)
