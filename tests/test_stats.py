import datasense as ds
import pandas as pd


myseries = pd.Series([1, 3, 6])


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
