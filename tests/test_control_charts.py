from pathlib import Path
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd

import datasense.control_charts as cc

from pytest import approx, mark


minitab_control = {
    ('x1', cc.X): {
        'sigma': 9.325113791639287,
        'ucl': 95.85564364650628,
        '+2sigma': 86.530529854867,
        '+1sigma': 77.2054160632277,
        'average': 67.88030227158842,
        '-1sigma': 58.55518847994913,
        '-2sigma': 49.23007468830984,
        'lcl': 39.90496089667056,
        # Average monthly cost = 169.70075567897103,
    },
    ('x1', cc.mR): {
        'sigma': 7.949659507372493,
        'ucl': 34.36770687908659,
        'average': 10.518728356969115,
        'lcl': 0.0,
    },
    ('x2', cc.X): {
        'sigma': 13.864253851131181,
        'ucl': 107.61839889153828,
        '+2sigma': 93.7541450404071,
        '+1sigma': 79.88989118927591,
        'average': 66.02563733814473,
        '-1sigma': 52.16138348701355,
        '-2sigma': 38.29712963588237,
        'lcl': 24.43287578475119,
        # Average monthly cost = 165.06409334536184,
    },
    ('x2', cc.mR): {
        'sigma': 11.819276408089333,
        'ucl': 51.096707568343966,
        'average': 15.638878344075971,
        'lcl': 0.0,
    },
    ('x3', cc.X): {
        'sigma': 13.636505245640144,
        'ucl': 112.77967930102798,
        '+2sigma': 99.14317405538785,
        '+1sigma': 85.50666880974771,
        'average': 71.87016356410756,
        '-1sigma': 58.23365831846741,
        '-2sigma': 44.59715307282727,
        'lcl': 30.960647827187124,
        # Average monthly cost = 179.6754089102689
    },
    ('x3', cc.mR): {
        'sigma': 11.625120721908223,
        'ucl': 50.25734008280675,
        'average': 15.38197791708208,
        'lcl': 0.0,
    },
    ('x4', cc.X): {
        'sigma': 12.376383658874893,
        'ucl': 103.14887306784789,
        '+2sigma': 90.772489408973,
        '+1sigma': 78.39610575009812,
        'average': 66.01972209122322,
        '-1sigma': 53.64333843234832,
        '-2sigma': 41.26695477347343,
        'lcl': 28.890571114598536,
        # Average monthly cost = 165.04930522805802
    },
    ('x4', cc.mR): {
        'sigma': 10.550867069190847,
        'ucl': 45.613161974783424,
        'average': 13.960560767210879,
        'lcl': 0.0,
    },
    ('x5', cc.X): {
        'sigma': 10.775989887807455,
        'ucl': 100.12743417820478,
        '+2sigma': 89.35144429039732,
        '+1sigma': 78.57545440258987,
        'average': 67.79946451478241,
        '-1sigma': 57.02347462697496,
        '-2sigma': 46.247484739167504,
        'lcl': 35.47149485136005,
        # Average monthly cost = 169.49866128695606
    },
    ('x5', cc.mR): {
        'sigma': 9.186531379355856,
        'ucl': 39.71491073151437,
        'average': 12.155316593446807,
        'lcl': 0.0,
    },
    ('x6', cc.X): {
        'sigma': 11.783722981682951,
        'ucl': 103.92297722960447,
        '+2sigma': 92.13925424792151,
        '+1sigma': 80.35553126623857,
        'average': 68.57180828455562,
        '-1sigma': 56.788085302872666,
        '-2sigma': 45.00436232118972,
        'lcl': 33.22063933950676,
        # Average monthly cost = 171.42952071138905
    },
    ('x6', cc.mR): {
        'sigma': 10.045623841884716,
        'ucl': 43.42891104899252,
        'average': 13.292039523338367,
        'lcl': 0.0,
    },
    ('x7', cc.X): {
        'sigma': 8.687102117162302,
        'ucl': 98.46106296174796,
        '+2sigma': 89.77396084458566,
        '+1sigma': 81.08685872742335,
        'average': 72.39975661026105,
        '-1sigma': 63.712654493098746,
        '-2sigma': 55.02555237593644,
        'lcl': 46.338450258774145,
        # Average monthly cost = 180.99939152565264
    },
    ('x7', cc.mR): {
        'sigma': 7.405754554880864,
        'ucl': 32.01631485280167,
        'average': 9.799051188159076,
        'lcl': 0.0,
    },
    ('x8', cc.X): {
        'sigma': 11.05402122034085,
        'ucl': 105.16427868737352,
        '+2sigma': 94.11025746703268,
        '+1sigma': 83.05623624669184,
        'average': 72.00221502635098,
        '-1sigma': 60.94819380601013,
        '-2sigma': 49.89417258566928,
        'lcl': 38.84015136532843,
        # Average monthly cost = 180.00553756587743
    },
    ('x8', cc.mR): {
        'sigma': 9.423553090340574,
        'ucl': 40.7395952075662,
        'average': 12.468935936544478,
        'lcl': 0.0,
    },
    ('x9', cc.X): {
        'sigma': 16.287717967060136,
        'ucl': 118.56904305834183,
        '+2sigma': 102.2813250912817,
        '+1sigma': 85.99360712422155,
        'average': 69.70588915716142,
        '-1sigma': 53.41817119010129,
        '-2sigma': 37.13045322304115,
        'lcl': 20.84273525598101,
        # Average monthly cost = 174.26472289290356
    },
    ('x9', cc.mR): {
        'sigma': 13.885279566918767,
        'ucl': 60.02838456760013,
        'average': 18.372545866843833,
        'lcl': 0.0,
    },
    ('x10', cc.X): {
        'sigma': 13.545500118962176,
        'ucl': 107.08955918260395,
        '+2sigma': 93.54405906364177,
        '+1sigma': 79.9985589446796,
        'average': 66.45305882571742,
        '-1sigma': 52.907558706755246,
        '-2sigma': 39.36205858779307,
        'lcl': 25.81655846883089,
        # Average monthly cost = 166.13264706429356
    },
    ('x10', cc.mR): {
        'sigma': 11.547538851415256,
        'ucl': 49.9219406884351,
        'average': 15.279324134189332,
        'lcl': 0.0,
    },
    ('x11', cc.X): {
        'sigma': 15.602231235682453,
        'ucl': 112.2459670130288,
        '+2sigma': 96.64373577734635,
        '+1sigma': 81.0415045416639,
        'average': 65.43927330598144,
        '-1sigma': 49.83704207029899,
        '-2sigma': 34.23481083461654,
        'lcl': 18.632579598934086,
        # Average monthly cost = 163.5981832649536
    },
    ('x11', cc.mR): {
        'sigma': 13.300902128419292,
        'ucl': 57.50202321910768,
        'average': 17.599316833849805,
        'lcl': 0.0,
    },
    ('x12', cc.X): {
        'sigma': 16.62870745902259,
        'ucl': 118.30040994890352,
        '+2sigma': 101.67170248988094,
        '+1sigma': 85.04299503085835,
        'average': 68.41428757183576,
        '-1sigma': 51.785580112813165,
        '-2sigma': 35.15687265379058,
        'lcl': 18.528165194767993,
        # Average monthly cost = 171.0357189295894
    },
    ('x12', cc.mR): {
        'sigma': 14.175973108816757,
        'ucl': 61.285101340227754,
        'average': 18.757182013777477,
        'lcl': 0.0,
    },
    (('x1', 'x4'), cc.Xbar): {
        'ucl': 88.87038521594829,
        'average': 67.94895631626599,
        'lcl': 47.027527416583695,
        'sigma': 6.973809633227431,
    },
    (('x1', 'x4'), cc.R): {
        'ucl': 65.531,
        'average': 28.718148069630562,
        'lcl': 0.0,
        'sigma': 12.271115430626988,
    },
    (('x5', 'x8'), cc.Xbar): {
        'ucl': 88.02663933927276,
        'average': 70.19331110898753,
        'lcl': 52.3599828787023,
        'sigma': 5.944442743428413,
    },
    (('x5', 'x8'), cc.R): {
        'ucl': 55.859,
        'average': 24.479215217438206,
        'lcl': 0.0,
        'sigma': 10.459841451336636,
    },
    (('x9', 'x12'), cc.Xbar): {
        'ucl': 88.1384161998066,
        'average': 67.50312721517402,
        'lcl': 46.86783823054144,
        'sigma': 6.878429661544193,
    },
    (('x9', 'x12'), cc.R): {
        'ucl': 64.635,
        'average': 28.32537334623899,
        'lcl': 0.0,
        'sigma': 12.103284832453163,
    },
}

test_25_12_csv = pd.read_csv(Path(__file__).with_name('test_25_12.csv'),
                             index_col='sample')


@mark.parametrize('column,expected',
                  [(name, values)
                   for (name, constructor), values
                   in minitab_control.items()
                   if constructor is cc.X])
@mark.parametrize('subgroup_size', [None, 2])
def test_X(column, expected, subgroup_size):
    X = cc.X(test_25_12_csv[[column]], subgroup_size=subgroup_size)
    assert X.sigma == approx(expected['sigma'])
    assert X.ucl == approx(expected['ucl'])
    assert X.sigmas[+2] == approx(expected['+2sigma'])
    assert X.sigmas[+1] == approx(expected['+1sigma'])
    assert X.mean == approx(expected['average'])
    assert X.sigmas[-1] == approx(expected['-1sigma'])
    assert X.sigmas[-2] == approx(expected['-2sigma'])
    assert X.lcl == approx(expected['lcl'])
    return  # below part broken
    fig = BytesIO()
    # TODO: fix more rendering parameters so as to be less affected by
    # environment, such as matplotlib defaults in config file, etc.
    try:
        X.ax().figure.savefig(fig, format='png')
        fig.seek(0)
        same = fig.read() == (
            Path(__file__).parent
                          .joinpath('prerenders', f'{column}-X.png')
                          .read_bytes()
        )
        assert same, 'Plots not the same; save/compare manually with debugger'
    finally:
        plt.clf()
        plt.close('all')


@mark.parametrize('column,expected',
                  [(name, values)
                   for (name, constructor), values
                   in minitab_control.items()
                   if constructor is cc.mR])
@mark.parametrize('subgroup_size', [None, 2])
def test_mR(column, expected, subgroup_size):
    mR = cc.mR(test_25_12_csv[[column]], subgroup_size=subgroup_size)
    assert mR.sigma == approx(expected['sigma'])
    assert mR.ucl == approx(expected['ucl'])
    assert mR.mean == approx(expected['average'])
    assert mR.lcl == approx(expected['lcl'])
    return  # below part broken
    fig = BytesIO()
    try:
        mR.ax().figure.savefig(fig, format='png')
        fig.seek(0)
        same = fig.read() == (
            Path(__file__).parent
                          .joinpath('prerenders', f'{column}-mR.png')
                          .read_bytes()
        )
        assert same, 'Plots not the same; save/compare manually with debugger'
    finally:
        plt.clf()
        plt.close('all')


@mark.parametrize('columns,expected',
                  [(slice(*columns), values)
                   for (columns, constructor), values
                   in minitab_control.items()
                   if constructor is cc.Xbar])
def test_Xbar(columns, expected):
    xbar = cc.Xbar(test_25_12_csv.loc[:, columns])
    assert xbar.ucl == approx(expected['ucl'])
    assert xbar.mean == approx(expected['average'])
    assert xbar.lcl == approx(expected['lcl'])
    assert xbar.sigma == approx(expected['sigma'])
    return  # below part broken
    fig = BytesIO()
    try:
        xbar.ax().figure.savefig(fig, format='png')
        fig.seek(0)
        # Workaround for slow pytest. Hangs here if not the same.
        same = fig.read() == (
            Path(__file__).parent
                          .joinpath('prerenders',
                                    f'{columns.start}-{columns.stop}-Xbar.png')
                          .read_bytes()
        )
        assert same, 'Plots not the same; save/compare manually with debugger'
    finally:
        plt.clf()
        plt.close('all')


@mark.parametrize('columns,expected',
                  [(slice(*columns), values)
                   for (columns, constructor), values
                   in minitab_control.items()
                   if constructor is cc.R])
def test_R(columns, expected):
    R = cc.R(test_25_12_csv.loc[:, columns])
    assert R.ucl == approx(expected['ucl'], rel=1e-4)
    assert R.mean == approx(expected['average'])
    assert R.lcl == approx(expected['lcl'])
    assert R.sigma == approx(expected['sigma'])
    return  # below part broken
    fig = BytesIO()
    try:
        R.ax().figure.savefig(fig, format='png')
        fig.seek(0)
        same = fig.read() == (
            Path(__file__).parent
                          .joinpath('prerenders',
                                    f'{columns.start}-{columns.stop}-R.png')
                          .read_bytes()
        )
        assert same, 'Plots not the same; save/compare manually with debugger'
    finally:
        plt.clf()
        plt.close('all')


def test_nwise():
    assert list(cc._nwise([1,2,3,4], 0)) == []
    assert list(cc._nwise([1,2,3,4], 1)) == [(1,), (2,), (3,), (4,)]
    assert list(cc._nwise([1,2,3,4], 2)) == [(1,2), (2,3), (3,4)]
    assert list(cc._nwise([1,2,3,4,5], 3)) == [(1,2,3), (2,3,4), (3,4,5)]
    assert list(cc._nwise([1,2,3,4,5], 5)) == [(1,2,3,4,5)]
