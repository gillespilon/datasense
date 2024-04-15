#! /usr/bin/env python3
"""
Example of XbarR control charts

The data file can be:
    .csv | .CSV | .ods | .ODS | .xlsx | .XLSX | .xlsm | .XLSM | .feather

The data file should be as follows, either A or B.

A: One column contains sample IDs, such as integers or floats, and they must be
in increasing order. This column can also be strings, with no restrictions. The
other columns contain data values, and there must be two or more of these
columns. The first row contains the labels for the columns.

B: There is no sample ID column. The other columns contain data values,
and there must be two or more of these columns. The first row contains the
labels for the columns.

Execute the script in a terminal:
 ./xbar_r_control_charts.py -pf xbar_r_example.csv -sc Sample -dc X1 X2 X3 X4
 ./xbar_r_control_charts.py -pf xbar_r_example.csv -dc X1 X2 X3 X4
"""

from pathlib import Path
from os import chdir
import argparse
import time

from datasense import control_charts as cc
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    chdir(Path(__file__).parent.resolve())  # required for cron
    parser = argparse.ArgumentParser(
        prog="xbar_r_control_charts.py",
        description="Create Xbar and R control charts and add Nelson's Rules"
    )
    parser.add_argument(
        "-pf",
        "--path_or_file",
        type=Path,
        required=True,
        help="Provide a path or file of the .XLSX or .CSV file (required)",
    )
    parser.add_argument(
        "-sc",
        "--sample_column",
        default=None,
        type=str,
        required=False,
        help="Provide a string of the sample column label (optional)",
    )
    parser.add_argument(
        "-dc",
        "--data_columns",
        nargs="+",
        default=None,
        type=str,
        required=True,
        help="Provide a string of the data column label (required)",
    )
    args = parser.parse_args()
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
    # data = create_data()
    usecols = [args.sample_column] + args.data_columns
    usecols = [item for item in usecols if item is not None]
    df = ds.read_file(
        file_name=args.path_or_file,
        usecols=usecols
    )
    if args.sample_column is None:
        data = df.copy()
    elif args.sample_column is not None:
        data = df.set_index(df.columns[0]).copy()
    print("path or file:", args.path_or_file)
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
    figsize: tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    xbar_chart_title: str = "Average Control Chart",
    xbar_chart_ylabel: str = "Measurement Xbar (units)",
    xbar_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "xbar_r_example"
) -> None:
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
    figsize: tuple[float, float] = (8, 6),
    colour: str = "#33bbee",
    r_chart_title: str = "Range Control Chart",
    r_chart_ylabel: str = "Measurement R (units)",
    r_chart_xlabel: str = "Sample",
    graph_file_prefix: str = "xbar_r_example"
) -> None:
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
