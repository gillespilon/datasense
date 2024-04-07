"""
Process capability refers to the ability of a process to meet a performance
standard (specification). A process is capable if you have:
- Specifications are defined and attainable.
- Can measure sufficiently well.
- Samples are representative.
- Process variation is stable and predictable.
- Process is on target with minimum dispersion.
"""

import math

from scipy.stats import chi2, norm
import pandas as pd
import numpy as np


df_constants = pd.DataFrame.from_dict(
    dict(
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
            0.607, 0.598])
    ),
    orient='index').transpose().set_index('n')


def cp(
    average: float | int,
    std_devn: float | int,
    subgroup_size: int,
    number_subgroups: int,
    lower_spec: float | int,
    upper_spec: float | int,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """
    Cp compares the width of the process specification to the width of the
    process variation. It does not take into consideration the deviation from
    the average. It "assumes" the process is centred between the specification
    limits. The standard deviation estimate is taken from a range or moving
    range control chart.

    Parameters
    ----------
    average : float | int,
        The average of the process.
    std_devn : float | int,
        The standard deviation of the process. It should be the "sample
        standard deviation".
    subgroup_size : int,
        This is the number of values in a control chart subgroup
    number_subgroups : int,
        This is the number of subgroups.
    lower_spec : float | int,
        The lower specification value.
    upper_spec : float | int,
        The upper specification value.
    alpha : float = 0.05
        The alpha value for the confidence interval calculations. An alpha of
        0.05 is used for a 95 % confidence interval.

    Returns
    -------
    capability : float
        The Pp process capability value.
    lower_bound : float
        The lower value of the confidence interval for Pp.
    upper_bound : float
        The upper value of the confidence interval for Pp.

    Example
    -------
    >>> import datasense as ds
    >>> average = 0.11001
    >>> std_devn = 0.89312
    >>> subgroup_size = 1
    >>> number_subgroups = 39
    >>> lower_spec = -4
    >>> upper_spec = 4
    >>> alpha = 0.05
    >>> result = ds.cp(
    >>>     average=average,
    >>>     std_devn=std_devn,
    >>>     subgroup_size=subgroup_size,
    >>>     number_subgroups=number_subgroups,
    >>>     lower_spec=lower_spec,
    >>>     upper_spec=upper_spec,
    >>>     alpha=alpha
    >>> )
    (1.4928938253911381, 1.141174267641542, 1.8439148118984439)
    """
    capability = (upper_spec - lower_spec) / (6 * std_devn)
    constant_name = ["d2", "d3"]
    d2, d3 =  df_constants.loc[subgroup_size, constant_name]
    # as per wheeler in advanced topics of SPC
    degrees_of_freedom = (d2 ** 2 * number_subgroups) / (2 * d3 ** 2) + 0.2
    chi2_lower = chi2.ppf(q=(alpha / 2), df=degrees_of_freedom)
    chi2_upper = chi2.ppf(q=(1 - alpha / 2), df=degrees_of_freedom)
    lower_bound = capability * math.sqrt(chi2_lower / degrees_of_freedom)
    upper_bound = capability * math.sqrt(chi2_upper / degrees_of_freedom)
    return (capability, lower_bound, upper_bound)


def cpk() -> None:
    """
    Cpk compares the width of the process specification to the width of the
    process variation. It takes into consideration the deviation from
    the average. The standard deviation estimate is taken from a range or
    moving range control chart.
    """
    pass


def cpm() -> None:
    """
    Ppk and Cpk calculate process capability with respect to the deviation from
    the average. If a process average is not equal to the specification target,
    the process capability is not as good as one would assume. Cpm calculates
    process capability with respect to the deviation from the average and the
    the deviation from the target. The Cpm formula is closely related to the
    Taguchi Loss Function.
    """
    pass


def pp(
    average: float | int,
    std_devn: float | int,
    sample_size: int,
    lower_spec: float | int,
    upper_spec: float | int,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """
    Pp compares the width of the process specification to the width of the
    process variation. It does not take into consideration the deviation from
    the average. It "assumes" the process is centred between the specification
    limits. The standard deviation uses the "sample standard deviation"
    formula.

    Parameters
    ----------
    average : float | int,
        The average of the process.
    std_devn : float | int,
        The standard deviation of the process. It should be the "sample
        standard deviation".
    sample_size : int,
        This is the sample size for the data being analysed.
    lower_spec : float | int,
        The lower specification value.
    upper_spec : float | int,
        The upper specification value.
    alpha : float = 0.05
        The alpha value for the confidence interval calculations. An alpha of
        0.05 is used for a 95 % confidence interval.

    Returns
    -------
    capability : float
        The Pp process capability value.
    lower_bound : float
        The lower value of the confidence interval for Pp.
    upper_bound : float
        The upper value of the confidence interval for Pp.

    Example
    -------
    >>> import datasense as ds
    >>> average = 0.11001
    >>> std_devn = 0.868663
    >>> sample_size = 40
    >>> lower_spec = -4
    >>> upper_spec = 4
    >>> alpha = 0.05
    >>> result = ds.pp(
    >>>     average=average,
    >>>     std_devn=std_devn,
    >>>     sample_size=sample_size,
    >>>     lower_spec=lower_spec,
    >>>     upper_spec=upper_spec,
    >>>     alpha=alpha
    >>> )
    (1.5349258956964131, 1.1953921108301047, 1.873778000024199)
    """
    capability = (upper_spec - lower_spec) / (6 * std_devn)
    degrees_of_freedom = sample_size - 1
    chi2_lower = chi2.ppf(q=alpha / 2, df=degrees_of_freedom)
    chi2_upper = chi2.ppf(q=1 - alpha / 2, df=degrees_of_freedom)
    lower_bound = capability * math.sqrt(chi2_lower / degrees_of_freedom)
    upper_bound = capability * math.sqrt(chi2_upper / degrees_of_freedom)
    return (capability, lower_bound, upper_bound)


def ppk(
    average: float | int,
    std_devn: float | int,
    sample_size: int,
    lower_spec: float | int,
    upper_spec: float | int,
    alpha: float = 0.05,
    toler: float | int = 6,
) -> tuple[float, float, float]:
    """
    Ppk compares the width of the process specification to the width of the
    process variation. It does take into consideration the deviation from
    the average. The standard deviation uses the "sample standard deviation"
    formula.

    Parameters
    ----------
    average : float | int,
        The average of the process.
    std_devn : float | int,
        The standard deviation of the process. It should be the "sample
        standard deviation".
    sample_size : int,
        This is the sample size for the data being analysed.
    lower_spec : float | int,
        The lower specification value.
    upper_spec : float | int,
        The upper specification value.
    alpha : float = 0.05
        The alpha value for the confidence interval calculations. An alpha of
        0.05 is used for a 95 % confidence interval.
    toler : float | int = 6
        The multiplier of the standard deviation tolerance.

    Returns
    -------
    capability : float
        The Ppk process capability value.
    lower_bound : float
        The lower value of the confidence interval for Ppk.
    upper_bound : float
        The upper value of the confidence interval for Ppk.

    Example
    -------
    >>> import datasense as ds
    >>> average = 0.11001
    >>> std_devn = 0.868663
    >>> sample_size = 40
    >>> lower_spec = -4
    >>> upper_spec = 4
    >>> alpha = 0.05
    >>> result = ds.ppk(
    >>>     average=average,
    >>>     std_devn=std_devn,
    >>>     sample_size=sample_size,
    >>>     lower_spec=lower_spec,
    >>>     upper_spec=upper_spec,
    >>>     alpha=alpha,
    >>>     toler=6
    >>> (
        1.4927115962500226, 1.5771401951428037, 1.4927115962500226,
        1.1457133294762083, 1.8397098630238369
    )
    """
    degrees_of_freedom = sample_size - 1
    ppk_lower = (average - lower_spec) / (3 * std_devn)
    ppk_upper = (upper_spec - average) / (3 * std_devn)
    capability = min(ppk_lower, ppk_upper)
    z = norm.ppf(q=(1 - alpha / 2))
    lower_bound = capability - z * math.sqrt(
        (1 / (((toler / 2) ** 2) * sample_size))
        + ((capability**2) / (2 * degrees_of_freedom))
    )
    upper_bound = capability + z * math.sqrt(
        (1 / (((toler / 2) ** 2) * sample_size))
        + ((capability**2) / (2 * degrees_of_freedom))
    )
    # upper_bound = capability * math.sqrt(chi2_upper / degrees_of_freedom)
    return (capability, ppk_lower, ppk_upper, lower_bound, upper_bound)


__all__ = (
    "cp",
    "cpk",
    "cpm",
    "pp",
    "ppk",
)
