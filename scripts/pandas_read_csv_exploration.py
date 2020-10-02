#! /usr/bin/env python3
"""
Pandas read_csv exploration
"""

from typing import Optional, Union

import datasense as ds
import pandas as pd

output_url = 'pandas_read_csv_exploration.html'
header_title = 'pandas_read_csv_exploration'
header_id = 'pandas-read-csv-exploration'


def main():
    # pd.options.display.max_columns = 500
    original_stdout = ds.html_begin(
        outputurl=output_url,
        headertitle=header_title,
        headerid=header_id
    )
    print('<pre>')
    df = create_dataframe()
    print('Create dataframe')
    print(df.tail())
    print()
    save_dataframe(df=df)
    # Example 1
    data = read_file(
        file_name='myfile.csv'
    )
    print('Example 1')
    print(data.tail())
    print()
    # Example 2
    data = read_file(
        file_name='myfile.csv',
        index_col='t'
    )
    print('Example 2')
    print(data.tail())
    print()
    # Example 3
    data = read_file(
        file_name='myfile.csv',
        index_col='y'
    )
    print('Example 3')
    print(data.tail())
    print('</pre>')
    ds.html_end(
        originalstdout=original_stdout,
        outputurl=output_url
    )


def create_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            'b': ds.random_data(distribution='bool'),
            'c': ds.random_data(distribution='categories'),
            'd': ds.timedelta_data(),
            's': ds.random_data(distribution='strings'),
            't': ds.datetime_data(),
            'x': ds.random_data(distribution='norm'),
            'y': ds.random_data(distribution='randint'),
            'z': ds.random_data(distribution='uniform')
        }
    )
    return df


def save_dataframe(df) -> None:
    df.to_csv(
        'myfile.csv',
        index=False
    )


def read_file(
    file_name: str,
    *,
    index_col: Optional[Union[str, bool]] = None,
    dtype: Optional[Union[str, dict]] = None
) -> pd.DataFrame:
    df = pd.read_csv(
        file_name,
        index_col=index_col,
        dtype=dtype
    )
    """
    Create a DataFrame from an external file.

    Parameters
    ----------
    file_name : str
        The name of the file to read.

    Returns
    -------
    df : pd.DataFrame
        The dataframe created from the external file.

    Examples
    --------
    Example 1
    >>> data = read_file(file_name='myfile.csv')

    Example 2
    Make a datetime column the dataframe index.
    >>> data = read_file(
    >>>     file_name='myfile.csv',
    >>>     index_col='t'
    >>> )

    Example 3
    Make an integer column the dataframe index.
    >>> data = read_file(
    >>>     file_name='myfile.csv',
    >>>     index_col='y'
    >>> )
    """
    return df


if __name__ == '__main__':
    main()
