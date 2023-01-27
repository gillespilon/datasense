#! /usr/bin/env python3
"""
Example of XbarR control charts

Requires datasense: https://github.com/gillespilon/datasense
"""

from typing import NoReturn, Tuple
import time

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    HEADER_TITLE = "XbarR Control Charts"
    OUTPUT_URL = "xbar_r_example.html"
    HEADER_ID = "xbar-r-example"
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=OUTPUT_URL,
        header_title=HEADER_TITLE,
        header_id=HEADER_ID
    )
    ds.style_graph()
    data = create_data()
    ds.page_break()
    xbar_chart(df=data)
    ds.page_break()
    r_chart(df=data)
    stop_time = time.time()
    ds.page_break()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=OUTPUT_URL
    )


def create_data() -> pd.DataFrame:
    """
    Create a dataframe.
    This function is for demonstration purposes.
    """
    df = pd.DataFrame(
        {
            "Sample":  [
                        1, 2, 3, 4, 5,
                        6, 7, 8, 9, 10,
                        11, 12, 13, 14, 15,
                        16, 17, 18, 19, 20,
                        21, 22, 23, 24, 25
                       ],
            "X1":      [
                        96, 68, 70, 68, 85,
                        57, 86, 56, 55, 73,
                        72, 70, 89, 59, 79,
                        71, 76, 80, 68, 43,
                        39, 83, 56, 95, 47
                       ],
            "X2":      [
                        69, 51, 69, 69, 69,
                        47, 69, 59, 81, 69,
                        69, 48, 76, 59, 53,
                        97, 51, 78, 66, 71,
                        72, 74, 69, 57, 68
                       ],
            "X3":      [
                        77, 71, 70, 64, 80,
                        45, 59, 53, 49, 82,
                        36, 78, 62, 93, 57,
                        66, 62, 71, 66, 48,
                        66, 56, 75, 88, 62
                       ],
            "X4":      [
                        63, 55, 91, 71, 48,
                        65, 65, 58, 69, 77,
                        82, 69, 57, 79, 38,
                        55, 84, 73, 103, 53,
                        79, 87, 51, 66, 74
                       ]
        }
    ).set_index("Sample")
    return df


def xbar_chart(
    *,
    df: pd.DataFrame,
    figsize: Tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    xbar_chart_title: str = "Average Control Chart",
    xbar_chart_ylabel: str = "Measurement Xbar (units)",
    xbar_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "xbar_r_example"
) -> NoReturn:
    """
    Creates an Xbar control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    """
    fig = plt.figure(figsize=figsize)
    xbar = cc.Xbar(data=df)
    ax = xbar.ax(fig=fig)
    ax.axhline(
        y=xbar.sigmas[+1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=xbar.sigmas[-1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=xbar.sigmas[+2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=xbar.sigmas[-2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    cc.draw_rule(
        xbar,
        ax,
        *cc.points_one(xbar),
        "1"
    )
    cc.draw_rule(
        xbar,
        ax,
        *cc.points_four(xbar),
        "4"
    )
    cc.draw_rule(
        xbar,
        ax,
        *cc.points_two(xbar),
        "2"
    )
    cc.draw_rules(
        cc=xbar,
        ax=ax
    )
    ax.set_title(label=xbar_chart_title)
    ax.set_ylabel(ylabel=xbar_chart_ylabel)
    ax.set_xlabel(xlabel=xbar_chart_xlabel)
    fig.savefig(fname=f"{graph_file_prefix}_xbar.svg")
    ds.html_figure(file_name=f"{graph_file_prefix}_xbar.svg")
    print(
        f"Xbar Report\n"
        f"===================\n"
        f"UCL        : {xbar.ucl.round(3)}\n"
        f"Xbarbar    : {xbar.mean.round(3)}\n"
        f"LCL        : {xbar.lcl.round(3)}\n"
        f"Sigma(Xbar): {xbar.sigma.round(3)}\n"
    )


def r_chart(
    *,
    df: pd.DataFrame,
    figsize: Tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    r_chart_title: str = "Range Control Chart",
    r_chart_ylabel: str = "Measurement R (units)",
    r_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "xbar_r_example"
) -> NoReturn:
    """
    Creates an R control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    """
    fig = plt.figure(figsize=figsize)
    r = cc.R(data=df)
    ax = r.ax(fig=fig)
    ax.axhline(
        y=r.sigmas[+1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=r.sigmas[-1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=r.sigmas[+2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=r.sigmas[-2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    cc.draw_rule(
        r,
        ax,
        *cc.points_one(r),
        "1"
    )
    ax.set_title(label=r_chart_title)
    ax.set_ylabel(ylabel=r_chart_ylabel)
    ax.set_xlabel(xlabel=r_chart_xlabel)
    fig.savefig(fname=f"{graph_file_prefix}_r.svg")
    ds.html_figure(file_name=f"{graph_file_prefix}_r.svg")
    print(
        f"R Report\n"
        f"===================\n"
        f"UCL        : {r.ucl.round(3)}\n"
        f"Rbar       : {r.mean.round(3)}\n"
        f"LCL        : {round(r.lcl, 3)}\n"
        f"Sigma(Xbar): {r.sigma.round(3)}\n"
    )


if __name__ == "__main__":
    main()
