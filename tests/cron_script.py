#! /usr/bin/env python3
"""
Execute pytest for datasense
"""

from pathlib import Path
from os import chdir
import webbrowser
import pytest


def main():
    # chdir(Path(__file__).parent.resolve())  # required for cron
    url = ("pytest.html")
    pytest.main(["--html=pytest.html"])
    webbrowser.open_new_tab(url=url)


if __name__ == "__main__":
    main()
