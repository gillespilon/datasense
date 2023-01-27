#! /usr/bin/env python3
"""
Example of XmR control charts

Requires datasense: https://github.com/gillespilon/datasense
"""

from typing import NoReturn, Tuple
import time

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    HEADER_TITLE = "XmR Control Charts"
    OUTPUT_URL = "x_mr_example.html"
    HEADER_ID = "x-mr-example"
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=OUTPUT_URL,
        header_title=HEADER_TITLE,
        header_id=HEADER_ID
    )
    ds.style_graph()
    data = create_data()
    ds.page_break()
    x_chart(df=data)
    ds.page_break()
    mr_chart(df=data)
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
    Creates a dataframe.
    """
    df = pd.DataFrame(
        {
            "Sample":  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            "X":       [
                25.0, 24.0, 38.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0,
                16.0, 16.0, 16.0
            ]
        }
    ).set_index("Sample")
    return df


def x_chart(
    *,
    df: pd.DataFrame,
    figsize: Tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    x_chart_title: str = "Individuals Control Chart",
    x_chart_ylabel: str = "Measurement X (units)",
    x_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "x_mr_example"
) -> NoReturn:
    """
    Creates an X control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    """
    fig = plt.figure(figsize=figsize)
    x = cc.X(data=df)
    ax = x.ax(fig=fig)
    ax.axhline(
        y=x.sigmas[+1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[-1],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[+2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    ax.axhline(
        y=x.sigmas[-2],
        linestyle="--",
        dashes=(5, 5),
        color=colour,
        alpha=0.5
    )
    cc.draw_rules(x, ax)
    ax.set_title(label=x_chart_title)
    ax.set_ylabel(ylabel=x_chart_ylabel)
    ax.set_xlabel(xlabel=x_chart_xlabel)
    fig.savefig(fname=f"{graph_file_prefix}_x.svg")
    ds.html_figure(file_name=f"{graph_file_prefix}_x.svg")
    print(
       f"X Report\n"
       f"===================\n"
       f"UCL        : {x.ucl.round(3)}\n"
       f"Xbar       : {x.mean.round(3)}\n"
       f"LCL        : {x.lcl.round(3)}\n"
       f"Sigma(X)   : {x.sigma.round(3)}\n"
    )


def mr_chart(
    *,
    df: pd.DataFrame,
    figsize: Tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    mr_chart_title: str = "Moving Range Control Chart",
    mr_chart_ylabel: str = "Measurement mR (units)",
    mr_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "x_mr_example"
) -> NoReturn:
    """
    Creates an mR control chart.
    Identifies out-of-control points.
    Adds chart and axis titles.
    Saves the figure in svg format.
    """
    fig = plt.figure(figsize=figsize)
    mr = cc.mR(data=df)
    ax = mr.ax(fig=fig)
    cc.draw_rule(
        mr,
        ax,
        *cc.points_one(mr),
        "1"
    )
    ax.set_title(label=mr_chart_title)
    ax.set_ylabel(ylabel=mr_chart_ylabel)
    ax.set_xlabel(xlabel=mr_chart_xlabel)
    fig.savefig(fname=f"{graph_file_prefix}_mr.svg")
    ds.html_figure(file_name=f"{graph_file_prefix}_mr.svg")
    print(
       f"mR Report\n"
       f"===================\n"
       f"UCL        : {mr.ucl.round(3)}\n"
       f"mRbar      : {mr.mean.round(3)}\n"
       f"LCL        : {round(mr.lcl, 3)}\n"
       f"Sigma(mR)  : {mr.sigma.round(3)}\n"
    )


if __name__ == "__main__":
    main()
