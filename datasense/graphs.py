'''
Graphical analysis
'''


from typing import Optional, Tuple
# from matplotlib.ticker import NullFormatter, NullLocator
# from matplotlib.dates import DateFormatter, MonthLocator
# import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.cm as cm
import pandas as pd


c = cm.Paired.colors


def plot_line_line_x_y1_y2(
    X: pd.Series,
    y1: pd.Series,
    y2: pd.Series,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> axes.Axes:
    '''
    Line plot of y1 versus X
    Line plot of y2 versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have the same units.

    X:  series for horizontal axis
    y1: series for y1 to plot on vertical axis
    y2: series for y2 to plot on vertical axis
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if X.dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax.plot(X, y1, marker=None, linestyle='-', color=c[1])
    ax.plot(X, y2, marker=None, linestyle='-', color=c[5])
    return ax


def plot_lineleft_lineright_x_y1_y2(
    df: pd.DataFrame,
    X: str,
    y1: str,
    y2: str,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> Tuple[axes.Axes]:
    '''
    Line plot of y1 left vertical axis versus X
    Line plot of y2 right vertical axis versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  column name for horizontal axis
    y1: column name for y1 to plot using left vertical axis
    y2: column name for y2 to plot using right vertical axis

    If smoothing is applied, the column must not contain NaN, inf, or -inf
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if df[X].dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax1.plot(df[X], df[y1], color=c[1])
    ax2.plot(df[X], df[y2], color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (ax1, ax2)


def plot_scatter_line_x_y1_y2(
    df: pd.DataFrame,
    X: str,
    y1: str,
    y2: str,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> axes.Axes:
    '''
    Scatter plot of y1 versus X
    Line plot of y2 versus X
    Optional smoothing applied to y1, y2

    This grpah is useful if y1 and y2 have the same units.

    x:  column name for horizontal axis
    y1: column name for y1 to plot on vertical axis
    y2: column name for y2 to plot on vertical axis
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if df[X].dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax.plot(df[X], df[y1], marker='.', linestyle='', color=c[1])
    ax.plot(df[X], df[y2], marker=None, linestyle='-', color=c[5])
    return ax


def plot_scatter_scatter_x_y1_y2(
    df: pd.DataFrame,
    X: str,
    y1: str,
    y2: str,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> axes.Axes:
    '''
    Scatter plot of y1 versus X
    Scatter plot of y2 versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have the same units.

    x:  column name for horizontal axis
    y1: column name for y1 to plot on vertical axis
    y2: column name for y2 to plot on vertical axis
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if df[X].dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax.plot(df[X], df[y1], marker='.', linestyle='', color=c[1])
    ax.plot(df[X], df[y2], marker='.', linestyle='', color=c[5])
    return ax


def plot_scatter_x_y(
    df: pd.DataFrame,
    X: str,
    y: str,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> axes.Axes:
    '''
    Scatter plot of y versus X
    Optional smoothing applied to y

    X: column name for horizontal axis
    y: column name for vertical axis
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax = fig.add_subplot(111)
    if df[X].dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax.plot(df[X], df[y], marker='.', linestyle='', color=c[1])
    return ax


def plot_scatterleft_scatterright_x_y1_y2(
    df: pd.DataFrame,
    X: str,
    y1: str,
    y2: str,
    figuresize: Optional[plt.Figure] = None,
    smoothing: str = None
) -> Tuple[axes.Axes]:
    '''
    Scatter plot of y1 left vertical axis versus X
    Scatter plot of y2 right vertical axis versus X
    Optional smoothing applied to y1, y2

    This graph is useful if y1 and y2 have different units or scales,
    and you wish to see if they are correlated.

    X:  column name for horizontal axis
    y1: column name for y1 to plot using left vertical axis
    y2: column name for y2 to plot using right vertical axis

    If smoothing is applied, the column must not contain NaN, inf, or -inf
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if df[X].dtype in ['datetime64[ns]']:
        fig.autofmt_xdate()
    ax1.plot(df[X], df[y1], marker='.', linestyle='', color=c[1])
    ax2.plot(df[X], df[y2], marker='.', linestyle='', color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (ax1, ax2)


__all__ = (
    'plot_line_line_x_y1_y2',
    'plot_lineleft_lineright_x_y1_y2',
    'plot_scatter_line_x_y1_y2',
    'plot_scatter_x_y',
    'plot_scatter_scatter_x_y1_y2',
    'plot_scatterleft_scatterright_x_y1_y2',
)
