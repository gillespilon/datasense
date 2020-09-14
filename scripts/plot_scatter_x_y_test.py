#! /usr/bin/env python3
'''
Test def plot_scatter_x_y() of graphs.py

time -f '%e' ./plot_scatter_x_y_test.py
./plot_scatter_x_y_test.py
'''

import datasense as ds


def main():
    df = ds.read_file(
        filename='norfolk.csv',
        abscissa='LAB_BOARD_DAT_COD',
        datetimeparser='%d%b%Y:%H:%M:%S'
    )
#     df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_scatter_x_y(
        df['LAB_BOARD_DAT_COD'],
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_x_y_datex_test.svg', format='svg')
    fig, ax = ds.plot_scatter_x_y(
        df['BOARD_MIXER_MANIFOLD_PRESS'],
        df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_x_y_floatx_test.svg', format='svg')


if __name__ == '__main__':
    main()
