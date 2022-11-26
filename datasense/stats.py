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
from typing import List, Tuple, Union
import statistics
import random
import math
import sys

from sklearn.linear_model import LinearRegression
from statsmodels.stats.power import TTestIndPower
from basis_expansions import NaturalCubicSpline
from scipy.stats.mstats import mquantiles as mq
from scipy.stats import norm, uniform, randint
from statsmodels.stats.power import TTestPower
from pandas.api.types import CategoricalDtype
import statsmodels.stats.diagnostic as smd
from scipy.interpolate import CubicSpline
from sklearn.pipeline import Pipeline
import statsmodels.api as sm
import scipy.stats as stats
from numpy import arange
import pandas as pd
import numpy as np

pd.options.display.max_columns = 600
pd.options.display.max_rows = 600


def nonparametric_summary(
    *,
    series: pd.Series,
    alphap: float = 1/3,
    betap: float = 1/3,
    decimals: int = 3
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
    decimals : int = 3
        The number of decimal places for rounding.

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
        R method 7, Splus 3.1, R default, pandas default, NumPy 'linear':
            alphap=1, betap=1
        R method 8:
            alphap=0.33, betap=0.33; NumPy 'median_unbiased'
        R method 9:
            alphap=0.375, betap=0.375
        Cunnane's method, SciPy default:
            alphap=0.4, betap=0.4
        APL method;
            alphap=0.35, betap=0.35

    Notes
    -----

    The 1.57 used to calculate the confidence intervals was empirically
    determined. See:
    McGill, Robert, John W. Tukey, and Wayne A. Larsen (Feb. 1978).
    “Variations of Box Plots”. In: The American Statistician
    32.1, pp. 12–16. doi: https://doi.org/10.2307/2683468. url:
    https://www.jstor.org/stable/2683468.

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
    cil = (q50 - 1.57 * iqr / math.sqrt(series.count()))[0]
    ciu = (q50 + 1.57 * iqr / math.sqrt(series.count()))[0]
    return pd.Series({
        "lower outer fence": round(number=lof[0], ndigits=decimals),
        "lower inner fence": round(number=lif[0], ndigits=decimals),
        "lower quartile": round(number=q25[0], ndigits=decimals),
        "median": round(number=q50[0], ndigits=decimals),
        "confidence interval": (
            round(number=cil, ndigits=decimals),
            round(number=ciu, ndigits=decimals)
        ),
        "upper quartile": round(number=q75[0], ndigits=decimals),
        "upper inner fence": round(number=uif[0], ndigits=decimals),
        "upper outer fence": round(number=uof[0], ndigits=decimals),
        "interquartile range": round(number=iqr[0], ndigits=decimals),
        "inner outliers":
            [
                round(number=x, ndigits=decimals)
                for x in series if x < lif or x > uif],
        "outer outliers":
            [
                round(number=x, ndigits=decimals)
                for x in series if x < lof or x > uof
            ],
        "minimum value": round(number=series.min(), ndigits=decimals),
        "maximum value": round(number=series.max(), ndigits=decimals),
        "count": series.count()
    })


def parametric_summary(
    *,
    series: pd.Series,
    decimals: int = 3
) -> pd.Series:
    """
    Return parametric statistics.

    Parameters
    ----------
    series : pd.Series
        The input series.
    decimals : int = 3
        The number of decimal places for rounding.

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
    ciaverage = stats.t.interval(
            confidence=0.95,
            df=len(series)-1,
            loc=np.mean(a=series),
            scale=stats.sem(series)
        )
    return pd.Series(
        data={
            "n": series.count(),
            "min": round(number=series.min(), ndigits=decimals),
            "max": round(number=series.max(), ndigits=decimals),
            "ave": round(number=series.mean(), ndigits=decimals),
            "confidence interval": (
                round(number=ciaverage[0], ndigits=decimals),
                round(number=ciaverage[1], ndigits=decimals)
            ),
            "s": round(number=series.std(), ndigits=decimals),
            "var": round(number=series.var(), ndigits=decimals),
        }
    )


def cubic_spline(
    *,
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
    spline: CubicSpline
        A cubic spline.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         "abscissa": ds.random_data(distribution="uniform"),
    >>>         "ordinate": ds.random_data(distribution="norm")
    >>>     }
    >>> ).sort_values(by=["abscissa"])
    >>> spline = ds.cubic_spline(
    >>>     df=df,
    >>>     abscissa="abscissa",
    >>>     ordinate="ordinate"
    >>> )
    >>> df["predicted"] = spline(df["abscissa"])
    >>> ds.plot_scatter_line_x_y1_y2(
    >>>     X=df["abscissa"],
    >>>     y1=df["ordinate"],
    >>>     y2=df["predicted"]
    >>> )
    >>> plt.show()
    """
    df = df.dropna(subset=[abscissa, ordinate])
    df = df.sort_values(by=abscissa, axis="rows", ascending=True)
    df = df.drop_duplicates(subset=abscissa, keep="first")
    print(df)
    print(df.dtypes)
    spline = CubicSpline(
        x=df[abscissa],
        y=df[ordinate]
    )
    return spline


def natural_cubic_spline(
    *,
    X: pd.Series,
    y: pd.Series,
    number_knots: int,
    list_knots: List[int] = None
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
    list_knots : List[int] = None
        A list of specific knots.

    Returns
    -------
    p: Pipeline
        The model object.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> import datasense as ds
    >>> X = ds.random_data(distribution="uniform").sort_values()
    >>> y = ds.random_data(distribution="norm")
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
        ("natural_cubic_spline", spline),
        ("linear_regression", LinearRegression(fit_intercept=True))
    ])
    p.fit(X, y)
    return p


def random_data(
    *,
    distribution: str = "norm",
    size: int = 42,
    loc: float = 0,
    scale: float = 1,
    low: int = 13,
    high: int = 70,
    strings: List[str] = ["female", "male"],
    categories: List[str] = ["small", "medium", "large"],
    random_state: int = None,
    fraction_nan: float = 0.13,
    name: str = None
) -> pd.Series:
    """
    Create a series of random items from a distribution.

    Parameters
    ----------
    distribution : str = "norm"
        A scipy.stats distribution, the standard normal by default.
    size : int = 42
        The number of rows to create.
    loc : float = 0
        The center of a distribution.
    scale : float = 1
        The spread of a distribution.
    low : int = 13,
        The low value (inclusive) for the integer distribution.
    high : int = 70,
        The high value (exclusive) for the integer distribution.
    strings : List[str] = ["female", "male"],
        The list of strings for the distribution of strings.
    categories : List[str] = ["small", "medium", "large"],
        The list of strings for the distribution of categories.
    random_state : int = None
        The random number seed.
    fraction_nan : float = 0.13
        The fraction of cells to be made np.NaN.
    name : str = None
        The name of the Series.

    Returns
    -------
    series: pd.Series
        A pandas series of random items.

    Notes
    -----
    distribution dtypes returned for distribution options:
    "uniform"    float64
    "bool"       boolean
    "boolean"    boolean (nullable)
    "strings"    str
    "norm"       float64
    "randint"    int64
    "randInt"    Int64 (nullable)
    "category"   category
    "categories" category of type CategoricalDtype(ordered=True)

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
    >>>     distribution="norm",
    >>>     size=113,
    >>>     loc=69,
    >>>     scale=13
    >>> )

    Example 4
    # Create series of random floats, standard uniform distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution="uniform")

    Example 5
    # Create series of random floats, standard uniform distribution,
    # with the default parameters.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution="uniform",
    >>>     random_state=42
    >>> )

    Example 6
    # Create series of random floats, uniform distribution, size = 113,
    # min = 13, max = 69.
    >>> s = ds.random_data(
    >>>     distribution="uniform",
    >>>     size=113,
    >>>     loc=13,
    >>>     scale=70
    >>> )

    Example 7
    # Create series of random integers, integer distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution="randint")

    Example 8
    # Create series of random nullable integers, integer distribution,
    # with the default parameters.
    >>> s = ds.random_data(distribution="randInt")

    Example 9
    # Create series of random integers, integer distribution, size = 113,
    # min = 0, max = 1.
    >>> s = ds.random_data(
    >>>     distribution="randint",
    >>>     size=113,
    >>>     low=0,
    >>>     high=2
    >>> )

    Example 10
    # Create series of random integers, integer distribution, size = 113,
    # min = 0, max = 1.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution="randint",
    >>>     size=113,
    >>>     low=0,
    >>>     high=2,
    >>>     random_state=42
    >>> )

    Example 11
    # Create series of random strings from the default list.
    >>> s = ds.random_data(distribution="strings")

    Example 12
    # Create series of random strings from a list of strings.
    >>> s = ds.random_data(
    >>>     distribution="strings",
    >>>     size=113,
    >>>     strings=["tom", "dick", "harry"]
    >>> )

    Example 13
    # Create series of random strings from a list of strings.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution="strings",
    >>>     size=113,
    >>>     strings=["tom", "dick", "harry"],
    >>>     random_state=42
    >>> )

    Example 14
    # Create series of random booleans with the default parameters.
    >>> s = ds.random_data(distribution="bool")

    Example 15
    # Create series of random nullable booleans with the default parameters.
    >>> s = ds.random_data(distribution="boolean")

    Example 16
    # Create series of random booleans, size = 113.
    >>> s = ds.random_data(
    >>> distribution="bool",
    >>> size=113
    >>> )

    Example 17
    # Create series of random booleans, size = 113.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>> distribution="bool",
    >>> size=113,
    >>> random_state=42
    >>> )

    Example 18
    # Create series of unordered categories.
    >>> s = ds.random_data(distribution="category")

    Example 19
    # Create series of ordered categories.
    >>> s = ds.random_data(distribution="categories")

    Example 20
    # Create series of ordered categories.
    >>> s = ds.random_data(
    >>>     distribution="categories",
    >>>     categories=["XS", "S", "M", "L", "XL"],
    >>>     size=113
    >>> )

    Example 21
    # Create series of ordered categories.
    # Set random_state seed for repeatable sample
    >>> s = ds.random_data(
    >>>     distribution="categories",
    >>>     categories=["XS", "S", "M", "L", "XL"],
    >>>     size=113,
    >>>     random_state=42
    >>> )

    Example 22
    # Create series of timedelta64[ns].
    >>> s = ds.random_data(
    >>>     distribution="timedelta",
    >>>     size=7
    >>> )
    >>> s

    Example 23
    # Create series of datetime64[ns].
    >>> s = ds.random_data(
    >>>     distribution="datetime",
    >>>     size=7
    >>> )
    >>> s
    """
    distribution_list_continuous = ["norm", "uniform"]
    distribution_list_discrete = ["randint", "randInt"]
    distribution_list_strings = ["strings"]
    distribution_list_bool = ["bool", "boolean"]
    distribution_list_categories = ["category", "categories"]
    if distribution in distribution_list_continuous:
        series = pd.Series(eval(distribution).rvs(
            size=size,
            loc=loc,
            scale=scale,
            random_state=random_state
            ),
            name=name
        )
    elif distribution in distribution_list_discrete:
        if distribution == "randInt":
            series = pd.Series(eval(distribution.lower()).rvs(
                low=low,
                high=high,
                size=size,
                random_state=random_state
                ),
                name=name
            )
            series[series.sample(frac=fraction_nan).index] = np.NaN
            series = series.astype(dtype="Int64")
        elif distribution == "randint":
            series = pd.Series(eval(distribution).rvs(
                low=low,
                high=high,
                size=size,
                random_state=random_state
                ),
                name=name
            ).astype(dtype="int64")
    elif distribution in distribution_list_bool:
        if distribution == "boolean":
            series = pd.Series(eval("randint").rvs(
                low=0,
                high=2,
                size=size,
                random_state=random_state
                ),
                name=name
            )
            series[series.sample(frac=fraction_nan).index] = np.NaN
            series = series.astype(dtype="boolean")
        elif distribution == "bool":
            series = pd.Series(eval("randint").rvs(
                low=0,
                high=2,
                size=size,
                random_state=random_state
                ),
                name=name
            ).astype(dtype="bool")
    elif distribution in distribution_list_strings:
        random.seed(a=random_state)
        series = pd.Series(
            random.choices(
                population=strings,
                k=size
            ),
            name=name
        )
    elif distribution in distribution_list_categories:
        if distribution == "categories":
            random.seed(a=random_state)
            series = pd.Series(
                random.choices(
                    population=categories,
                    k=size
                ),
                name=name
            ).astype(
                CategoricalDtype(
                    categories=categories,
                    ordered=True
                )
            )
        elif distribution == "category":
            random.seed(a=random_state)
            series = pd.Series(
                random.choices(
                    population=categories,
                    k=size
                ),
                name=name
            ).astype(dtype="category")
    elif distribution == "timedelta":
        series = timedelta_data(time_delta_days=size-1).rename(name)
    elif distribution == "datetime":
        series = datetime_data(time_delta_days=size-1).rename(name)
    else:
        return print(
            f"Distribution instance {distribution} is not implemented "
            "in datasense."
            )
        sys.exit()
    return series


def datetime_data(
    *,
    start_year: str = None,
    start_month: str = None,
    start_day: str = None,
    start_hour: str = None,
    start_minute: str = None,
    start_second: str = None,
    end_year: str = None,
    end_month: str = None,
    end_day: str = None,
    end_hour: str = None,
    end_minute: str = None,
    end_second: str = None,
    time_delta_days: int = 41,
    time_delta_hours: int = 24
) -> pd.Series:
    """
    Create a series of datetime data.

    Parameters
    ----------
    start_year : str = None,
        The start year of the series.
    start_month : str = None,
        The start month of the series.
    start_day : str = None,
        The start day of the series.
    start_hour : str = None,
        The start hour of the series.
    start_minute : str = None,
        The start minute of the series.
    start_second : str = None,
        The start second of the series.
    end_year : str = None,
        The end year of the series.
    end_month : str = None,
        The end month of the series.
    end_day : str = None,
        The end day of the series.
    end_hour : str = None,
        The end hour of the series.
    end_minute : str = None,
        The end minute of the series.
    end_second : str = None,
        The end second of the series.
    time_delta_days : int = 41,
        The daily increment for the series.
    time_delta_hours : int = 24
        The hourly increment for the series.

    Returns
    -------
    series: pd.Series
        The datetime series.

    Example
    -------
    Example 1
    >>> import datasense as ds
    >>> # Create a default datetime series
    >>> X = ds.datetime_data()

    Example 2
    >>> # Create a datetime series of one month in increments of six hours
    >>> X = ds.datetime_data(
    >>>     start_year="2020",
    >>>     start_month="01",
    >>>     start_day="01",
    >>>     start_hour="00",
    >>>     start_minute="00",
    >>>     start_second="00",
    >>>     end_year="2020",
    >>>     end_month="02",
    >>>     end_day="01",
    >>>     end_hour="00",
    >>>     end_minute="00",
    >>>     end_second="00",
    >>>     time_delta_hours=6
    >>> )
    """
    # TODO: Complete this code for all possibilities of timedelta
    if start_year:
        timestart = (
            start_year + "-" + start_month +
            "-" + start_day + "T" + start_hour +
            ":" + start_minute + ":" + start_second
        )
        timeend = (
            end_year + "-" + end_month +
            "-" + end_day + "T" + end_hour +
            ":" + end_minute + ":" + end_second
        )
    else:
        date_time_start = datetime.now()
        date_time_end = date_time_start + timedelta(
            days=time_delta_days,
            hours=time_delta_hours
        )
        timestart = (f"{(date_time_start):%FT%T}")
        timeend = (f"{(date_time_end):%FT%T}")
    # TODO: pandas has timestamp limitations of about 584 years
    # http://pandas-docs.github.io/pandas-docs-travis/user_guide/timeseries.html#timeseries-timestamp-limits
    # Need to fix above and below
    series = pd.Series(
        arange(
            start=timestart,
            stop=timeend,
            step=timedelta(hours=time_delta_hours),
            dtype="datetime64[s]"
        )
    )
    return series


def timedelta_data(
    *,
    time_delta_days: int = 41
) -> pd.Series:
    # TODO: Add other parameters beyond time_delta_days
    """
    Create a series of timedelta data.

    Parameters
    ----------
    time_delta_days : int = 41
        The number of rows to create.

    Returns
    -------
    series : pd.Series
        The output series.

    Example
    -------
    >>> import datasense as ds
    >>> number_days_plus_one = 42
    >>> series = timedelta_data(time_delta_days=number_days_plus_one)
    """
    series = datetime_data(time_delta_days=time_delta_days) -\
        datetime_data(time_delta_days=time_delta_days)
    return series


def one_sample_t(
    *,
    series: pd.Series,
    hypothesized_value: Union[int, float],
    alternative_hypothesis: str = "two-sided",
    significance_level: float = 0.05,
    width: int = 7,
    decimals: int = 3
) -> Tuple[float, float, float]:
    """
    One-sample t test.

    - Parametric statistics are calculated for the sample.
    - Non-parametric statistics are calculated for the sample.
    - The assumption for normality of each sample is evaluated.
        - Shapiro-Wilk, a parametric test
        - Anderson-Darling, a non-parametric test
        - Kolmogorov-Smirnov, a non-parametric test

    Parameters
    ----------
    series : pd.Series,
        The Series of data, consisting of one column with a label y.
    hypothesized_value : Union[int, float]
        The hypothesized value for the test.
    alternative_hypothesis : str = "two-sided",
        The alternative hypothesis for the t test.
        "two-sided" the sample is different from the hypothesized value
        "less" the sample is less than the hypothesized value
        "greater" the sample is greater than the hypothesized value
    significance_level : float = 0.05
        The significance level for rejecting the null hypothesis.
    width : int = 7
        The width for the formatted number.
    decimals : int = 3
        The number of decimal places for the formatted number.

    Returns
    -------
    t statistic : float
        The t statistic for the hypothesis.
    p value : float
        The p value for the t statistic.
    power : float
        The power of the t test.

    Examples
    --------
    Example 1
    import datasense as ds
    >>> t_test_result = ds.one_sample_t(
    >>>     series=series,
    >>>     hypothesized_value=hypothesized_value,
    >>>     alternative_hypothesis="two-sided",
    >>>     significance_level=0.05,
    >>>     width=7,
    >>>     significance_level=0.05
    >>> )
    # t_test_result is a tuple of t statistic, p value, power of the test

    Example 2
    >>> t_test_result = ds.one_sample_t(
    >>>     series=series,
    >>>     hypothesized_value=hypothesized_value,
    >>>     alternative_hypothesis="less",
    >>>     significance_level=0.05,
    >>>     width=7,
    >>>     significance_level=0.05
    >>> )
    # t_test_result is a tuple of t statistic, p value, power of the test

    Example 3
    >>> t_test_result = ds.one_sample_t(
    >>>     series=series,
    >>>     hypothesized_value=hypothesized_value,
    >>>     alternative_hypothesis="greater",
    >>>     significance_level=0.05,
    >>>     width=7,
    >>>     significance_level=0.05
    >>> )
    # t_test_result is a tuple of t statistic, p value, power of the test
    """
    print(
        "The one-sample t test is used to determine if the average of one "
        "sample of data is statistically, significantly different from a "
        "hypothesized value."
    )
    print()
    print("Assumptions")
    print("-----------")
    print()
    print("The data are continuous interval or ratio scales.")
    print()
    print(
        "The data in each sample follow a normal distribution with mean mu "
        "and variance sigma squared."
    )
    print("The data should be sampled independently from the population.")
    print()
    print("Results")
    print("-------")
    print()
    parametric_statistics = parametric_summary(
        series=series,
        decimals=decimals
    ).to_string()
    print("Parametric statistics for y")
    print(parametric_statistics)
    print()
    nonparametric_statistics = nonparametric_summary(
        series=series,
        alphap=1/3,
        betap=1/3,
        decimals=decimals
    ).to_string()
    print()
    print("Shapiro-Wilk results for normal distribution lack-of-fit test")
    shapiro_wilk_test_statistic, shapiro_wilk_p_value =\
        stats.shapiro(x=series)
    print(
        "Shapiro-Wilk test statistic: "
        f"{shapiro_wilk_test_statistic:{width}.{decimals}f}"
    )
    print(
        "Shapiro-Wilk p value       : "
        f"{shapiro_wilk_p_value:{width}.{decimals}f}")
    if shapiro_wilk_p_value < significance_level:
        print(
            "The data in the sample probably do not follow a normal "
            "distribution."
        )
    else:
        print(
            "The data in the sample probably follow a normal "
            "distribution."
        )
    print()
    print("Non-parametric statistics for y")
    print(nonparametric_statistics)
    print()
    ad_test_statistic, ad_critical_values, ad_significance_level =\
        stats.anderson(x=series, dist="norm")
    # uncomment these lines when Anaconda release Python 3.10
    # start uncomment
    # match significance_level:
    #     case 0.25:
    #         item = 0
    #     case 0.10:
    #         item = 1
    #     case 0.05:
    #         item = 2
    #     case 0.025:
    #         item = 3
    #     case 0.01:
    #         item = 4
    #     case 0.005:
    #         item = 5
    # end uncomment
    # start delele
    if significance_level == 0.25:
        item = 0
    elif significance_level == 0.10:
        item = 1
    elif significance_level == 0.05:
        item = 2
    elif significance_level == 0.025:
        item = 3
    elif significance_level == 0.01:
        item = 4
    elif significance_level == 0.005:
        item = 5
    # end delete
    print(
        "Anderson-Darling results for normal distribution lack-of-fit test"
    )
    print(
        "Anderson-Darling test statistic: "
        f"{ad_test_statistic:{width}.{decimals}f}")
    print(
        "Anderson-Darling critical value: "
        f"{ad_critical_values[item]:{width}.{decimals}f}"
    )
    if ad_test_statistic > ad_critical_values[item]:
        print(
            "The data in the sample probably do not follow a normal "
            "distribution."
        )
    else:
        print(
            "The data in the sample probably follow a normal "
            "distribution."
        )
    print()
    kolmogorov_smirnov_test_statistic, kolmogorov_smirnov_test_pvalue = \
        ksstat, kspvalue = smd.kstest_normal(
            x=series,
            dist="norm",
            pvalmethod="approx"
        )
    print(
        "Kolmogorov-Smirnov results for normal distribution lack-of-fit test"
    )
    print(
        "Kolmogorov-Smirnov test statistic: "
        f"{kolmogorov_smirnov_test_statistic:{width}.{decimals}f}")
    print(
        "Kolmogorov-Smirnov p value: "
        f"{kolmogorov_smirnov_test_pvalue:{width}.{decimals}f}"
    )
    if kolmogorov_smirnov_test_pvalue < significance_level:
        print(
            "The data in the sample probably do not follow a normal "
            "distribution."
        )
    else:
        print(
            "The data in the sample probably follow a normal "
            "distribution."
        )
    print()
    if alternative_hypothesis == "two-sided":
        message_ho =\
            "Ho: average of sample == hypothesized_value\n"\
            "Ha: average of sample != hypothesized_value\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that the sample "\
            "average is different from the hypothesized value."
        message_ha =\
            "Ho: average of sample == hypothesized value\n"\
            "Ha: average of sample != hypothesized value\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that the sample "\
            "average is different from the hypothesized value."
        t_test_result = stats.ttest_1samp(
            a=series,
            popmean=hypothesized_value,
            alternative=alternative_hypothesis
        )
        power = TTestPower().power(
            effect_size=math.fabs(
                (hypothesized_value - series.mean()) / series.std()
            ),
            nobs=series.count(),
            alpha=significance_level,
            alternative='two-sided'
        )
        t_value_alpha_by_two = (
            -1 * stats.t.isf(
                q=significance_level / 2,
                df=series.count() - 1
            )
        )
        t_value_one_minus_alpha_by_two = (
            stats.t.isf(
                q=significance_level / 2,
                df=series.count() - 1
            )
        )
        hypothesis_test_ci_lower_bound = (
            series.mean() + series.sem() * t_value_alpha_by_two
        )
        hypothesis_test_ci_upper_bound = (
            series.mean() + series.sem() * t_value_one_minus_alpha_by_two
        )
        if t_test_result.pvalue < significance_level:
            print(message_ha)
        else:
            print(message_ho)
        print()
        print("t test results")
        print(f"average             {series.mean():{width}.{decimals}f}")
        print(f"hypothesized value  {hypothesized_value:{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound:{width}.{decimals}f}"
        )
        print(
            "t test statistic    "
            f"{t_test_result.statistic:{width}.{decimals}f}"
        )
        print(
            f"t test p value      {t_test_result.pvalue:{width}.{decimals}f}"
        )
        print(f"significance level  {significance_level:{width}.{decimals}f}")
        print(f"power of the test   {power:{width}.{decimals}f}")
        print()
    elif alternative_hypothesis == "less":
        message_ho =\
            "Ho: average of sample == hypothesized value\n"\
            "Ha: average of sample < hypothesized value\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that "\
            "the sample average is less than the "\
            "hypothesized value."
        message_ha =\
            "Ho: average of sample == hypothesized value\n"\
            "Ha: average of sample < hypothesized value\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that "\
            "the sample average is less than the "\
            "hypothesized value."
        t_test_result = stats.ttest_1samp(
            a=series,
            popmean=hypothesized_value,
            alternative=alternative_hypothesis
        )
        power = TTestPower().power(
            effect_size=math.fabs(
                (hypothesized_value - series.mean()) / series.std()
            ),
            nobs=series.count(),
            alpha=significance_level,
            alternative='smaller'
        )
        t_value_alpha = (
            stats.t.isf(
                q=significance_level,
                df=series.count() - 1
            )
        )
        hypothesis_test_ci_lower_bound = "N/A"
        hypothesis_test_ci_upper_bound = (
            series.mean() + series.sem() * t_value_alpha
        )
        if t_test_result.pvalue < significance_level:
            print(message_ha)
        else:
            print(message_ho)
        print()
        print("t test results")
        print(f"average             {series.mean():{width}.{decimals}f}")
        print(f"hypothesized value  {hypothesized_value:{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound}, "
            f"{hypothesis_test_ci_upper_bound:{width}.{decimals}f}"
        )
        print(
            "t test statistic    "
            f"{t_test_result.statistic:{width}.{decimals}f}"
        )
        print(
            f"t test p value      {t_test_result.pvalue:{width}.{decimals}f}"
        )
        print(f"significance level  {significance_level:{width}.{decimals}f}")
        print(f"power of the test   {power:{width}.{decimals}f}")
        print()
    elif alternative_hypothesis == "greater":
        message_ho =\
            "Ho: average of sample == hypothesized value\n"\
            "Ha: average of sample > hypothesized value\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that "\
            "the average of the sample is greater than the "\
            "hypothesized value."
        message_ha =\
            "Ho: average of sample == hypothesized value\n"\
            "Ha: average of sample > hypothesized value\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that "\
            "the average of the sample is greater than the "\
            "hypothesized value."
        t_test_result = stats.ttest_1samp(
            a=series,
            popmean=hypothesized_value,
            alternative=alternative_hypothesis
        )
        power = TTestPower().power(
            effect_size=math.fabs(
                (hypothesized_value - series.mean()) / series.std()
            ),
            nobs=series.count(),
            alpha=significance_level,
            alternative='larger'
        )
        t_value_alpha = (
            -1 * stats.t.isf(
                q=significance_level,
                df=series.count() - 1
            )
        )
        hypothesis_test_ci_lower_bound = (
            series.mean() + series.sem() * t_value_alpha
        )
        hypothesis_test_ci_upper_bound = "N/A"
        if t_test_result.pvalue < significance_level:
            print(message_ha)
        else:
            print(message_ho)
        print()
        print("t test results")
        print(f"average             {series.mean():{width}.{decimals}f}")
        print(f"hypothesized value  {hypothesized_value:{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound}"
        )
        print(
            "t test statistic    "
            f"{t_test_result.statistic:{width}.{decimals}f}"
        )
        print(
            f"t test p value      {t_test_result.pvalue:{width}.{decimals}f}"
        )
        print(f"significance level  {significance_level:{width}.{decimals}f}")
        print(f"power of the test   {power:{width}.{decimals}f}")
        print()
    return (
        t_test_result.statistic, t_test_result.pvalue, power,
        shapiro_wilk_test_statistic, shapiro_wilk_p_value,
        ad_test_statistic, ad_critical_values[2],
        ksstat, kspvalue,
        hypothesis_test_ci_lower_bound, hypothesis_test_ci_upper_bound
    )


def two_sample_t(
    *,
    series1: pd.Series,
    series2: pd.Series,
    alternative_hypothesis: str = "two-sided",
    significance_level: float = 0.05,
    width: int = 7,
    decimals: int = 3
) -> Tuple[float, float, float]:
    """
    Two-sample t test.

    - Parametric statistics are calculated for each sample.
    - Non-parametric statistics are calculated for each sample.
    - The assumption for normality of each sample is evaluted.
        - Shapiro-Wilk, a parametric test
        - Anderson-Darling, a non-parametric test
    - The homogeneity of variance of the samples is evaluated.
        - Bartlett, a parametric test
        - Levene, a non-parametric test

    Parameters
    ----------
    series1 : pd.Series
        The first series of data, with a name.
    series2 : pd.Series
        The second series of data, with a name.
    alternative_hypothesis : str = "two-sided",
        The alternative hypothesis for the t test.
        "two-sided" the sample averages are different
        "less" the average of sample 1 is < the average of sample 2
        "greater" the average of sample 1 is > the average of sample 2
    significance_level : float = 0.05
        The significance level for rejecting the null hypothesis.
    width : int = 7
        The width for the formatted number.
    decimals : int = 3
        The number of decimal places for the formatted number.

    Returns
    -------
    t statistic : float
        The t statistic for the hypothesis.
    p value : float
        The p value for the t statistic.
    power : float
        The power of the t test.

    Examples
    --------
    Example 1
    Ha: the average of sample one is not equal to the average of sample two.
    alternative = "two-sided"
    >>> import datasense as ds
    >>> ds.two_sample_t(
    >>>     series1=series1,
    >>>     series2=series2,
    >>>     alternative_hypothesis="two-sided",
    >>>     significance_level=0.05
    >>> )

    Example 2
    Ha: the average of sample one is less than the average of sample two.
    alternative = "less than"
    >>> ds.two_sample_t(
    >>>     series1=series1,
    >>>     series2=series2,
    >>>     alternative_hypothesis="less",
    >>>     significance_level=0.05
    >>> )

    Example 3
    Ha: the average of sample one is greater than the average of sample three.
    alternative = "greater than"
    >>> ds.two_sample_t(
    >>>     series1=series1,
    >>>     series2=series2,
    >>>     alternative_hypothesis="greater",
    >>>     significance_level=0.05
    >>> )
    """
    # uncomment these lines when Anaconda releases Python 3.10
    # start uncomment
    # match alternative_hypothesis:
    #     case "two-sided":
    #         alternative = "two-sided"
    #         message_ho =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one != average of sample two\n"\
    #             "Fail to reject the null hypothesis Ho. "\
    #             "Continue to accept the null hypothesis Ho. "\
    #             "There is insufficient evidence to show that the sample "\
    #             "averages are different."
    #         message_ha =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one != average of sample two\n"\
    #             "Reject the null hypothesis Ho. "\
    #             "Accept the alternative hypothesis Ha. "\
    #             "There is sufficient evidence to show that the sample "\
    #             "averages are different."
    #     case "less than":
    #         alternative = "less"
    #         message_ho =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one < average of sample two\n"\
    #             "Fail to reject the null hypothesis Ho. "\
    #             "Continue to accept the null hypothesis Ho. "\
    #             "There is insufficient evidence to show that "\
    #             "the average of sample 1 is less than the "\
    #             "average of sample 2."
    #         message_ha =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one < average of sample two\n"\
    #             "Reject the null hypothesis Ho. "\
    #             "Accept the alternative hypothesis Ha. "\
    #             "There is sufficient evidence to show that "\
    #             "the average of sample 1 is less than the "\
    #             "average of sample 2."
    #     case "greater than":
    #         alternative = "greater"
    #         message_ho =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one > average of sample two\n"\
    #             "Fail to reject the null hypothesis Ho. "\
    #             "Continue to accept the null hypothesis Ho. "\
    #             "There is insufficient evidence to show that "\
    #             "the average of sample 1 is greater than the "\
    #             "average of sample 2."
    #         message_ha =\
    #             "Ho: average of sample one == average of sample two\n"\
    #             "Ha: average of sample one > average of sample two\n"\
    #             "Reject the null hypothesis Ho. "\
    #             "Accept the alternative hypothesis Ha. "\
    #             "There is sufficient evidence to show that "\
    #             "the average of sample 1 is greater than the "\
    #             "average of sample 2."
    # end uncomment
    # delete these lines when Anaconda releases Python 3.10
    # start delete
    print(
        "The two-sample t test is used to determine if the averages of two "
        "samples of data are statistically, significantly different from each "
        "other."
    )
    print()
    print("Assumptions")
    print("-----------")
    print()
    print("The data are continuous interval or ratio scales.")
    print()
    print(
        "The data in each sample follow a normal distribution with mean mu "
        "and variance sigma squared."
    )
    print()
    print(
        "The sample variances follow a chi-squared distribution "
        "with rho degrees of freedom under the null hypothesis, where rho "
        "is a positive constant."
    )
    print()
    print(
        "(sample average - population average) and the sample standard "
        "deviation are independent."
    )
    print()
    print("The size of each sample may be equal or unequal.")
    print()
    print("The variance of each sample may be equal or unequal.")
    print()
    print(
        "The data should be sampled independently from the two populations "
        "being compared."
    )
    print()
    print("Results")
    print("-------")
    print()
    if alternative_hypothesis == "two-sided":
        alternative_hypothesis_for_power = "two-sided"
        message_ho =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one != average of sample two\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that the sample "\
            "averages are different."
        message_ha =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one != average of sample two\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that the sample "\
            "averages are different."
    elif alternative_hypothesis == "less":
        alternative_hypothesis_for_power = "smaller"
        message_ho =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one < average of sample two\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that "\
            "the average of sample 1 is less than the "\
            "average of sample 2."
        message_ha =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one < average of sample two\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that "\
            "the average of sample 1 is less than the "\
            "average of sample 2."
    elif alternative_hypothesis == "greater":
        alternative_hypothesis_for_power = "larger"
        message_ho =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one > average of sample two\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that "\
            "the average of sample 1 is greater than the "\
            "average of sample 2."
        message_ha =\
            "Ho: average of sample one == average of sample two\n"\
            "Ha: average of sample one > average of sample two\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that "\
            "the average of sample 1 is greater than the "\
            "average of sample 2."
    # end delete
    print("Parametric analysis")
    print()
    levels = [1, 2]
    n_one = series1.count()
    n_two = series2.count()
    variance_sample_one = statistics.variance(data=series1)
    variance_sample_two = statistics.variance(data=series2)
    pooled_variance = (
        (n_one - 1) * variance_sample_one +
        (n_two - 1) * variance_sample_two
    ) / (n_one + n_two - 2)
    pooled_standard_deviation = math.sqrt(pooled_variance)
    effect_size = (
        math.fabs(series1.mean() - series2.mean()) /
        pooled_standard_deviation
    )
    delta_one_two = series1.mean() - series2.mean()
    t_critical_equal = stats.t.isf(
        q=significance_level / 2,
        df=n_one + n_two - 2
    )
    hypothesis_test_ci_lower_bound = (
        delta_one_two - t_critical_equal * pooled_standard_deviation *
        math.sqrt(1 / n_one + 1 / n_two)
    )
    hypothesis_test_ci_upper_bound = (
        delta_one_two + t_critical_equal * pooled_standard_deviation *
        math.sqrt(1 / n_one + 1 / n_two)
    )
    for level in levels:
        print(f"Sample {level}")
        print()
        if level == 1:
            series = series1
        else:
            series = series2
        parametric_statistics = parametric_summary(
            series=series,
            decimals=decimals
        ).to_string()
        print(parametric_statistics)
        print()
        print("Shapiro-Wilk results for normal distribution lack-of-fit test")
        shapiro_wilk_test_statistic, shapiro_wilk_p_value =\
            stats.shapiro(x=series)
        if level == 1:
            swstat1 = shapiro_wilk_test_statistic
            swpvalue1 = shapiro_wilk_p_value
        else:
            swstat2 = shapiro_wilk_test_statistic
            swpvalue2 = shapiro_wilk_p_value
        print(
            "Shapiro-Wilk test statistic: "
            f"{shapiro_wilk_test_statistic:{width}.{decimals}f}"
        )
        print(
            "Shapiro-Wilk p value       : "
            f"{shapiro_wilk_p_value:{width}.{decimals}f}"
        )
        if shapiro_wilk_p_value < significance_level:
            print(
                f"The data in sample {level} probably do not follow a normal "
                "distribution. It is not advised to continue with the "
                "homogeneity of variance test."
            )
        else:
            print(
                f"The data in sample {level} probably follow a normal "
                "distribution. OK to proceed to homogeneity of variance test."
            )
        print()
    bartlett_test_statistic, bartlett_p_value = stats.bartlett(
        series1,
        series2
    )
    print("Bartlett results for homogeneity of variance test")
    print(
        "Bartlett test statistic: "
        f"{bartlett_test_statistic:{width}.{decimals}f}"
    )
    print(f"Bartlett p value       : {bartlett_p_value:{width}.{decimals}f}")
    if bartlett_p_value < significance_level:
        print("The two samples probably do not have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=series1,
            b=series2,
            equal_var=False,
            alternative=alternative_hypothesis
        )
        power = TTestIndPower().power(
            effect_size=effect_size,
            nobs1=n_one,
            alpha=significance_level,
            ratio=(n_two / n_one),
            alternative=alternative_hypothesis_for_power
        )
        print("t test results")
        print(f"average of sample 1: {series1.mean():{width}.{decimals}f}")
        print(f"average of sample 2: {series2.mean():{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound}"
        )
        print(f"t test statistic   : {t_test_statistic:{width}.{decimals}f}")
        print(f"t test p value     : {t_test_p_value:{width}.{decimals}f}")
        print(f"significance level : {significance_level:{width}.{decimals}f}")
        print(f"power of the test  : {power:{width}.{decimals}f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    else:
        print("The two samples probably have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=series1,
            b=series2,
            equal_var=True,
            alternative=alternative_hypothesis
        )
        power = TTestIndPower().power(
            effect_size=effect_size,
            nobs1=n_one,
            alpha=significance_level,
            ratio=(n_two / n_one),
            alternative=alternative_hypothesis_for_power
        )
        print("t test results")
        print(f"average of sample 1: {series1.mean():{width}.{decimals}f}")
        print(f"average of sample 2: {series2.mean():{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound}"
        )
        print(f"t test statistic   : {t_test_statistic:{width}.{decimals}f}")
        print(f"t test p value     : {t_test_p_value:{width}.{decimals}f}")
        print(f"significance level : {significance_level:{width}.{decimals}f}")
        print(f"power of the test  : {power:{width}.{decimals}f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    print()
    print("Non-parametric analysis")
    print()
    for level in levels:
        print(f"Sample {level}")
        print()
        if level == 1:
            series = series1
        else:
            series = series2
        nonparametric_statistics = nonparametric_summary(
            series=series,
            decimals=decimals
        ).to_string()
        print(nonparametric_statistics)
        print()
        ad_test_statistic, ad_critical_values, ad_significance_level =\
            stats.anderson(x=series, dist="norm")
        if level == 1:
            ad_test_statistic_1 = ad_test_statistic
            ad_critical_value_1 = ad_critical_values[2]
        else:
            ad_test_statistic_2 = ad_test_statistic
            ad_critical_value_2 = ad_critical_values[2]
        # uncomment these lines when Anaconda release Python 3.10
        # start uncomment
        # match significance_level:
        #     case 0.25:
        #         item = 0
        #     case 0.10:
        #         item = 1
        #     case 0.05:
        #         item = 2
        #     case 0.025:
        #         item = 3
        #     case 0.01:
        #         item = 4
        #     case 0.005:
        #         item = 5
        # end uncomment
        # start delele
        if significance_level == 0.25:
            item = 0
        elif significance_level == 0.10:
            item = 1
        elif significance_level == 0.05:
            item = 2
        elif significance_level == 0.025:
            item = 3
        elif significance_level == 0.01:
            item = 4
        elif significance_level == 0.005:
            item = 5
        # end delete
        print(
            "Anderson-Darling results for normal distribution lack-of-fit test"
        )
        print(
            "Anderson-Darling test statistic: "
            f"{ad_test_statistic:{width}.{decimals}f}"
        )
        print(
            "Anderson-Darling critical value: "
            f"{ad_critical_values[item]:{width}.{decimals}f}"
        )
        if ad_test_statistic > ad_critical_values[item]:
            print(
                f"The data in sample {level} probably do not follow a normal "
                "distribution. It is not advised to continue with the "
                "two-sample t test."
            )
        else:
            print(
                f"The data in sample {level} probably follow a normal "
                "distribution. OK to proceed to test for equal variances."
            )
        print()
    # calculate Levene
    levene_test_statistic, levene_p_value = stats.levene(
        series1,
        series2
    )
    print("Levene results for homogeneity of variance")
    print(
        f"Levene test statistic: {levene_test_statistic:{width}.{decimals}f}"
    )
    print(f"Levene p value: {levene_p_value:{width}.{decimals}f}")
    if levene_p_value < significance_level:
        print("The two samples probably do not have equal variances.")
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=series1,
            b=series2,
            equal_var=False,
            alternative=alternative_hypothesis
        )
        power = TTestIndPower().power(
            effect_size=effect_size,
            nobs1=n_one,
            alpha=significance_level,
            ratio=(n_two / n_one),
            alternative=alternative_hypothesis_for_power
        )
        print("t test results")
        print(f"average of sample 1: {series1.mean():{width}.{decimals}f}")
        print(f"average of sample 2: {series2.mean():{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound}"
        )
        print(f"t test statistic   : {t_test_statistic:{width}.{decimals}f}")
        print(f"t test p value     : {t_test_p_value:{width}.{decimals}f}")
        print(f"significance level : {significance_level:{width}.{decimals}f}")
        print(f"power of the test  : {power:{width}.{decimals}f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    else:
        print("The two samples probably have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=series1,
            b=series2,
            equal_var=True,
            alternative=alternative_hypothesis
        )
        power = TTestIndPower().power(
            effect_size=effect_size,
            nobs1=n_one,
            alpha=significance_level,
            ratio=(n_two / n_one),
            alternative=alternative_hypothesis_for_power
        )
        print("t test results")
        print(f"average of sample 1: {series1.mean():{width}.{decimals}f}")
        print(f"average of sample 2: {series2.mean():{width}.{decimals}f}")
        print(
            "confidence interval "
            f"{hypothesis_test_ci_lower_bound:{width}.{decimals}f}, "
            f"{hypothesis_test_ci_upper_bound}"
        )
        print(f"t test statistic  : {t_test_statistic:{width}.{decimals}f}")
        print(f"t test p value    : {t_test_p_value:{width}.{decimals}f}")
        print(f"significance level: {significance_level:{width}.{decimals}f}")
        print(f"power of the test : {power:{width}.{decimals}f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    print()
    return (
        t_test_statistic, t_test_p_value, power,
        swstat1, swpvalue1, swstat2, swpvalue2,
        bartlett_test_statistic, bartlett_p_value,
        ad_test_statistic_1, ad_critical_value_1,
        ad_test_statistic_2, ad_critical_value_2,
        hypothesis_test_ci_lower_bound, hypothesis_test_ci_upper_bound
    )


def paired_t(
    *,
    series1: pd.Series,
    series2: pd.Series,
    hypothesized_value: Union[int, float, bool] = None,
    alternative_hypothesis: str = "two-sided",
    significance_level: float = 0.05,
    width: int = 7,
    decimals: int = 3
) -> Tuple[float, float]:
    """
    Two-sample t test.

    - Parametric statistics are calculated for each sample.
    - Non-parametric statistics are calculated for each sample.
    - The assumption for normality of each sample is evaluted.
        - Shapiro-Wilk, a parametric test
        - Anderson-Darling, a non-parametric test
    - The homogeneity of variance of the samples is evaluated.
        - Bartlett, a parametric test
        - Levene, a non-parametric test

    Parameters
    ----------
    series1 : pd.Series
        The first series of data, with a name.
    series2 : pd.Series
        The second series of data, with a name.
    hypothesized_value : Union[int, float, bool] = None
        The hypothesized value for the test.
    alternative_hypothesis : str = "two-sided",
        The alternative hypothesis for the paired t test.
        "two-sided" the average of the differences are not zero or some
        hypothesized value
        "less" the average of the differences are less than zero or some
        hypothesized value
        "greater" the average of the differences are greater than zero or some
        hypothesized value
    significance_level : float = 0.05
        The significance level for rejecting the null hypothesis.
    width : int = 7
        The width for the formatted number.
    decimals : int = 3
        The number of decimal places for the formatted number.

    Returns
    -------
    t_test_statistic : float
        The calculated t statistic for the hypothesis.
    t_test_p_value : float
        The calculated p value for the calculated t statistic.
    shapiro_wilk_test_statistic : float
        The Shapiro-Wilk calculated t statistic.
    shapiro_wilk_p_value : float
        The Shapiro-Wilk calculated p value for the calculated t statistic.
    ad_test_statistic : float
        The Anderson-Darling calculated t statistic.
    ad_critical_values[2] : float
        The Anderson-Darling calculated p value for the calculated t statistic
        at alpha = 0.05.
    kolmogorov_smirnov_test_statistic : float
        The Kolmogorov-Smirnov calculated t statistic.
    kolmogorov_smirnov_test_pvalue : float
        The Komogorov-Smirnov calculated p value for the calculated
        t statistic.

    """
    print(
        "The paired-sample t test is used to determine whether the average "
        "of the differences between two paired samples differs from zero or "
        "some hypothesized value."
    )
    print()
    print("Assumptions")
    print("-----------")
    print()
    print("The data are continuous interval or ratio scales.")
    print()
    print(
        "The data in each sample follow a normal distribution with mean mu "
        "and variance sigma squared."
    )
    print()
    print(
        "The sample variances follow a chi-squared distribution "
        "with rho degrees of freedom under the null hypothesis, where rho "
        "is a positive constant."
    )
    print()
    print(
        "(sample average - population average) and the sample standard "
        "deviation are independent."
    )
    print()
    print("The size of each sample may be equal or unequal.")
    print()
    print("The variance of each sample may be equal or unequal.")
    print()
    print(
        "The data should be sampled independently from the two populations "
        "being compared."
    )
    print()
    print("Results")
    print("-------")
    print()
    # series_differences = series2 - series1
    if hypothesized_value is None:
        hypothesized_value = 0
    series_differences = series1 - series2
    series_differences_average = series_differences.mean()
    degrees_of_freedom = len(series_differences) - 1
    series_differences_standard_deviation = series_differences.std()
    t_test_statistic = (
        (series_differences_average - hypothesized_value) *
        math.sqrt(len(series_differences)) /
        series_differences_standard_deviation
    )
    t_critical_two_tail = stats.t.isf(
        q=significance_level / 2,
        df=degrees_of_freedom
    )
    t_critical_one_tail = stats.t.isf(
        q=significance_level,
        df=degrees_of_freedom
    )
    print()
    if alternative_hypothesis == "two-sided":
        alternative_hypothesis_for_power = "two-sided"
        message_ho =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences != "\
            f"{hypothesized_value}\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that the population "\
            "average of the differences != "\
            f"{hypothesized_value}."
        message_ha =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences != "\
            f"{hypothesized_value}\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that the population "\
            "average of the differences != "\
            f"{hypothesized_value}."
        t_test_p_value = stats.t.sf(
            x=math.fabs(t_test_statistic),
            df=degrees_of_freedom
        ) * 2
    elif alternative_hypothesis == "less":
        alternative_hypothesis_for_power = "smaller"
        message_ho =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences < "\
            f"{hypothesized_value}\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that the population "\
            "average of the differences < "\
            f"{hypothesized_value}."
        message_ha =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences < "\
            f"{hypothesized_value}\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that the population "\
            "average of the differences < "\
            f"{hypothesized_value}."
        t_test_p_value = 1 - stats.t.sf(
            x=(t_test_statistic),
            df=degrees_of_freedom
        )
    elif alternative_hypothesis == "greater":
        alternative_hypothesis_for_power = "larger"
        message_ho =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences > "\
            f"{hypothesized_value}\n"\
            "Fail to reject the null hypothesis Ho. "\
            "Continue to accept the null hypothesis Ho. "\
            "There is insufficient evidence to show that the population "\
            "average of the differences > "\
            f"{hypothesized_value}."
        message_ha =\
            "Ho: The population average of the differences = "\
            f"{hypothesized_value}\n"\
            "Ha: The population average of the differences > "\
            f"{hypothesized_value}\n"\
            "Reject the null hypothesis Ho. "\
            "Accept the alternative hypothesis Ha. "\
            "There is sufficient evidence to show that the population "\
            "average of the differences > "\
            f"{hypothesized_value}."
        t_test_p_value = stats.t.sf(
            x=(t_test_statistic),
            df=degrees_of_freedom
        )
    print("Parametric analysis")
    print()
    levels = [1, 2]
    for level in levels:
        if level == 1:
            series = series1
        else:
            series = series2
        parametric_statistics = parametric_summary(
            series=series,
            decimals=decimals
        ).to_string()
        print(f"Parametric statistics for y level {level}")
        print(parametric_statistics)
        print()
    print("Shapiro-Wilk results for normal distribution lack-of-fit test")
    shapiro_wilk_test_statistic, shapiro_wilk_p_value =\
        stats.shapiro(x=series_differences)
    print(
        "Shapiro-Wilk test statistic: "
        f"{shapiro_wilk_test_statistic:{width}.{decimals}f}"
    )
    print(
        "Shapiro-Wilk p value       : "
        f"{shapiro_wilk_p_value:{width}.{decimals}f}"
    )
    if shapiro_wilk_p_value < significance_level:
        print(
            "The differences between the pairs of data probably do not follow "
            "a normal distribution."
        )
    else:
        print(
            "The differences between the pairs of data probably follow "
            "a normal distribution."
        )
    print()
    print("Non-parametric analysis")
    print()
    for level in levels:
        if level == 1:
            series = series1
        else:
            series = series2
        nonparametric_statistics = nonparametric_summary(
            series=series,
            alphap=1/3,
            betap=1/3,
            decimals=decimals
        ).to_string()
        print(f"Non-parametric statistics for y level {level}")
        print(nonparametric_statistics)
        print()
    ad_test_statistic, ad_critical_values, ad_significance_level =\
        stats.anderson(x=series_differences, dist="norm")
    # uncomment these lines when Anaconda release Python 3.10
    # start uncomment
    # match significance_level:
    #     case 0.25:
    #         item = 0
    #     case 0.10:
    #         item = 1
    #     case 0.05:
    #         item = 2
    #     case 0.025:
    #         item = 3
    #     case 0.01:
    #         item = 4
    #     case 0.005:
    #         item = 5
    # end uncomment
    # start delele
    if significance_level == 0.25:
        item = 0
    elif significance_level == 0.10:
        item = 1
    elif significance_level == 0.05:
        item = 2
    elif significance_level == 0.025:
        item = 3
    elif significance_level == 0.01:
        item = 4
    elif significance_level == 0.005:
        item = 5
    # end delete
    print(
        "Anderson-Darling results for normal distribution lack-of-fit test"
    )
    print(
        "Anderson-Darling test statistic: "
        f"{ad_test_statistic:{width}.{decimals}f}"
    )
    print(
        "Anderson-Darling critical value: "
        f"{ad_critical_values[item]:{width}.{decimals}f}"
    )
    if ad_test_statistic > ad_critical_values[item]:
        print(
            "The differences between the pairs of data probably do not follow "
            "a normal distribution."
        )
    else:
        print(
            "The differences between the pairs of data probably follow "
            "a normal distribution."
        )
    print()
    kolmogorov_smirnov_test_statistic, kolmogorov_smirnov_test_pvalue = \
        ksstat, kspvalue = smd.kstest_normal(
            x=series_differences,
            dist="norm",
            pvalmethod="approx"
        )
    print(
        "Kolmogorov-Smirnov results for normal distribution lack-of-fit test"
    )
    print(
        "Kolmogorov-Smirnov test statistic: "
        f"{kolmogorov_smirnov_test_statistic:{width}.{decimals}f}")
    print(
        "Kolmogorov-Smirnov p value       : "
        f"{kolmogorov_smirnov_test_pvalue:{width}.{decimals}f}"
    )
    if kolmogorov_smirnov_test_pvalue < significance_level:
        print(
            "The differences between the pairs of data probably do not follow "
            "a normal distribution."
        )
    else:
        print(
            "The differences between the pairs of data probably follow "
            "a normal distribution."
        )
    print()
    print("t test results")
    print(
        "average of sample 1                  : "
        f"{series1.mean():{width}.{decimals}f}"
    )
    print(
        "average of sample 2                  : "
        f"{series2.mean():{width}.{decimals}f}"
    )
    print(
        "average of the differences           : "
        f"{series_differences_average:{width}.{decimals}f}"
    )
    print(
        "hypothesized difference              : "
        f"{hypothesized_value:{width}.{decimals}f}"
    )
    print(
        "standard deviation of the differences: "
        f"{series_differences_standard_deviation:{width}.{decimals}f}"
    )
    print(
        "t test statistic                     : "
        f"{t_test_statistic:{width}.{decimals}f}"
    )
    if alternative_hypothesis == "two-sided":
        print(
            "t test critical two-tailed           : "
            f"{t_critical_two_tail       :{width}.{decimals}f}"
        )
    else:
        print(
            "t test critical one-tailed           : "
            f"{t_critical_one_tail       :{width}.{decimals}f}"
        )
    print(
        "t test p value                       : "
        f"{t_test_p_value:{width}.{decimals}f}"
    )
    if t_test_p_value < significance_level:
        print(message_ha)
    else:
        print(message_ho)

    return (
        t_test_statistic, t_test_p_value,
        shapiro_wilk_test_statistic, shapiro_wilk_p_value,
        ad_test_statistic, ad_critical_values[2],
        kolmogorov_smirnov_test_statistic, kolmogorov_smirnov_test_pvalue
    )


def linear_regression(
    *,
    df: pd.DataFrame,
    x_column: List[str],
    y_column: str,
    prediction_column: str
) -> pd.DataFrame:
    """
    Linear regression with one or more X series and one Y series. The variables
    are integers or floats.

    Parameters
    ----------
    df : pd.DataFrame,
        The DataFrame of data.
    x_column : List[str],
        The list of column names for the X series.
    y_column : str,
        The column name for the Y series.
    prediction_column : str
        The column name for the prediction series. This must match what is
        created by the fit() command in statsmodels.

    Returns
    -------
    df_predictions
        The DataFrame with the results and the X, Y series from the submitted
        DataFrame.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> x_column = "x"
    >>> y_column = "y"
    >>> prediction_column = "mean"
    >>> df_predictions = ds.linear_regression(
    >>>     df=df,
    >>>     x_column=[x_column],
    >>>     y_column=y_column,
    >>>     prediction_column=prediction_column
    >>> )

    Example 2
    >>> x_column = ["interest_rate", "unemployment_rate"]
    >>> y_column = "index_price"
    >>> prediction_column = "mean"
    >>> df_predictions = ds.linear_regression(
    >>>     df=df,
    >>>     x_column=x_column,
    >>>     y_column=y_column,
    >>>     prediction_column=prediction_column
    >>> )
    """
    x = sm.add_constant(data=df[x_column])
    y = df[y_column]
    fitted_model = sm.OLS(
        endog=y,
        exog=x,
        missing="drop"
    ).fit(
        method="pinv",
        cov_type="nonrobust"
    )
    print(fitted_model.summary())
    df_predictions = (
        fitted_model.get_prediction().summary_frame(alpha=0.05).sort_values(
            by=prediction_column
        )
    )
    columns = x_column + [y_column]
    df_predictions = df_predictions.join(other=df[columns])
    return df_predictions, fitted_model


__all__ = (
    "nonparametric_summary",
    "natural_cubic_spline",
    "parametric_summary",
    "linear_regression",
    "timedelta_data",
    "datetime_data",
    "cubic_spline",
    "two_sample_t",
    "one_sample_t",
    "random_data",
    "paired_t",
)
