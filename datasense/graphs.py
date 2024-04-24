"""
Graphical analysis

All examples use the following, as required:
    import datasense as ds
    import matplotlib.pyplot as plt

Colours used are colour-blind friendly.
    blue    "#0077bb"
    cyan    "#33bbee"
    teal    "#009988"
    orange  "#ee7733"
    red     "#cc3311"
    magenta "#ee3377"
    grey    "#bbbbbb"
"""

from datetime import datetime
from pathlib import Path
import math

from scipy.stats import boxcox, boxcox_normplot, norm, probplot
from datasense import natural_cubic_spline, html_ds
from matplotlib.ticker import StrMethodFormatter
from matplotlib.offsetbox import AnchoredText
from matplotlib import rcParams as rc
import matplotlib.dates as mdates
import matplotlib.artist as mpla
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import pyqrcode as pq
import pandas as pd
import numpy as np


# colour-blind friendly in order of application
colour_blue = "#0077bb"
colour_cyan = "#33bbee"
colour_teal = "#009988"
colour_orange = "#ee7733"
colour_red = "#cc3311"
colour_magenta = "#ee3388"
colour_grey = "#bbbbbb"

# other colours
colour_white = "#ffffff"


def plot_scatter_y(
    *,
    y: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    colour: str = colour_blue,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Scatter plot of y. Optional smoothing applied to y.

    The abscissa is a series of integers 1 to the size of y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    y: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker: str = "."
        The type of plot point.
    markersize: float = 8
        The size of the plot point (pt).
    colour: str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_y(y=series_y)

    >>> import datasense as ds
    >>> fig, ax = ds.plot_scatter_y(
    ...     y=series_y,
    ...     figsize=(8, 4.5),
    ...     marker="o",
    ...     markersize=4,
    ...     colour=colour_orange
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    # generate X series, required if using smoothing
    X = pd.Series(range(1, y.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle="None",
            color=colour,
        )
    elif smoothing == "natural_cubic_spline":
        model = natural_cubic_spline(X=X, y=y, number_knots=number_knots)
        ax.plot(
            X,
            model.predict(X),
            marker=marker,
            markersize=markersize,
            linestyle="None",
            color=colour,
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_x_y(
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 4,
    colour: str = colour_blue,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Scatter plot of y versus X.  Optional smoothing applied to y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    x: pd.Series
        The data to plot on the abscissa.
    y: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker: str = "."
        The type of plot point.
    markersize: float = 4
        The size of the plot point (pt).
    colour: str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> series_x = ds.datetime_data()
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_x_y(
    ...     X=series_x,
    ...     y=series_y
    ... )

    >>> import datasense as ds
    >>> series_x = ds.random_data(distribution="randint").sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    ...     X=series_x,
    ...     y=series_y,
    ...     figsize=(8, 4.5),
    ...     marker="o",
    ...     markersize=8,
    ...     colour=colour_red
    ... )


    >>> import datasense as ds
    >>> series_x = ds.random_data(distribution="uniform").sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    ...     X=series_x,
    ...     y=series_y
    ... )


    >>> import datasense as ds
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    ...     X=series_x,
    ...     y=series_y
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle="None",
            color=colour,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(X=XX, y=y, number_knots=number_knots)
        ax.plot(
            X,
            model.predict(XX),
            marker=marker,
            markersize=markersize,
            linestyle="None",
            color=colour,
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_y(
        *,
    y: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
    colour: str = colour_blue,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Line plot of y. Optional smoothing applied to y.

    The abscissa is a series of integers 1 to the size of y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    y: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker: str = "."
        The type of plot point.
    markersize: float = 8
        The size of the plot point (pt).
    linestyle: str = "-"
        The style for the line.
    colour: str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_line_y(y=series_y)

    >>> import datasense as ds
    >>> fig, ax = ds.plot_line_y(
    ...     y=series_y,
    ...     figsize=(8, 4.5),
    ...     marker="o",
    ...     markersize=4,
    ...     colour=colour_orange
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    X = pd.Series(range(1, y.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            color=colour,
        )
    elif smoothing == "natural_cubic_spline":
        model = natural_cubic_spline(X=X, y=y, number_knots=number_knots)
        ax.plot(
            X,
            model.predict(X),
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            color=colour,
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_x_y(
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
    linewidth: float = 1,
    colour: str = colour_blue,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Scatter plot of y versus X. Optional smoothing applied to y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker: str = "."
        The type of plot point.
    markersize: float = 8
        The size of the plot point (pt).
    linestyle: str = "-"
        The style of the line joining the points.
    linewidth: float = 1
        The width of the line joining the points.
    colour: str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines: bool = True
        IF True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> X = ds.datetime_data()
    >>> y = ds.random_data()
    >>> fig, ax = ds.plot_line_x_y(
    ...     X=X,
    ...     y=y
    ... )

    >>> import datasense as ds
    >>> X = ds.random_data(distribution="randint").sort_values()
    >>> y = ds.random_data()
    >>> fig, ax = ds.plot_line_x_y(
    ...     X=X,
    ...     y=y,
    ...     figsize=(8, 4.5),
    ...     marker="o",
    ...     markersize=8,
    ...     linestyle=":",
    ...     linewidth=5,
    ...     colour="#ee3377"
    ... )

    >>> import datasense as ds
    >>> X = ds.random_data(distribution="uniform").sort_values()
    >>> y = ds.random_data()
    >>> fig, ax = ds.plot_line_x_y(
    ...     X=X,
    ...     y=y
    ... )

    >>> import datasense as ds
    >>> X = ds.random_data().sort_values()
    >>> y = ds.random_data()
    >>> fig, ax = ds.plot_line_x_y(
    ...     X=X,
    ...     y=y
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            linewidth=linewidth,
            color=colour,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            # TODO: is this necessary?
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(X=XX, y=y, number_knots=number_knots)
        (
            ax.plot(
                X,
                model.predict(XX),
                marker=marker,
                markersize=markersize,
                linestyle=linestyle,
                linewidth=linewidth,
                color=colour,
            ),
        )
    if remove_spines:
        despine(ax=ax)
    plt.close("all")
    return (fig, ax)


def plot_scatter_scatter_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker1: str = ".",
    marker2: str = ".",
    markersize1: int = 8,
    markersize2: int = 8,
    linestyle1: str = "None",
    linestyle2: str = "None",
    linewidth1: float = 1,
    linewidth2: float = 1,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
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
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the ordinate.
    y2: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker1: str = "."
        The type of plot point for y1.
    marker2: str = "."
        The type of plot point for y2.
    markersize1: int = 8
        The size of the plot point for y1.
    markersize2: int = 8
        The size of the plot point for y2.
    linestyle1: str = "None"
        The style of the line for y1.
    linestyle2: str = "None"
        The style of the line for y2.
    linewidth1: float = 1
        The width of the line for y1.
    linewidth2: float = 1
        The width of the line for y2.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.
    remove_spines: booll = True
        IF True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> series_x = ds.datetime_data()
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    ...     X=series_x,
    ...     y1=series_y1,
    ...     y2=series_y2
    ... )

    >>> import datasense as ds
    >>> series_x = ds.random_data(distribution="uniform")
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    ...     X=series_x,
    ...     y1=series_y1,
    ...     y2=series_y2,
    ...     figsize=(8, 5),
    ...     marker1="o",
    ...     marker2="+",
    ...     markersize1=8,
    ...     markersize2=12,
    ...     colour1=colour_red,
    ...     colour2=colour_magenta,
    ...     labellegendy1="y1",
    ...     labellegendy2="y2"
    ... )
    >>> ax.legend(frameon=False) # doctest: +SKIP
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax.plot(
            X,
            model1.predict(X),
            marker=marker1,
            markersize=markersize1,
            linestyle="None",
            linewidth=linewidth1,
            color=colour1,
        )
        ax.plot(
            X,
            model2.predict(X),
            marker=marker2,
            markersize=markersize2,
            linestyle="None",
            linewidth=linewidth2,
            color=colour2,
        )
        ax.plot(X, model1.predict(XX), marker=".", linestyle="", color=colour1)
        ax.plot(X, model2.predict(XX), marker=".", linestyle="", color=colour2)
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_scatter_x1_x2_y1_y2(
    *,
    X1: pd.Series,
    X2: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker1: str = ".",
    marker2: str = ".",
    markersize1: int = 8,
    markersize2: int = 8,
    linestyle1: str = "None",
    linestyle2: str = "None",
    linewidth1: float = 1,
    linewidth2: float = 1,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
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
    X1: pd.Series
        The data to plot on the abscissa.
    X2: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the ordinate.
    y2: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker1: str = "."
        The type of plot point for y1.
    marker2: str = "."
        The type of plot point for y2.
    markersize1: int = 8
        The size of the plot point for y1.
    markersize2: int = 8
        The size of the plot point for y2.
    linestyle1: str = "None"
        The style of the line for y1.
    linestyle2: str = "None"
        The style of the line for y2.
    linewidth1: float = 1
        The width of the line for y1.
    linewidth2: float = 1
        The width of the line for y2.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> series_x1 = ds.datetime_data()
    >>> series_x2 = ds.datetime_data()
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    ...     X1=series_x1,
    ...     X2=series_x2,
    ...     y1=series_y1,
    ...     y2=series_y2
    ... )

    >>> import datasense as ds
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    ...     X1=series_x1,
    ...     X2=series_x2,
    ...     y1=series_y1,
    ...     y2=series_y2,
    ...     smoothing="natural_cubic_spline",
    ...     number_knots=7
    ... )

    >>> import datasense as ds
    >>> series_x1 = ds.random_data(distribution="uniform").sort_values()
    >>> series_x2 = ds.random_data(distribution="uniform").sort_values()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    ...     X1=series_x1,
    ...     X2=series_x2,
    ...     y1=series_y1,
    ...     y2=series_y2,
    ...     figsize=(8, 5),
    ...     marker1="o",
    ...     marker2="+",
    ...     markersize1=8,
    ...     markersize2=12,
    ...     colour1=colour_red,
    ...     colour2=colour_magenta,
    ...     labellegendy1="y1",
    ...     labellegendy2="y2"
    ... )
    >>> ax.legend(frameon=False) # doctest: +SKIP

    >>> import datasense as ds
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    ...     X1=series_x1,
    ...     X2=series_x2,
    ...     y1=series_y1,
    ...     y2=series_y2,
    ...     figsize=(8, 5),
    ...     marker1="o",
    ...     marker2="+",
    ...     markersize1=8,
    ...     markersize2=12,
    ...     colour1=colour_red,
    ...     colour2=colour_magenta,
    ...     labellegendy1="y1",
    ...     labellegendy2="y2",
    ...     smoothing="natural_cubic_spline",
    ...     number_knots=7
    ... )
    >>> ax.legend(frameon=False) # doctest: +SKIP
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if (X1.dtype and X2.dtype) in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X1,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X2,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2,
        )
    elif smoothing == "natural_cubic_spline":
        if (X1.dtype and X2.dtype) in ["datetime64[ns]"]:
            XX1 = pd.to_numeric(X1)
            XX2 = pd.to_numeric(X2)
            fig.autofmt_xdate()
        else:
            XX1 = X1
            XX2 = X2
        model1 = natural_cubic_spline(X=XX1, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX2, y=y2, number_knots=number_knots)
        ax.plot(
            X1,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X2,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2,
        )
        ax.plot(
            X1,
            model1.predict(XX1),
            marker=marker1,
            markersize=0,
            linestyle="-",
            linewidth=linewidth1,
            color=colour1,
        )
        ax.plot(
            X2,
            model2.predict(XX2),
            marker=marker2,
            markersize=0,
            linestyle="-",
            linewidth=linewidth2,
            color=colour2,
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_line_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    y1_marker: str = ".",
    y2_marker: str = "",
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Scatter plot of y1 versus X.
    Line plot of y2 versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The series for the horizontal axis.
    y1: pd.Series
        The series for y1 to plot on the vertical axis.
    y2: pd.Series
        The series for y2 to plot on the vertical axis.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots to create.
    marker: str = None
        The type of marker
    colour1: str = colour_blue
        The colour of y1.
    colour2: str = colour_cyan
        The colour of y2.
    labellegendy1: str = None
        The legend for y1.
    labellegendy2: str = None
        The legend for y2.
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> number_knots = 100
    >>> figsize = (6, 4)
    >>> X = ds.random_data(distribution="uniform").sort_values()
    >>> y = ds.random_data(distribution="norm")
    >>> model = ds.natural_cubic_spline(
    ...     X=X,
    ...     y=y,
    ...     number_knots=number_knots
    ... )
    >>> fig, ax = ds.plot_scatter_line_x_y1_y2(
    ...     X=X,
    ...     y1=y,
    ...     y2=model.predict(X),
    ...     figsize=figsize,
    ...     labellegendy2=f'number knots = {number_knots}'
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y1,
            marker=y1_marker,
            linestyle="",
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X,
            y2,
            marker=y2_marker,
            linestyle="-",
            color=colour2,
            label=labellegendy2,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax.plot(
            X,
            model1.predict(XX),
            marker=y1_marker,
            linestyle="",
            color=colour1,
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=y2_marker,
            linestyle="-",
            color=colour2,
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_line_y1_y2(
    *,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker1: str = ".",
    marker2: str = ".",
    markersize1: int = 8,
    markersize2: int = 8,
    linestyle1: str = "-",
    linestyle2: str = "-",
    linewidth1: float = 1,
    linewidth2: float = 1,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
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
    y1: pd.Series
        The data to plot on the ordinate.
    y2: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    marker1: str = "."
        The type of plot point for y1.
    marker2: str = "."
        The type of plot point for y2.
    markersize1: int = 8
        The size of the plot point for y1 (pt).
    markersize2: int = 8
        The size of the plot point for y2 (pt).
    linestyle1: str = "_"
        The style of the line for y1.
    linestyle2: str = "_"
        The style of the line for y2.
    linewidth1: float = 1
        The width of the line for y1.
    linewidth2: float = 1
        The width of the line for y2.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_line_line_y1_y2(
    ...     y1=series_y1,
    ...     y2=series_y2
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
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
            label=labellegendy1,
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2,
        )
    elif smoothing == "natural_cubic_spline":
        model1 = natural_cubic_spline(X=X, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=X, y=y2, number_knots=number_knots)
        ax.plot(
            X, model1.predict(X), marker=None, linestyle="-", color=colour1
        )
        ax.plot(
            X, model2.predict(X), marker=None, linestyle="-", color=colour2
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_line_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker1: str = ".",
    marker2: str = ".",
    markersize1: int = 8,
    markersize2: int = 8,
    linestyle1: str = "-",
    linestyle2: str = "-",
    linewidth1: float = 1,
    linewidth2: float = 1,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Line plot of y1 versus X.
    Line plot of y2 versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the y1 ordinate.
    y2: pd.Series
        The data to plot on the y2 ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply. Options: "natural_cubic_spline"
    number_knots: int = None
        the number of knows for natural cubic spline smoothing.
    marker1: str = "."
        The type of plot point for y1.
    marker2: str = "."
        The type of plot point for y2.
    markersize1: int = 8
        The size of the plot point for y1.
    markersize2: int = 8
        The size of the plot point for y2.
    linestyle1: str = "-"
        The style of the line for y1.
    linestyle2: str = "-"
        The style of the line for y2.
    linewidth1: float = 1
        The width of the line for y1.
    linewidth2: float = 1
        The width of the line for y2.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.
    remove_spines: booll = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> figsize = (6, 4)
    >>> X = ds.datetime_data()
    >>> y1 = ds.random_data()
    >>> y2 = ds.random_data()
    >>> fig, ax = ds.plot_line_line_x_y1_y2(
    ...     X=X,
    ...     y1=y1,
    ...     y2=y2,
    ...     figsize=figsize
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y1,
            marker=marker1,
            markersize=markersize1,
            linestyle=linestyle1,
            linewidth=linewidth1,
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X,
            y2,
            marker=marker2,
            markersize=markersize2,
            linestyle=linestyle2,
            linewidth=linewidth2,
            color=colour2,
            label=labellegendy2,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax.plot(
            X, model1.predict(XX), marker=None, linestyle="-", color=colour1
        )
        ax.plot(
            X, model2.predict(XX), marker=None, linestyle="-", color=colour2
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_line_line_x_y1_y2_y3(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    y3: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    colour3: str = colour_teal,
    labellegendy1: str = None,
    labellegendy2: str = None,
    labellegendy3: str = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Line plot of y1 versus X.
    Line plot of y2 versus X.
    Line plot of y3 versus X.
    Optional smoothing applied to y1, y2, y3.

    This graph is useful if y1, y2, and y3 have the same units.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the y1 ordinate.
    y2: pd.Series
        The data to plot on the y2 ordinate.
    y3: pd.Series
        The data to plot on the y3 ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        the number of knows for natural cubic spline smoothing.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    colour2: str = colour_teal
        The colour of the line for y2.
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.
    labellegendy3: str = None
        The legend label of the line y3.
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> import pandas as pd
    >>> figsize = (6, 4)
    >>> df = pd.DataFrame(data={
    ...     'x1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ...     'y1': [
    ...         8000, 9000, 10000, 11000, 12000,
    ...         13000, 14000, 15000, 16000, 17000
    ...     ],
    ...     'y2': [
    ...         7630.59, 12091.24, 12610.42, 14382.62, 23275.12,
    ...         21676.23, 22264.38, 20776.82, 21384.69, 17041.38
    ...     ]
    ... }).sort_values(by=["x1"])
    >>> x1 = df["x1"]
    >>> y1 = df["y1"]
    >>> y2 = df["y2"]
    >>> (
    ...     fitted_model, predictions, confidence_interval_lower,
    ...     confidence_interval_upper, prediction_interval_lower,
    ...     prediction_interval_upper
    ... ) = ds.linear_regression(
    ...     X=x1,
    ...     y=y2
    ... )
    >>> fig, ax = ds.plot_line_line_line_x_y1_y2_y3(
    ...     X=x1,
    ...     y1=y1,
    ...     y2=y2,
    ...     y3=predictions,
    ...     figsize=figsize,
    ...     labellegendy1="target",
    ...     labellegendy2="actual",
    ...     labellegendy3="predicted"
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X,
            y1,
            marker=None,
            linestyle="-",
            color=colour1,
            label=labellegendy1,
        )
        ax.plot(
            X,
            y2,
            marker=None,
            linestyle="-",
            color=colour2,
            label=labellegendy2,
        )
        ax.plot(
            X,
            y3,
            marker=None,
            linestyle="-",
            color=colour3,
            label=labellegendy3,
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        model3 = natural_cubic_spline(X=XX, y=y3, number_knots=number_knots)
        ax.plot(
            X, model1.predict(XX), marker=None, linestyle="-", color=colour1
        )
        ax.plot(
            X, model2.predict(XX), marker=None, linestyle="-", color=colour2
        )
        ax.plot(
            X, model3.predict(XX), marker=None, linestyle="-", color=colour3
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatterleft_scatterright_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    linestyle1: str = "None",
    linestyle2: str = "None",
) -> tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    Scatter plot of y1 left vertical axis versus X.
    Scatter plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the y1 ordinate.
    y2: pd.Series
        The data to plot on the y2 ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        the number of knows for natural cubic spline smoothing.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    linestyle1: str = "None"
        The style of the line for y1.
    linestyle2: str = "None"
        The style of the line for y2.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> X = ds.random_data(distribution="randint").sort_values()
    >>> y1 = ds.random_data(distribution="norm")
    >>> y2 = ds.random_data(distribution="norm")
    >>> fig, ax1, ax2 = ds.plot_scatterleft_scatterright_x_y1_y2(
    ...     X=X,
    ...     y1=y1,
    ...     y2=y2,
    ...     figsize=(6, 4),
    ...     linestyle2="-"
    ... )
    """
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax1)
        ax1.plot(X, y1, marker=".", linestyle=linestyle1, color=colour1)
        ax2.plot(X, y2, marker=".", linestyle=linestyle2, color=colour2)
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax1.plot(
            X,
            model1.predict(XX),
            marker=".",
            linestyle=linestyle1,
            color=colour1,
        )
        ax2.plot(
            X,
            model2.predict(XX),
            marker=".",
            linestyle=linestyle2,
            color=colour2,
        )
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    return (fig, ax1, ax2)


def plot_lineleft_lineright_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    linestyle1: str = "-",
    linestyle2: str = "-",
    marker1: str = ".",
    marker1size: float = 8,
    marker2: str = ".",
    marker2size: float = 8,
    labellegendy1: str = None,
    labellegendy2: str = None,
    xticklabels_rotation = None,
    defaultfmt = "%Y-%m-%d",
) -> tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    Line plot of y1 left vertical axis versus X.
    Line plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the ordinate.
    y2: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    linestyle1: str = "-"
        The style of the line for y1.
    linestyle2: str = "-"
        The style of the line for y2.
    marker1: str = "."
        The type of plot point for y1.
    markersize1: int = 8
        The size of the plot point for y1 (pt).
    marker2: str = "."
        The type of plot point for y2.
    markersize2: int = 8
        The size of the plot point for y2 (pt).
    labellegendy1: str = None
        The legend label of the line y1.
    labellegendy2: str = None
        The legend label of the line y2.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> import pandas as pd
    >>> figsize = (6, 4)
    >>> df = pd.DataFrame(data={
    ...     "X": [
    ...         "2018-07-31", "2018-08-04", "2018-08-06", "2018-08-11",
    ...         "2018-08-12", "2018-08-15", "2018-08-16", "2018-08-17",
    ...         "2018-08-18", "2018-08-25", "2018-09-15"
    ...     ],
    ...     "y1": [10, 15, 30, 35, 40, 45, 40, 30, 35, 50, 75],
    ...     "y2": [20, 35, 20, 15, 30, 45, 50, 40, 45, 50, 65]
    ... })
    >>> fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
    ...     X=df["X"],
    ...     y1=df["y1"],
    ...     y2=df["y2"],
    ...     figsize=figsize
    ... )

    >>> import datasense as ds
    >>> import pandas as pd
    >>> figsize = (6, 4)
    >>> df = pd.DataFrame(data={
    ...     "X": [
    ...         "2018-07-31", "2018-08-04", "2018-08-06", "2018-08-11",
    ...         "2018-08-12", "2018-08-15", "2018-08-16", "2018-08-17",
    ...         "2018-08-18", "2018-08-25", "2018-09-15"
    ...     ],
    ...     "y1": [10, 15, 30, 35, 40, 45, 40, 30, 35, 50, 75],
    ...     "y2": [20, 35, 20, 15, 30, 45, 50, 40, 45, 50, 65]
    ... })
    >>> df["X"] = pd.to_datetime(df["X"])
    >>> fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
    ...     X=df["X"],
    ...     y1=df["y1"],
    ...     y2=df["y2"],
    ...     smoothing="natural_cubic_spline",
    ...     number_knots=5,
    ...     figsize=figsize
    ... )
    """
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax1, defaultfmt=defaultfmt)
        ax1.plot(X, y1, color=colour1, marker=marker1, markersize=marker1size, label=labellegendy1)
        ax2.plot(X, y2, color=colour2, marker=marker2, markersize=marker2size, label=labellegendy2)
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax1.plot(X, model1.predict(XX), color=colour1, linestyle=linestyle1)
        ax2.plot(X, model2.predict(XX), color=colour2, linestyle=linestyle2)
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    mpla.setp(
        obj=ax1.get_xticklabels(),
        rotation=xticklabels_rotation,
        ha="right",
        rotation_mode="anchor",
    )
    plt.close("all")
    return (fig, ax1, ax2)


def plot_barleft_lineright_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    barwidth: float = 10,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    linestyle1: str = "-",
    linestyle2: str = "-",
    marker2: str = "o",
) -> tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    Bar plot of y1 left vertical axis versus X.
    Line plot of y2 right vertical axis versus X.
    Optional smoothing applied to y1, y2.

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X: pd.Series
        The data to plot on the abscissa.
    y1: pd.Series
        The data to plot on the ordinate.
    y2: pd.Series
        The data to plot on the ordinate.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing: str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots: int = None
        The number of knots for natural cubic spline smoothing.
    barwidth: float = 10
        The width of the bars.
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    linestyle1: str = "-"
        The style of the line for y1.
    linestyle2: str = "-"
        The style of the line for y2.
    marker2: str = "o"
        The type of plot point for y2.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> X = ds.datetime_data()
    >>> y1 = ds.random_data()
    >>> y2 = ds.random_data()
    >>> figsize = (6, 4)
    >>> fig, ax1, ax2 = ds.plot_barleft_lineright_x_y1_y2(
    ...     X=X,
    ...     y1=y1,
    ...     y2=y2,
    ...     figsize=figsize,
    ...     barwidth=20,
    ...     colour1="#cc3311",
    ...     colour2="#ee3377"
    ... )
    """
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax1)
        ax1.bar(X, y1, barwidth, color=colour1)
        ax2.plot(X, y2, color=colour2, marker=marker2)
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(X=XX, y=y1, number_knots=number_knots)
        model2 = natural_cubic_spline(X=XX, y=y2, number_knots=number_knots)
        ax1.plot(X, model1.predict(XX), color=colour1, linestyle=linestyle1)
        ax2.plot(X, model2.predict(XX), color=colour2, linestyle=linestyle2)
    for tl in ax1.get_yticklabels():
        tl.set_color(colour1)
    for tl in ax2.get_yticklabels():
        tl.set_color(colour2)
    return (fig, ax1, ax2)


def plot_pareto(
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: tuple[float, float] = None,
    width: float = 0.8,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
) -> tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    Parameters
    ----------
    X: pd.Series
        The data to plot on the ordinate.
    y: pd.Series
        The data to plot on the abscissa.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    width: float = 0.8
        The width of the bars (in).
    colour1: str = colour_blue
        The colour of the line for y1.
    colour2: str = colour_cyan
        The colour of the line for y2.
    marker: str = "."
        The type of plot point.
    markersize: float = 8
        The size of the plot point (pt).
    linestyle: str = "-"
        The style of the line joining the points.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> data = pd.DataFrame(
    ...     {
    ...         "ordinate": ["Mo", "Larry", "Curly", "Shemp", "Joe"],
    ...         "abscissa": [21, 2, 10, 4, 16]
    ...     }
    ... )
    >>> fig, ax1, ax2 = ds.plot_pareto(
    ...     X=data["ordinate"],
    ...     y=data["abscissa"]
    ... )
    """
    df = pd.concat([X, y], axis=1).sort_values(
        by=y.name, axis=0, ascending=False, kind="mergesort"
    )
    total_y = df[y.name].sum()
    df["percentage"] = df[y.name] / total_y * 100
    df["cumulative_percentage"] = df["percentage"].cumsum(skipna=True)
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax2 = ax1.twinx()
    ax1.bar(x=df[X.name], height=df[y.name], width=width, color=colour1)
    ax2.plot(
        df[X.name],
        df["cumulative_percentage"],
        marker=marker,
        markersize=markersize,
        linestyle=linestyle,
        color=colour2,
    )
    return (fig, ax1, ax2)


def format_dates(
    *,
    fig: plt.Figure,
    ax: axes.Axes,
    defaultfmt: str = "%Y-%m-%d"
) -> None:
    """
    Format dates and ticks for plotting.

    Parameters
    ----------
    fig: plt.Figure
        A matplotlib figure.
    ax: axes.Axes
        A matplotlib Axes.
    defaultfmt: str = "%Y-%m-%d"
        The date string.

    Example
    -------

    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ds.format_dates(
    ...     fig=fig,
    ...     ax=ax
    ... )
    """
    loc = mdates.AutoDateLocator()
    fmt = mdates.AutoDateFormatter(locator=loc, defaultfmt=defaultfmt)
    ax.xaxis.set_major_locator(locator=loc)
    ax.xaxis.set_major_formatter(formatter=fmt)
    fig.autofmt_xdate()


def probability_plot(
    *,
    data: pd.Series,
    figsize: tuple[float, float] = None,
    distribution: object = norm,
    fit: bool = True,
    plot: object = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Plot a probability plot of data against the quantiles of a specified
    theoretical distribution.

    Parameters
    ----------
    data: pd.Series
        A pandas Series.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    distribution: object = norm
        Fit a normal distribution by default.
    fit: bool = True
        Fit a least-squares regression line to the data if True.
    plot: object = None
        If given, plot the quantiles and least-squares fit.
    colour1: str = colour_blue,
        The colour of line 1.
    colour2: str = colour_cyan
        The colour of line 2.
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> data = ds.random_data()
    >>> fig, ax = ds.probability_plot(data=data)
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    (osm, osr), (slope, intercept, r) = probplot(
        x=data, dist=distribution, fit=True, plot=ax
    )
    ax.get_lines()[0].set(color=colour1, markersize=4)
    ax.get_lines()[1].set(color=colour2)
    if fit:
        r_squared = r * r
        equation = f"$r^2 = {r_squared:.3f}$"
        despine(ax=ax)
        text = AnchoredText(s=equation, loc="upper left", frameon=False)
        ax.add_artist(a=text)
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def despine(*, ax: axes.Axes) -> None:
    """
    Remove the top and right spines of a graph.

    Parameters
    ----------
    ax: axes.Axes
        A matplotlib Axes.

    Example
    -------

    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> despine(ax=ax)
    """
    ax.spines[["top", "right"]].set_visible(b=False)


def plot_histogram(
    *,
    series: pd.Series,
    number_bins: int = None,
    bin_range: tuple[int, int] | tuple[int, int] = None,
    figsize: tuple[float, float] = None,
    bin_width: int = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    bin_label_bool: bool = False,
    color: str = colour_blue,
    remove_spines: bool = True,
    probability_density_function: bool = False,
    percentiles: tuple[float, float] = None,
    percentiles_colour: str = colour_red,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    series: pd.Series
        The input series.
    number_bins: int = None
        The number of equal-width bins in the range s.max() - s.min().
    bin_range: tuple[int, int] | tuple[int, int] = None
        The lower and upper range of the bins. If not provided, range is
        (s.min(), s.max()).
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    bin_width: int = None
        The width of the bin in same units as the series s.
    edgecolor: str = colour_white
        The hexadecimal color value for the bar edges.
    linewidth: int = 1
        The bar edges line width (point).
    bin_label_bool: bool = False
        If True, label the bars with count and percentage of total.
    color: str = colour_blue
        The color of the bar faces.
    remove_spines: bool = True
        If True, remove top and right spines of axes.
    probability_density_function: bool = False
        If True, a density parameter normalizes the bin heights so that the
        integral of the histogram is 1. The resulting histogram is an
        approximation of the probability density function.
    percentiles: tuple[float, float] = [0.025, 0.975]
        The percentiles for plotting vertical lines on the histogram.
    percentiles_colour: str = colour_red
        The colour of the vertical lines for the percentiles.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    Create a series of random floats, normal distribution, with the default
    parameters.

    >>> import datasense as ds
    >>> s = ds.random_data()
    >>> fig, ax = ds.plot_histogram(series=s)

    Create a series of random integers, integer distribution, size = 113,
    min = 0, max = 13.

    >>> import datasense as ds
    >>> s = ds.random_data(
    ...     distribution="randint",
    ...     size=113,
    ...     low=0,
    ...     high=14
    ... )
    >>> fig, ax = ds.plot_histogram(series=s)

    Create a series of random integers, integer distribution, size = 113,
    min = 0, max = 13.
    Set histogram parameters to control bin width.

    >>> import datasense as ds
    >>> s = ds.random_data(
    ...     distribution="randint",
    ...     size=113,
    ...     low=0,
    ...     high=14
    ... )
    >>> fig, ax = ds.plot_histogram(
    ...     series=s,
    ...     bin_width=1
    ... )

    Create a series of random integers, integer distribution, size = 113,
    min = 0, height = 14.
    Set histogram parameters to control bin width and plotting range.

    >>> import datasense as ds
    >>> s = ds.random_data(
    ...     distribution="randint",
    ...     size=113,
    ...     low=0,
    ...     high=13
    ... )
    >>> fig, ax = ds.plot_histogram(
    ...     series=s,
    ...     bin_width=1,
    ...     bin_range=(0, 10)
    ... )

    Create a series of random floats, size = 113,
    average = 69, standard deviation = 13.
    Set histogram parameters to control bin width and plotting range.

    >>> import datasense as ds
    >>> s = ds.random_data(
    ...     distribution="norm",
    ...     size=113,
    ...     loc=69,
    ...     scale=13
    ... )
    >>> fig, ax = ds.plot_histogram(
    ...     series=s,
    ...     bin_width=5,
    ...     bin_range=(30, 110)
    ... )

    Create a series of random floats, size = 113,
    average = 69, standard deviation = 13.
    Set histogram parameters to control bin width, plotting range, labels.
    Set colour of the bars.
    Plot the probability density function on top of the histogram.

    >>> import datasense as ds
    >>> s = ds.random_data(
    ...     distribution="norm",
    ...     size=113,
    ...     loc=69,
    ...     scale=13
    ... )
    >>> fig, ax = ds.plot_histogram(
    ...     series=s,
    ...     bin_width=5,
    ...     bin_range=(30, 110),
    ...     figsize=(10,8),
    ...     bin_label_bool=True,
    ...     color="#33bbee"
    ... )
    >>> ax.set_xlabel(xlabel="X-axis label", labelpad=30) # doctest: +SKIP
    >>> plt.tight_layout()
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    if bin_width and not bin_range:
        x = (series.max() - series.min()) / bin_width
        number_bins = math.ceil(x)
    elif bin_width and bin_range:
        number_bins = int((bin_range[1] - bin_range[0]) / bin_width)
        bin_range = bin_range
    counts, bins, patches = ax.hist(
        x=series,
        bins=number_bins,
        range=bin_range,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color,
        density=True,
    )
    if probability_density_function:
        series_std_dev = series.std()
        series_ave = series.mean()
        y_fit = (1 / (np.sqrt(2 * np.pi) * series_std_dev)) * np.exp(
            -0.5 * (1 / series_std_dev * (bins - series_ave)) ** 2
        )
        ax.plot(bins, y_fit, linestyle="--", color="r")
    if bin_label_bool:
        ax.set_xticks(ticks=bins)
        ax.xaxis.set_major_formatter(
            formatter=StrMethodFormatter(fmt="{x:0.0f}")
        )
        bin_centers = 0.5 * np.diff(bins) + bins[:-1]
        for count, x in zip(counts, bin_centers):
            ax.annotate(
                text=f"{str(int(count))}",
                xy=(x, 0),
                xytext=(0, -18),
                xycoords=("data", "axes fraction"),
                textcoords="offset points",
                va="top",
                ha="center",
            )
            percent = f"{(100 * float(count) / counts.sum()):0.0f} %"
            ax.annotate(
                text=percent,
                xy=(x, 0),
                xytext=(0, -32),
                xycoords=("data", "axes fraction"),
                textcoords="offset points",
                va="top",
                ha="center",
            )
    if remove_spines:
        despine(ax=ax)
    if percentiles:
        ax.axvline(series.quantile(q=percentiles[0]), color=percentiles_colour)
        ax.axvline(series.quantile(q=percentiles[1]), color=percentiles_colour)
    return (fig, ax)


def plot_horizontal_bars(
    *,
    y: list[int] | list[float] | list[str],
    width: list[int] | list[float],
    height: float = 0.8,
    figsize: tuple[float, float] = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    color: str = colour_blue,
    left: datetime | int | float = None,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    y: list[int] | list[float] | list[str],
        The y coordinates of the bars.
    width: list[int] | list[float],
        The width(s) of the bars.
    height: float = 0.8,
        The height of the bars.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    edgecolor: str = colour_white,
        The hexadecimal color value for the bar edges.
    linewidth: int = 1,
        The bar edges line width (point).
    color: str = colour_blue
        The color of the bar faces.
    left: datetime | int | float = None
        The x coordinates of the left sides of the bars.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> y = ["Yes", "No"]
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    ...     y=y,
    ...     width=width
    ... )

    >>> import datasense as ds
    >>> y = ["Yes", "No"]
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    ...     y=y,
    ...     width=width,
    ...     height=0.4
    ... )

    Create Gantt chart

    >>> import datasense as ds
    >>> import datetime
    >>> data = {
    ...     "start": ["2021-11-01", "2021-11-03", "2021-11-04", "2021-11-08"],
    ...     "end": ["2021-11-08", "2021-11-16", "2021-11-11", "2021-11-13"],
    ...     "task": ["task 1", "task 2", "task 3", "task 4"]
    ... }
    >>> columns = ["task", "start", "end", "duration", "start_relative"]
    >>> data_types = {
    ...     "start": "datetime64[ns]",
    ...     "end": "datetime64[ns]",
    ...     "task": "str"
    ... }
    >>> df = (pd.DataFrame(data=data)).astype(dtype=data_types)
    >>> df[columns[3]] = (df[columns[2]] - df[columns[1]]).dt.days + 1
    >>> df = df.sort_values(
    ...     by=[columns[1]],
    ...     axis=0,
    ...     ascending=[True]
    ... )
    >>> start = df[columns[1]].min()
    >>> end = df[columns[2]].max()
    >>> start = df[columns[1]].min()
    >>> duration = (end - start).days + 1
    >>> x_ticks = [x for x in range(duration + 1)]
    >>> x_labels = [
    ...     f"{(start + datetime.timedelta(days=x)):%Y-%m-%d}"
    ...     for x in x_ticks
    ... ]
    >>> df[columns[4]] = (df[columns[1]] - start).dt.days
    >>> fig, ax = ds.plot_horizontal_bars(
    ...     y=df[columns[0]],
    ...     width=df[columns[3]],
    ...     left=df[columns[4]]
    ... )
    >>> ax.invert_yaxis() # doctest: +SKIP
    >>> ax.set_xticks(ticks=x_ticks) # doctest: +SKIP
    >>> ax.set_xticklabels(labels=x_labels, rotation=45) # doctest: +SKIP
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.barh(
        y=y,
        width=width,
        height=height,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color,
        left=left,
    )
    return (fig, ax)


def plot_vertical_bars(
    *,
    x: list[int] | list[float] | list[str],
    height: list[int] | list[float],
    width: float = 0.8,
    figsize: tuple[float, float] = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    color: str = colour_blue,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x: list[int] | list[float] | list[str],
        The x coordinates of the bars.
    height: list[int] | list[float],
        The height(s) of the bars.
    width: float = 0.8,
        The width of the bars.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    edgecolor: str = colour_white,
        The hexadecimal color value for the bar edges.
    linewidth: int = 1,
        The bar edges line width (point).
    color: str = colour_blue
        The color of the bar faces.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> x = ["Yes", "No"]
    >>> height = [69, 31]
    >>> fig, ax = ds.plot_vertical_bars(
    ...     x=x,
    ...     height=height
    ... )

    >>> import datasense as ds
    >>> x = ["Yes", "No"]
    >>> height = [69, 31]
    >>> fig, ax = ds.plot_vertical_bars(
    ...     x=x,
    ...     height=height,
    ...     width=0.4
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.bar(
        x=x,
        height=height,
        width=width,
        edgecolor=edgecolor,
        linewidth=linewidth,
        color=color,
    )
    plt.close("all")
    return (fig, ax)


def plot_pie(
    *,
    x: list[int] | list[float],
    labels: list[int] | list[float] | list[str],
    figsize: tuple[float, float] = None,
    startangle: float = 0,
    colors: list[str] = None,
    autopct: str = "%1.1f%%",
) -> tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x: list[int] | list[float],
        The wedge sizes.
    labels: list[int] | list[float] | list[str],
        The labels of the wedges.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    startangle: float = 0,
        The start angle of the pie, counterclockwise from the x axis.
    colors: list[str] = None
        The color of the wedges.
    autopct: str = "%1.1f%%"
        Label the wedges with their numeric value. If None, no label.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Examples
    --------

    >>> import datasense as ds
    >>> x = [69, 31]
    >>> labels = ["Yes", "No"]
    >>> fig, ax = ds.plot_pie(
    ...     x=x,
    ...     labels=labels
    ... )

    >>> import datasense as ds
    >>> x = [69, 31]
    >>> labels = ["Yes", "No"]
    >>> fig, ax = ds.plot_pie(
    ...     x=x,
    ...     labels=labels,
    ...     startangle=90,
    ...     colors=[
    ...         colour_blue, colour_cyan, colour_teal, colour_orange,
    ...         colour_red, colour_magenta, colour_grey
    ...     ]
    ... )
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.pie(
        x=x,
        labels=labels,
        startangle=startangle,
        colors=colors,
        autopct=autopct,
    )
    return (fig, ax)


def waterfall(
    *,
    df: pd.DataFrame,
    path_in: Path | str,
    xticklabels_rotation: float = 45,
    last_column: str = "NET",
    ylim_min: float | None = None,
    ylim_max: float | None = None,
    positive_colour: str = "green",
    negative_colour: str = "red",
    first_bar_colour: str = "blue",
    last_bar_colour: str = "blue",
    grid_alpha: float = 0.2,
    graph_format: str = "svg",
    title: str = "Waterfall Chart",
) -> pd.DataFrame:
    """
    Create a waterfall chart, to understand the cumulative effect of
    sequentially introduced positive or negative values.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to convert to a waterfall DataFrame.
    path_in: Path | str
        The path of the data file.
    xticklabels_rotation: float = 45
        The angle to rotate the xticklabels.
    last_column: str = "NET"
        The name of the last column in the waterfall chart.
    ylim_min: float | None = None
        The lower limit of the y axis.
    ylim_max: float | None = None
        The upper limit of the y axis.
    positive_colour: str = "green"
        The colour of the positive bars.
    negative_colour: str = "red"
        The colour of the negative bars.
    first_bar_colour: str = "blue"
        The colour of the first bar.
    last_bar_colour: str = "blue"
        The colour of the last bar.
    grid_alpha: float = 0.2
        The fraction of the full colour of the grid.
    graph_format: str = "svg"
        The output format of the graph.
    title: str = "Waterfall Chart"
        The title on the graph.

    Returns
    -------
    df: pd.DataFrame
        The waterfall DataFrame.

    Example
    -------
    Budget waterfall chart

    >>> import pandas as pd
    # the df shown here is a proxy for waterfall_budget.xlsx
    >>> df = pd.DataFrame(data={
    ...     'Categories': [
    ...         'Base', 'Inflation', 'Merit Raises',
    ...         'Market Wages', 'Volume', 'Fuel',
    ...         'Other', 'Compliance', 'Reorganization',
    ...         'Consolidations', 'Initiative Savings',
    ...         'Consultants'
    ...     ],
    ...     'Amount ($MM)': [
    ...         423.5, 11.7, 2.9, 1.1, 1.5, 0.1,
    ...         5.3, 1.1, -2.7, -23.3, -6.4, -8
    ...     ],
    ... })
    >>> df = ds.waterfall(
    ...     df=df,
    ...     path_in="waterfall_budget.xls"
    ...     ylim_min=400,
    ...     ylim_max=455,
    ... )
    """
    path_in = Path(path_in)
    xlabel = df.columns[0]
    ylabel = df.columns[-1]
    df = df.set_index(df.columns[0])
    amount = df.columns[0]
    df_blank = df[amount].cumsum().shift(1).fillna(0)
    df_total = df.sum()[amount]
    df.loc[last_column] = df_total
    df_blank.loc[last_column] = df_total
    # step is a Series
    step = df_blank.reset_index(drop=True).repeat(3).shift(-1)
    step[1::3] = np.nan
    df_blank.loc[last_column] = 0
    fig, ax = plt.subplots()
    x = df.index  # bar positions
    # create the waterfall chart, no need for a stacked argument
    ax.bar(x=x, height=df[amount], width=0.4, bottom=df_blank)
    ax.set_ylim(ylim_min, ylim_max)
    # set bar colors based on values
    for i, p in enumerate(ax.patches):
        if df.iloc[i][amount] > 0:
            p.set_facecolor(positive_colour)
        else:
            p.set_facecolor(negative_colour)
    # Change color of the first and last bars
    # ax.patches contains a list of bar objects in the plot
    ax.patches[0].set_facecolor(first_bar_colour)
    ax.patches[-1].set_facecolor(last_bar_colour)
    ax.plot(step.index, step.values, "b", linewidth=0.5)
    ax.tick_params(axis="x", labelsize=14, labelrotation=90)
    ax.tick_params(axis="y", labelsize=14)
    ax.grid(visible=True, which="major", axis="y", alpha=grid_alpha)
    ax.set_ylabel(ylabel=ylabel, weight="bold", fontsize=16)
    ax.set_xlabel(xlabel=xlabel, weight="bold", fontsize=16)
    ax.set_title(label=title, weight="bold", fontsize=18)
    despine(ax=ax)
    mpla.setp(
        obj=ax.get_xticklabels(),
        rotation=xticklabels_rotation,
        ha="right",
        rotation_mode="anchor",
    )
    path_graph = path_in.with_suffix("." + graph_format)
    fig.savefig(fname=path_graph, format=graph_format, bbox_inches="tight")
    html_ds.html_figure(file_name=path_graph)
    return df


def plot_stacked_bars(
    *,
    x: list[int] | list[float] | list[str],
    height1: list[int] | list[float],
    label1: str = None,
    height2: list[int] | list[float] = None,
    label2: str = None,
    height3: list[int] | list[float] = None,
    label3: str = None,
    height4: list[int] | list[float] = None,
    label4: str = None,
    height5: list[int] | list[float] = None,
    label5: str = None,
    height6: list[int] | list[float] = None,
    label6: str = None,
    height7: list[int] | list[float] = None,
    label7: str = None,
    width: float = 0.8,
    figsize: tuple[float, float] = None,
    color: [list[str]] = [
        colour_blue,
        colour_cyan,
        colour_teal,
        colour_orange,
        colour_red,
        colour_magenta,
        colour_grey,
    ],
) -> tuple[plt.Figure, axes.Axes]:
    """
    Stacked vertical bar plot of up to seven levels per bar.

    Parameters
    ----------
    x: list[int] | list[float] | list[str],
        The x coordinates of the bars.
    height1: list[int] | list[float],
        The height of the level 1 bars.
    label1: str = None,
        The label of the level 1 bars.
    height2: list[int] | list[float],
        The height of the level 2 bars.
    label2: str = None,
        The label of the level 2 bars.
    height3: list[int] | list[float],
        The height of the level 3 bars.
    label3: str = None,
        The label of the level 3 bars.
    height4: list[int] | list[float],
        The height of the level 4 bars.
    label4: str = None,
        The label of the level 4 bars.
    height5: list[int] | list[float],
        The height of the level 5 bars.
    label5: str = None,
        The label of the level 5 bars.
    height6: list[int] | list[float],
        The height of the level 6 bars.
    label6: str = None,
        The label of the level 6 bars.
    height7: list[int] | list[float],
        The height of the level 7 bars.
    label7: str = None,
        The label of the level 7 bars.
    width: float = 0.8,
        The width of the bars.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    color: str = [
        colour_blue, colour_cyan, colour_teal, colour_orange, colour_red,
        colour_magenta, colour_grey
    ]
        The color of the bar faces, up to seven levels.

    Returns
    -------
    fig, ax: tuple[plt.Figure, axes.Axes]

    Examples
    --------

    >>> import datasense as ds
    >>> x = ["G1", "G2", "G3", "G4", "G5"]
    >>> height1 = [20, 35, 30, 35, 27]
    >>> label1 = "A"
    >>> width = 0.35
    >>> height2 = [25, 32, 34, 20, 25]
    >>> label2 = "B"
    >>> fig, ax = ds.plot_stacked_bars(
    ...     x=x,
    ...     height1=height1,
    ...     label1=label1,
    ...     height2=height2,
    ...     label2=label2
    ... )
    >>> fig.legend(frameon=False, loc="upper right") # doctest: +SKIP

    >>> import datasense as ds
    >>> x = ["G1", "G2", "G3", "G4", "G5"]
    >>> height1 = [20, 35, 30, 35, 27]
    >>> label1 = "A"
    >>> width = 0.35
    >>> height2 = [25, 32, 34, 20, 25]
    >>> label2 = "B"
    >>> height3 = [30, 34, 23, 27, 32]
    >>> label3 = "C"
    >>> height4 = [30, 34, 23, 27, 32]
    >>> label4 = "D"
    >>> height5 = [30, 34, 23, 27, 32]
    >>> label5 = "E"
    >>> height6 = [30, 34, 23, 27, 32]
    >>> label6 = "F"
    >>> height7 = [30, 34, 23, 27, 32]
    >>> label7 = "G"
    >>> fig, ax = ds.plot_stacked_bars(
    ...     x=x,
    ...     height1=height1,
    ...     label1=label1,
    ...     width=width,
    ...     figsize=(9, 6),
    ...     height2=height2,
    ...     label2=label2,
    ...     height3=height3,
    ...     label3=label3,
    ...     height4=height4,
    ...     label4=label4,
    ...     height5=height5,
    ...     label5=label5,
    ...     height6=height6,
    ...     label6=label6,
    ...     height7=height7,
    ...     label7=label7,
    ... )
    >>> fig.legend(frameon=False, loc="upper right") # doctest: +SKIP
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.bar(x=x, height=height1, label=label1, width=width, color=color[0])
    if label2:
        ax.bar(
            x=x,
            height=height2,
            label=label2,
            width=width,
            bottom=height1,
            color=color[1],
        )
    if label3:
        bottom = np.add(height1, height2).tolist()
        ax.bar(
            x=x,
            height=height3,
            label=label3,
            width=width,
            bottom=bottom,
            color=color[2],
        )
    if label4:
        bottom = np.add(bottom, height3).tolist()
        ax.bar(
            x=x,
            height=height4,
            label=label4,
            width=width,
            bottom=bottom,
            color=color[3],
        )
    if label5:
        bottom = np.add(bottom, height4).tolist()
        ax.bar(
            x=x,
            height=height5,
            label=label5,
            width=width,
            bottom=bottom,
            color=color[4],
        )
    if label6:
        bottom = np.add(bottom, height5).tolist()
        ax.bar(
            x=x,
            height=height6,
            label=label6,
            width=width,
            bottom=bottom,
            color=color[5],
        )
    if label7:
        bottom = np.add(bottom, height6).tolist()
        ax.bar(
            x=x,
            height=height7,
            label=label7,
            width=width,
            bottom=bottom,
            color=color[6],
        )
    return (fig, ax)


def qr_code(*, qr_code_string: str, qr_code_path: Path) -> None:
    """
    Create a QR code and save as .svg and .png.

    Parameters
    ----------
    qr_code_string: str
        Text for the QR code
    qr_code_path: Path
        Text for the path

    Example
    -------

    >>> import datasense as ds
    >>> code_string = "mystring"
    >>> code_path = Path("str_of_path")
    >>> ds.qr_code(qr_code_string=code_string, qr_code_path=code_path)
    """
    pq.create(content=qr_code_string).svg(
        qr_code_path.with_suffix(".svg"), scale=4
    )
    pq.create(content=qr_code_string).png(
        qr_code_path.with_suffix(".png"), scale=4
    )


def plot_boxplot(
    *,
    series: pd.Series,
    notch: bool = True,
    showmeans: bool = None,
    figsize: tuple[float, float] = None,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Create a box-and-whisker plot with several elements:
    - minimum
    - first quartile
    - second quartile (median)
    - confidence interval of the second quartile
    - third quartile
    - maximum
    - outliers

    Parameters
    ----------
    series: pd.Series
        The input series.
    notch: bool = True,
        Boolean to show the confidence interval of the second quartile.
    showmeans: bool = None,
        Boolean to show average.
    figsize: tuple[float, float] = None,
        The (width, height) of the figure (in, in).
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    --------

    >>> import datasense as ds
    >>> series = ds.random_data()
    >>> fig, ax = ds.plot_boxplot(series=series)
    >>> ax.set_title(label="Box-and-whisker plot") # doctest: +SKIP
    >>> ax.set_xticks(ticks=[1], labels=["series"]) # doctest: +SKIP
    >>> ax.set_ylabel("y") # doctest: +SKIP
    >>> ds.despine(ax=ax) # doctest: +SKIP
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.boxplot(x=series, notch=notch, showmeans=showmeans)
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def dd_to_dms(dd: list[float]) -> list[tuple[int, int, float, str]]:
    """
    Converts a list of decimal degrees (DD) to a list of tuples containing
    degrees, minutes, and seconds (DMS).

    Parameters
    ----------
    dd: list[float]
        A list of two floats representing decimal degrees
        (latitude, longitude).

    Returns
    -------
    list[tuple[int, int, float, str]]
        A list of tuples containing degrees, minutes, seconds, and hemisphere
        (DMS) for latitude and longitude.

    Examples
    --------

    Ottawa Parliament

    >>> import datasense as ds
    >>> dd = [45.4250225, -75.6970594]
    >>> dsm = ds.dd_to_dms(dd=dd)
    >>> dms
    [(45, 25, 30.081, 'N'), (75, 41, 49.41384, 'W')]

    Effel Tower

    >>> dd = [48.858393, 2.257616]
    >>> dms = ds.dd_to_dms(dd=dd)
    >>> dms
    [(48, 51, 30.2148, 'N'), (2, 15, 27.4176, 'E')]

    Machu Pichu

    >>> dd = [-13.163194, -72.547842]
    >>> dms = ds.dd_to_dms(dd=dd)
    >>> dms
    [(13, 9, 47.4984, 'S'), (72, 32, 52.2312, 'W')]

    Sydney Opera House

    >>> dd = [-33.8567433, 151.1784306]
    >>> dms = ds.dd_to_dms(dd=dd)
    >>> dms
    [(33, 51, 24.27588, 'S'), (151, 10, 42.35016, 'E')]

    Notes
    -----
    DMS. Latitude north of the equation is "N" and south of the equator is "S".
    Longitude west of longitude 0 (Greenwich UK) is "W" and east is "E".

    DD. Latitude north of the equation is a positive float and south negative.
    Longitude west of longitude 0 is negative and east is positive.
    """
    dms_locations = []
    dms_hemisphere = []
    for item in dd:
        degrees = int(abs(item))
        minutes = (abs(item) - degrees) * 60
        seconds = round((minutes - int(minutes)) * 60, 5)
        dms_locations.append((degrees, int(minutes), seconds))
    if dd[0] > 0:
        dms_hemisphere.append("N")
    else:
        dms_hemisphere.append("S")
    if dd[1] > 0:
        dms_hemisphere.append("E")
    else:
        dms_hemisphere.append("W")
    dms = []
    for item in dms_locations:
        dms_tuple = item + (dms_hemisphere.pop(0),)
        dms.append(dms_tuple)
    return dms


def dms_to_dd(
    dms: list[tuple[int, int, float, str]]
) -> tuple[float, float]:
    """
    Converts a list of tuples containing degrees, minutes, and seconds (DMS)
    to decimal degrees (DD).

    Parameters
    ----------
    dms: list[tuple[int, int, float, str]]
        A list of tuples containing degrees, minutes, seconds, and hemisphere.

    Returns
    -------
    list[float]
        A list of two floats containing two decimal degrees (DD) for
        latitude and longitude.

    Examples
    --------
    Ottawa Parliament

    >>> import datasense as ds
    >>> dms = [(45, 25, 30.081, 'N'), (75, 41, 49.41384, 'W')]
    >>> dd = ds.dms_to_dd(dms=dms)
    >>> dd
    [45.4250225, -75.6970594]

    Effel Tower

    >>> dms = [(48, 51, 30.2148, 'N'), (2, 15, 27.4176, 'E')]
    >>> dd = ds.dms_to_dd(dms=dms)
    >>> dd
    [48.858393, 2.257616]

    Machu Pichu

    >>> dms = [(13, 9, 47.4984, 'S'), (72, 32, 52.2312, 'W')]
    >>> dd = ds.dms_to_dd(dms=ds)
    >>> dd
    [-13.163194, -72.547842]

    Sydney Opera House

    >>> dms = [(33, 51, 24.27588, 'S'), (151, 10, 42.35016, 'E')]
    >>> dd = ds.dms_to_dd(dms=dms)
    >>> dd
    [-33.8567433, 151.1784306]

    Notes
    -----
    DMS. Latitude north of the equation is "N" and south of the equator is "S".
    Longitude west of longitude 0 (Greenwich UK) is "W" and east is "E".

    DD. Latitude north of the equation is a positive float and south negative.
    Longitude west of longitude 0 is negative and east is positive.
    """

    dd_locations = []
    for degrees, minutes, seconds, hemisphere in dms:
      # Convert DMS to DD
      dd = round(degrees + minutes / 60 + seconds / 3600, 7)
      # Handle hemisphere sign
      if hemisphere in ("W", "S"):
        dd *= -1
      dd_locations.append(dd)
    return list(dd_locations)


def style_graph() -> None:
    """
    Style graphs.

    Fonts
    -----
    For Linux these are stored:
    /usr/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/

    Example
    -------

    >>> import datasense as ds
    >>> ds.style_graph()

    References
    ----------
    https://matplotlib.org/stable/tutorials/introductory/customizing.html

    """
    rc["axes.titlecolor"] = "#000000"
    rc["axes.labelweight"] = "bold"
    rc["axes.titleweight"] = "bold"
    rc["axes.labelsize"] = 12
    rc["axes.titlesize"] = 15
    rc["figure.titleweight"] = "bold"
    rc["figure.titlesize"] = 15
    # rc["font.family"] = "monospace"
    # rc["font.monospace"] = "DejaVu Sans Mono"
    rc["xtick.labelsize"] = 10
    rc["ytick.labelsize"] = 10
    rc["lines.linestyle"] = "-"
    rc["lines.markersize"] = 6
    rc["lines.marker"] = "."


def empirical_cdf(
    *,
    s: pd.Series,
    figsize: tuple[float, float] = None,
    marker: str = ".",
    markersize: float = 4,
    colour: str = colour_blue,
    remove_spines: bool = True,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Create an empirical cumulative distribution function.

    Parameters
    ----------
    s: pd.Series
        The input series.
    figsize: tuple[float, float] = None
        The (width, height) of the figure (in, in).
    marker: str = "."
        The type of plot point.
    markersize: float = 4
        The size of the plot point (pt).
    colour: str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines: bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> import datasense as ds
    >>> series_x = ds.random_data(
    ...     loc=69,
    ...     scale=13
    ... )
    >>> fig, ax = ds.empirical_cdf(s=series_x)

    Notes
    -----
    scipy is working on scipy.stats.ecdf post version 1.10.1
    """
    x_data = np.sort(a=s, axis=-1, kind=None, order=None)
    y_data = np.arange(start=1, stop=len(x_data) + 1) / len(x_data)
    fig, ax = plot_scatter_x_y(X=x_data, y=y_data)
    ax.set_title(label="Empirical Cumulative Distribution Function")
    ax.set_ylabel("Fraction")
    return (fig, ax)


def plot_boxcox(
    *,
    s: pd.Series | np.ndarray,
    la: int = -20,
    lb: int = 20,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    marker: str = ".",
    markersize: float = 4,
    ylabel: str = "Correlation Coefficient",
    remove_spines: bool = True,
    lmbda: float | int | None = None,
    alpha: float = 0.05,
) -> tuple[plt.Figure, axes.Axes]:
    """
    Box-Cox normality plot

    Parameters
    ----------
    s: pd.Series | np.ndarray
        The data series or NumPy array.
    la: int = -20
    lb: int = 20
        The lower and upper bounds for the lmbda values to pass to boxcox for
        Box-Cox transformations. These are also the limits of the horizontal
        axis of the plot if that is generated.
    colour1: str = colour_blue
        The colour of the plot points.
    colour2: str = colour_cyan
        The colour of the lower and upper bound lines.
    marker: str = "."
        The type of plot points.
    markersize: float = 4
        The size of the plot points.
    ylabel: str = "Correlation Coefficient"
        The label of the y axis.
    remove_spines: bool = True
        If True, remove top and right spines of axes.
    lmbda: float | int | None = None
        If lmbda is None (default), find the value of lmbda that maximizes the
        log-likelihood function and return it as the second output argument.
        If lmbda is not None, do the transformation for that value.
    alpha: float = 0.05
        If lmbda is None and alpha is not None (default), return the
        100 * (1-alpha)% confidence interval for lmbda as the third output
        argument. Must be between 0.0 and 1.0. If lmbda is not None, alpha is
        ignored.

    Returns
    -------
    tuple[plt.Figure, axes.Axes]
        A matplotlib Figure and Axes tuple.

        - fig: plt.Figure
            A matplotlib Figure.
        - ax: axes.Axes
            A matplotlib Axes.

    Example
    -------

    >>> from scipy import stats
    >>> import datasense as ds
    >>> s = stats.loggamma.rvs(5, size=500) + 5
    >>> fig, ax = ds.plot_boxcox(s=s)

    Notes
    -----
    Series must be > 0

    References
    ----------
    - https://www.itl.nist.gov/div898/handbook/eda/section3/eda336.htm
    - https://www.itl.nist.gov/div898/handbook/eda/section3/boxcox.htm
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    boxcox_normplot(x=s, la=la, lb=lb, plot=ax)
    ax.get_lines()[0].set(color=colour1, marker=marker, markersize=markersize)
    boxcox_array, lmax_mle, (min_ci, max_ci) = boxcox(
        x=s, lmbda=lmbda, alpha=alpha, optimizer=None
    )
    ax.axvline(x=min_ci, color=colour2, label=f"min CI = {min_ci:7.3f}")
    ax.axvline(lmax_mle, color=colour1, label=f"λ      = {lmax_mle:7.3f}")
    ax.axvline(x=max_ci, color=colour2, label=f"max CI = {max_ci:7.3f}")
    ax.set_ylabel(ylabel=ylabel)
    ax.legend(frameon=False, prop={"family": "monospace", "size": 8})
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


__all__ = (
    "plot_scatterleft_scatterright_x_y1_y2",
    "plot_scatter_scatter_x1_x2_y1_y2",
    "plot_lineleft_lineright_x_y1_y2",
    "plot_barleft_lineright_x_y1_y2",
    "plot_line_line_line_x_y1_y2_y3",
    "plot_scatter_scatter_x_y1_y2",
    "plot_scatter_line_x_y1_y2",
    "plot_line_line_x_y1_y2",
    "plot_horizontal_bars",
    "plot_line_line_y1_y2",
    "plot_vertical_bars",
    "plot_stacked_bars",
    "probability_plot",
    "plot_scatter_x_y",
    "plot_histogram",
    "plot_scatter_y",
    "empirical_cdf",
    "plot_line_x_y",
    "format_dates",
    "plot_boxplot",
    "plot_boxcox",
    "plot_line_y",
    "plot_pareto",
    "style_graph",
    "dd_to_dms",
    "dms_to_dd",
    "waterfall",
    "plot_pie",
    "despine",
    "qr_code",
)
