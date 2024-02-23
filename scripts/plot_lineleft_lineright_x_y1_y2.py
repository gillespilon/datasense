#! /usr/bin/env python3
"""
Create y1, y2 vs. X line plots with dual Y axes.
"""

import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.artist as mpla
import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    output_url = "plot_lineleft_lineright_x_y1_y2.html"
    header_title = "plot_lineleft_lineright_x_y1_y2"
    header_id = "plot-lineleft-lineright-x-y1-y2"
    xticklabels_rotation = 45
    labellegendy1 = "y1"
    labellegendy2 = "y2"
    figsize = (8, 5)
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    df = pd.DataFrame(
        data={
            "X": [
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
                "JAN",
            ],
            # "X": [
            #     "2023-02",
            #     "2023-03",
            #     "2023-04",
            #     "2023-05",
            #     "2023-06",
            #     "2023-07",
            #     "2023-08",
            #     "2023-09",
            #     "2023-10",
            #     "2023-11",
            #     "2023-12",
            #     "2024-01",
            # ],
            "y1": [
                44487,
                33470,
                24657,
                46056,
                39499,
                39153,
                77082,
                56987,
                54610,
                62899,
                68318,
                67059,
            ],
            "y2": [
                12571,
                9261,
                7093,
                12970,
                8673,
                5121,
                9047,
                8978,
                8399,
                7909,
                6877,
                8300,
            ],
        }
    )
    # uncomment one of the following if df["X"] are strings of format "yyyy-mm"
    # df["X"] = df["X"].astype("datetime64[ns]")  # less strict
    # df["X"] = pd.to_datetime(arg = df["X"], format="%Y-%m")  # more strict
    fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
        X=df["X"],
        y1=df["y1"],
        y2=df["y2"],
        figsize=figsize,
        labellegendy1=labellegendy1,
        labellegendy2=labellegendy2,
        xticklabels_rotation=xticklabels_rotation,
        defaultfmt="%Y-%m",
    )
    if df["X"].dtype in ["datetime64[ns]"]:
        print(True)
    else:
        print(False)
    fig.legend(frameon=False)
    fig.savefig(fname="plot_lineleft_lineright_x_y1_y2.svg", format="svg")
    ds.html_figure(file_name="plot_lineleft_lineright_x_y1_y2.svg")
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


if __name__ == "__main__":
    main()
