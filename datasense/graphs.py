'''
Graphical analysis
'''


from typing import Optional, Tuple
import matplotlib.axes as axes
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import NullFormatter, NullLocator
import pandas as pd


c = cm.Paired.colors


def plot_line_x_y1_y2(
    df: pd.DataFrame,
    X: str,
    y1: str,
    y2: str,
    figuresize: Optional[plt.Figure] = None
) -> Tuple[axes.Axes]:
    '''
    Line plot of y1 left vertical axis versus x
    Line plot of y2 right vertical axis versus x
    Smoothing applied to y1, y2
    '''
    if figuresize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figuresize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    if df[X].dtype in ['int64', 'float64']:
        ax1.plot(df[X], df[y1], color=c[1])
        ax2.plot(df[X], df[y2], color=c[5])
    elif df[X].dtype in ['datetime64[ns]']:
        ax1.plot(df[X], df[y1], color=c[1])
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(NullLocator())
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
        ax1.xaxis.set_minor_formatter(NullFormatter())
        ax2.plot(df[X], df[y2], color=c[5])
    for tl in ax1.get_yticklabels():
        tl.set_color(c[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(c[5])
    return (ax1, ax2)


__all__ = (
    'plot_line_x_y1_y2',
)
