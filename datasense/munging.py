import pandas as pd


def dataframe_info(df: pd.DataFrame, filein: str) -> pd.DataFrame:
    '''
    Display count of rows (rows_in_count)
    Display count of empty rows (rows_empty_count)
    Display count of non-empty rows (rows_non_empty_count)
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


__all__ = (
    'dataframe_info',
)

