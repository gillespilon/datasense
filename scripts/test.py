#! /usr/bin/env python3
import matplotlib.pyplot as plt
from numpy.random import default_rng
import datasense as ds
import pandas as pd

rng = default_rng()
data = rng.standard_normal(size=42)
series = pd.Series(data)
fig, ax = ds.plot_scatter_y(y=series)
plt.show()

rng = default_rng()
data = rng.standard_normal(size=42)
series = pd.Series(data)
fig, ax = ds.plot_scatter_y(
    y=series,
    figuresize=(8, 6),
    marker='o',
    markersize=8,
    colour='#cc3311'
)
plt.show()
