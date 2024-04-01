"""
Taguchi Methods
"""


def taguchi_loss_function(
    *,
    average: float | int,
    std_dev: float | int,
    target: float | int,
    cost: float | int,
    x: float | int,
) -> float:
    """
    Calculate the average cost of use (ACU). It is also called the loss
    function.

    Parameters
    ----------
    average : float
        It is the average measurement value for the product stream. It is best
        to use a control chart (Xbar R | X mR) to estimate the average.
    std_dev : float
        It is the standard deviation of the product stream. It is best to use
        a control chart (Xbar R | X mR) to estimate the average.
    target : float
        It is the target value of the product stream.
    cost : float
        It is the cost of scrap, rework, or repair for a single unit of
        product.
    x : float
        It is the measurement value at which an item is scrapped, reworked, or
        repaired.

    Returns:
    --------
    acu : float

    Example
    -------
    >>> import datasense as ds
    >>> average = 4.66
    >>> std_dev = 1.80
    >>> target = 7.5
    >>> cost = 0.25
    >>> x = 15
    >>> acu = ds.taguchi_loss_function(
    ...     average=average,
    ...     std_dev=std_dev,
    ...     target=target,
    ...     cost=cost,
    ...     x=x,
    ... )
    >>> acu
    0.05024711111111111
    """
    # Calcuate the shape parameter.
    k = cost / (x - target) ** 2
    # Calculate the ACU.
    acu = k * (std_dev ** 2 + (average - target) ** 2)
    return acu


__all__ = (
    "taguchi_loss_function",
)

