import datasense as ds
import pandas as pd


from pytest import approx, mark


X = pd.Series(
    data=[
        25.0, 24.0, 35.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0, 16.0,
        16.0, 16.0
    ]
)


# def check_nonparametric_summary(myseries, expected):
#     result = ds.nonparametric_summary(myseries)
#     assert result == expected


def test_nonparametric_summary():
    ds.nonparametric_summary(myseries)
    return


def test_parametric_summary():
    series = ds.parametric_summary(series=X)
    assert series[0] == 13
    assert series[1] == 10.0
    assert series[2] == 35.5
    assert series[3] == 18.392
    assert series[4] == (14.012638095621575, 22.77197728899381)
    assert series[5] == 7.248
    assert series[6] == 52.527

# TODO:
# Add utility function for series, expected
# Add test for method 6
# Add test for method 8
