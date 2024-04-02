"""
Process capability refers to the ability of a process to meet a performance
standard (specification). A process is capable if you have:
- Specifications are defined and attainable.
- Can measure sufficiently well.
- Samples are representative.
- Process variation is stable and predictable.
- Process is on target with minimum dispersion.
"""


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


def pp() -> None:
    """
    Pp compares the width of the process specification to the width of the
    process variation. It does not take into consideration the deviation from
    the average. It "assumes" the process is centred between the specification
    limits. The standard deviation uses the "sample standard deviation"
    formula.
    """
    pass


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
