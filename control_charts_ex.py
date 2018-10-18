#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import X
from datasense import mR

chart_data = pd.read_csv(Path(__file__).parent / '../control_charts/xmr.csv',
                         index_col='Sample') \
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
#plt.clf()
mr = mR(chart_data)
print('mR chart')
print('Upper control limit', mr.ucl, sep=' = ')
print('Average moving range', mr.mean, sep=' = ')
print('Lower control limit', mr.lcl, sep=' = ')
print(f'Sigma(X)', mr.sigma, sep=' = ')
print('-3 Sigma, -2 Sigma, … + 3 Sigma',
        ', '.join(map(str, [mr.sigmas[i] for i in range(-3, 4)])),
        sep=' = ')
mr.ax.set_title('mR')
plt.show()
#plt.clf()
