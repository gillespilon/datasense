#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import X


chart_data = pd.read_csv(Path(__file__).parent / '../control_charts/xmr.csv',
                         index_col='Time') \
               .iloc[:, 0:]
x = X(chart_data)
print('X chart')
print('Upper control limit', x.ucl, sep=' = ')
print('Average moving range', x.mean, sep=' = ')
print('Lower control limit', x.lcl, sep=' = ')
print(f'Sigma(X)', x.sigma, sep=' = ')
print('-3 Sigma, -2 Sigma, … + 3 Sigma',
        ', '.join(map(str, [x.sigmas[i] for i in range(-3, 4)])),
        sep=' = ')
x.ax.set_title('X')
plt.show()
plt.clf()
