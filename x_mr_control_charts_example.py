#! /usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from datasense import X, mR

chart_data = pd.read_csv(Path(__file__).parent / 'xmr.csv',
                         index_col='Sample').iloc[:, 0:]
x = X(chart_data) # This default method works for subgroup of 2.
#  x = X(chart_data, 2) # One way to specify the subgroup size.
#  x = X(chart_data, subgropu_size=2) # Another way to specify.

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
ax1.figure.savefig('x.svg', format='svg') # Comment if you wish interactive
# plt.show() # Uncomment if you wish interactive
plt.clf() # Comment if you wish interactive
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
ax2.figure.savefig('mr.svg', format='svg') # Comment if you wish interactive
# plt.show() # Uncomment if you wish interactive
plt.clf() # Comment if you wish interactive
