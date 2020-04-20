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

# Examples

In the [scripts](scripts/) directory, there are example scripts and data files.

- [XmR control charts](#xmr-control-charts)
- [XbarR control charts](#xbarr-control-charts)
- [cubic spline for Y vs X line plot](#cubic-spline-for-y-vs-x-line-plot)

## XmR control charts

![X control chart](scripts/x_mr_example_x.svg)

![mR control chart](scripts/x_mr_example_mr.svg)

## XbarR control charts

![Xbar control chart](scripts/xbar_r_example_xbar.svg)

![R control chart](scripts/xbar_r_example_r.svg)

# Cubic spline for Y vs X line plot

![cubic spline for Y vs X line plot](scripts/cubic_spline_datetime.svg)
