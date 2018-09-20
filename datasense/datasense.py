import pandas as pd

def five_number_summary(data: pd.Series) -> pd.DataFrame:
    """
    Return five statistics

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    """
    return pd.DataFrame(
        [(interpolation,
          data.min(),
          data.quantile(0.25, interpolation=interpolation),
          data.quantile(0.50, interpolation=interpolation),
          data.quantile(0.75, interpolation=interpolation),
          data.max())
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest',
             'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2',
                 'q3', 'max']
    ).set_index(['interpolation'])


def six_number_summary(data: pd.Series) -> pd.DataFrame:
    """
    Return six statistics

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    iqr            = interquartile range
    """
    # Pourqoi pas juste:
    #     five = five_number_summary(data)
    #     five['iqr'] = five['q3'] - five['q1']
    #     return five
    return pd.DataFrame(
        [(interpolation,
          data.min(),
          data.quantile(0.25, interpolation=interpolation),
          data.quantile(0.50, interpolation=interpolation),
          data.quantile(0.75, interpolation=interpolation),
          data.max(),
          (data.quantile(0.75, interpolation=interpolation) -
           data.quantile(0.25, interpolation=interpolation)))
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2', 'q3', 'max', 'iqr']
    ).set_index(['interpolation'])


def seven_number_summary(data: pd.Series) -> pd.DataFrame:
    """
    Return six statistics

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    iqr            = interquartile range
    n              = sample size
    """
    # Pourqoi pas juste:
    #     five = five_number_summary(data)
    #     five['iqr'] = five['q3'] - five['q1']
    #     return five
    return pd.DataFrame(
        [(interpolation,
          data.min(),
          data.quantile(0.25, interpolation=interpolation),
          data.quantile(0.50, interpolation=interpolation),
          data.quantile(0.75, interpolation=interpolation),
          data.max(),
          (data.quantile(0.75, interpolation=interpolation) -
           data.quantile(0.25, interpolation=interpolation)),
          data.count())
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2', 'q3', 'max', 'iqr', 'n']
    ).set_index(['interpolation'])

