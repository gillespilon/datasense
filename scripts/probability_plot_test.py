#! /usr/bin/env python3
"""
Test def probability_plot() of graphs.py.

tim e-f '%e' ./probability_plot_test.py
./probability_plot_test.py
"""

from matplotlib.pyplot import show
from scipy.stats import norm
import datasense as ds

data = norm.rvs(size=42)
fig, ax = ds.probability_plot(
    data=data
)
show()
