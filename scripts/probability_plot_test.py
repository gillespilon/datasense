#! /usr/bin/env python3
"""
test
"""

from scipy.stats import norm
import datasense as ds

data = norm.rvs(size=42)
fig, ax = ds.probability_plot(
    data=data
)
fig.savefig('test.svg')
