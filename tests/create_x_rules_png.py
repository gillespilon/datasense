#! /usr/bin/env python3
"""
Create X-rules.png for testing datasense.control_charts.draw_rules()
"""

from pathlib import Path

import datasense.control_charts as cc
import pandas as pd


def main():
    df = pd.DataFrame({
        'Sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'X': [25.0, 24.0, 35.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0, 16.0,
              16.0, 16.0],
    }).set_index('Sample')
    path = Path("prerenders", "X-rules.png")
    X = cc.X(data=df[['X']])
    ax = X.ax()
    cc.draw_rules(
        cc=X,
        ax=ax
    )
    ax.figure.savefig(
                fname=path,
                format="png"
            )


if __name__ == "__main__":
    main()
