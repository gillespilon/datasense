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

from scipy.stats import chi2


def cp() -> None:
    """
    Cp compares the width of the process specification to the width of the
    process variation. It does not take into consideration the deviation from
    the average. It "assumes" the process is centred between the specification
    limits. The standard deviation estimate is taken from a range or moving
    range control chart.
    """
    pass


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


def ppk() -> None:
    """
    Ppk compares the width of the process specification to the width of the
    process variation. It does take into consideration the deviation from
    the average. The standard deviation uses the "sample standard deviation"
    formula.
    """
    pass


__all__ = (
    "cp",
    "cpk",
    "cpm",
    "pp",
    "ppk",
)
