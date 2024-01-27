# In brevi

This repository contains a package of statistical and graphical functions
that I use in my work of making sense of data to create information
and understanding.

# To install #

Do this if this is your first-time installation. Ensure you have `git` installed.

```
pip install --user -e "git+https://github.com/gillespilon/datasense#egg=datasense"
```

# To update #

Do this if this is an update anytime after your first-time installation.

```
pip install --user --upgrade -e "git+https://github.com/gillespilon/datasense#egg=datasense"
```
# Documentation

This is built into the docstrings of the functions. These can be easily accessed using pydoc.

    pydoc datasense
    > ...
    > DESCRIPTION
    >     Tools for statistical, graphical, and predictive analysis:
    >     - Supervised machine learning
    >     - Six Sigma methodology
    >     - Regular expressions
    >     - Process variation
    >     - Excel file edits
    >     - Data Science
    >     - Automation
    >     - Analytics
    > ...
    >     Why this?
    >     - Equivalent Python functions that are available in R, SAS, JMP, Minitab
    >     - Other packages have limited process control analysis features.
    >     - Other packages are abandoned or inadequately supported.
    >     - Functions to support measurement system analysis.
    >     - Functions to simplify statistics, graphs, etc.
    >     - Functions to support process control charts.
    >     - Functions to support SQL functionality.
    >     - Develop a free open-source package.

    > PACKAGE CONTENTS
    >     automation
    >     control_charts
    >     graphs
    >     html_ds
    >     msa
    >     munging
    >     pyxl
    >     rgx
    >     sequel
    >     stats

    pydoc datasense.graphs
    pydoc datasense.graphs.probability_plot
    etc.

# Modules

## automation.py

TBD

## control_charts.py

TBD

## graphs.py

TBD

## html_ds.py

TBD

## msa.py

TBD

## munging.py

TBD
## pyxl.py


TBD

## rgx.py

TBD

## sequel.py

TBD

## stats.py

TBD

# Example scripts

In the [scripts](scripts/) directory, there are example scripts and data files.

- [XmR control charts](#xmr-control-charts)
- [XbarR control charts](#xbarr-control-charts)
- [Cubic spline for Y vs X line plot](#cubic-spline-for-y-vs-x-line-plot)
- [Exponentially weighted average for Y vs X line plot](#exponentially-weighted-average-for-y-vs-x-line-plot)
- [Piecewise natural cubic spline](#piecewise-natural-cubic-spline)

# Example graphs

![X control chart](scripts/x_mr_example_x.svg)

![mR control chart](scripts/x_mr_example_mr.svg)

![Xbar control chart](scripts/xbar_r_example_xbar.svg)

![R control chart](scripts/xbar_r_example_r.svg)

![cubic spline for Y vs X line plot](scripts/cubic_spline_datetime_float.svg)

![cubic spline for Y vs X line plot](scripts/cubic_spline_integer_float.svg)

![Exponentially weighted average for Y vs X line plot](scripts/exponentially_weighted_average_datetime_float.svg)

![Exponentially weighted average for Y vs X line plot](scripts/exponentially_weighted_average_integer_float.svg)

![Piecewise natural cubic spline](scripts/spline_piecewise_natural_cubic_spline_TARGET_FEATURE_30.svg)

# References

To cite this repository, please use:

@software{datasense,
  author      = {Gilles Pilon},
  title       = {datasense},
  url         = {https://github.com/gillespilon/datasense},
  version     = {0.2},
  date        = {2024-01-11}
}
