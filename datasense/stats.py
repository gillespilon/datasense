import pandas as pd


def nonparametric_summary(series: pd.Series) -> pd.DataFrame:
    '''
    Return nonparametric statistics

    Returns
    -------
    n              = sample size
    min            = minimum value
    max            = maximum value
    quantile(0.50) = median
    confidence interval of the median
    iqr            = interquartile range
    confidence interval of the interquartile range
    # Pourqoi pas juste:
    #     five = five_number_summary(series)
    #     five['iqr'] = five['q3'] - five['q1']
    #     return five
    '''
    return pd.DataFrame(
        [(interpolation,
          series.count(),
          series.min(),
          series.quantile(0.25, interpolation=interpolation),
          series.quantile(0.50, interpolation=interpolation),
          series.quantile(0.75, interpolation=interpolation),
          (series.quantile(0.75, interpolation=interpolation) -
           series.quantile(0.25, interpolation=interpolation)),
          series.max())
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'n', 'min', 'q1', 'q2', 'q3', 'iqr', 'max']
    ).set_index(['interpolation'])


def parametric_summary(series: pd.Series) -> pd.DataFrame:
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
    return pd.DataFrame(
        [(series.count(),
          series.min(),
          series.max(),
          series.mean(),
          series.std(),
          series.var())],
        columns=['n', 'min', 'max', 'ave', 's', 'var'])


__all__ = (
    'nonparametric_summary',
    'parametric_summary',
)
