#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import X, mR

chart_data = pd.read_csv(Path(__file__).parent / 'xmr.csv',
                         index_col='Sample').iloc[:, 0:]
x = X(chart_data)
print('X chart')
print('Upper control limit', x.ucl, sep=' = ')
print('Average moving range', x.mean, sep=' = ')
print('Lower control limit', x.lcl, sep=' = ')
print(f'Sigma(X)', x.sigma, sep=' = ')
for i in range(-3, 4):
    print(f'{i} Sigma', ' '.join(map(str, [x.sigmas[i]])), sep=' = ')
ax1 = x.ax
ax1.set_title('X control chart' + '\n' 'Subtitle')
ax1.set_ylabel('Response (units)')
ax1.set_xlabel('X axis label')
plt.show()
#plt.clf()
mr = mR(chart_data)
print('mR chart')
print('Upper control limit', mr.ucl, sep=' = ')
print('Average moving range', mr.mean, sep=' = ')
print('Lower control limit', mr.lcl, sep=' = ')
print(f'Sigma(X)', mr.sigma, sep=' = ')
for i in range(-3, 4):
    print(f'{i} Sigma', ' '.join(map(str, [mr.sigmas[i]])), sep=' = ')
ax2 = mr.ax
ax2.set_title('mR control chart' + '\n' 'Subtitle')
ax2.set_ylabel('Response (units)')
ax2.set_xlabel('X axis label')
plt.show()
#plt.clf()
