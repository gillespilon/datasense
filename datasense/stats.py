"""
Statistical analysis

- Non-parametric statistical summary
- Parametric statistical summary
- Cubic spline smoothing for Y vs X, can handle missing values
- Piecewise natural cubic spline helper
- Generate random data of various distributions
- Generate datetime data
- Generate timedelta data
"""

from datetime import datetime, timedelta
from typing import List, Optional
import random
import sys

from sklearn.linear_model import LinearRegression
from basis_expansions import NaturalCubicSpline
from scipy.stats.mstats import mquantiles as mq
from pandas.api.types import CategoricalDtype
from scipy.interpolate import CubicSpline
from sklearn.pipeline import Pipeline
from numpy import arange
import pandas as pd
import numpy as np

pd.options.display.max_columns = 600
pd.options.display.max_rows = 600


def nonparametric_summary(
    series: pd.Series,
    alphap: float = 1/3,
    betap: float = 1/3
) -> pd.Series:
    """
    Calculate empirical quantiles for a series.

    Parameters
    ----------
    series : pd.Series
        The input series.
    alphap : float = 1/3
        Plotting positions.
    betap : float = 1/3
        Plotting positions.

        scipy.stats.mstats.mquantiles plotting positions:
        R method 1, SAS method 3:
            not yet implemented in scipy.stats.mstats.mquantiles
        R method 2, SAS method 5:
            not yet implemented in scipy.stats.mstats.mquantiles
        R method 3, SAS method 2:
            not yet implemented in scipy.stats.mstats.mquantiles
        R method 4, SAS method 1:
            alphap=0, betap=1
        R method 5:
            alphap=0.5, betap=0.5
        R method 6, SAS method 4, Minitab, SPSS:
            alphap=0, betap=0
        R method 7, Splus 3.1:
            alphap=1, betap=1
        R method 8:
            alphap=0.33, betap=0.33; is the recommended, default method
        R method 9:
            alphap=0.375, betap=0.375
        Cunnane's method:
            alphap=0.4, betap=0.4
        APL method;
            alphap=0.35, betap=0.35

    Returns
    -------
    pd.Series containing:
        lower outer fence : float
        lower inner fence : float
        lower quartile : float
        median : float
        upper quartile : float
        upper inner fence : float
        upper outer fence : float
        interquartile range : float
        inner outliers : List[float]
        outer outliers : List[float]
        minimum value : float
        maximum value : float
        count : int

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> series = ds.random_data()
    >>> series = ds.nonparametric_summary(series=series)
    >>> print(series)

    Example 2
    >>> series = ds.nonparametric_summary(
    >>>     series=series,
    >>>     alphap=0,
    >>>     betap=0
    >>> )
    >>> print(series)
    """
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
    """
    Return parametric statistics.

    Parameters
    ----------
    series : pd.Series
        The input series.

    Returns
    -------
    pd.Series
        The output series containing:
        n : sample size
        min : minimum value
        max : maximum value
        ave : average
        s : sample standard deviation
        var : sample variance

    Example
    -------
    >>> import datasense as ds
    >>> series = ds.random_data()
    >>> series = ds.parametric_summary(series=series)
    >>> print(series)
    """
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
    """
    Estimates the spline object for the abscissa and ordinate of a dataframe.

    - Requires that abscissa, ordinate be integer or float
    - Removes rows where there are missing values in abscissa and ordinate
    - Removes duplicate rows
    - Sorts the dataframe by abscissa in increasing order

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    abscissa : str
        The name of the abscissa column.
    ordinate : str
        The name of the ordinate column.

    Returns
    -------
    CubicSpline
        A cubic spline.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         'abscissa': ds.random_data(distribution='uniform'),
    >>>         'ordinate': ds.random_data(distribution='norm')
    >>>     }
    >>> ).sort_values(by=['abscissa'])
    >>> spline = ds.cubic_spline(
    >>>     df=df,
    >>>     abscissa='abscissa',
    >>>     ordinate='ordinate'
    >>> )
    >>> df['predicted'] = spline(df['abscissa'])
    >>> ds.plot_scatter_line_x_y1_y2(
    >>>     X=df['abscissa'],
    >>>     y1=df['ordinate'],
    >>>     y2=df['predicted']
    >>> )
    >>> plt.show()
    """
    df = df.dropna(subset=[abscissa, ordinate])
    df = df.sort_values(by=abscissa, axis='rows', ascending=True)
    df = df.drop_duplicates(subset=abscissa, keep='first')
    print(df)
    print(df.dtypes)
    spline = CubicSpline(
        x=df[abscissa],
        y=df[ordinate]
    )
    return spline


def natural_cubic_spline(
    X: pd.Series,
    y: pd.Series,
    number_knots: int,
    *,
    list_knots: Optional[List[int]] = None
) -> Pipeline:
    """
    Piecewise natural cubic spline helper function

    If number_knots is given, the calculated knots are equally-spaced
    within minval and maxval. The endpoints are not included as knots.

    The X series must be in increasing order.
    The y series must not contain missing values.

    Parameters
    ----------
    X : pd.Series
        The data series of the abscissa.
    y : pd.Series
        The data series of the ordinate.
    number_knots : int
        The number of knots for the spline.
    list_knots : Optional[List[int]] = None
        A list of specific knots.

    Returns
    -------
    p : sklearn.pipeline.Pipeline
        The model object.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> X = ds.random_data(distribution='uniform').sort_values()
    >>> y = ds.random_data(distribution='norm')
    >>> p = ds.natural_cubic_spline(
    >>>     X=X,
    >>>     y=y,
    >>>     number_knots=10
    >>> )
    >>> fig, ax = ds.plot_scatter_line_x_y1_y2(
    >>>     X=X,
    >>>     y1=y,
    >>>     y2=p.predict(X)
    >>> )
    >>> plt.show()
    """

    if list_knots:
        spline = NaturalCubicSpline(knots=list_knots)
    else:
        spline = NaturalCubicSpline(
            max=max(X),
            min=min(X),
            n_knots=number_knots
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
    high: Optional[int] = 70,
    strings: Optional[List[str]] = ['female', 'male'],
    categories: Optional[List[str]] = ['small', 'medium', 'large'],
    random_state: Optional[int] = None
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
    low : Optional[int] = 13,
        The low value (inclusive) for the integer distribution.
    high : Optional[int] = 70,
        The high value (exclusive) for the integer distribution.
    strings : Optional[List[str]] = ['female', 'male'],
        The list of strings for the distribution of strings.
    categories : Optional[List[str]] = ['small', 'medium', 'large'],
        The list of strings for the distribution of categories.
    random_state : Optional[int] = None
        The random number seed.

    Returns
    -------
    pd.Series
        A pandas series of random items.

    Notes
    -----
    distribution dtypes returned for distribution options:
    'uniform'    float64
    'bool'       boolean
    'boolean'    boolean (nullable)
    'strings'    str
    'norm'       float64
    'randint'    int64
    'randInt'    Int64 (nullable)
    'category'   category
    'categories' category of type CategoricalDtype(ordered=True)

    Examples
    --------
    Example 1
    # Generate a series of random floats, normal distribution,
    # with the default parameters.
    >>> import datasense as ds
    >>> s = ds.random_data()

    # Example 2
    # Generate a series of random floats, normal distribution,
    # with the default parameters.
    # Set random_state seed for repeatable sample.
    >>> s = ds.random_data(random_state=42)

    Example 3
    # Create a series of random float, normal distribution,
    # with sample size = 113, mean = 69, standard deviation = 13.
    >>> s = ds.random_data(
    >>>     distribution='norm',
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )

    Example 4
    # Create series of random floats, standard uniform distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution='uniform')

    Example 5
    # Create series of random floats, standard uniform distribution,
    # with the default parameters.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution='uniform',
    >>>     random_state=42
    >>> )

    Example 6
    # Create series of random floats, uniform distribution, size = 113,
    # min = 13, max = 69.
    >>> s = ds.random_data(
    >>>     distribution='uniform',
    >>>     size=113,
    >>>     loc=13,
    >>>     scale=70
    >>> )

    Example 7
    # Create series of random integers, integer distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution='randint')

    Example 8
    # Create series of random nullable integers, integer distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution='randInt')

    Example 9
    # Create series of random integers, integer distribution, size = 113,
    # min = 0, max = 1.
    >>> s = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     low=0,
    >>>     high=2
    >>> )

    Example 10
    # Create series of random integers, integer distribution, size = 113,
    # min = 0, max = 1.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution='randint',
    >>>     size=113,
    >>>     low=0,
    >>>     high=2,
    >>>     random_state=42
    >>> )

    Example 11
    # Create series of random strings from the default list.
    >>> s = ds.random_data(distribution='strings')

    Example 12
    # Create series of random strings from a list of strings.
    >>> s = ds.random_data(
    >>>     distribution='strings',
    >>>     size=113,
    >>>     strings=['tom', 'dick', 'harry']
    >>> )

    Example 13
    # Create series of random strings from a list of strings.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution='strings',
    >>>     size=113,
    >>>     strings=['tom', 'dick', 'harry'],
    >>>     random_state=42
    >>> )

    Example 14
    # Create series of random booleans with the default parameters.
    >>> s = ds.random_data(distribution='bool')

    Example 15
    # Create series of random nullable booleans with the default parameters.
    >>> s = ds.random_data(distribution='boolean')

    Example 16
    # Create series of random booleans, size = 113.
    >>> s = ds.random_data(
    >>> distribution='bool',
    >>> size=113
    >>> )

    Example 17
    # Create series of random booleans, size = 113.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>> distribution='bool',
    >>> size=113,
    >>> random_state=42
    >>> )

    Example 18
    # Create series of unordered categories.
    >>> s = ds.random_data(distribution='category')

    Example 19
    # Create series of ordered categories.
    >>> s = ds.random_data(distribution='categories')

    Example 20
    # Create series of ordered categories.
    >>> s = ds.random_data(
    >>>     distribution='categories',
    >>>     categories=['XS', 'S', 'M', 'L', 'XL'],
    >>>     size=113
    >>> )

    Example 21
    # Create series of ordered categories.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution='categories',
    >>>     categories=['XS', 'S', 'M', 'L', 'XL'],
    >>>     size=113,
    >>>     random_state=42
    >>> )

    Example 22
    # Create series of timedelta64[ns].
    >>> s = ds.random_data(
    >>>     distribution='timedelta',
    >>>     size=7
    >>> )
    >>> s

    Example 23
    # Create series of datetime64[ns].
    >>> s = ds.random_data(
    >>>     distribution='datetime',
    >>>     size=7
    >>> )
    >>> s
    """
    distribution_list_continuous = ['norm', 'uniform']
    distribution_list_discrete = ['randint', 'randInt']
    distribution_list_strings = ['strings']
    distribution_list_bool = ['bool', 'boolean']
    distribution_list_categories = ['category', 'categories']
    if distribution in distribution_list_continuous:
        series = pd.Series(eval(distribution).rvs(
            size=size,
            loc=loc,
            scale=scale,
            random_state=random_state
            )
        )
    elif distribution in distribution_list_discrete:
        if distribution == 'randInt':
            series = pd.Series(eval(distribution.lower()).rvs(
                low=low,
                high=high,
                size=size,
                random_state=random_state
                )
            ).astype(dtype='Int64')
        elif distribution == 'randint':
            series = pd.Series(eval(distribution).rvs(
                low=low,
                high=high,
                size=size,
                random_state=random_state
                )
            ).astype(dtype='int64')
    elif distribution in distribution_list_bool:
        if distribution == 'boolean':
            series = pd.Series(eval('randint').rvs(
                low=0,
                high=2,
                size=size,
                random_state=random_state
                )
            ).astype(dtype='boolean')
        elif distribution == 'bool':
            series = pd.Series(eval('randint').rvs(
                low=0,
                high=2,
                size=size,
                random_state=random_state
                )
            ).astype(dtype='bool')
    elif distribution in distribution_list_strings:
        random.seed(a=random_state)
        series = pd.Series(
            random.choices(
                population=strings,
                k=size
            )
        )
    elif distribution in distribution_list_categories:
        if distribution == 'categories':
            random.seed(a=random_state)
            series = pd.Series(
                random.choices(
                    population=categories,
                    k=size
                )
            ).astype(
                CategoricalDtype(
                    categories=categories,
                    ordered=True
                )
            )
        elif distribution == 'category':
            random.seed(a=random_state)
            series = pd.Series(
                random.choices(
                    population=categories,
                    k=size
                )
            ).astype('category')
    elif distribution == 'timedelta':
        series = timedelta_data(time_delta_days=size-1)
    elif distribution == 'datetime':
        series = datetime_data(time_delta_days=size-1)
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
    time_delta_days: Optional[int] = 41,
    time_delta_hours: Optional[int] = 24
) -> pd.Series:
    """
    Create a series of datetime data.

    Parameters
    ----------
    start_year : Optional[str] = None,
        The start year of the series.
    start_month : Optional[str] = None,
        The start month of the series.
    start_day : Optional[str] = None,
        The start day of the series.
    start_hour : Optional[str] = None,
        The start hour of the series.
    start_minute : Optional[str] = None,
        The start minute of the series.
    start_second : Optional[str] = None,
        The start second of the series.
    end_year : Optional[str] = None,
        The end year of the series.
    end_month : Optional[str] = None,
        The end month of the series.
    end_day : Optional[str] = None,
        The end day of the series.
    end_hour : Optional[str] = None,
        The end hour of the series.
    end_minute : Optional[str] = None,
        The end minute of the series.
    end_second : Optional[str] = None,
        The end second of the series.
    time_delta_days : Optional[int] = 42,
        The daily increment for the series.
    time_delta_hours : Optional[int] = 24
        The hourly increment for the series.

    Returns
    -------
    pd.Series
        The datetime series.

    Example
    -------
    Example 1
    >>> # Create a default datetime series
    >>> X = ds.datetime_data()

    Example 2
    >>> # Create a datetime series of one month in increments of six hours
    >>> X = ds.datetime_data(
    >>>     start_year='2020',
    >>>     start_month='01',
    >>>     start_day='01',
    >>>     start_hour='00',
    >>>     start_minute='00',
    >>>     start_second='00',
    >>>     end_year='2020',
    >>>     end_month='02',
    >>>     end_day='01',
    >>>     end_hour='00',
    >>>     end_minute='00',
    >>>     end_second='00',
    >>>     time_delta_hours=6
    >>> )
    """
    # TODO: Complete this code for all possibilities of timedelta
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
        date_time_end = date_time_start + timedelta(
            days=time_delta_days,
            hours=time_delta_hours
        )
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
            step=timedelta(hours=time_delta_hours),
            dtype='datetime64[s]'
        )
    )
    return series


def timedelta_data(
    *,
    time_delta_days: Optional[int] = 41
) -> pd.Series:
    # TODO: Add other parameters beyond time_delta_days
    """
    Create a series of timedelta data.

    Parameters
    ----------
    time_delta_days : Optional[int] = 41
        The number of rows to create.

    Returns
    -------
    series : pd.Series
        The output series.
    """
    series = datetime_data(time_delta_days=time_delta_days) -\
        datetime_data(time_delta_days=time_delta_days)
    return series


__all__ = (
    'nonparametric_summary',
    'parametric_summary',
    'cubic_spline',
    'natural_cubic_spline',
    'random_data',
    'datetime_data',
    'timedelta_data',
)
