import datasense.stats as st
import pandas as pd


myseries = pd.Series([1, 3, 6])


def test_nonparametric_summary():
    st.nonparametric_summary(myseries)
    return


def test_parametric_summary():
    st.parametric_summary(myseries)
    return
