'''
Statistical analysis
'''


import pandas as pd
import numpy as np
from scipy.stats.mstats import mquantiles as mq


def nonparametric_summary(series: pd.Series,
                          alphap=1/3,
                          betap=1/3) -> pd.DataFrame:
    # TODO: implement at least 8 methods of nonparametrics
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
    alphap=0.33, betap=0.33; is the recommended method

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
    # lof = (q25 - iqr * 3).clip(min=0)
    # lif = (q25 - iqr * 1.5).clip(min=0)
    # uif = (q75 + iqr * 1.5).clip(min=0)
    # uof = (q75 + iqr * 3).clip(min=0)
    lof = (q25 - iqr * 3)
    lif = (q25 - iqr * 1.5)
    uif = (q75 + iqr * 1.5)
    uof = (q75 + iqr * 3)
    # inner_outliers = [x for x in series.round(3) if x < lif or x > uif]
    # outliers_outer = [x for x in series.round(3) if x < lof or x > uof]
    inner_outliers = [x for x in series if x < lif or x > uif]
    outliers_outer = [x for x in series if x < lof or x > uof]
    minval = series.min()
    maxval = series.max()
    return pd.Series({
        # 'lower outer fence': lof[0].round(3),
        # 'lower inner fence': lif[0].round(3),
        # 'lower quartile': q25[0].round(3),
        # 'median': q50[0].round(3),
        # 'upper quartile': q75[0].round(3),
        # 'upper inner fence': uif[0].round(3),
        # 'upper outer fence': uof[0].round(3),
        # 'interquartile range': iqr[0].round(3),
        'lower outer fence': lof[0],
        'lower inner fence': lif[0],
        'lower quartile': q25[0],
        'median': q50[0],
        'upper quartile': q75[0],
        'upper inner fence': uif[0],
        'upper outer fence': uof[0],
        'interquartile range': iqr[0],
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
