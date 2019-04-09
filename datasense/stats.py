import pandas as pd
import numpy as np
from scipy.stats.mstats import mquantiles as mq


def nonparametric_summary(series: pd.Series) -> pd.DataFrame:
    # TODO: add alphap, betap as parameters in the parameter list
    # TODO: implement at least 8 methods of nonparametrics
    '''
    Calculate empirical quantiles for a series.

    R method 8 uses:
    alphap=0.33, betap=0.33 and is the recommended method

    Minitab uses R method 6:
    alphap=0, betap=0
    '''
    xm = np.ma.masked_array(series, mask=np.isnan(series))
    minval = series.min()
    maxval = series.max()
    q50 = mq(xm, prob=(0.50), alphap=0.33, betap=0.33)
    q75 = mq(xm, prob=(0.75), alphap=0.33, betap=0.33)
    q25 = mq(xm, prob=(0.25), alphap=0.33, betap=0.33)
    iqr = q75 - q25
    # Calculate the inner fences.
    uif = (q75 + iqr * 1.5).clip(min=0)
    lif = (q25 - iqr * 1.5).clip(min=0)
    # Calculate the outer fences.
    uof = (q75 + iqr * 3).clip(min=0)
    lof = (q25 - iqr * 3).clip(min=0)
    # Identify outliers outside inner fences.
    inner_outliers = [x for x in series.round(1) if x < lif or x > uif]
    # Identify outliers outside outer fences.
    outliers_outer = [x for x in series.round(1) if x < lof or x > uof]
    return pd.Series({
        'lower outer fence': lof[0].round(1),
        'lower inner fence': lif[0].round(1),
        'lower quartile': q25[0].round(1),
        'median': q50[0].round(1),
        'upper quartile': q75[0].round(1),
        'upper inner fence': uif[0].round(1),
        'upper outer fence': uof[0].round(1),
        'interquartile range': iqr[0].round(1),
        'inner outliers': inner_outliers,
        'outer outliers': outliers_outer,
        'minimum value': minval,
        'maximum value': maxval
    })


def parametric_summary(series: pd.Series) -> pd.Series:
    '''
    Return parametric statistics

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


__all__ = (
    'nonparametric_summary',
    'parametric_summary',
)
