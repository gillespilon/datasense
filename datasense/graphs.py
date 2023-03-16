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

from typing import List, NoReturn, Tuple, Union
from datetime import datetime
from pathlib import Path
import math

from matplotlib.ticker import StrMethodFormatter
from matplotlib.offsetbox import AnchoredText
from datasense import natural_cubic_spline
from scipy.stats import norm, probplot
from matplotlib import rcParams as rc
import matplotlib.dates as mdates
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
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    colour: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
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
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker : str = "."
        The type of plot point.
    markersize : float = 8
        The size of the plot point (pt).
    colour : str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>>
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_y(y=series_y)

    Example 2
    >>> fig, ax = ds.plot_scatter_y(
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker="o",
    >>>     markersize=4,
    >>>     colour=colour_orange
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    # generate X series, required if using smoothing
    X = pd.Series(range(1, y.size + 1, 1))
    if smoothing is None:
        ax.plot(
            X, y, marker=marker, markersize=markersize, linestyle="None",
            color=colour
        )
    elif smoothing == "natural_cubic_spline":
        model = natural_cubic_spline(X=X, y=y, number_knots=number_knots)
        ax.plot(
            X, model.predict(X), marker=marker, markersize=markersize,
            linestyle="None", color=colour
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_x_y(
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 4,
    colour: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
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
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker : str = "."
        The type of plot point.
    markersize : float = 4
        The size of the plot point (pt).
    colour : str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>>
    >>> series_x = ds.datetime_data()
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )

    Example 2
    >>> series_x = ds.random_data(distribution="randint").sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker="o",
    >>>     markersize=8,
    >>>     colour=colour_red
    >>> )

    Example 3
    >>> series_x = ds.random_data(distribution="uniform").sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )

    Example 4
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_scatter_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(fig=fig, ax=ax)
        ax.plot(
            X, y, marker=marker, markersize=markersize, linestyle="None",
            color=colour
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(X=XX, y=y, number_knots=number_knots)
        ax.plot(
            X, model.predict(XX), marker=marker, markersize=markersize,
            linestyle="None", color=colour
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_y(
    *,
    y: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
    colour: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
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
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker : str = "."
        The type of plot point.
    markersize : float = 8
        The size of the plot point (pt).
    linestyle : str = "-"
        The style for the line.
    colour : str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_line_y(y=series_y)

    Example 2
    >>> fig, ax = ds.plot_line_y(
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker="o",
    >>>     markersize=4,
    >>>     colour=colour_orange
    >>> )
    >>> )
    """
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
    elif smoothing == "natural_cubic_spline":
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
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_x_y(
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
    linewidth: float = 1,
    colour: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Scatter plot of y versus X. Optional smoothing applied to y.

    If smoothing is applied, the series must not contain NaN, inf, or -inf.
    Fit a piecewise cubic function the the constraint that the fitted curve is
    linear outside the range of the knots. The fitter curve is continuously
    differentiable to the second order at all of the knots.

    Parameters
    ----------
    X : pd.Series
        The data to plot on the abscissa.
    y : pd.Series
        The data to plot on the ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker : str = "."
        The type of plot point.
    markersize : float = 8
        The size of the plot point (pt).
    linestyle : str = "-"
        The style of the line joining the points.
    linewidth : float = 1
        The width of the line joining the points.
    colour : str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines : bool = True
        IF True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> series_x = ds.datetime_data()
    >>> series_y = ds.random_data()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )

    Example 2
    >>> series_x = ds.random_data(distribution="randint").sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y,
    >>>     figsize=(8, 4.5),
    >>>     marker="o",
    >>>     markersize=8,
    >>>     linestyle=":",
    >>>     linewidth=5,
    >>>     colour=colour_magenta
    >>> )

    Example 3
    >>> series_x = ds.random_data(distribution="uniform").sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )

    Example 4
    >>> series_x = ds.random_data().sort_values()
    >>> fig, ax = ds.plot_line_x_y(
    >>>     X=series_x,
    >>>     y=series_y
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
            )
        ax.plot(
            X,
            y,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            linewidth=linewidth,
            color=colour
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            linestyle=linestyle,
            linewidth=linewidth,
            color=colour),
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_scatter_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
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
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker1 : str = "."
        The type of plot point for y1.
    marker2 : str = "."
        The type of plot point for y2.
    markersize1 : int = 8
        The size of the plot point for y1.
    markersize2 : int = 8
        The size of the plot point for y2.
    linestyle1 : str = "None"
        The style of the line for y1.
    linestyle2 : str = "None"
        The style of the line for y2.
    linewidth1 : float = 1
        The width of the line for y1.
    linewidth2 : float = 1
        The width of the line for y2.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    labellegendy1 : str = None
        The legend label of the line y1.
    labellegendy2 : str = None
        The legend label of the line y2.
    remove_spines : booll = True
        IF True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
    >>> series_x = ds.datetime_data()
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    >>>     X=series_x,
    >>>     y1=series_y1,
    >>>     y2=series_y2
    >>> )

    Example 2
    >>> series_x = ds.random_data(distribution="uniform")
    >>> fig, ax = ds.plot_scatter_scatter_x_y1_y2(
    >>>     X=series_x,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1="o",
    >>>     marker2="+",
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1=colour_red,
    >>>     colour2=colour_magenta,
    >>>     labellegendy1="y1",
    >>>     labellegendy2="y2"
    >>> )
    >>> ax.legend(frameon=False)
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
            )
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
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            linestyle="None",
            linewidth=linewidth1,
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(X),
            marker=marker2,
            markersize=markersize2,
            linestyle="None",
            linewidth=linewidth2,
            color=colour2
        )
        ax.plot(
            X,
            model1.predict(XX),
            marker=".",
            linestyle="",
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=".",
            linestyle="",
            color=colour2
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_scatter_x1_x2_y1_y2(
    *,
    X1: pd.Series,
    X2: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
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
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
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
    X1 : pd.Series
        The data to plot on the abscissa.
    X2 : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker1 : str = "."
        The type of plot point for y1.
    marker2 : str = "."
        The type of plot point for y2.
    markersize1 : int = 8
        The size of the plot point for y1.
    markersize2 : int = 8
        The size of the plot point for y2.
    linestyle1 : str = "None"
        The style of the line for y1.
    linestyle2 : str = "None"
        The style of the line for y2.
    linewidth1 : float = 1
        The width of the line for y1.
    linewidth2 : float = 1
        The width of the line for y2.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    labellegendy1 : str = None
        The legend label of the line y1.
    labellegendy2 : str = None
        The legend label of the line y2.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Examples
    --------
    Example 1
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

    Example 2
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     smoothing="natural_cubic_spline",
    >>>     number_knots=7
    >>> )

    Example 3
    >>> series_x1 = ds.random_data(distribution="uniform").sort_values()
    >>> series_x2 = ds.random_data(distribution="uniform").sort_values()
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1="o",
    >>>     marker2="+",
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1=colour_red,
    >>>     colour2=colour_magenta,
    >>>     labellegendy1="y1",
    >>>     labellegendy2="y2"
    >>> )
    >>> ax.legend(frameon=False)

    Example 4
    >>> fig, ax = ds.plot_scatter_scatter_x1_x2_y1_y2(
    >>>     X1=series_x1,
    >>>     X2=series_x2,
    >>>     y1=series_y1,
    >>>     y2=series_y2,
    >>>     figsize=(8, 5),
    >>>     marker1="o",
    >>>     marker2="+",
    >>>     markersize1=8,
    >>>     markersize2=12,
    >>>     colour1=colour_red,
    >>>     colour2=colour_magenta,
    >>>     labellegendy1="y1",
    >>>     labellegendy2="y2",
    >>>     smoothing="natural_cubic_spline",
    >>>     number_knots=7
    >>> )
    >>> ax.legend(frameon=False)
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if (X1.dtype and X2.dtype) in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
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
    elif smoothing == "natural_cubic_spline":
        if (X1.dtype and X2.dtype) in ["datetime64[ns]"]:
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
            linestyle="-",
            linewidth=linewidth1,
            color=colour1
        )
        ax.plot(
            X2,
            model2.predict(XX2),
            marker=marker2,
            markersize=0,
            linestyle="-",
            linewidth=linewidth2,
            color=colour2
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatter_line_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    y1_marker: str = ".",
    y2_marker: str = "",
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    labellegendy1: str = None,
    labellegendy2: str = None,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
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
    X : pd.Series
        The series for the horizontal axis.
    y1 : pd.Series
        The series for y1 to plot on the vertical axis.
    y2 : pd.Series
        The series for y2 to plot on the vertical axis.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots to create.
    marker : str = None
        The type of marker
    colour1 : str = colour_blue
        The colour of y1.
    colour2 : str = colour_cyan
        The colour of y2.
    labellegendy1 : str = None
        The legend for y1.
    labellegendy2 : str = None
        The legend for y2.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> number_knots = 100
    >>> model = ds.natural_cubic_spline(
    >>>     X=X,
    >>>     y=y,
    >>>     number_knots=number_knots
    >>> )
    >>> fig, ax = ds.plot_scatter_line_x_y1_y2(
    >>>     X=X,
    >>>     y1=y,
    >>>     y2=model.predict(X),
    >>>     figsize=figsize,
    >>>     labellegendy2=f'number knots = {number_knots}'
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
            )
        ax.plot(
            X,
            y1,
            marker=y1_marker,
            linestyle="",
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=y2_marker,
            linestyle="-",
            color=colour2,
            label=labellegendy2
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            marker=y1_marker,
            linestyle="",
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=y2_marker,
            linestyle="-",
            color=colour2
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_line_y1_y2(
    *,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
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
    remove_spines: bool = True
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
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    marker1 : str = "."
        The type of plot point for y1.
    marker2 : str = "."
        The type of plot point for y2.
    markersize1 : int = 8
        The size of the plot point for y1 (pt).
    markersize2 : int = 8
        The size of the plot point for y2 (pt).
    linestyle1 : str = "_"
        The style of the line for y1.
    linestyle2 : str = "_"
        The style of the line for y2.
    linewidth1 : float = 1
        The width of the line for y1.
    linewidth2 : float = 1
        The width of the line for y2.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    labellegendy1 : str = None
        The legend label of the line y1.
    labellegendy2 : str = None
        The legend label of the line y2.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> series_y1 = ds.random_data()
    >>> series_y2 = ds.random_data()
    >>> fig, ax = ds.plot_line_line_y1_y2(
    >>>     y1=series_y1,
    >>>     y2=series_y2
    >>> )
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
    elif smoothing == "natural_cubic_spline":
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
            linestyle="-",
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(X),
            marker=None,
            linestyle="-",
            color=colour2
            )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_line_line_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
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
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the y1 ordinate.
    y2 : pd.Series
        The data to plot on the y2 ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        the number of knows for natural cubic spline smoothing.
    marker1 : str = "."
        The type of plot point for y1.
    marker2 : str = "."
        The type of plot point for y2.
    markersize1 : int = 8
        The size of the plot point for y1.
    markersize2 : int = 8
        The size of the plot point for y2.
    linestyle1 : str = "-"
        The style of the line for y1.
    linestyle2 : str = "-"
        The style of the line for y2.
    linewidth1 : float = 1
        The width of the line for y1.
    linewidth2 : float = 1
        The width of the line for y2.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    labellegendy1 : str = None
        The legend label of the line y1.
    labellegendy2 : str = None
        The legend label of the line y2.
    remove_spines : booll = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Exanple
    -------
    >>> figure_width_height = (15, 7)
    >>> fig, ax = ds.plot_line_line_x_y1_y2(
    >>>     X=X,
    >>>     y1=y1,
    >>>     y2=y2,
    >>>     figsize=figure_width_height,
    >>>     labellegendy1=column_actual,
    >>>     labellegendy2=column_target,
    >>>     marker2=None,
    >>>     linestyle1='None',
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
            )
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
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            linestyle="-",
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=None,
            linestyle="-",
            color=colour2
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
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    colour3: str = colour_teal,
    labellegendy1: str = None,
    labellegendy2: str = None,
    labellegendy3: str = None,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the y1 ordinate.
    y2 : pd.Series
        The data to plot on the y2 ordinate.
    y3 : pd.Series
        The data to plot on the y3 ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        the number of knows for natural cubic spline smoothing.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    colour2 : str = colour_teal
        The colour of the line for y2.
    labellegendy1 : str = None
        The legend label of the line y1.
    labellegendy2 : str = None
        The legend label of the line y2.
    labellegendy3 : str = None
        The legend label of the line y3.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> figsize = (6, 4)
    >>> column_target="TargetBalance",
    >>> column_actual="ActualBalance",
    >>> column_actual="Predicted"
    >>> fig, ax = ds.plot_line_line_line_x_y1_y2_y3(
    >>>     X=X,
    >>>     y1=target,
    >>>     y2=actual,
    >>>     y3=predicted,
    >>>     figsize=figsize,
    >>>     labellegendy1=column_target,
    >>>     labellegendy2=column_actual,
    >>>     labellegendy3=column_predicted
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax
            )
        ax.plot(
            X,
            y1,
            marker=None,
            linestyle="-",
            color=colour1,
            label=labellegendy1
        )
        ax.plot(
            X,
            y2,
            marker=None,
            linestyle="-",
            color=colour2,
            label=labellegendy2
        )
        ax.plot(
            X,
            y3,
            marker=None,
            linestyle="-",
            color=colour3,
            label=labellegendy3
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            linestyle="-",
            color=colour1
        )
        ax.plot(
            X,
            model2.predict(XX),
            marker=None,
            linestyle="-",
            color=colour2
        )
        ax.plot(
            X,
            model3.predict(XX),
            marker=None,
            linestyle="-",
            color=colour3
        )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_scatterleft_scatterright_x_y1_y2(
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    linestyle1: str = "None",
    linestyle2: str = "None"
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the y1 ordinate.
    y2 : pd.Series
        The data to plot on the y2 ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        the number of knows for natural cubic spline smoothing.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    linestyle1 : str = "None"
        The style of the line for y1.
    linestyle2 : str = "None"
        The style of the line for y2.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes, axes.Axes]
        A matplotlib figure and Axes tuples.

    Example
    -------
    >>> fig, ax1, ax2 = ds.plot_scatterleft_scatterright_x_y1_y2(
    >>>     X=df["X"],
    >>>     y1=df["y1"],
    >>>     y2=df["y2"],
    >>>     figsize=(6, 4),
    >>>     linestyle2="-"
    >>> )
    """
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax1
            )
        ax1.plot(
            X,
            y1,
            marker=".",
            linestyle=linestyle1,
            color=colour1
        )
        ax2.plot(
            X,
            y2,
            marker=".",
            linestyle=linestyle2,
            color=colour2
        )
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
            marker=".",
            linestyle=linestyle1,
            color=colour1
        )
        ax2.plot(
            X,
            model2.predict(XX),
            marker=".",
            linestyle=linestyle2,
            color=colour2
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
    figsize: Tuple[float, float] = None,
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
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    linestyle1 : str = "-"
        The style of the line for y1.
    linestyle2 : str = "-"
        The style of the line for y2.
    marker1 : str = "."
        The type of plot point for y1.
    markersize1 : int = 8
        The size of the plot point for y1 (pt).
    marker2 : str = "."
        The type of plot point for y2.
    markersize2 : int = 8
        The size of the plot point for y2 (pt).

    Returns
    -------
    Tuple[plt.Figure, axes.Axes, axes.Axes]
        A matplotlib figure and Axes tuples.

    Examples
    --------
    Example1
    >>> fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
    >>>     X=df[column_abscissa_datetime_one],
    >>>     y1=df[column_ordinate_one],
    >>>     y2=df[column_ordinate_two],
    >>>     figsize=figsize
    >>> )

    Example2
    >>> fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
    >>>     X=df[column_abscissa_datetime_one],
    >>>     y1=df[column_ordinate_one],
    >>>     y2=df[column_ordinate_two],
    >>>     smoothing="natural_cubic_spline",
    >>>     number_knots=5,
    >>>     figsize=figsize
    >>> )
    """
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax1
            )
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
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
    *,
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figsize: Tuple[float, float] = None,
    smoothing: str = None,
    number_knots: int = None,
    barwidth: float = 10,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    linestyle1: str = "-",
    linestyle2: str = "-",
    marker2: str = "o"
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
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
    X : pd.Series
        The data to plot on the abscissa.
    y1 : pd.Series
        The data to plot on the ordinate.
    y2 : pd.Series
        The data to plot on the ordinate.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    smoothing : str = None
        The type of smoothing to apply.
        Options: "natural_cubic_spline"
    number_knots : int = None
        The number of knots for natural cubic spline smoothing.
    barwidth : float = 10
        The width of the bars.
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    linestyle1 : str = "-"
        The style of the line for y1.
    linestyle2 : str = "-"
        The style of the line for y2.
    marker2 : str = "o"
        The type of plot point for y2.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes, axes.Axes]
        A matplotlib figure and Axes tuples.

    Example
    -------
    >>> fig, ax1, ax2 = ds.plot_barleft_lineright_x_y1_y2(
    >>>     X=X,
    >>>     y1=y1,
    >>>     y2=y2,
    >>>     figsize=figsize,
    >>>     barwidth=20,
    >>>     colour1=colour1,
    >>>     colour2=colour2
    >>> )
    """
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ["datetime64[ns]"]:
            format_dates(
                fig=fig,
                ax=ax1
            )
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
    elif smoothing == "natural_cubic_spline":
        if X.dtype in ["datetime64[ns]"]:
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
    *,
    X: pd.Series,
    y: pd.Series,
    figsize: Tuple[float, float] = None,
    width: float = 0.8,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    marker: str = ".",
    markersize: float = 8,
    linestyle: str = "-",
) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
    """
    Parameters
    ----------
    X : pd.Series
        The data to plot on the ordinate.
    y : pd.Series
        The data to plot on the abscissa.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    width : float = 0.8
        The width of the bars (in).
    colour1 : str = colour_blue
        The colour of the line for y1.
    colour2 : str = colour_cyan
        The colour of the line for y2.
    marker : str = "."
        The type of plot point.
    markersize : float = 8
        The size of the plot point (pt).
    linestyle : str = "-"
        The style of the line joining the points.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> data = pd.DataFrame(
    >>>     {
    >>>         "ordinate": ["Mo", "Larry", "Curly", "Shemp", "Joe"],
    >>>         "abscissa": [21, 2, 10, 4, 16]
    >>>     }
    >>> )
    >>> fig, ax1, ax2 = ds.plot_pareto(
    >>>     X=data["ordinate"],
    >>>     y=data["abscissa"]
    >>> )
    """
    df = pd.concat(
        [X, y],
        axis=1
    ).sort_values(
        by=y.name,
        axis=0,
        ascending=False,
        kind="mergesort"
    )
    total_y = df[y.name].sum()
    df["percentage"] = df[y.name] / total_y * 100
    df["cumulative_percentage"] = df["percentage"].cumsum(skipna=True)
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
        df["cumulative_percentage"],
        marker=marker,
        markersize=markersize,
        linestyle=linestyle,
        color=colour2
    )
    return (fig, ax1, ax2)


def format_dates(
    *,
    fig: plt.Figure,
    ax: axes.Axes
) -> NoReturn:
    """
    Format dates and ticks for plotting.

    Parameters
    ----------
    fig : plt.Figure
        A matplotlib figure.
    ax : axes.Axes
        A matplotlib Axes.

    Example
    -------
    >>> ds.format_dates(
    >>>     fig=fig,
    >>>     ax=ax
    >>> )
    """
    loc = mdates.AutoDateLocator()
    fmt = mdates.AutoDateFormatter(locator=loc)
    ax.xaxis.set_major_locator(locator=loc)
    ax.xaxis.set_major_formatter(formatter=fmt)
    fig.autofmt_xdate()


def probability_plot(
    *,
    data: pd.Series,
    figsize: Tuple[float, float] = None,
    distribution: object = norm,
    fit: bool = True,
    plot: object = None,
    colour1: str = colour_blue,
    colour2: str = colour_cyan,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Plot a probability plot of data against the quantiles of a specified
    theoretical distribution.

    Parameters
    ----------
    data : pd.Series
        A pandas Series.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    distribution : object = norm
        Fit a normal distribution by default.
    fit : bool = True
        Fit a least-squares regression line to the data if True.
    plot : object = None
        If given, plot the quantiles and least-squares fit.
    colour1 : str = colour_blue,
        The colour of line 1.
    colour2 : str = colour_cyan
        The colour of line 2.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    Tuple[plt.Figure, axes.Axes]
        A matplotlib figure and Axes tuple.

    Example
    -------
    >>> data = ds.random_data()
    >>> fig, ax = ds.probability_plot(data=data)
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
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


def despine(
    *,
    ax: axes.Axes
) -> NoReturn:
    """
    Remove the top and right spines of a graph.

    Parameters
    ----------
    ax : axes.Axes
        A matplotlib Axes.

    Example
    -------
    >>> despine(ax=ax)
    """
    ax.spines[["top", "right"]].set_visible(b=False)


def plot_histogram(
    *,
    series: pd.Series,
    number_bins: int = None,
    bin_range: [Tuple[int, int] | Tuple[int, int]] = None,
    figsize: Tuple[float, float] = None,
    bin_width: int = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    bin_label_bool: bool = False,
    color: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    series : pd.Series
        The input series.
    number_bins : int = None
        The number of equal-width bins in the range s.max() - s.min().
    bin_range : [Tuple[int, int] | Tuple[int, int]] = None
        The lower and upper range of the bins. If not provided, range is
        (s.min(), s.max()).
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    bin_width : int = None
        The width of the bin in same units as the series s.
    edgecolor : str = colour_white
        The hexadecimal color value for the bar edges.
    linewidth : int = 1
        The bar edges line width (point).
    bin_label_bool : bool = False
        If True, label the bars with count and percentage of total.
    color : str = colour_blue
        The color of the bar faces.
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    # Create a series of random floats, normal distribution,
    # with the default parameters.
    >>> s = ds.random_data()
    >>> fig, ax = ds.plot_histogram(series=s)

    Example 2
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, max = 13.
    >>> s = ds.random_data(
    >>>     distribution="randint",
    >>>     size=113,
    >>>     low=0,
    >>>     high=14
    >>> )
    >>> fig, ax = ds.plot_histogram(series=s)

    Example 3
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, max = 13.
    # Set histogram parameters to control bin width.
    >>> s = ds.random_data(
    >>>     distribution="randint",
    >>>     size=113,
    >>>     low=0,
    >>>     high=14
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     series=s,
    >>>     bin_width=1
)

    Example 4
    # Create a series of random integers, integer distribution, size = 113,
    # min = 0, hight = 14,
    # Set histogram parameters to control bin width and plotting range.
    >>> s = ds.random_data(
    >>>     distribution="randint",
    >>>     size=113,
    >>>     low=0,
    >>>     high=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     series=s,
    >>>     bin_width=1,
    >>>     bin_range=(0, 10)
    >>> )

    Example 5
    # Create a series of random floats, size = 113,
    # average = 69, standard deviation = 13.
    # Set histogram parameters to control bin width and plotting range.
    >>> s = ds.random_data(
    >>>     distribution="norm",
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     series=s,
    >>>     bin_width=5,
    >>>     bin_range=(30, 110)
    >>> )

    Example 6
    # Create a series of random floats, size = 113,
    # average = 69, standard deviation = 13.
    # Set histogram parameters to control bin width, plotting range, labels.
    # Set colour of the bars.
    >>> s = ds.random_data(
    >>>     distribution="norm",
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )
    >>> fig, ax = ds.plot_histogram(
    >>>     series=s,
    >>>     bin_width=5,
    >>>     bin_range=(30, 110),
    >>>     figsize=(10,8),
    >>>     bin_label_bool=True,
    >>>     color=colour_cyan
    >>>     ax.set_xlabel(xlabel="X-axis label", labelpad=30)
    >>>     plt.tight_layout()
    >>> )
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
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
        color=color
    )
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
                xycoords=(
                    "data",
                    "axes fraction"
                ),
                textcoords="offset points",
                va="top",
                ha="center"
            )
            percent = f"{(100 * float(count) / counts.sum()):0.0f} %"
            ax.annotate(
                text=percent,
                xy=(x, 0),
                xytext=(0, -32),
                xycoords=(
                    "data",
                    "axes fraction"
                ),
                textcoords="offset points",
                va="top",
                ha="center"
            )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def plot_horizontal_bars(
    *,
    y: [List[int] | List[float] | List[str]],
    width: [List[int] | List[float]],
    height: float = 0.8,
    figsize: Tuple[float, float] = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    color: str = colour_blue,
    left: [datetime | int | float] = None
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    y : [List[int] | List[float] | List[str]],
        The y coordinates of the bars.
    width : [List[int] | List[float]],
        The width(s) of the bars.
    height : float = 0.8,
        The height of the bars.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    edgecolor : str = colour_white,
        The hexadecimal color value for the bar edges.
    linewidth : int = 1,
        The bar edges line width (point).
    color : str = colour_blue
        The color of the bar faces.
    left : [datetime | int | float] = None
        The x coordinates of the left sides of the bars.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> y = ["Yes", "No"]
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    >>>     y=y,
    >>>     width=width
    >>> )

    Example 2
    >>> y = ["Yes", "No"]
    >>> width = [69, 31]
    >>> fig, ax = ds.plot_horizontal_bars(
    >>>     y=y,
    >>>     width=width,
    >>>>    height=0.4
    >>> )

    Example 3
    Create Gantt chart
    >>> data = {
    >>>     "start": ["2021-11-01", "2021-11-03", "2021-11-04", "2021-11-08"],
    >>>     "end": ["2021-11-08", "2021-11-16", "2021-11-11", "2021-11-13"],
    >>>     "task": ["task 1", "task 2", "task 3", "task 4"]
    >>> }
    >>> columns = ["task", "start", "end", "duration", "start_relative"]
    >>> data_types = {
    >>>     "start": "datetime64[ns]",
    >>>     "end": "datetime64[ns]",
    >>>     "task": "str"
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
            >>>     f"{(start + datetime.timedelta(days=x)):%Y-%m-%d}"}
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
    """
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
    *,
    x: Union[List[int], List[float], List[str]],
    height: Union[List[int], List[float]],
    width: float = 0.8,
    figsize: Tuple[float, float] = None,
    edgecolor: str = colour_white,
    linewidth: int = 1,
    color: str = colour_blue
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x : Union[List[int], List[float], List[str]],
        The x coordinates of the bars.
    height : Union[List[int], List[float]],
        The height(s) of the bars.
    width : float = 0.8,
        The width of the bars.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    edgecolor : str = colour_white,
        The hexadecimal color value for the bar edges.
    linewidth : int = 1,
        The bar edges line width (point).
    color : str = colour_blue
        The color of the bar faces.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> x = ["Yes", "No"]
    >>> height = [69, 31]
    >>> fig, ax = ds.plot_vertical_bars(
    >>>     x=x,
    >>>     height=height
    >>> )

    Example 2
    >>> x = ["Yes", "No"]
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
    *,
    x: Union[List[int], List[float]],
    labels: Union[List[int], List[float], List[str]],
    figsize: Tuple[float, float] = None,
    startangle: float = 0,
    colors: List[str] = None,
    autopct: str = "%1.1f%%"
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Parameters
    ----------
    x : Union[List[int], List[float]],
        The wedge sizes.
    labels : Union[List[int], List[float], List[str]],
        The labels of the wedges.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    startangle : float = 0,
        The start angle of the pie, counterclockwise from the x axis.
    colors : List[str] = None
        The color of the wedges.
    autopct : str = "%1.1f%%"
        Label the wedges with their numeric value. If None, no label.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> x = [69, 31]
    >>> labels = ["Yes", "No"]
    >>> fig, ax = ds.plot_pie(
    >>>     x=x,
    >>>     labels=labels
    >>> )

    Example 2
    >>> x = [69, 31]
    >>> labels = ["Yes", "No"]
    >>> fig, ax = ds.plot_pie(
    >>>     x=x,
    >>>     labels=labels,
    >>>     startangle=90,
    >>>     colors=[
    >>>         colour_blue, colour_cyan, colour_teal, colour_orange,
    >>>         colour_red, colour_magenta, colour_grey
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
    *,
    x: Union[List[int], List[float], List[str]],
    height1: Union[List[int], List[float]],
    label1: str = None,
    height2: Union[List[int], List[float]] = None,
    label2: str = None,
    height3: Union[List[int], List[float]] = None,
    label3: str = None,
    height4: Union[List[int], List[float]] = None,
    label4: str = None,
    height5: Union[List[int], List[float]] = None,
    label5: str = None,
    height6: Union[List[int], List[float]] = None,
    label6: str = None,
    height7: Union[List[int], List[float]] = None,
    label7: str = None,
    width: float = 0.8,
    figsize: Tuple[float, float] = None,
    color: Union[List[str]] = [
        colour_blue, colour_cyan, colour_teal, colour_orange, colour_red,
        colour_magenta, colour_grey
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
    label1 : str = None,
        The label of the level 1 bars.
    height2 : Union[List[int], List[float]],
        The height of the level 2 bars.
    label2 : str = None,
        The label of the level 2 bars.
    height3 : Union[List[int], List[float]],
        The height of the level 3 bars.
    label3 : str = None,
        The label of the level 3 bars.
    height4 : Union[List[int], List[float]],
        The height of the level 4 bars.
    label4 : str = None,
        The label of the level 4 bars.
    height5 : Union[List[int], List[float]],
        The height of the level 5 bars.
    label5 : str = None,
        The label of the level 5 bars.
    height6 : Union[List[int], List[float]],
        The height of the level 6 bars.
    label6 : str = None,
        The label of the level 6 bars.
    height7 : Union[List[int], List[float]],
        The height of the level 7 bars.
    label7 : str = None,
        The label of the level 7 bars.
    width : float = 0.8,
        The width of the bars.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    color : str = [
        colour_blue, colour_cyan, colour_teal, colour_orange, colour_red,
        colour_magenta, colour_grey
    ]
        The color of the bar faces, up to seven levels.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Examples
    --------
    Example 1
    >>> x = ["G1", "G2", "G3", "G4", "G5"]
    >>> height1 = [20, 35, 30, 35, 27]
    >>> label1 = "A"
    >>> width = 0.35
    >>> height2 = [25, 32, 34, 20, 25]
    >>> label2 = "B"
    >>> fig, ax = ds.plot_stacked_bars(
    >>>     x=x,
    >>>     height1=height1,
    >>>     label1=label1,
    >>>     height2=height2,
    >>>     label2=label2
    >>> )
    >>> fig.legend(frameon=False, loc="upper right")

    Example 2
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
    >>> fig.legend(frameon=False, loc="upper right")
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


def qr_code(*, qr_code_string: str, qr_code_path: Path) -> NoReturn:
    """
    Create a QR code and save as .svg and .png.

    Parameters
    ----------
    qr_code_string : str
        Text for the QR code
    qr_code_path : Path
        Text for the path

    Example
    -------
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
    notch: bool = None,
    showmeans: bool = None,
    figsize: Tuple[float, float] = None,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Create a box-and-whisker plot with several elements:
    - minimum
    - first quartile
    - second quartile (median)
    - third quartile
    - maximum
    - outliers

    Parameters
    ----------
    series : pd.Series
        The input series.
    notch: bool = None,
        Boolean to show notch.
    showmeans: bool = None,
        Boolean to show average.
    figsize : Tuple[float, float] = None,
        The (width, height) of the figure (in, in).
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Example
    --------
    >>> series = ds.random_data()
    >>> fig, ax = ds.plot_boxplot(series=series)
    >>> ax.set_title(label="Box-and-whisker plot")
    >>> ds.despine(ax=ax)
    >>> ax.set_xticks(ticks=[1], labels=["series"])
    >>> ax.set_ylabel("y")
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.boxplot(
        x=series,
        notch=notch,
        showmeans=showmeans
    )
    if remove_spines:
        despine(ax=ax)
    return (fig, ax)


def decimal_degrees(
        degrees: int, minutes: int, seconds: float, hemisphere: str
) -> Tuple[float, str]:
    """
    Convert degrees, minutes, seconds location to decimal location.

    Reference: https://bit.ly/3OUgeXO

    Parameters
    ----------
    degrees : int
        The degree portion of the location.
    minutes : int
        The minutes portion of the location.
    seconds : float
        The seconds portion of the location.
    hemisphere : str
        The relevant hemisphere: N, S, W, E

    Returns
    -------
    float
        The location in decimal notation.
    hemisphere : str
        The relevant hemisphere: N, S, W, E

    Examples
    --------
    Example 1
    >>> location_deg_min_sec = [(40, 38, 2.99976, "N"), (14, 36, 9.927, "E")]
    >>> location_decimal = [
    >>>     ds.decimal_degrees(degrees=w, minutes=x, seconds=y, hemisphere=z)
    >>>     for w, x, y, z in location_deg_min_sec
    >>> ]
    >>> [(40.6341666, 'N'), (14.6027575, 'E')]

    Example 2
    >>> location_deg_min_sec = [(34, 49, 59.06532, "S"), (20, 0, 0, "E")]
    >>> location_decimal = [
    >>>     ds.decimal_degrees(degrees=w, minutes=x, seconds=y, hemisphere=z)
    >>>     for w, x, y, z in location_deg_min_sec
    >>> ]
    >>> [(-34.8330737, 'S'), (20.0, 'E')]

    Example 3
    >>> location_deg_min_sec = [(40, 41, 21.31224, "N"), (74, 2, 48.1002, "W")]
    >>> location_decimal = [
    >>>     ds.decimal_degrees(degrees=w, minutes=x, seconds=y, hemisphere=z)
    >>>     for w, x, y, z in location_deg_min_sec
    >>> ]
    >>> [(40.6892534, 'N'), (-74.0466945, 'W')]

    Example 4
    >>> location_deg_min_sec = \
    >>>     [(-13, 9, 47.89404, "S"), (-72, 32, 44.78892, "W")]
    >>> location_decimal = [
    >>>     ds.decimal_degrees(degrees=w, minutes=x, seconds=y, hemisphere=z)
    >>>     for w, x, y, z in location_deg_min_sec
    >>> ]
    >>> [(-13.1633039, 'S'), (-72.5457747, 'W')]
    """
    deg = abs(degrees) + minutes / 60 + seconds / 3600
    if hemisphere == "N":
        deg = abs(deg)
    elif hemisphere == "S":
        deg = -1 * deg
    elif hemisphere == "W":
        deg = -1 * deg
    elif hemisphere == "E":
        deg = abs(deg)
    return (round(deg, 7), hemisphere)


def deg_min_sec(
    decimal_deg_min_sec: float, hemisphere: str
) -> Tuple[int, int, float, str]:
    """
    Convert decimal location to degrees, minutes, seconds location.

    Reference: https://bit.ly/3OUgeXO

    Parameters
    ----------
    decimal_deg_min_sec : float
        The location in decimal notation.
    hemisphere : str
        The relevant hemisphere: N, S, W, E

    Returns
    -------
    Tuple[int, int, float, str]
        The location in degrees, minutes, seconds, hemisphere.

    Examples
    --------
    Example 1
    >>> location_decimal = [(40.6341666, "N"), (14.6027575, "E")]
    >>> location_deg_min_sec = [
    >>>     ds.deg_min_sec(decimal_deg_min_sec=x, hemisphere=y)
    >>>     for x, y in location_decimal
    >>> ]
    >>> [(40, 38, 2.99976, 'N'), (14, 36, 9.927, 'E')]

    Example 2
    >>> location_decimal = [(34.8330737, "S"), (20, "E")]
    >>> location_deg_min_sec = [
    >>>     ds.deg_min_sec(decimal_deg_min_sec=x, hemisphere=y)
    >>>     for x, y in location_decimal
    >>> ]
    >>> [(34, 49, 59.06532, 'S'), (20, 0, 0, 'E')]

    Example 3
    >>> location_decimal = [(40.6892534, "N"), (-74.0466945, "W")]
    >>> location_deg_min_sec = [
    >>>     ds.deg_min_sec(decimal_deg_min_sec=x, hemisphere=y)
    >>>     for x, y in location_decimal
    >>> ]
    >>> [(40, 41, 21.31224, 'N'), (-74, 2, 48.1002, 'W')]

    Example 4
    >>> location_decimal = [(-13.1633039, "S"), (-72.5457747, "W")]
    >>> location_deg_min_sec = [
    >>>     ds.deg_min_sec(decimal_deg_min_sec=x, hemisphere=y)
    >>>     for x, y in location_decimal
    >>> ]
    >>> [(-13, 9, 47.89404, 'S'), (-72, 32, 44.78892, 'W')]
    """
    min, sec = divmod(abs(decimal_deg_min_sec) * 3600, 60)
    deg, min = divmod(min, 60)
    deg = int(decimal_deg_min_sec)
    return (deg, int(min), round(sec, 9), hemisphere)


def style_graph() -> NoReturn:
    """
    Style graphs.

    Reference
    ---------
    https://matplotlib.org/stable/tutorials/introductory/customizing.html

    Fonts
    -----
    For Linux these are stored:
    /usr/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/

    Example
    -------
    >>> ds.style_graph()
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
    figsize: Tuple[float, float] = None,
    marker: str = ".",
    markersize: float = 4,
    colour: str = colour_blue,
    remove_spines: bool = True
) -> Tuple[plt.Figure, axes.Axes]:
    """
    Create an empirical cumulative distribution function.

    Parameters
    ----------
    s : pd.Series
        The input series.
    figsize : Tuple[float, float] = None
        The (width, height) of the figure (in, in).
    marker : str = "."
        The type of plot point.
    markersize : float = 4
        The size of the plot point (pt).
    colour : str = colour_blue
        The colour of the plot point (hexadecimal triplet string).
    remove_spines : bool = True
        If True, remove top and right spines of axes.

    Returns
    -------
    fig, ax : Tuple[plt.Figure, axes.Axes]

    Example
    -------
    >>> import datasense as ds
    >>> series_x = ds.random_data(
    >>>     loc=69,
    >>>     scale=13
    >>> )
    >>> fig, ax = ds.empirical_cdf(s=series_x)

    Notes
    -----
    scipy is working on scipy.stats.ecdf post version 1.10.1
    """
    x_data = np.sort(
        a=s,
        axis=-1,
        kind=None,
        order=None
    )
    y_data = np.arange(start=1, stop=len(x_data) + 1) / len(x_data)
    fig, ax = plot_scatter_x_y(
        X=x_data,
        y=y_data
    )
    ax.set_title(label="Empirical Cumulative Distribution Function")
    ax.set_ylabel("Fraction")
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
    "decimal_degrees",
    "plot_histogram",
    "plot_scatter_y",
    "empirical_cdf",
    "plot_line_x_y",
    "format_dates",
    "plot_boxplot",
    "deg_min_sec",
    "plot_line_y",
    "plot_pareto",
    "style_graph",
    "plot_pie",
    "despine",
    "qr_code",
)
