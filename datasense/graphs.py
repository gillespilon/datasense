'''
Graphical analysis
'''


from typing import Optional, Tuple

from datasense import natural_cubic_spline
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.cm as cm
import pandas as pd


c = cm.Paired.colors


def plot_scatter_x_y(
    X: pd.Series,
    y: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> (plt.figure, axes.Axes):
    '''
    Scatter plot of y versus X
    Optional smoothing applied to y

    X: series for horizontal axis
    y: series for vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax.plot(X, y, marker='.', linestyle='', color=c[1])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(XX, y, numknots)
        ax.plot(X, model.predict(XX), marker='.', linestyle='', color=c[1])
    return (fig, ax)


def plot_line_x_y(
    X: pd.Series,
    y: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> (plt.figure, axes.Axes):
    '''
    Scatter plot of y versus X
    Optional smoothing applied to y

    X: series for horizontal axis
    y: series for vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax.plot(X, y, marker='', color=c[1])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model = natural_cubic_spline(XX, y, numknots)
        ax.plot(X, model.predict(XX), marker='', color=c[1])
    return (fig, ax)


def plot_scatter_scatter_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> axes.Axes:
    '''
    Scatter plot of y1 versus X
    Scatter plot of y2 versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have the same units.

    x:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax.plot(X, y1, marker='.', linestyle='', color=c[1])
        ax.plot(X, y2, marker='.', linestyle='', color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(XX, y1, numknots)
        model2 = natural_cubic_spline(XX, y2, numknots)
        ax.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax.plot(X, model2.predict(XX), marker='.', linestyle='', color=c[5])
    return (fig, ax)


def plot_scatter_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> axes.Axes:
    '''
    Scatter plot of y1 versus X
    Line plot of y2 versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have the same units.

    x:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax.plot(X, y1, marker='.', linestyle='', color=c[1])
        ax.plot(X, y2, marker=None, linestyle='-', color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(XX, y1, numknots)
        model2 = natural_cubic_spline(XX, y2, numknots)
        ax.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax.plot(X, model2.predict(XX), marker=None, linestyle='-', color=c[5])
    return (fig, ax)


def plot_line_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> axes.Axes:
    '''
    Line plot of y1 versus X
    Line plot of y2 versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have the same units.

    X:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax.plot(X, y1, marker=None, linestyle='-', color=c[1])
        ax.plot(X, y2, marker=None, linestyle='-', color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(XX, y1, numknots)
        model2 = natural_cubic_spline(XX, y2, numknots)
        ax.plot(X, model1.predict(XX), marker=None, linestyle='-', color=c[1])
        ax.plot(X, model2.predict(XX), marker=None, linestyle='-', color=c[5])
    return (fig, ax)


def plot_scatterleft_scatterright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> Tuple[axes.Axes]:
    '''
    Scatter plot of y1 left vertical axis versus X
    Scatter plot of y2 right vertical axis versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  series for horizontal axis
    y1: series for y1 to plot using left vertical axis
    y2: series for y2 to plot using right vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax1.plot(X, y1, marker='.', linestyle='', color=c[1])
        ax2.plot(X, y2, marker='.', linestyle='', color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(XX, y1, numknots)
        model2 = natural_cubic_spline(XX, y2, numknots)
        ax1.plot(X, model1.predict(XX), marker='.', linestyle='', color=c[1])
        ax2.plot(X, model2.predict(XX), marker='.', linestyle='', color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (ax1, ax2)


def plot_lineleft_lineright_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None,
    numknots: int = None
) -> Tuple[axes.Axes]:
    '''
    Line plot of y1 left vertical axis versus X
    Line plot of y2 right vertical axis versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    x:  series for horizontal axis
    y1: series for y1 to plot using left vertical axis
    y2: series for y2 to plot using right vertical axis

    If smoothing is applied, the series must not contain NaN, inf, or -inf
    '''
    fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if smoothing is None:
        if X.dtype in ['datetime64[ns]']:
            loc = mdates.AutoDateLocator()
            fmt = mdates.AutoDateFormatter(loc)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(fmt)
            fig.autofmt_xdate()
        ax1.plot(X, y1, color=c[1])
        ax2.plot(X, y2, color=c[5])
    elif smoothing == 'natural_cubic_spline':
        if X.dtype in ['datetime64[ns]']:
            XX = pd.to_numeric(X)
            fig.autofmt_xdate()
        else:
            XX = X
        model1 = natural_cubic_spline(XX, y1, numknots)
        model2 = natural_cubic_spline(XX, y2, numknots)
        ax1.plot(X, model1.predict(XX), color=c[1])
        ax2.plot(X, model2.predict(XX), color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (ax1, ax2)


__all__ = (
    'plot_scatter_x_y',
    'plot_line_x_y',
    'plot_scatter_scatter_x_y1_y2',
    'plot_scatter_line_x_y1_y2',
    'plot_line_line_x_y1_y2',
    'plot_scatterleft_scatterright_x_y1_y2',
    'plot_lineleft_lineright_x_y1_y2',
)
