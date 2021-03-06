#! /usr/bin/env python3
'''
Test def plot_pareto() of graphs.py

time -f '%e' ./plot_pareto.py
./plot_pareto.py
'''

import datasense as ds
import pandas as pd

output_url = 'plot_pareto.html'
header_title = 'plot_pareto'
header_id = 'plot-pareto'


def main():
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print(help(ds.plot_pareto))
    # Example 1
    data = pd.DataFrame(
        {
            'ordinate': ['Mo', 'Larry', 'Curly', 'Shemp', 'Joe'],
            'abscissa': [21, 2, 10, 4, 16]
        }
    )
    fig, ax1, ax2 = ds.plot_pareto(
        X=data['ordinate'],
        y=data['abscissa']
    )
    fig.savefig(
        fname='pareto.svg',
        format='svg'
    )
    ds.html_figure(file_name='pareto.svg')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
