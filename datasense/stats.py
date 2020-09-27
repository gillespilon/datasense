'''
Statistical analysis

- Non-parametric statistical summary
- Parametric statistical summary
- Cubic spline smoothing for Y vs X, can handle missing values
- Piecewise natural cubic spline helper
'''

from datetime import datetime, timedelta
from typing import List, Optional
import random
import sys

from sklearn.linear_model import LinearRegression
from basis_expansions import NaturalCubicSpline
from scipy.stats.mstats import mquantiles as mq
from scipy.interpolate import CubicSpline
from scipy.stats import norm, uniform, randint
from sklearn.pipeline import Pipeline
from numpy import arange
import pandas as pd
import numpy as np


def nonparametric_summary(
    series: pd.Series,
    alphap: float = 1/3,
    betap: float = 1/3
) -> pd.DataFrame:
    '''
    Calculate empirical quantiles for a series.

    scipy.stats.mstats.mquantiles

    R method 1, SAS method 3:
    not implemented

    R method 2, SAS method 5:
    not implemented

    R method 3, SAS method 2:
    not implemented

    R method 4, SAS method 1:
    alphap=0, betap=1

    R method 5:
    alphap=0.5, betap=0.5

    R method 6, SAS method 4, Minitab, SPSS:
    alphap=0, betap=0

    R method 7:
    alphap=1, betap=1

    R method 8:
    alphap=0.33, betap=0.33; is the recommended, default method

    R method 9:
    alphap=0.375, betap=0.375

    Cunnane's method:
    alphap=0.4, betap=0.4

    APL method;
    alphap=0.35, betap=0.35
    '''

    xm = np.ma.masked_array(series, mask=np.isnan(series))
    q25 = mq(xm, prob=(0.25), alphap=alphap, betap=betap)
    q50 = mq(xm, prob=(0.50), alphap=alphap, betap=betap)
    q75 = mq(xm, prob=(0.75), alphap=alphap, betap=betap)
    iqr = q75 - q25
    lof = (q25 - iqr * 3)
    lif = (q25 - iqr * 1.5)
    uif = (q75 + iqr * 1.5)
    uof = (q75 + iqr * 3)
    return pd.Series({
        'lower outer fence': lof[0],
        'lower inner fence': lif[0],
        'lower quartile': q25[0],
        'median': q50[0],
        'upper quartile': q75[0],
        'upper inner fence': uif[0],
        'upper outer fence': uof[0],
        'interquartile range': iqr[0],
        'inner outliers': [x for x in series if x < lif or x > uif],
        'outer outliers': [x for x in series if x < lof or x > uof],
        'minimum value': series.min(),
        'maximum value': series.max(),
        'count': series.count()
    })


def parametric_summary(series: pd.Series) -> pd.Series:
    '''
    Return parametric statistics.

    Returns
    -------
    n              = sample size
    min            = minimum value
    max            = maximum value
    average
    confidence interval of the average
    s              = sample standard deviation
    confidence interval of the sample standard deviation
    var            = sample variance
    confidence interval of the sample variance
    '''

    return pd.Series({
        'n': series.count(),
        'min': series.min(),
        'max': series.max(),
        'ave': series.mean(),
        's': series.std(),
        'var': series.var(),
    })


def cubic_spline(
    df: pd.DataFrame,
    abscissa: str,
    ordinate: str
) -> CubicSpline:
    '''
    Estimates the spline object for abscissa, ordinate of a dataframe
    Requires that abscissa, ordinate be integer or float
    Removes rows where there are missing values in abscissa and ordinate
    Removes duplicate rows
    Sorts the dataframe by abscissa in increasing order
    '''

    df = df.dropna(subset=[abscissa, ordinate])
    df = df.sort_values(by=abscissa, axis='rows', ascending=True)
    df = df.drop_duplicates(subset=abscissa, keep='first')
    spline = CubicSpline(df[abscissa], df[ordinate])
    return spline


def natural_cubic_spline(
    X: pd.Series,
    y: pd.Series,
    *,
    numberknots: Optional[int] = None,
    listknots: Optional[List[int]] = None
) -> Pipeline:
    '''
    Piecewise natural cubic spline helper function

    Provide numberknots or listknots

    If numberknots is given, the calculated knots are equally-spaced
    within minval and maxval. The endpoints are not included as knots.

    min:          the minimum of the interval containing the knots
    max:          the maximum of the interval containing the knots
    numberknots:  the number of knots to create.
    listknots:    the knots
    spline:       the model object
    '''

    if listknots:
        spline = NaturalCubicSpline(knots=listknots)
    else:
        spline = NaturalCubicSpline(
            max=max(X), min=min(X), n_knots=numberknots
        )
    p = Pipeline([
        ('natural_cubic_spline', spline),
        ('linear_regression', LinearRegression(fit_intercept=True))
    ])
    p.fit(X, y)
    return p


def random_data(
    *,
    distribution: Optional[str] = 'norm',
    size: Optional[int] = 42,
    loc: Optional[float] = 0,
    scale: Optional[float] = 1,
    low: Optional[int] = 13,
    high: Optional[int] = 69,
    strings: Optional[List[str]] = ['female', 'male']
) -> pd.Series:
    """

    Create a series of random items from a distribution.
    Parameters
    ----------
    distribution : str = 'norm'
        A scipy.stats distribution, the standard normal by default.
    size : int = 42
        The number of rows to create.
    loc : float = 0
        The center of a distribution.
    scale : float = 1
        The spread of a distribution.

    Returns
    -------
    pd.Series
        A pandas series of random items.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> from scipy.stats import norm, uniform
    >>> # Create series of the standard normal distribution, size = 42
    >>> series = ds.random_data()

    Example 2
    >>> # Create series of the normal distribution, size = 113, mean = 69,
    >>> # standard deviation = 13
    >>> series = ds.random_data(
    >>>     distribution='norm',
    >>>     size=117,
    >>>     loc=53,
    >>>     scale=11
    >>> )

    Example 3
    >>> # Create series of the standard uniform distribution, size = 42
    >>> series = ds.random_data(distribution='uniform')

    Example 4
    >>> # Create series of the uniform distribution, size = 113,
    >>> # min = 13, max = 69
    >>> series = ds.random_data(
    >>>     distribution='uniform',
    >>>     size=113,
    >>>     loc=13,
    >>>     scale=69
    >>> )

    Example 5
    >>> series = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     loc=13,
    >>>     scale=69
    >>> )

    Example 6
    >>> # Create series of random strings from the default list
    >>> series = ds.random_data(distribution='strings')

    Example 7
    >>> # Create series of random strings from a list of strings
    >>> series = ds.random_data(
    >>>     distribution='strings',
    >>>     size=113,
    >>>     strings=['tom', 'dick', 'harry']
    """
    distribution_list_continuous = ['norm', 'uniform']
    distribution_list_discrete = ['randint']
    distribution_list_strings = ['strings']
    distribution_list_bool = ['bool']
    if distribution in distribution_list_continuous:
        series = pd.Series(eval(distribution).rvs(
            size=size,
            loc=loc,
            scale=scale
            )
        )
    elif distribution in distribution_list_discrete:
        series = pd.Series(eval(distribution).rvs(
            low=low,
            high=high,
            size=size
            )
        )
    elif distribution in distribution_list_bool:
        series = pd.Series(eval('randint').rvs(
            low=0,
            high=2,
            size=size
            ).astype(dtype='bool')
        )
    elif distribution in distribution_list_strings:
        series = pd.Series(
            random.choices(
                population=strings,
                k=size
            )
        )
    else:
        return print(
            f'Distribution instance {distribution} is not implemented '
            'in datasense.'
            )
        sys.exit()
    return series


def datetime_data(
    *,
    start_year: Optional[str] = None,
    start_month: Optional[str] = None,
    start_day: Optional[str] = None,
    start_hour: Optional[str] = None,
    start_minute: Optional[str] = None,
    start_second: Optional[str] = None,
    end_year: Optional[str] = None,
    end_month: Optional[str] = None,
    end_day: Optional[str] = None,
    end_hour: Optional[str] = None,
    end_minute: Optional[str] = None,
    end_second: Optional[str] = None,
    time_delta: Optional[int] = 24
) -> pd.Series:
    if start_year:
        timestart = (
            start_year + '-' + start_month +
            '-' + start_day + 'T' + start_hour +
            ':' + start_minute + ':' + start_second
        )
        timeend = (
            end_year + '-' + end_month +
            '-' + end_day + 'T' + end_hour +
            ':' + end_minute + ':' + end_second
        )
    else:
        date_time_start = datetime.now()
        date_time_end = date_time_start + timedelta(days=42)
        timestart = (
            date_time_start.strftime('%Y') + '-' +
            date_time_start.strftime('%m') + '-' +
            date_time_start.strftime('%d') + 'T' +
            date_time_start.strftime('%H') + ':' +
            date_time_start.strftime('%M') + ':' +
            date_time_start.strftime('%S')
        )
        timeend = (
            date_time_end.strftime('%Y') + '-' +
            date_time_end.strftime('%m') + '-' +
            date_time_end.strftime('%d') + 'T' +
            date_time_end.strftime('%H') + ':' +
            date_time_end.strftime('%M') + ':' +
            date_time_end.strftime('%S')
        )
    series = pd.Series(
        arange(
            start=timestart,
            stop=timeend,
            step=timedelta(hours=time_delta),
            dtype='datetime64[s]'
        )
    )
    return series


__all__ = (
    'nonparametric_summary',
    'parametric_summary',
    'cubic_spline',
    'natural_cubic_spline',
    'random_data',
    'datetime_data',
)
