import warnings

from pandas.testing import assert_series_equal
import datasense as ds
import pandas as pd
import numpy as np


warnings.filterwarnings("ignore")
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
df_linear_regression = pd.DataFrame(
    data={
        "X": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y": [
            8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68
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
    assert result.equals(other=expected)


def test_parametric_summary():
    result = ds.parametric_summary(series=X)
    expected = pd.Series(
        data={
            "n": 13, "min": 10.0, "max": 35.5, "ave": 18.392,
            "confidence interval": (14.012638095621575, 22.77197728899381),
            "s": 7.248, "var": 52.527
        }
    )
    assert result.equals(other=expected)


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
            0.656986598718789, 0.989358246623382, 0.41211848524175704
        ]
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
    pipeline = ds.natural_cubic_spline(
        X=df_linear_regression["X"],
        y=df_linear_regression["y"],
        number_knots=10
    )
    X = ds.random_data(
        size=13,
        random_state=41
    )
    out = pipeline.predict(X=X)
    result = pd.Series(data=out)
    exp = np.array(
        object=[
            -8.449635833832208, -7.369397489580049, -6.950373342494703,
            -10.332163099070616, -6.0396793560020665, -10.66288509157907,
            -8.112999744210992, -5.399095580784705, -11.197986327827774,
            -10.397763790060722, -9.309492784412193, -10.481589542995772,
            -9.887572653190901
        ]
    )
    expected = pd.Series(data=exp)
    assert result.equals(other=expected)


def test_random_data():
    result = ds.random_data(
        size=13,
        random_state=41
    )
    expected = pd.Series(
        data=[
            -0.2707123230673205, 0.10484805260974006, 0.25052781572357197,
            -0.9251999652780767, 0.567143660285906, -1.040180216082938,
            -0.15367595145793744, 0.7898518103468191, -1.2262158464418542,
            -0.9480069877134585, -0.5696539419300647, -0.9771502146977724,
            -0.7706317111835508
        ]
    )
    assert result.equals(other=expected)


def test_datetime_data():
    result = ds.datetime_data(
        start_year="2020",
        start_month="01",
        start_day="01",
        start_hour="00",
        start_minute="00",
        start_second="00",
        end_year="2020",
        end_month="01",
        end_day="01",
        end_hour="07",
        end_minute="00",
        end_second="00",
        time_delta_days=7,
        time_delta_hours=1
    )
    expected = pd.Series(
        data=[
            "2020-01-01 00:00:00", "2020-01-01 01:00:00",
            "2020-01-01 02:00:00", "2020-01-01 03:00:00",
            "2020-01-01 04:00:00", "2020-01-01 05:00:00",
            "2020-01-01 06:00:00"
        ]
    ).astype(dtype="datetime64[s]")
    assert result.equals(other=expected)


def test_timedelta_data():
    result = ds.timedelta_data(time_delta_days=7)
    expected = pd.Series(
        data=[0, 0, 0, 0, 0, 0, 0, 0]
    ).astype(dtype="timedelta64[s]")
    assert result.equals(other=expected)


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
    result = ds.two_sample_t(
        df=df_two_sample_t,
        xlabel="X",
        ylabel="y",
        alternative_hypothesis="less than",
        significance_level=0.05
    )
    expected = (2.206697123558633, 0.9797183435219122)
    assert result == expected
    result = ds.two_sample_t(
        df=df_two_sample_t,
        xlabel="X",
        ylabel="y",
        alternative_hypothesis="greater than",
        significance_level=0.05
    )
    expected = (2.206697123558633, 0.020281656478087752)
    assert result == expected


def test_linear_regression():
    result, fitted_model = ds.linear_regression(
        df=df_linear_regression,
        x_column=["X"],
        y_column="y",
        prediction_column="mean"
    )
    expected = pd.DataFrame(
        data={
            "mean": [
                5.000454545454545, 5.500545454545454, 6.000636363636364,
                6.500727272727273, 7.000818181818182, 7.500909090909091,
                8.001, 8.501090909090909, 9.001181818181818,
                9.501272727272728, 10.001363636363635
            ],
            "mean_se": [
                0.6975383483900705, 0.6012024482970638, 0.5139381619839436,
                0.44116198724493344, 0.3910483061947432, 0.3728499305445431,
                0.3910483061947433, 0.4411619872449333, 0.5139381619839437,
                0.6012024482970639, 0.6975383483900705
            ],
            "mean_ci_lower": [
                3.4225131743574257, 4.140531029872831, 4.838027469298446,
                5.502749523352097, 6.116205454982011, 6.657463949900272,
                7.116387273163829, 7.503113159715733, 7.8385729238439,
                8.141258302600104, 8.423422265266517
            ],
            "mean_ci_upper": [
                6.578395916551664, 6.860559879218078, 7.163245257974282,
                7.498705022102449, 7.885430908654352, 8.34435423191791,
                8.88561272683617, 9.499068658466085, 10.163790712519736,
                10.861287151945351, 11.579305007460754
            ],
            "obs_ci_lower": [
                1.7887111348712654, 2.3900734646180624, 2.97127071947934,
                3.5306504466075843, 4.066889682129447, 4.579129415660348,
                5.067071500311265, 5.53101408297122, 5.971816174024794,
                6.3908007373453355, 6.7896202257803555
            ],
            "obs_ci_upper": [
                8.212197956037825, 8.611017444472846, 9.030002007793387,
                9.470804098846962, 9.934746681506915, 10.422688766157833,
                10.934928499688734, 11.471167735210598, 12.030547462338841,
                12.61174471720012, 13.213107046946915
            ],
            "X": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "y": [
                4.26, 5.68, 7.24, 4.82, 6.95, 8.81, 8.04, 8.33, 10.84, 7.58,
                9.96
            ]
        },
        index=[7, 10, 6, 9, 1, 3, 0, 4, 8, 2, 5]
    )
    assert result.equals(other=expected)
