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

def five_number_summary(data: pd.Series) -> pd.DataFrame:
   return pd.DataFrame([(interpolation,
        data.min(),
        data.quantile(0.25, interpolation=interpolation),
        data.quantile(0.50, interpolation=interpolation),
        data.quantile(0.75, interpolation=interpolation),
        data.max())
        for interpolation
            in ('linear', 'lower', 'higher', 'nearest',
                'midpoint')],
            columns=['interpolation', 'min', 'q1', 'q2',
                     'q3', 'max']).\
            set_index(['interpolation'])

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

def six_number_summary(data: pd.Series) -> pd.DataFrame:
   return pd.DataFrame([(interpolation,
        data.min(),
        data.quantile(0.25, interpolation=interpolation),
        data.quantile(0.50, interpolation=interpolation),
        data.quantile(0.75, interpolation=interpolation),
        data.max(),
        (data.quantile(0.75, interpolation=interpolation) -\
         data.quantile(0.25, interpolation=interpolation))
        )
        for interpolation
            in ('linear', 'lower', 'higher', 'nearest',
                'midpoint')],
            columns=['interpolation', 'min', 'q1', 'q2',
                     'q3', 'max', 'iqr']).\
            set_index(['interpolation'])
