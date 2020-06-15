#! /usr/bin/env python3


'''
A piecewise natural cubic spline (cubic curves in the interior segments, linear
in the exterior segments) is used to interpolate points to fit the data while
smoothing out the noise. A large number of data are fitted with low-degree
polynomials, to eliminate excessive oscillations and non-convergence.

References

[Drury, Matthew. Basis Expansions](https://github.com/madrury/basis-expansions)

[Leal, Lois Anne. Numerical Interpolation: Natural Cubic Spline]
(https://towardsdatascience.com/numerical-interpolation-natural-cubic-spline
-52c1157b98ac)

[SAS/GRAPH SYMBOL Statement (INTERPOL=SM&lt;nn&gt;&lt;P&gt;&lt;S&gt;)]
(https://documentation.sas.com/?docsetId=graphref&docsetTarget=n0c0j84n1e2jz9n
1bhkn41o3v0d6.htm&docsetVersion=9.4&locale=en#p115cutvcmx2dln1cdo96duwmxru)

[Wikipedia. Smoothing spline](https://en.wikipedia.org/wiki/Smoothing_spline)

[Wikipedia. Spline (mathematics)]
(https://en.wikipedia.org/wiki/Spline_(mathematics))

time -f '%e' ./piecewise_natural_cubic_spline.py
./piecewise_natural_cubic_spline.py

The graphs can be viewed with the view_spline_graphs.html file created.
'''


from multiprocessing import Pool
from pathlib import Path
from shutil import rmtree
from typing import Tuple
import itertools
import sys
import datasense as ds
import matplotlib.axes as axes
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd


# Data set must not contain NaN, inf, or -inf
parameters = pd.read_excel(
    'piecewise_natural_cubic_spline_parameters.csv',
    index_col=False
)
file_names = [x for x in parameters['File names']
              if str(x) != 'nan']
targets = [x for x in parameters['Targets']
           if str(x) != 'nan']
features = [x for x in parameters['Features']
            if str(x) != 'nan']
num_knots = [int(x) for x in parameters['Number of knots']
             if str(x) != 'nan']
graphics_directory = 'piecewise_natural_cubic_spline_graphs'
figure_width_height = (9, 5)
x_axis_label = 'Abscissa'
y_axis_label = 'Ordinate'
axis_title = 'Piecewise natural cubic spline'
c = cm.Paired.colors


def main():
    set_up_graphics_directory(graphics_directory)
    original_stdout = sys.stdout
    sys.stdout = open('view_spline_graphs.html', 'w')
    html_header()
    for file, target, feature in itertools.product(
        file_names, targets, features
    ):
        data = pd.read_csv(file)
        x = data[feature]
        y = data[target]
        min_val = min(x)
        max_val = max(x)
        t = ((x, y, min_val, max_val, file, target, feature, knot)
             for knot in num_knots)
        with Pool() as pool:
            for _ in pool.imap_unordered(plot_scatter_line, t):
                pass
        for knot in num_knots:
            print(
                f'<p><img src="{graphics_directory}/'
                f'spline_{file.strip(".csv")}_'
                f'{target}_{feature}_{knot}.svg"/></p>'
            )
    html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout


def set_up_graphics_directory(graphdir: str) -> None:
    '''
    Create an empty directory
    '''
    try:
        rmtree(graphdir)
    except Exception:
        pass
    Path(graphdir).mkdir(parents=True, exist_ok=True)


def html_header():
    print('<!DOCTYPE html>')
    print('<html lang="" xml:lang="" xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta charset="utf-8"/>')
    print(
        '<meta content="width=device-width, initial-scale=1.0, '
        'user-scalable=yes" name="viewport"/>'
    )
    print('<title>Piecewise natural cubic spline graphs</title>')
    print('</head>')
    print('<body>')
    print(
        '<h1 class="title"'
        ' id="piecewise-natural-cubic-spline-graphs">'
        'Piecewise natural cubic spline graphs</h1>'
    )


def html_footer():
    print('</body>')
    print('</html>')


def plot_scatter_line(t: Tuple[str, str]) -> None:
    x, y, min_val, max_val, file, target, feature, numknots = t
    model = ds.natural_cubic_spline(
        x, y, min_val, max_val, numberknots=numknots
    )
    fig = plt.figure(figsize=figure_width_height)
    ax = fig.add_subplot(111)
    ax.plot(x, y, ls='', marker='.', color=c[1], alpha=0.20)
    ax.plot(
        x, model.predict(x), marker='', color=c[5],
        label=f'number knots = {numknots}'
    )
    ax.legend(frameon=False, loc='best')
    ax.set_title(
        f'{axis_title}\n'
        f'file: {file} '
        f'column: {target}'
    )
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    despine(ax)
    ax.figure.savefig(
        f'{graphics_directory}'
        f'/spline_'
        f'{file.strip(".csv")}_'
        f'{target}_{feature}_'
        f'{numknots}.svg',
        format='svg'
    )


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.

    There is only one x axis, on the bottom, and one y axis, on the left.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


if __name__ == '__main__':
    main()
