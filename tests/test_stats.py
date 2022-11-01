import datasense as ds
import pandas as pd


X = pd.Series(
    data=[
        25.0, 24.0, 35.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0, 16.0,
        16.0, 16.0
    ]
)
df_integer_float = pd.DataFrame(
    data={
        "abscissa": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "ordinate": [
            0, 0.841470984807896, 0.909297426825682, 0.141120008059867,
            -0.756802495307928, -0.958924274663138, -0.279415498198926,
            0.656986598718789, 0.989358246623382, 0.412118485241757
        ]
    }
)
df_datetime_float = pd.DataFrame(
    data={
        "abscissa": [
            "2020-01-01 12:00:00", "2020-01-02 12:00:00",
            "2020-01-03 12:00:00", "2020-01-04 12:00:00",
            "2020-01-05 12:00:00", "2020-01-06 12:00:00",
            "2020-01-07 12:00:00", "2020-01-08 12:00:00",
            "2020-01-09 12:00:00", "2020-01-10 12:00:00"
        ],
        "ordinate": [
            0, 0.841470984807896, 0.909297426825682, 0.141120008059867,
            -0.756802495307928, -0.958924274663138, -0.279415498198926,
            0.656986598718789, 0.989358246623382, 0.412118485241757
        ]
    }
).astype(dtype={'abscissa': 'datetime64[s]'})
df_two_sample_t = pd.DataFrame(
    data={
        "X": [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2
        ],
        "y": [
            32, 37, 35, 38, 41, 44, 35, 31, 34, 38, 42,
            36, 31, 30, 31, 34, 36, 39, 32, 31
        ]
    }
)


def test_nonparametric_summary():
    """
    Test for method 8
    """
    result = ds.nonparametric_summary(series=X)
    expected = pd.Series(
        data={
            "lower outer fence": -15.4, "lower inner fence": -0.85,
            "lower quartile": 13.7, "median": 16.0,
            "confidence interval": (11.776235355842992, 20.223764644157008),
            "upper quartile": 23.4,
            "upper inner fence": 37.95, "upper outer fence": 52.5,
            "interquartile range": 9.7,
            "inner outliers": [], "outer outliers": [],
            "minimum value": 10.0, "maximum value": 35.5, "count": 13
        }
    )
    assert (result == expected).all()


def test_parametric_summary():
    result = ds.parametric_summary(series=X)
    expected = pd.Series(
        data={
            "n": 13, "min": 10.0, "max": 35.5, "ave": 18.392,
            "confidence interval": (14.012638095621575, 22.77197728899381),
            "s": 7.248, "var": 52.527
        }
    )
    assert (result == expected).all()


def test_cubic_spline():
    cubic_spline = ds.cubic_spline(
        df=df_integer_float,
        abscissa="abscissa",
        ordinate="ordinate"
    )
    result = cubic_spline(x=df_integer_float["abscissa"])
    expected = (
        [
            0., 0.841470984807896, 0.909297426825682, 0.141120008059867,
            -0.756802495307928, -0.958924274663138, -0.279415498198926,
            0.656986598718789, 0.989358246623382, 0.41211848524175704]
    )
    assert (result == expected).all()
    cubic_spline = ds.cubic_spline(
        df=df_datetime_float,
        abscissa="abscissa",
        ordinate="ordinate"
    )
    result = cubic_spline(x=df_datetime_float["abscissa"])
    expected = (
        [
            0., 0.841470984807896, 0.909297426825682, 0.141120008059867,
            -0.756802495307928, -0.958924274663138, -0.279415498198926,
            0.656986598718789, 0.989358246623382, 0.41211848524175704
        ]
    )
    assert (result == expected).all()


def test_natural_cubic_spline():
    pass


def test_random_data():
    pass


def test_datetime_data():
    pass


def test_timedelta_data():
    pass


def test_two_sample_t():
    result = ds.two_sample_t(
        df=df_two_sample_t,
        xlabel="X",
        ylabel="y",
        alternative_hypothesis="unequal",
        significance_level=0.05
    )
    expected = (2.206697123558633, 0.040563312956175504)
    assert result == expected

def test_linear_regression():
    pass
