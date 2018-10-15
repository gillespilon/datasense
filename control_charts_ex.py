#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import ProcessBehaviourCharts


chart_data = pd.read_csv(Path(__file__).with_name('xbarr.csv'),
                         index_col='Sample')
pbc = ProcessBehaviourCharts(chart_data)
for f, title in [(pbc.R_chart, 'R chart'),
                 (pbc.Xbar_chart, 'Xbar chart')]:
    cc = f()
    print(title)
    print('Upper control limit', cc.ucl, sep=' = ')
    print('Average moving range', cc.mean, sep=' = ')
    print('Lower control limit', cc.lcl, sep=' = ')
    print(f'Sigma({title})', cc.sigma, sep=' = ')
    print('-3 Sigma, -2 Sigma, … + 3 Sigma',
          ', '.join(map(str, [cc.sigmas[i] for i in range(-3, 4)])),
          sep=' = ')
    plt.show()
    plt.clf()
    input('Press <Enter> to continue ')
    print()
    print(80 * '-')
    print()
