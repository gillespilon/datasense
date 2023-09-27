"""
Automation functions
"""

from typing import List


def water_coffee_tea(
    *,
    mugs_coffee: int = 0,
    cups_tea: int = 0,
    mugs_tea: int = 0,
    water_coffee_filter_mass: int = 150,
    water_tea_cup_mass: int = 400,
    water_tea_mug_mass: int = 300,
    water_coffee_mass: int = 220
) -> List[int]:
    """
    Calculate the water mass required for coffee mugs, tea cups, and tea mugs.
    All units are g.

    Parameters
    ----------

    mugs_coffee : int = 0,
        The number of coffee mugs.
    cups_tea : int = 0,
        The number of tea cups.
    mugs_tea : int = 0,
        The number of tea mugs.
    water_coffee_filter_mass : int = 150,
        The mass of water to wet one coffee filter.
    water_tea_cup_mass : int = 400,
        The mass of water for a tea cup.
    water_tea_mug_mass : int = 300,
        The mass of water for a coffee mug.
    water_coffee_mass : int = 220
        The mass of water to wet the coffee grinds.

    Returns
    -------
        water : int
            The total amount of water to boil (g).
        coffee_mug_water : int
            The amount of water for the coffee mugs (g).
        coffee_filter_water : int
            The amount of water to wet the coffee filters (g).
        tea_cup_water : int
            The amount of water for the tea cups (g).
        tea_mug_water : int
            The amount of water for the tea mugs (g).

    Examples
    --------

    Example 1
    ---------
    >>> water_coffee_tea(
    ... mugs_coffee=1,
    ... cups_tea=0,
    ... mugs_tea=0
    ... )
    (370, 220, 150, 0, 0)

    Example 2
    ---------
    >>> coffee_mug_water, coffee_filter_water = [water_coffee_tea(
    ... mugs_coffee=1,
    ... cups_tea=0,
    ... mugs_tea=0
    ... )[i] for i in [1, 2]]
    >>> print(coffee_mug_water, coffee_filter_water)
    220 150

    Example 3
    ---------
    >>> all_coffee_water = water_coffee_tea(
    ... mugs_coffee=1,
    ... cups_tea=0,
    ... mugs_tea=0
    ... )[0:3]
    >>> print(all_coffee_water)
    (370, 220, 150)
    """
    coffee_mug_water = mugs_coffee * water_coffee_mass
    coffee_filter_water = mugs_coffee * water_coffee_filter_mass
    tea_cup_water = cups_tea * water_tea_cup_mass
    tea_mug_water = mugs_tea * water_tea_mug_mass
    water = coffee_mug_water + coffee_filter_water + tea_cup_water + \
        tea_mug_water
    return (
        water, coffee_mug_water, coffee_filter_water, tea_cup_water,
        tea_mug_water
    )


__all__ = (
    "water_coffee_tea",
)
