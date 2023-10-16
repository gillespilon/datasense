"""
Automation functions
"""

from typing import List


def fahrenheit_to_celsius_table(
    min_fahrenheit: int = 350,
    max_fahrenheit: int = 450,
    fahrenheit_increment: int = 5,
    rounding_increment: int = 5
):
    """
    Generates an HTML table of Fahrenheit to Celsius conversions.

    Parameters
    ----------
    min_fahrenheit : int = 350
        The minimum Fahrenheit temperature to include in the table.
    max_fahrenheit : int = 450
        The maximum Fahrenheit temperature to include in the table.
    fahrenheit_increment : int = 5
        The increment in Fahrenheit degrees between each row in the table.
    rounding_increment : int = 5
        The increment of rounding in the ones place value.

    Returns
    -------
    An HTML table of Fahrenheit to Celsius conversions.

    Example
    -------
    >>> import datasense as ds
    >>> output_url = 'fahrenheit_to_celsius.html'
    >>> header_title = 'Fahrenheit to Celsius'
    >>> header_id = 'fahrenehit-to-celsius'
    >>> original_stdout = ds.html_begin(
    ...     output_url=output_url,
    ...     header_title=header_title,
    ...     header_id=header_id
    ... )
    >>> table = ds.fahrenheit_to_celsius_table()
    >>> print(table)
    >>> ds.html_end(
    ...     original_stdout=original_stdout,
    ...     output_url=output_url
    ... )
    """
    html_table = """
    <table>
      <tr>
        <th>Fahrenheit</th>
        <th>Celsius</th>
      </tr>
    """
    for fahrenheit in range(
        min_fahrenheit,
        max_fahrenheit + fahrenheit_increment,
        fahrenheit_increment
    ):
        celsius = (
            rounding_increment *
            round(((fahrenheit - 32) * 5 / 9) / rounding_increment)
        )
        html_table += """
        <tr>
          <td>{}</td>
          <td>{}</td>
        </tr>
        """.format(fahrenheit, celsius)
    html_table += """
    </table>
    """
    return html_table


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
    >>> import datasense as ds
    >>> ds.water_coffee_tea(
    ...     mugs_coffee=1,
    ...     cups_tea=0,
    ...     mugs_tea=0
    ... )
    (370, 220, 150, 0, 0)

    Example 2
    ---------
    >>> import datasense as ds
    >>> coffee_mug_water, coffee_filter_water = [ds.water_coffee_tea(
    ...     mugs_coffee=1,
    ...     cups_tea=0,
    ...     mugs_tea=0
    ... )[i] for i in [1, 2]]
    >>> print(coffee_mug_water, coffee_filter_water)
    220 150

    Example 3
    ---------
    >>> import datasense as ds
    >>> all_coffee_water = ds.water_coffee_tea(
    ...     mugs_coffee=1,
    ...     cups_tea=0,
    ...     mugs_tea=0
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
    "fahrenheit_to_celsius_table",
    "water_coffee_tea",
)
