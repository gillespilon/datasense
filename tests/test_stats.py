import datasense as ds
import pandas as pd


from pytest import approx, mark


myseries = pd.Series([1, 3, 6])


# def check_nonparametric_summary(myseries, expected):
#     result = ds.nonparametric_summary(myseries)
#     assert result == expected


def test_nonparametric_summary():
    ds.nonparametric_summary(myseries)
    return


def test_parametric_summary():
    ds.parametric_summary(myseries)
    return

# TODO:
# Add utility function for series, expected
# Add test for method 6
# Add test for method 8
