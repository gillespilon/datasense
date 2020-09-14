#! /usr/bin/env python3
import matplotlib.pyplot as plt
from numpy.random import default_rng
import datasense as ds
import pandas as pd

rng = default_rng()
data_x = rng.uniform(
    low=13,
    high=69,
    size=42
)
series_x = pd.Series(data_x)
data_y = rng.standard_normal(size=42)
series_y = pd.Series(data_y)
fig, ax = ds.plot_scatter_x_y(
    X=series_x,
    y=series_y
)
plt.show()

data_x = rng.uniform(
    low=13,
    high=69,
    size=42
)
series_x = pd.Series(data_x)
data_y = rng.standard_normal(size=42)
series_y = pd.Series(data_y)
fig, ax = ds.plot_scatter_x_y(
    X=series_x,
    y=series_y,
    figuresize=(8, 6),
    marker='o',
    markersize=8,
    colour='#cc3311'
)
plt.show()
