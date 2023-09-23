import datasense as ds


def test_water_coffee_tea():
    result = ds.water_coffee_tea(
            mugs_coffee=0,
            cups_tea=0,
            mugs_tea=0
        )
    expected = (0, 0, 0, 0, 0)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=0,
            cups_tea=0,
            mugs_tea=1
        )
    expected = (300, 0, 0, 0, 300)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=0,
            cups_tea=1,
            mugs_tea=0
        )
    expected = (400, 0, 0, 400, 0)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=0,
            cups_tea=1,
            mugs_tea=1
        )
    expected = (700, 0, 0, 400, 300)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=1,
            cups_tea=0,
            mugs_tea=0
        )
    expected = (370, 220, 150, 0, 0)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=1,
            cups_tea=0,
            mugs_tea=1
        )
    expected = (670, 220, 150, 0, 300)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=1,
            cups_tea=1,
            mugs_tea=0
        )
    expected = (770, 220, 150, 400, 0)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=1,
            cups_tea=1,
            mugs_tea=1
        )
    expected = (1070, 220, 150, 400, 300)
    assert result == expected
    result = ds.water_coffee_tea(
            mugs_coffee=2,
            cups_tea=0,
            mugs_tea=0
        )
    expected = (740, 440, 300, 0, 0)
    assert result == expected
