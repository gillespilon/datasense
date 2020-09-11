#! /usr/bin/env python3

'''
Test def plot_scatter_y() of graphs.py

time -f '%e' ./plot_scatter_y_test.py
./plot_scatter_y_test.py
'''

import datasense as ds


def main():
    df = ds.read_file(
        filename='norfolk.csv',
        abscissa='LAB_BOARD_DAT_COD',
        datetimeparser='%d%b%Y:%H:%M:%S'
    )
    df = df.iloc[601:700, :]
    print(df.head())
    print(df.dtypes)
    fig, ax = ds.plot_scatter_y(
        y=df['BOARD_MIXER_KW'],
        figuresize=(8, 6),
        marker='1',
        markersize=4,
        colour='#ee7733'
    )
    fig.savefig('plot_scatter_y_test.svg')


if __name__ == '__main__':
    main()
