'''
datasense

Statistical and graphical functions for:

- Data science
- Analysing process variation
- Six Sigma methodology

Why this?

- Wanted functions to support process control charts.
- Wanted functions to support measurement system analysis.
- Develop a package that is open-source for those unable to buy software.
- Wanted Python functions that are available in R and SAS.
- Other packages have limited features for process control analysis.
- Other packages are abandone or inadequately supported.
'''

# TODO: Measurement system analysis (MSA) using control charts.
# TODO: MSA range chart.
# TODO: MSA range chart.
# TODO: MSA average chart.
# TODO: MSA parallelism chart.
# TODO: MSA main effects chart (ANOME).
# TODO: MSA mean ranges chart (ANOMR).
# TODO: MSA test-retest error.
# TODO: MSA probable error.
# TODO: MSA intraclass correlation coefficient with operator bias.
# TODO: MSA intraclass correlation coefficient without operator bias.

from typing import NamedTuple, Union, Tuple
import math

import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import scipy.stats.mstats as ms


_QUANTILES = (0.25, 0.50, 0.75)
_QUANTILE_METHODS = [
    (0, 1), (0.5, 0.5), (0, 0), (1, 1), (0.33, 0.33), (0.375, 0.375)
]


def sommaire_cinq_numeros(series: pd.Series) -> pd.DataFrame:
    '''
    Return five statistics using mquantiles

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    '''
    return pd.DataFrame(
        [(alphap,
          betap,
          series.min(),
          *ms.mquantiles(series,
                         prob=_QUANTILES,
                         alphap=alphap,
                         betap=betap).round(3),
          series.max())
         for alphap, betap
         in _QUANTILE_METHODS],
        columns=['alphap', 'betap', 'min', 'q1', 'q2', 'q3', 'max']
    ).set_index(['alphap', 'betap'])


def five_number_summary(series: pd.Series) -> pd.DataFrame:
    '''
    Return five statistics

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    '''
    return pd.DataFrame(
        [(interpolation,
          series.min(),
          series.quantile(0.25, interpolation=interpolation),
          series.quantile(0.50, interpolation=interpolation),
          series.quantile(0.75, interpolation=interpolation),
          series.max())
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2', 'q3', 'max']
    ).set_index(['interpolation'])


def six_number_summary(series: pd.Series) -> pd.DataFrame:
    '''
    Return six statistics

    Returns
    -------
    min            = minimum value
    quantile(0.25) = first quartile
    quantile(0.50) = median
    quantile(0.75) = third quartile
    max            = maximum value
    iqr            = interquartile range
    '''
    # Pourqoi pas juste:
    #     five = five_number_summary(series)
    #     five['iqr'] = five['q3'] - five['q1']
    #     return five
    return pd.DataFrame(
        [(interpolation,
          series.min(),
          series.quantile(0.25, interpolation=interpolation),
          series.quantile(0.50, interpolation=interpolation),
          series.quantile(0.75, interpolation=interpolation),
          series.max(),
          (series.quantile(0.75, interpolation=interpolation) -
           series.quantile(0.25, interpolation=interpolation)))
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2', 'q3', 'max', 'iqr']
    ).set_index(['interpolation'])


def seven_number_summary(series: pd.Series) -> pd.DataFrame:
    '''
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
    '''
    # Pourqoi pas juste:
    #     five = five_number_summary(series)
    #     five['iqr'] = five['q3'] - five['q1']
    #     return five
    return pd.DataFrame(
        [(interpolation,
          series.min(),
          series.quantile(0.25, interpolation=interpolation),
          series.quantile(0.50, interpolation=interpolation),
          series.quantile(0.75, interpolation=interpolation),
          series.max(),
          (series.quantile(0.75, interpolation=interpolation) -
           series.quantile(0.25, interpolation=interpolation)),
          series.count())
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'min', 'q1', 'q2', 'q3', 'max', 'iqr', 'n']
    ).set_index(['interpolation'])


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
    '''
    return pd.DataFrame(
        [(interpolation,
          series.count(),
          series.min(),
          series.max(),
          series.quantile(0.50, interpolation=interpolation),
          (series.quantile(0.75, interpolation=interpolation) -
           series.quantile(0.25, interpolation=interpolation)))
         for interpolation
         in ('linear', 'lower', 'higher', 'nearest', 'midpoint')],
        columns=['interpolation', 'n', 'min', 'max', 'q2', 'iqr']
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


def control_chart_constants(n: int, col: str) -> float:
    '''
    This function creates a dataframe from a dictionary of constants and
    returns requested constants.
    '''
    d = dict(
        n=np.array([
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 100]),
        A2=np.array([
            1.881, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308,
            0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203, 0.194, 0.187,
            0.180, 0.173, 0.167, 0.162, 0.157, 0.153, 0.134, 0.120, 0.110,
            0.101, 0.094, 0.088, 0.083, 0.079, 0.075, 0.072, 0.069, 0.066,
            0.064, 0.060]),
        A3=np.array([
            2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975,
            0.927, 0.886, 0.850, 0.817, 0.789, 0.763, 0.739, 0.718, 0.698,
            0.680, 0.663, 0.647, 0.633, 0.619, 0.606]),
        B3=np.array([
            0, 0, 0, 0, 0.030, 0.118, 0.185, 0.239, 0.284, 0.321, 0.354,
            0.382, 0.406, 0.428, 0.448, 0.466, 0.482, 0.497, 0.510, 0.523,
            0.534, 0.545, 0.555, 0.565]),
        B4=np.array([
            3.267, 2.568, 2.266, 2.089, 1.970, 1.882, 1.815, 1.761, 1.716,
            1.679, 1.646, 1.618, 1.594, 1.572, 1.552, 1.534, 1.518, 1.503,
            1.490, 1.477, 1.466, 1.455, 1.445, 1.435]),
        c2=np.array([
            0.5642, 0.7236, 0.7979, 0.8407, 0.8686, 0.8882, 0.9027, 0.9139,
            0.9227, 0.9300, 0.9359, 0.9410, 0.9453, 0.9490, 0.9523, 0.9551,
            0.9576, 0.9599, 0.9619, 0.9638, 0.9655, 0.9670, 0.9684, 0.9695,
            0.9748, 0.9784, 0.9811, 0.9832, 0.9849, 0.9863, 0.9874, 0.9884,
            0.9892, 0.9900, 0.9906, 0.9911, 0.9916, 0.9925]),
        c4=np.array([
            0.7979, 0.8862, 0.9213, 0.9400, 0.9515, 0.9594, 0.9650, 0.9693,
            0.9727, 0.9754, 0.9776, 0.9794, 0.9810, 0.9823, 0.9835, 0.9845,
            0.9854, 0.9862, 0.9869, 0.9876, 0.9882, 0.9887, 0.9892, 0.9896]),
        d2=np.array([
            1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078,
            3.173, 3.258, 3.336, 3.407, 3.472, 3.532, 3.588, 3.640, 3.689,
            3.735, 3.778, 3.819, 3.858, 3.895, 3.931, 4.086, 4.213, 4.322,
            4.415, 4.498, 4.572, 4.639, 4.699, 4.755, 4.806, 4.854, 4.898,
            4.939, 5.015]),
        d3=np.array([
            0.8525, 0.8884, 0.8798, 0.8641, 0.8480, 0.8332, 0.8198, 0.8078,
            0.7971, 0.7873, 0.7785, 0.7704, 0.7630, 0.7562, 0.7499, 0.7441,
            0.7386, 0.7335, 0.7287, 0.7272, 0.7199, 0.7159, 0.7121, 0.7084,
            0.6927, 0.6799, 0.6692, 0.6601, 0.6521, 0.6452, 0.6389, 0.6333,
            0.6283, 0.6236, 0.6194, 0.6154, 0.6118, 0.6052]),
        D3=np.array([
            'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 0.076, 0.136, 0.184, 0.223,
            0.256, 0.283, 0.307, 0.328, 0.347, 0.363, 0.378, 0.391, 0.403,
            0.415, 0.423, 0.434, 0.443, 0.452, 0.459, 0.491, 0.516, 0.535,
            0.551, 0.565, 0.577, 0.587, 0.596, 0.604, 0.611, 0.617, 0.623,
            0.628, 0.638]),
        d4=np.array([
            0.954, 1.588, 1.978, 2.257, 2.472, 2.645, 2.791, 2.915, 3.024,
            3.121, 3.207, 3.285, 3.356, 3.422, 3.482, 3.538, 3.591, 3.640,
            3.686, 3.730, 3.771, 3.811, 3.847, 3.883, 4.037, 4.166, 4.274,
            4.372, 4.450, 4.521, 4.591, 4.649, 4.707, 4.757, 4.806, 4.849,
            4.892, 4.968]),
        D4=np.array([
            3.267, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816, 1.777,
            1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622, 1.609, 1.597,
            1.585, 1.577, 1.566, 1.557, 1.548, 1.541, 1.509, 1.484, 1.465,
            1.449, 1.435, 1.423, 1.413, 1.404, 1.396, 1.389, 1.383, 1.377,
            1.372, 1.362]),
        E2=np.array([
            2.660, 1.772, 1.457, 1.290, 1.184, 1.109, 1.054, 1.010, 0.975,
            0.945, 0.921, 0.899, 0.881, 0.864, 0.849, 0.836, 0.824, 0.813,
            0.803, 0.794, 0.786, 0.778, 0.770, 0.763, 0.734, 0.712, 0.694,
            0.680, 0.667, 0.656, 0.647, 0.638, 0.631, 0.624, 0.618, 0.612,
            0.607, 0.598]))
    constants = pd.DataFrame.from_dict(d, orient='index').transpose()
    constant = constants[col][constants['n'] == n].values[0]  # type: ignore
    return constant


def control_chart_xmr(
        df: pd.DataFrame,
        subgroup_size: int = 2,
        x_chart_title: str = 'X control chart title',
        x_chart_subtitle: str = 'X control chart subtitle',
        x_chart_ylabel: str = 'Response (units)',
        x_chart_xlabel: str = 'Sample',
        x_chart_svgfilename: str = 'y_x',
        mr_chart_title: str = 'mR control chart title',
        mr_chart_subtitle: str = 'mR control chart subtitle',
        mr_chart_ylabel: str = 'Response (units)',
        mr_chart_xlabel: str = 'Sample',
        mr_chart_svgfilename: str = 'y_mr') -> axes.Axes:
    '''
    Produces two charts, an X chart of individual values and a mR chart
    of moving range values.
    '''
    # Define the X chart labels.
    n = subgroup_size
    # Moving range chart statistics.
    # Calculate average moving range.
    average_mr = (
        df.iloc[:, 1]
          .rolling(n)
          .agg(lambda x: x.iloc[0] - x.iloc[1])
          .abs()
          .mean()
    )
    d2 = control_chart_constants(n, 'd2')
    d3 = control_chart_constants(n, 'd3')
    # Calculate Sigma(R).
    sigma_r = average_mr * d3 / d2
    # Calculate the range chart upper control limit.
    r_chart_ucl = average_mr + 3 * sigma_r
    # Calculate the range chart lower control limit.
    r_chart_lcl = average_mr - 3 * sigma_r
    if (r_chart_lcl < 0).any():
        r_chart_lcl = 0
    # X chart statistics.
    # Calculate the average of all values.
    average = df.iloc[:, 1].mean()
    # Calculate Sigma(X).
    sigma_x = average_mr / d2
    # Calculate the X chart upper control limit.
    x_chart_ucl = average + 3 * sigma_x
    # Calculate two Sigma(X) above the average.
    plus_two_sigma_x = average + 2 * sigma_x
    # Calculate one Sigma(X) above the average.
    plus_one_sigma_x = average + sigma_x
    # Calculate the X chart lower control limit.
    x_chart_lcl = average - 3 * sigma_x
    # Calculate two Sigma(X) below the average.
    minus_two_sigma_x = average - 2 * sigma_x
    # Calculate one Sigma(X) below the average.
    minus_one_sigma_x = average - sigma_x
    # Use a colour-blind friendly colormap, 'Paired'.
    lines_c, limits_c, average_c, *_ = cm.Paired.colors
    # Create the X chart.
    ax = (
        df.set_index(df.columns[0])
          .plot.line(legend=False, marker='o', markersize=3, color=lines_c)
    )
    # Get the X axis limits to use to set the limits for the mR chart.
    xmin, xmax = ax.get_xlim()
    # Remove the top and right spines.
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')
    # Add average line to X chart.
    ax.axhline(y=average, color=average_c)
    # Add the upper control limits for the X chart.
    ax.axhline(y=x_chart_ucl, color=limits_c)
    # Add the lower control limits for the X chart.
    ax.axhline(y=x_chart_lcl, color=limits_c)
    # Add the chart title and subtitle
    ax.set_title(x_chart_title + '\n' + x_chart_subtitle, fontweight='bold')
    # Add the Y axis label.
    ax.set_ylabel(x_chart_ylabel)
    # Add the X axis label.
    ax.set_xlabel(x_chart_xlabel)
    # Save the graph as svg.
    ax.figure.savefig(f'{x_chart_svgfilename}.svg', format='svg')
    plt.show()
    # Create the mR chart.
    ax = (df.set_index(df.columns[0])
            .rolling(n)
            .agg(lambda x: x.iloc[0] - x.iloc[1])
            .abs()
            .plot.line(legend=False, marker='o',
                       markersize=3, color=lines_c,))
    # Set the X axis limits of the mR chart to be the same as the X chart.
    ax.set_xlim(xmin, xmax)
    # Remove the top and right spines.
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')
    # Add average line to mR chart.
    ax.axhline(y=average_mr, color=average_c)
    # Add the upper control limits for the mR chart.
    ax.axhline(y=r_chart_ucl, color=limits_c)
    # Add the lower control limits for the mR chart.
    ax.axhline(y=r_chart_lcl, color=limits_c)
    # Add the chart title and subtitle
    ax.set_title(mr_chart_title + '\n' + mr_chart_subtitle, fontweight='bold')
    # Add the Y axis label.
    ax.set_ylabel(mr_chart_ylabel)
    # Add the X axis label.
    ax.set_xlabel(mr_chart_xlabel)
    # Save the graph as svg.
    ax.figure.savefig(f'{mr_chart_svgfilename}.svg', format='svg')
    plt.show()
    # __import__('pdb').set_trace()
    return ax


def control_chart_xbarr(
        df: pd.DataFrame,
        subgroup_size: int = 5,
        xbar_chart_title: str = 'Xbar control chart title',
        xbar_chart_subtitle: str = 'Xbar control chart subtitle',
        xbar_chart_ylabel: str = 'Response (units)',
        xbar_chart_xlabel: str = 'Sample',
        xbar_chart_svgfilename: str = 'y_xbar',
        r_chart_title: str = 'R control chart title',
        r_chart_subtitle: str = 'R control chart subtitle',
        r_chart_ylabel: str = 'Response (units)',
        r_chart_xlabel: str = 'Sample',
        r_chart_svgfilename: str = 'y_r') -> Tuple[axes.Axes, axes.Axes]:
    '''
    Produces two charts, an Xbar chart of average values and an R chart
    of range values.
    '''


def _despine(ax: axes.Axes) -> None:
    'Remove the top and right spines'
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


class Sigmas:
    def __init__(self, mean: float, sigma: float):
        self._mean = mean
        self._sigma = sigma

    def __getitem__(self, index: Union[int, slice]) -> float:
        if isinstance(index, int):
            return self._mean + index * self._sigma
        elif isinstance(index, slice):
            raise NotImplementedError()
        else:
            raise ValueError()


class ControlChart(NamedTuple):
    ucl: float  # Upper control limit
    lcl: float  # Lower control limit
    sigma: float  # E.g., Sigma(R)
    mean: float  # E.g., Average moving range
    ax: axes.Axes  # Plot

    def __str__(self) -> str:
        raise NotImplementedError()

    @property
    def sigmas(self):
        '''
        TODO

        Ex:

            cc = ProcessBehaviourCharts(df)
            cc.X_chart.sigmas[-3]  # or +2
        '''
        return Sigmas(mean=self.mean, sigma=self.sigma)


class ProcessBehaviourCharts:
    def __init__(self, data: pd.DataFrame):
        self._subgroup_size = len(data.columns)
        assert self._subgroup_size >= 2
        self._df = data.copy()

    def X_chart(self) -> ControlChart:
        raise NotImplementedError()

    def mR_chart(self) -> ControlChart:
        raise NotImplementedError()

    '''
    df = …
    pbc = ProcessBehaviourCharts(df)
    r = pbc.R_chart()
    r.ax.set_title(df.caption)
    r.ax.set_ylabel('Response')
    r.ax.set_xlabel('Sample')
    r.ax.savefig('foo.svg')
    '''

    def R_chart(self) -> ControlChart:
        # TODO: Factor out?
        d_two = control_chart_constants(n=len(self._df.columns), col='d2')
        d_three = control_chart_constants(n=len(self._df.columns), col='d3')

        # TODO: factor out
        # R chart statistics
        # Calculate average range
        average_range = (self._df.max(axis='columns') -
                         self._df.min(axis='columns')).mean()

        # Calculate the range chart upper control limit.
        range_chart_upper_control_limit = (
            average_range
            + 3
            * d_three
            * average_range
            / d_two
        )
        # Calculate the range chart lower control limit.
        range_chart_lower_control_limit = (
            average_range
            - 3
            * d_three
            * average_range
            / d_two
        )
        # Set the moving range lower control limit to 0 if it is < 0.
        if range_chart_lower_control_limit < 0:
            range_chart_lower_control_limit = 0.0

        # Create a graph of "range values v. sample".
        ax = (
            self._df.max(axis='columns')
            - self._df.min(axis='columns')
        ).plot.line(legend=False,
                    marker='o',
                    markersize=3,
                    color='blue')
        ax.axhline(y=average_range, color='b')
        ax.axhline(y=range_chart_upper_control_limit, color='r')
        ax.axhline(y=range_chart_lower_control_limit, color='r')
        _despine(ax)

        return ControlChart(ucl=range_chart_upper_control_limit,
                            lcl=range_chart_lower_control_limit,
                            mean=average_range,
                            sigma=average_range * d_three / d_two,
                            ax=ax)

    def Xbar_chart(self) -> ControlChart:
        # TODO: factor out
        # R chart statistics
        # Calculate average range
        average_range = (self._df.max(axis='columns') -
                         self._df.min(axis='columns')).mean()

        # TODO: Factor out?
        d_two = control_chart_constants(n=self._subgroup_size, col='d2')

        # Xbar chart statistics
        # Calculate average of averages.
        average_of_averages = (self._df.mean(axis='columns')).mean()
        # Calculate the averages chart upper control limit.
        ucl = (
            average_of_averages
            + 3
            * average_range
            / (d_two * math.sqrt(self._subgroup_size))
        )
        # Calculate the averages chart lower control limit.
        lcl = (
            average_of_averages
            - 3
            * average_range
            / (d_two * math.sqrt(self._subgroup_size))
        )

        # Create a graph of "average values v. sample".
        ax = self._df.mean(axis='columns') \
                     .plot.line(legend=False,
                                marker='o',
                                markersize=3,
                                color='blue')
        ax.axhline(y=average_of_averages, color='b')
        ax.axhline(y=ucl, color='r')
        ax.axhline(y=lcl, color='r')
        _despine(ax)

        return ControlChart(ucl=ucl,
                            lcl=lcl,
                            sigma=average_range
                            / d_two
                            / math.sqrt(self._subgroup_size),
                            mean=average_of_averages,
                            ax=ax)


__all__ = (
    'sommaire_cinq_numeros',
    'five_number_summary',
    'six_number_summary',
    'seven_number_summary',
    'nonparametric_summary',
    'parametric_summary',
    'control_chart_constants',
    'control_chart_xmr',
    'control_chart_xbarr',
    'ControlChart',
    'ProcessBehaviourCharts',
)
