import warnings

from pandas.testing import assert_series_equal
from pytest import approx
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
series1_two_sample_t = pd.Series(
    data=[32, 37, 35, 28, 41, 44, 35, 31, 34, 38, 42],
    name="y1"
)
series2_two_sample_t = pd.Series(
    data=[36, 31, 30, 31, 34, 36, 29, 32, 31],
    name="y2"
)
series_one_sample_t = pd.Series(
    data=[
        211, 572, 558, 250, 478, 307, 184, 435, 460, 308, 188, 111, 676, 326,
        142, 255, 205, 77, 190, 320, 407, 333, 488, 374, 409
    ]
)
df_linear_regression = pd.DataFrame(
    data={
        "X": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y": [
            8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68
        ]
    }
)
series1_paired = pd.Series(
    data=[
        68, 76, 74, 71, 71, 72, 75, 83, 75, 74, 76, 77, 78, 75, 75, 84, 77,
        69, 75, 65
    ],
    name="before"
)
series2_paired = pd.Series(
    data=[
        67, 77, 74, 74, 69, 70, 71, 77, 71, 74, 73, 68, 71, 72, 77, 80, 74,
        73, 72, 62
    ],
    name="after"
)


def test_nonparametric_summary():
    """
    Test for method 8
    """
    result = ds.nonparametric_summary(
        series=X,
        alphap=1/3,
        betap=1/3,
        decimals=3
    )
    expected = pd.Series(
        data={
            "lower outer fence": -15.4, "lower inner fence": -0.85,
            "lower quartile": 13.7, "median": 16.0,
            "confidence interval": (11.776, 20.224),
            "upper quartile": 23.4,
            "upper inner fence": 37.95, "upper outer fence": 52.5,
            "interquartile range": 9.7,
            "inner outliers": [], "outer outliers": [],
            "minimum value": 10.0, "maximum value": 35.5, "count": 13
        }
    )
    assert result.equals(other=expected)


def test_parametric_summary():
    result = ds.parametric_summary(
        series=X,
        decimals=3
    )
    expected = pd.Series(
        data={
            "n": 13, "min": 10.0, "max": 35.5, "ave": 18.392,
            "confidence interval": (14.013, 22.772),
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
            -8.449635833832144, -7.369397489579985, -6.950373342494639,
            -10.332163099070552, -6.039679356002003, -10.662885091579007,
            -8.112999744210928, -5.399095580784641, -11.197986327827710,
            -10.397763790060658, -9.309492784412129, -10.481589542995708,
            -9.887572653190837
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


def test_one_sample_t():
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="two-sided"
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic, Shapiro-Wilk p value,
    # Anderson-Darling statistic, Anderson-Darling critical value for
    # alpha 0.05,
    # Kolmogorov-Smirnov statistic, Kolmogorov-Smirnov p value,
    # hypothesis test CI lower bound, hypothesis test CI upper bound
    # )
    expected = (
        -2.2519472501384548, 0.0337482297588424, 0.5798034164658731,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        266.9185820624180678, 394.2014179375819367
    )
    assert result == expected
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="less"
    )
    expected = (
        -2.2519472501384548, 0.0168741148794212, 6.257488453140399e-05,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        "N/A", 383.3159655856088079
    )
    assert result == expected
    result = ds.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=400,
        alternative_hypothesis="greater"
    )
    expected = (
        -2.2519472501384548, 0.9831258851205789, 0.7063989742605766,
        0.9746975302696228, 0.7642895579338074,
        0.2270875306568172, 0.7030000000000000,
        0.1009686916604779, 0.7255204234760189,
        277.8040344143911966, "N/A"
    )
    assert result == expected


def test_two_sample_t():
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="two-sided",
        significance_level=0.05,
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic sample 1, Shapiro-Wilk p value sample 1,
    # Shapiro-Wilk statistic sample 2, Shapiro-Wilk p value sample 2,
    # Bartlett test statistic, Bartlett p value,
    # Anderson-Darling test statistic, Anderson-Darling p value`
    # )
    expected = (
        2.1353336482435243, 0.0467302735601054, 0.5243039932709265,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755

    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="less",
        significance_level=0.05,
    )
    expected = (
        2.1353336482435243, 0.9766348632199473, 0.00010611922933969828,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755
    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="greater",
        significance_level=0.05,
    )
    expected = (
        2.1353336482435243, 0.0233651367800527, 0.6587984489683615,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755
    )
    assert result == expected


def test_paired_t():
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="two-sided",
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic, Shapiro-Wilk p value,
    # Anderson-Darling test statistic, Anderson-Darling p value
    # )
    expected = (
        3.0234339882840073, 0.006989193823492975,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
    assert result == expected
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="less"
    )
    expected = (
        3.0234339882840073, 0.9965054030882535,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
    assert result == expected
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="greater"
    )
    expected = (
        3.0234339882840073, 0.0034945969117464873,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
    assert result == expected
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="two-sided",
        hypothesized_value=4
    )
    expected = (
        -2.4737187176869146, 0.022976718604245508,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
    assert result == expected
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="less",
        hypothesized_value=4
    )
    expected = (
        -2.4737187176869146, 0.011488359302122775,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
    assert result == expected
    result = ds.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="greater",
        hypothesized_value=4
    )
    expected = (
        -2.4737187176869146, 0.9885116406978772,
        0.9718567132949829, 0.7935113906860352,
        0.33171651643374744, 0.692,
        0.14709700945048904, 0.3071349516596349
    )
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
