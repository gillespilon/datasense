#! /usr/bin/env python3
"""
Create y1, y2 vs. X line plots with dual Y axes.

Usage examples:

./plot_lineleft_lineright_x_y1_y2.py -h
./plot_lineleft_lineright_x_y1_y2.py
./plot_lineleft_lineright_x_y1_y2.py -ds <path> -df mmm
./plot_lineleft_lineright_x_y1_y2.py -ds <path> -df yyyy-mm
"""

from pathlib import Path
import argparse

import datasense as ds
import pandas as pd


def main():
    output_url = "plot_lineleft_lineright_x_y1_y2.html"
    header_title = "plot_lineleft_lineright_x_y1_y2"
    header_id = "plot-lineleft-lineright-x-y1-y2"
    xticklabels_rotation = 45
    figsize = (8, 5)
    parser = argparse.ArgumentParser(
        prog="plot_lineleft_lineright_x_y1_y2.py",
        description="Create a dual-axis Y1, Y2 vs. X chart",
    )
    parser.add_argument(
        "-ds",
        "--data_source",
        default=Path("plot_lineleft_lineright_x_y1_y2.ods"),
        type=Path,
        required=False,
        help="Provide a path or file xlsx XLSX csv CSV ods ODS (optional)",
    )
    parser.add_argument(
        "-df",
        "--date_format",
        default="yyyy-mm",
        type=str,
        required=False,
        help="Provide date format mmm (FEB) or yyyy-mm (2024-02) (required)",
    )
    parser.add_argument(
        "-gp",
        "--graph_path",
        default="plot_lineleft_lineright_x_y1_y2.svg",
        type=Path,
        required=False,
        help="Provide a string of the graph title (optional)",
    )
    parser.add_argument(
        "-gt",
        "--graph_title",
        default="Y1, Y2 vs X",
        type=str,
        required=False,
        help="Provide a string of the graph title (optional)",
    )
    args = parser.parse_args()
    df = ds.read_file(file_name=args.data_source)
    X = df.columns[0]
    y1 = df.columns[1]
    y2 = df.columns[2]
    date_format = args.date_format
    match date_format:
        case "yyyy-mm":
            df["X"] = pd.to_datetime(arg=df[X], format="%Y-%m")
        case "mmm":
            pass
        case _:
            print(
                'Error. Enter "yyyy-mm"or "mmmm" for parameter "date_format"'
            )
    # df = pd.DataFrame(
    #     data={
    #         "X": [
    #             "FEB",
    #             "MAR",
    #             "APR",
    #             "MAY",
    #             "JUN",
    #             "JUL",
    #             "AUG",
    #             "SEP",
    #             "OCT",
    #             "NOV",
    #             "DEC",
    #             "JAN",
    #         ],
    #         # "X": [
    #         #     "2023-02",
    #         #     "2023-03",
    #         #     "2023-04",
    #         #     "2023-05",
    #         #     "2023-06",
    #         #     "2023-07",
    #         #     "2023-08",
    #         #     "2023-09",
    #         #     "2023-10",
    #         #     "2023-11",
    #         #     "2023-12",
    #         #     "2024-01",
    #         # ],
    #         "y1": [
    #             44487,
    #             33470,
    #             24657,
    #             46056,
    #             39499,
    #             39153,
    #             77082,
    #             56987,
    #             54610,
    #             62899,
    #             68318,
    #             67059,
    #         ],
    #         "y2": [
    #             12571,
    #             9261,
    #             7093,
    #             12970,
    #             8673,
    #             5121,
    #             9047,
    #             8978,
    #             8399,
    #             7909,
    #             6877,
    #             8300,
    #         ],
    #     }
    # )
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    fig, ax1, ax2 = ds.plot_lineleft_lineright_x_y1_y2(
        X=df[X],
        y1=df[y1],
        y2=df[y2],
        figsize=figsize,
        labellegendy1=y1,
        labellegendy2=y2,
        xticklabels_rotation=xticklabels_rotation,
        defaultfmt="%Y-%m",
    )
    ax1.set_xlabel(xlabel=X, weight="bold", fontsize=12)
    ax1.set_ylabel(ylabel=y1, weight="bold", fontsize=12)
    ax2.set_ylabel(ylabel=y2, weight="bold", fontsize=12)
    fig.suptitle(t=args.graph_title, weight="bold", fontsize=18)
    fig.legend(frameon=False)
    graph_path = args.graph_path
    graph_format = graph_path.suffix[1:]
    fig.savefig(fname=graph_path, format=graph_format, bbox_inches="tight")
    ds.html_figure(file_name=graph_path)
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


if __name__ == "__main__":
    main()
