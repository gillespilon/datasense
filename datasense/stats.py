import pandas as pd
import numpy as np
from scipy.stats.mstats import mquantiles as mq


def nonparametric_summary(series: pd.Series,
                          alphap=1/3,
                          betap=1/3) -> pd.DataFrame:
    # TODO: implement at least 8 methods of nonparametrics
    '''
    Calculate empirical quantiles for a series.

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

    R method 6, Minitab:
    alphap=0, betap=0

    R method 7:
    alphap=1, betap=1

    R method 8 uses:
    alphap=0.33, betap=0.33; is the recommended method
    '''
    xm = np.ma.masked_array(series, mask=np.isnan(series))
    q25 = mq(xm, prob=(0.25), alphap=0.33, betap=0.33)
    q50 = mq(xm, prob=(0.50), alphap=0.33, betap=0.33)
    q75 = mq(xm, prob=(0.75), alphap=0.33, betap=0.33)
    iqr = q75 - q25
    lof = (q25 - iqr * 3).clip(min=0)
    lif = (q25 - iqr * 1.5).clip(min=0)
    uif = (q75 + iqr * 1.5).clip(min=0)
    uof = (q75 + iqr * 3).clip(min=0)
    inner_outliers = [x for x in series.round(1) if x < lif or x > uif]
    outliers_outer = [x for x in series.round(1) if x < lof or x > uof]
    minval = series.min()
    maxval = series.max()
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
