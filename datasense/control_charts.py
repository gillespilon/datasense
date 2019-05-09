from typing import Union, Optional
from abc import ABC, abstractmethod
from math import sqrt

from cached_property import cached_property
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.axes as axes


_QUANTILES = (0.25, 0.50, 0.75)
_QUANTILE_METHODS = [
    (0, 1), (0.5, 0.5), (0, 0), (1, 1), (0.33, 0.33), (0.375, 0.375)
]


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


class ControlChart(ABC):
    def __init__(self, data: pd.DataFrame):
        self._df = data

    @cached_property
    @abstractmethod
    def ucl(self) -> float:  # pragma: no cover
        'upper control limit'
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def lcl(self) -> float:  # pragma: no cover
        'lower control limit'
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def sigma(self) -> float:  # pragma: no cover
        'sigma appropriate to method used'
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def mean(self) -> float:  # pragma: no cover
        'average'
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def ax(self) -> axes.Axes:  # pragma: no cover
        'Matplotlib control chart plot'
        raise NotImplementedError()

    #@abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    @cached_property
    def sigmas(self):
        '''
        TODO

        Ex:

            cc = ProcessBehaviourCharts(df)
            cc.X_chart.sigmas[-3]  # or +2
        '''
        return Sigmas(mean=self.mean, sigma=self.sigma)

    # TODO: cache
    def _average_mr(self, subgroup_size: Optional[int] = 2) -> float:
        'Average moving range'
        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        _ = self._df.iloc[:, 0]
        return (
            _.rolling(subgroup_size).max() -
            _.rolling(subgroup_size).min()
        ).mean()


c = cm.Paired.colors
# c[0] c[1] ... c[11]
# See "paired" in "qualitative colormaps"
# https://matplotlib.org/tutorials/colors/colormaps.html


class X(ControlChart):
    def __init__(self, data: pd.DataFrame, subgroup_size: Optional[int] = 2):
        super().__init__(data)

        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        self.subgroup_size = subgroup_size

    @cached_property
    def _d2(self) -> float:
        return control_chart_constants(self.subgroup_size, 'd2')

    @cached_property
    def sigma(self) -> float:
        return self._average_mr(self.subgroup_size) / self._d2

    @cached_property
    def ucl(self) -> float:
        return self.mean + 3 * self.sigma

    @cached_property
    def lcl(self) -> float:
        return self.mean - 3 * self.sigma

    @cached_property
    def mean(self) -> float:
        return self._df.iloc[:, 0].mean()

    @cached_property
    def ax(self) -> axes.Axes:
        ax = self._df.plot.line(legend=False, marker='o', markersize=3,
                                color=c[0])
        # Remove the top and right spines.
        _despine(ax)
        # Add average line to X chart.
        ax.axhline(y=self.mean, color=c[2])
        # Add the upper control limits for the X chart.
        ax.axhline(y=self.ucl, color=c[1])
        # Add the lower control limits for the X chart.
        ax.axhline(y=self.lcl, color=c[1])

        return ax


class mR(ControlChart):
    def __init__(self, data: pd.DataFrame, subgroup_size: Optional[int] = 2):
        super().__init__(data)

        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        self.subgroup_size = subgroup_size

    @cached_property
    def _d2(self) -> float:
        return control_chart_constants(self.subgroup_size, 'd2')

    @cached_property
    def _d3(self) -> float:
        return control_chart_constants(self.subgroup_size, 'd3')

    @cached_property
    def sigma(self) -> float:
        'Sigma(R)'
        return self._average_mr(self.subgroup_size) * self._d3 / self._d2

    @cached_property
    def ucl(self) -> float:
        return self._average_mr(self.subgroup_size) + 3 * self.sigma

    @cached_property
    def lcl(self) -> float:
        r_chart_lcl = self._average_mr(self.subgroup_size) - 3 * self.sigma
        if r_chart_lcl < 0:
            r_chart_lcl = 0
        return r_chart_lcl

    @cached_property
    def mean(self) -> float:
        return self._average_mr(self.subgroup_size)

    @cached_property
    def ax(self) -> axes.Axes:
        'Matplotlib control chart plot'
        ax = (
            self._df.rolling(self.subgroup_size).max() -
            self._df.rolling(self.subgroup_size).min()
        ).plot.line(legend=False, marker='o',
                    markersize=3, color=c[0],)
        # TODO? ax.set_xlim(0, len(self._df.columns))
        _despine(ax)
        ax.axhline(y=self.mean, color=c[2])
        ax.axhline(y=self.ucl, color=c[1])
        ax.axhline(y=self.lcl, color=c[1])

        return ax


class R(ControlChart):
    @cached_property
    def _d2(self) -> float:
        return control_chart_constants(n=len(self._df.columns), col='d2')

    @cached_property
    def _d3(self) -> float:
        return control_chart_constants(n=len(self._df.columns), col='d3')

    @cached_property
    def mean(self) -> float:
        'Average range'
        return (
            self._df.max(axis='columns') - self._df.min(axis='columns')
        ).mean()

    @cached_property
    def ucl(self) -> float:
        return (
            self.mean
            + 3
            * self._d3
            * self.mean
            / self._d2
        )

    @cached_property
    def lcl(self) -> float:
        ret = (
            self.mean
            - 3
            * self._d3
            * self.mean
            / self._d2
        )
        # Set the moving range lower control limit to 0 if it is < 0.
        if ret < 0:
            ret = 0.0
        return ret

    @cached_property
    def ax(self) -> axes.Axes:
        ax = (
            self._df.max(axis='columns')
            - self._df.min(axis='columns')
        ).plot.line(legend=False,
                    marker='o',
                    markersize=3,
                    color=c[0])
        ax.axhline(y=self.mean, color=c[2])
        ax.axhline(y=self.ucl, color=c[1])
        ax.axhline(y=self.lcl, color=c[1])
        _despine(ax)
        return ax

    @cached_property
    def sigma(self) -> float:
        return self.mean * self._d3 / self._d2


class Xbar(ControlChart):
    @cached_property
    def _average_range(self) -> float:
        'Average range'
        return (
            self._df.max(axis='columns') -
            self._df.min(axis='columns')
        ).mean()

    @cached_property
    def _subgroup_size(self) -> int:
        return len(self._df.columns)

    @cached_property
    def _d2(self) -> float:
        return control_chart_constants(n=self._subgroup_size, col='d2')

    @cached_property
    def mean(self) -> float:
        'Average of averages'
        return self._df.mean(axis='columns').mean()

    @cached_property
    def ucl(self) -> float:
        return (
            self.mean
            + 3
            * self._average_range
            / (self._d2 * sqrt(self._subgroup_size))
        )

    @cached_property
    def lcl(self) -> float:
        return (
            self.mean
            - 3
            * self._average_range
            / (self._d2 * sqrt(self._subgroup_size))
        )

    @cached_property
    def ax(self) -> axes.Axes:
        'average values v. sample'
        ax = self._df.mean(axis='columns') \
                     .plot.line(legend=False,
                                marker='o',
                                markersize=3,
                                color=c[0])
        ax.axhline(y=self.mean, color=c[2])
        ax.axhline(y=self.ucl, color=c[1])
        ax.axhline(y=self.lcl, color=c[1])
        _despine(ax)
        return ax

    @cached_property
    def sigma(self) -> float:
        return self._average_range / self._d2 / sqrt(self._subgroup_size)


__all__ = (
    'ControlChart',
    'X',
    'mR',
    'R',
    'Xbar',
)
