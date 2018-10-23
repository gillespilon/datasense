#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import Xbar, R

chart_data = pd.read_csv(Path(__file__).parent / 'xbarr.csv',
                         index_col='Sample').iloc[:, 0:]
xbar = Xbar(chart_data)
print('Xbar chart')
print('Upper control limit', xbar.ucl, sep=' = ')
print('Average moving range', xbar.mean, sep=' = ')
print('Lower control limit', xbar.lcl, sep=' = ')
print(f'Sigma(Xbar)', xbar.sigma, sep=' = ')
for i in range(-3, 4):
    print(f'{i} Sigma', ' '.join(map(str, [xbar.sigmas[i]])), sep=' = ')
ax1 = xbar.ax
ax1.set_title('Xbar control chart' + '\n' 'Subtitle')
ax1.set_ylabel('Response (units)')
ax1.set_xlabel('X axis label')
ax1.figure.savefig('xbar.svg', format='svg') # Comment if you wish interactive
# plt.show() # Uncomment if you wish interactive
plt.clf() # Comment if you wish interactive
r = R(chart_data)
print('R chart')
print('Upper control limit', r.ucl, sep=' = ')
print('Average moving range', r.mean, sep=' = ')
print('Lower control limit', r.lcl, sep=' = ')
print(f'Sigma(X)', r.sigma, sep=' = ')
for i in range(-3, 4):
    print(f'{i} Sigma', ' '.join(map(str, [r.sigmas[i]])), sep=' = ')
ax2 = r.ax
ax2.set_title('R control chart' + '\n' 'Subtitle')
ax2.set_ylabel('Response (units)')
ax2.set_xlabel('X axis label')
ax2.figure.savefig('r.svg', format='svg') # Comment if you wish interactive
# plt.show() # Uncomment if you wish interactive
plt.clf() # Comment if you wish interactive
