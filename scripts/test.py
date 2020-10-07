#! /usr/bin/env python3
import matplotlib.pyplot as plt
import datasense as ds
X = ds.random_data(distribution='uniform').sort_values()
y = ds.random_data(distribution='norm')
p = ds.natural_cubic_spline(
    X=X,
    y=y,
    number_knots=10
)
fig, ax = ds.plot_scatter_line_x_y1_y2(
    X=X,
    y1=y,
    y2=p.predict(X)
)
plt.show()
