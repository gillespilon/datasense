import datasense as ds
import pandas as pd


from pytest import approx, mark


X = pd.Series(
    data=[
        25.0, 24.0, 35.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0, 16.0,
        16.0, 16.0
    ]
)
data = {
    "abscissa": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "ordinate": [
        0, 0.841470984807896, 0.909297426825682, 0.141120008059867,
        -0.756802495307928, -0.958924274663138, -0.279415498198926,
        0.656986598718789, 0.989358246623382, 0.412118485241757
    ]
}
df = pd.DataFrame(data=data)

# test for method 8
def test_nonparametric_summary():
    series=ds.nonparametric_summary(series=X)
    assert series[0] == -15.4
    assert series[1] == -0.85
    assert series[2] == 13.7
    assert series[3] == 16.0
    assert series[4] == (11.776235355842992, 20.223764644157008)
    assert series[5] == 23.4
    assert series[6] == 37.95
    assert series[7] == 52.5
    assert series[8] == 9.7
    assert series[9] == []
    assert series[10] == []
    assert series[11] == 10.0
    assert series[12] == 35.5
    assert series[13] == 13


def test_parametric_summary():
    series = ds.parametric_summary(series=X)
    assert series[0] == 13
    assert series[1] == 10.0
    assert series[2] == 35.5
    assert series[3] == 18.392
    assert series[4] == (14.012638095621575, 22.77197728899381)
    assert series[5] == 7.248
    assert series[6] == 52.527

def test_cubic_spline():
    cubic_spline = ds.cubic_spline(
        df=df,
        abscissa="abscissa",
        ordinate="ordinate"
    )
    result = cubic_spline(x=df["abscissa"])
    expected = (
        [
            0., 0.841470984807896, 0.909297426825682, 0.141120008059867,
            -0.756802495307928, -0.958924274663138, -0.279415498198926,
            0.656986598718789, 0.989358246623382, 0.41211848524175704]
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
    pass


def test_linear_regression():
    pass
