'''
Data munging
'''


from datetime import datetime
from typing import List, Tuple


import pandas as pd
from beautifultable import BeautifulTable


def dataframe_info(df: pd.DataFrame, filein: str) -> pd.DataFrame:
    '''
    Display count of rows (rows_in_count)
    Display count of empty rows (rows_empty_count)
    Display count of non-empty rows (rows_out_count)
    Display count of columns (columns_in_count)
    Display count of empty columns (columns_empty_count)
    Display count of non-empty columns (columns_non_empty_count)
    Display table of data type, empty cell count, and empty cell percentage
        for non-empty columns
    Display count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Display count and list of float columns
        (columns_float_count, columns_float_list)
    Display count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Display count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Display count and list of string columns
        (columns_object_count, columns_object_list)
    Display count and list of empty columns
        (columns_empty_count, columns_empty_list)
    '''
    df, rows_in_count, rows_out_count, rows_empty_count = process_rows(df)
    df, columns_in_count, columns_non_empty_count, columns_empty_count,\
        columns_empty_list, columns_non_empty_list, columns_float_list,\
        columns_float_count, columns_integer_list, columns_integer_count,\
        columns_datetime_list, columns_datetime_count,\
        columns_object_list, columns_object_count\
        = process_columns(df)
    print(f'Dataframe information for {filein}')
    print('---------------------------------')
    print()
    print(f'Rows total        : {rows_in_count}')
    print(f'Rows empty        : {rows_empty_count} (deleted)')
    print(f'Rows not empty    : {rows_out_count}')
    print(f'Columns total     : {columns_in_count}')
    print(f'Columns empty     : {columns_empty_count} (deleted)')
    print(f'Columns not empty : {columns_non_empty_count}')
    print()
    number_empty_cells_in_columns(df)
    print(f'List of {columns_non_empty_count} non-empty columns:\n'
          f'{columns_non_empty_list}')
    print()
    print(f'List of {columns_float_count} float columns:\n'
          f'{columns_float_list}')
    print()
    print(f'List of {columns_integer_count} integer columns:\n'
          f'{columns_integer_list}')
    print()
    print(f'List of {columns_datetime_count} datetime columns:\n'
          f'{columns_datetime_list}')
    print()
    print(f'List of {columns_object_count} string columns:\n'
          f'{columns_object_list}')
    print()
    print(f'List of {columns_empty_count} empty columns:\n'
          f'{columns_empty_list}')
    print()
    return df


def find_int_float_columns(df: pd.DataFrame) -> List[str]:
    '''
    Find all integer and float columns
    '''
    columns_int_float = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype in ('int64', 'float64')
    })
    print('There are',
          len(columns_int_float),
          'not-null integer & float columns in',
          len(df.columns),
          'total columns.')
    # print(columns_int_float)
    print()
    return columns_int_float


def number_empty_cells_in_columns(df: pd.DataFrame) -> None:
    '''
    Create a table of data type, empty-cell count, and empty-all percentage
    for non-empty columns.
    '''
    print('Information about non-empty columns')
    table = BeautifulTable(max_width=90)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    column_alignments = {
        'Column': BeautifulTable.ALIGN_LEFT,
        'Data type': BeautifulTable.ALIGN_LEFT,
        'Empty cell count': BeautifulTable.ALIGN_RIGHT,
        'Empty cell percentage': BeautifulTable.ALIGN_RIGHT,
    }
    table.column_headers = list(column_alignments.keys())
    for item, (_column_name, alignment) in\
            enumerate(column_alignments.items()):
        table.column_alignments[item] = alignment
    num_rows = df.shape[0]
    for column_name in df:
        try:
            sum_nan = sum(pd.isnull(df[column_name]))
            percent_nan = round(sum_nan / num_rows * 100, 3)
            table.append_row(
                [column_name,
                 df[column_name].dtype,
                 sum_nan,
                 percent_nan]
            )
        except KeyError:
            print('Error on column:', column_name)
    print(table)
    print()


def process_columns(df: pd.DataFrame) -> Tuple[
    pd.DataFrame,
    int,
    int,
    int,
    List[str],
    List[str],
    List[str],
    int,
    List[str],
    int,
    List[str],
    int,
    List[str],
    int
]:
    '''
    Create count of columns
        (columns_in_count)
    Create count and list of empty columns
        (columns_empty_count, columns_empty_list)
    Create count and list of non-empty columns
        (columns_non_empty_count, columns_non_empty_list)
    Delete empty columns
    Create count and list of float columns
        (columns_float_count, columns_float_list)
    Create count and list of integer columns
        (columns_integer_count, columns_integer_list)
    Create count and list of datetime columns
        (columns_datetime_count, columns_datetime_list)
    Create count and list of string columns
        (columns_object_count, columns_object_list)
    '''
    columns_empty_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].isnull().all()
    })
    columns_in_count = len(df.columns)
    columns_empty_count = len(columns_empty_list)
    columns_non_empty_count = columns_in_count - columns_empty_count
    df = df.drop(columns_empty_list, axis='columns')
    columns_non_empty_list = sorted(df.columns)
    columns_float_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'float'
    })
    columns_float_count = len(columns_float_list)
    columns_integer_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'int64'
    })
    columns_integer_count = len(columns_integer_list)
    columns_datetime_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'datetime64[ns]'
    })
    columns_datetime_count = len(columns_datetime_list)
    columns_object_list = sorted({
        column_name for column_name in df.columns
        if df[column_name].dtype == 'object'
    })
    columns_object_count = len(columns_object_list)
    return (
        df, columns_in_count, columns_non_empty_count,
        columns_empty_count, columns_empty_list, columns_non_empty_list,
        columns_float_list, columns_float_count,
        columns_integer_list, columns_integer_count,
        columns_datetime_list, columns_datetime_count,
        columns_object_list, columns_object_count
    )


def process_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, int, int, int]:
    '''
    Count number of rows (rows_in_count)
    Delete empty rows
    Count number of non-empty rows (rows_out_count)
    Count number of empty rows (rows_empty_count)
    '''
    rows_in_count = df.shape[0]
    df = df.dropna(axis='rows', how='all')
    rows_out_count = df.shape[0]
    rows_empty_count = rows_in_count - rows_out_count
    return df, rows_in_count, rows_out_count, rows_empty_count


def read_file(
    filename: str,
    datecolumnsort: str = None,
    columnnamessort: str = False
) -> pd.DataFrame:
    '''
    Creates a dataframe.
    Reads an ods, csv, or xlsx file.
    '''
    if '.ods' in filename:
        df = pd.read_excel(
            filename,
            engine='odf',
            parse_dates=datecolumnsort,
            date_parser=lambda s: datetime.strptime(s, '%d%b%Y:%H:%M:%S'),
        )
    elif '.csv' in filename:
        df = pd.read_csv(
            filename,
            parse_dates=datecolumnsort,
            date_parser=lambda s: datetime.strptime(s, '%d%b%Y:%H:%M:%S'),
        )
    elif '.xlsx' in filename:
        df = pd.read_excel(
            filename,
            engine='odf',
            parse_dates=datecolumnsort,
            date_parser=lambda s: datetime.strptime(s, '%d%b%Y:%H:%M:%S'),
        )
    if datecolumnsort is not None:
        df = df.sort_values(
            by=datecolumnsort,
            axis='rows',
            ascending=True
        )
    if columnnamessort is True:
        sortedcolumnnames = sorted(df.columns)
        df = df[sortedcolumnnames]
    return df


__all__ = (
    'dataframe_info',
    'find_int_float_columns',
    'number_empty_cells_in_columns',
    'process_columns',
    'process_rows',
    'read_file'
)
