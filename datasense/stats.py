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
from typing import List, Tuple
import random
import sys

from sklearn.linear_model import LinearRegression
from basis_expansions import NaturalCubicSpline
from scipy.stats.mstats import mquantiles as mq
from scipy.stats import norm, uniform, randint
from pandas.api.types import CategoricalDtype
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
    cil = (q50 - 1.57 * iqr / np.sqrt(series.count()))[0]
    ciu = (q50 + 1.57 * iqr / np.sqrt(series.count()))[0]
    return pd.Series({
        "lower outer fence": round(lof[0], decimals),
        "lower inner fence": round(lif[0], decimals),
        "lower quartile": round(q25[0], decimals),
        "median": round(q50[0], decimals),
        "confidence interval": (cil, ciu),
        "upper quartile": round(q75[0], decimals),
        "upper inner fence": round(uif[0], decimals),
        "upper outer fence": round(uof[0], decimals),
        "interquartile range": round(iqr[0], decimals),
        "inner outliers":
            [round(x, decimals) for x in series if x < lif or x > uif],
        "outer outliers":
            [round(x, decimals) for x in series if x < lof or x > uof],
        "minimum value": round(series.min(), 3),
        "maximum value": round(series.max(), 3),
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
    return pd.Series({
        "n": series.count(),
        "min": round(series.min(), decimals),
        "max": round(series.max(), decimals),
        "ave": round(series.mean(), decimals),
        "confidence interval": (ciaverage[0], ciaverage[1]),
        "s": round(series.std(), decimals),
        "var": round(series.var(), decimals),
    })


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
    >>> number_days_plus_one = 42
    >>> series = timedelta_data(time_delta_days=number_days_plus_one)
    """
    series = datetime_data(time_delta_days=time_delta_days) -\
        datetime_data(time_delta_days=time_delta_days)
    return series


def two_sample_t(
    *,
    df: pd.DataFrame,
    xlabel: str,
    ylabel: str,
    alternative_hypothesis: str = "unequal",
    significance_level: float = 0.05
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
    df : pd.DataFrame,
        The DataFrame of data, consisting of two columns, each with a column
        label in row 0. One column contains the labels for the sample. The
        other column contains the data for the sample.
    xlabel : str,
        The column label for the sample identities.
    ylabel : str,
        The column label for the data.
    alternative_hypothesis : str = "unequal",
        The alternative hypothesis for the t test.
        "unequal" the sample averages are different
        "less than" the average of sample 1 is < the average of sample 2
        "greater than" the average of sample 1 is > the average of sample 2
    significance_level : float = 0.05
        The signficance level for rejecting the null hypothesis.

    Returns
    -------
    t statistic : float
        The t statistic for the hypothesis.
    p value : float
        The p value for the t statistic.

    Examples
    --------
    Example 1
    Ha: the average of sample one is not equal to the average of sample two.
    alternative = "unequal"
    >>> ds.two_sample_t(
    >>>     df=df, xlabel="x", ylabel="y", alternative_hypothesis="unequal",
    >>>     significance_level=0.05
    >>> )

    Example 2
    Ha: the average of sample one is less than the average of sample two.
    alternative = "less than"
    >>> ds.two_sample_t(
    >>>     df=df, xlabel="x", ylabel="y",
    >>>     alternative_hypothesis="less than",
    >>>     significance_level=0.05
    >>> )

    Example 3
    Ha: the average of sample one is greater than the average of sample three.
    alternative = "greater than"
    >>> ds.two_sample_t(
    >>>     df=df, xlabel="x", ylabel="y", alternative_hypothesis="less than",
    >>>     significance_level=0.05
    >>> )
    """
    # uncomment these lines when Anaconda releases Python 3.10
    # start uncomment
    # match alternative_hypothesis:
    #     case "unequal":
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
    if alternative_hypothesis == "unequal":
        alternative = "two-sided"
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
    elif alternative_hypothesis == "less than":
        alternative = "less"
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
    elif alternative_hypothesis == "greater than":
        alternative = "greater"
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
    print("Parametric analysis")
    print()
    levels = df[xlabel].sort_values().unique()
    if len(levels) != 2:
        print(f"Levels must equal 2. Levels in DataFrame equal {levels}")
    for level in np.nditer(op=levels):
        print(f"Sample {level}")
        print()
        series = df[ylabel][df[xlabel] == level]
        parametric_statistics = parametric_summary(series=series)
        print(parametric_statistics.to_string())
        print()
        print("Shapiro-Wilk results for normal distribution lack-of-fit test")
        shapiro_wilk_test_statistic, shapiro_wilk_p_value =\
            stats.shapiro(x=series)
        print(
            f"Shapiro-Wilk test statistic: {shapiro_wilk_test_statistic:7.3f}"
        )
        print(f"Shapiro-Wilk p value       : {shapiro_wilk_p_value:7.3f}")
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
        df[ylabel][df[xlabel] == levels[0]],
        df[ylabel][df[xlabel] == levels[1]]
    )
    print("Bartlett results for homogeneity of variance test")
    print(f"Bartlett test statistic: {bartlett_test_statistic:7.3f}")
    print(f"Bartlett p value       : {bartlett_p_value:7.3f}")
    if bartlett_p_value < significance_level:
        print("The two samples probably do not have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=df[ylabel][df[xlabel] == levels[0]],
            b=df[ylabel][df[xlabel] == levels[1]],
            equal_var=False,
            alternative=alternative
        )
        print("t test results")
        print(f"t test statistic  : {t_test_statistic:7.3f}")
        print(f"t test p value    : {t_test_p_value:7.3f}")
        print(f"significance level: {significance_level:7.3f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    else:
        print("The two samples probably have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=df[ylabel][df[xlabel] == levels[0]],
            b=df[ylabel][df[xlabel] == levels[1]],
            equal_var=True,
            alternative=alternative
        )
        print("t test results")
        print(f"t test statistic  : {t_test_statistic:7.3f}")
        print(f"t test p value    : {t_test_p_value:7.3f}")
        print(f"significance level: {significance_level:7.3f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    print()
    print("Non-parametric analysis")
    print()
    for level in np.nditer(op=levels):
        print(f"Sample {level}")
        print()
        series = df[ylabel][df[xlabel] == level]
        nonparametric_statistics = nonparametric_summary(series=series)
        print(nonparametric_statistics.to_string())
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
        print(f"Anderson-Darling test statistic: {ad_test_statistic:7.3f}")
        print(
            f"Anderson-Darling critical value: {ad_critical_values[item]:7.3f}"
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
        df[ylabel][df[xlabel] == levels[0]],
        df[ylabel][df[xlabel] == levels[1]]
    )
    print("Levene results for homogeneity of variance")
    print(f"Levene test statistic: {levene_test_statistic:7.3f}")
    print(f"Levene p value: {levene_p_value:7.3f}")
    if levene_p_value < significance_level:
        print("The two samples probably do not have equal variances.")
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=df[ylabel][df[xlabel] == levels[0]],
            b=df[ylabel][df[xlabel] == levels[1]],
            equal_var=False,
            alternative=alternative
        )
        print("t test results")
        print(f"t test statistic  : {t_test_statistic:7.3f}")
        print(f"t test p value    : {t_test_p_value:7.3f}")
        print(f"significance level: {significance_level:7.3f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    else:
        print("The two samples probably have equal variances.")
        print()
        t_test_statistic, t_test_p_value = stats.ttest_ind(
            a=df[ylabel][df[xlabel] == levels[0]],
            b=df[ylabel][df[xlabel] == levels[1]],
            equal_var=True,
            alternative=alternative
        )
        print("t test results")
        print(f"t test statistic  : {t_test_statistic:7.3f}")
        print(f"t test p value    : {t_test_p_value:7.3f}")
        print(f"significance level: {significance_level:7.3f}")
        if t_test_p_value < significance_level:
            print(message_ha)
        else:
            print(message_ho)
    print()


def linear_regression(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    prediction_column: str
) -> pd.DataFrame:
    x = sm.add_constant(data=df[x_column])
    y = df[y_column]
    results = sm.OLS(
        endog=y,
        exog=x,
        missing="drop"
    ).fit(
        method="pinv",
        cov_type="nonrobust"
    )
    print(results.summary())
    df_predictions = (
        results.get_prediction().summary_frame(alpha=0.05).sort_values(
            by=prediction_column
        )
    )
    df_predictions = df_predictions.join(other=df[[x_column, y_column]])
    return df_predictions


__all__ = (
    "nonparametric_summary",
    "natural_cubic_spline",
    "parametric_summary",
    "linear_regression",
    "timedelta_data",
    "datetime_data",
    "cubic_spline",
    "two_sample_t",
    "random_data",
)
