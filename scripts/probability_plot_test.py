#! /usr/bin/env python3
"""
test
"""

from matplotlib.pyplot import show
from scipy.stats import norm
import datasense as ds

data = norm.rvs(size=42)
fig, ax = ds.probability_plot(
    data=data
)
show()
