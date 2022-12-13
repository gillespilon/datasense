import warnings

import datasense as ds
import pandas as pd
import numpy as np


df_empty_test = pd.DataFrame(
    data=dict(
        floats=[1.0, np.NaN, 3.0, np.NaN, 5.0, 6.0, np.NaN],
        text=["A", "B", "C", "D", "E", "F", np.NaN],
        dates=[
            "1956-06-08", "1956-06-08",
            "1956-06-08", "1956-06-08",
            "1956-06-08", "1956-06-08",
            pd.NaT
        ],
        all_nan=[np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
        all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
        all_none=[None, None, None, None, None, None, None],
        all_space=["", " ", "", " ", "", "", ""],
        nan_space=[np.NaN, "", " ", np.NaN, np.NaN, np.NaN, np.NaN],
        nan_none=[np.NaN, None, np.NaN, np.NaN, None, np.NaN, None],
        mixed=[None, np.NaN, pd.NaT, pd.NaT, None, np.NaN, pd.NaT],
        integers=[1, 2, np.NaN, 4, 5, 6, np.NaN],
    )
).replace(
    r"^\s+$",
    np.NaN,
    regex=True
).replace(
    "",
    np.NaN,
    regex=True
).astype(
    dtype={
        "integers": "Int64",
        "floats": "float64",
        "text": "object",
        "dates": "datetime64[ns]",
        "all_nan": "float64",
        "all_nat": "datetime64[ns]",
        "all_none": "float64",
        "all_space": "float64",
        "nan_space": "float64",
        "nan_none": "float64",
        "mixed": "datetime64[ns]"
    }
)


def test_listone_contains_all_listtwo_substrings():
    pass


def test_list_directories_within_directory():
    pass


def test_number_empty_cells_in_columns():
    pass


def test_parameters_dict_replacement():
    pass


def test_parameters_text_replacement():
    pass


def test_ask_save_as_file_name_path():
    pass


def test_ask_open_file_name_path():
    pass


def test_find_int_float_columns():
    pass


def test_find_timedelta_columns():
    pass


def test_create_dataframe_norm():
    pass


def test_directory_remove_file():
    pass


def test_replace_column_values():
    pass


def test_feature_percent_empty():
    pass


def test_find_category_columns():
    pass


def test_find_datetime_columns():
    pass


def test_list_one_list_two_ops():
    pass


def test_series_replace_string():
    pass


def test_delete_empty_columns():
    """
    Test that all elements of a column:
    - are empty for all columns
    - are empty for specific columns
    """
    result1 = ds.delete_empty_columns(df=df_empty_test)
    expected1 = pd.DataFrame(
        data=dict(
            floats=[1.0, np.NaN, 3.0, np.NaN, 5.0, 6.0, np.NaN],
            text=["A", "B", "C", "D", "E", "F", np.NaN],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                pd.NaT
            ],
            integers=[1, 2, np.NaN, 4, 5, 6, np.NaN],
        )
    ).replace(
        r"^\s+$",
        np.NaN,
        regex=True
    ).replace(
        "",
        np.NaN,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
        }
    )
    assert result1.equals(other=expected1)
    list_empty_columns = ["mixed", "nan_none"]
    # Delete columns using list_empty_columns
    result2 = ds.delete_empty_columns(
        df=df_empty_test,
        list_empty_columns=list_empty_columns
    )
    expected2 = pd.DataFrame(
        data=dict(
            floats=[1.0, np.NaN, 3.0, np.NaN, 5.0, 6.0, np.NaN],
            text=["A", "B", "C", "D", "E", "F", np.NaN],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                pd.NaT
            ],
            all_nan=[np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
            all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            all_none=[None, None, None, None, None, None, None],
            all_space=["", " ", "", " ", "", "", ""],
            nan_space=[np.NaN, "", " ", np.NaN, np.NaN, np.NaN, np.NaN],
            integers=[1, 2, np.NaN, 4, 5, 6, np.NaN],
        )
    ).replace(
        r"^\s+$",
        np.NaN,
        regex=True
    ).replace(
        "",
        np.NaN,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
            "all_nan": "float64",
            "all_nat": "datetime64[ns]",
            "all_none": "float64",
            "all_space": "float64",
            "nan_space": "float64"
        }
    )
    assert result2.equals(other=expected2)


def test_replace_text_numbers():
    pass


def test_directory_file_print():
    pass


def test_directory_file_list():
    pass


def test_find_object_columns():
    pass


def test_rename_some_columns():
    pass


def test_ask_directory_path():
    pass


def test_rename_all_columns():
    pass


def test_find_float_columns():
    pass


def test_remove_punctuation():
    pass


def test_print_list_by_item():
    pass


def test_delete_empty_rows():
    """
    Test delete empty rows:
    - all elements for a row for all columns
    - all elements for a row for specific columns
    """
    # Delete columns where all elements of a column are empty
    result = ds.delete_empty_rows(df=df_empty_test)
    expected = pd.DataFrame(
        data=dict(
            floats=[1.0, np.NaN, 3.0, np.NaN, 5.0, 6.0],
            text=["A", "B", "C", "D", "E", "F"],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08"
            ],
            all_nan=[np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
            all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            all_none=[None, None, None, None, None, None],
            all_space=["", " ", "", " ", "", ""],
            nan_space=[np.NaN, "", " ", np.NaN, np.NaN, np.NaN],
            nan_none=[np.NaN, None, np.NaN, np.NaN, None, np.NaN],
            mixed=[None, np.NaN, pd.NaT, pd.NaT, None, np.NaN],
            integers=[1, 2, np.NaN, 4, 5, 6],
        )
    ).replace(
        r"^\s+$",
        np.NaN,
        regex=True
    ).replace(
        "",
        np.NaN,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
            "all_nan": "float64",
            "all_nat": "datetime64[ns]",
            "all_none": "float64",
            "all_space": "float64",
            "nan_space": "float64",
            "nan_none": "float64",
            "mixed": "datetime64[ns]"
        }
    )
    assert result.equals(other=expected)


def test_find_bool_columns():
    pass


def test_create_dataframe():
    pass


def test_create_directory():
    pass


def test_delete_directory():
    pass


def test_find_int_columns():
    pass


def test_list_change_case():
    pass


def test_rename_directory():
    pass


def test_process_columns():
    pass


def test_copy_directory():
    pass


def test_dataframe_info():
    pass


def test_delete_columns():
    pass


def test_quit_sap_excel():
    pass


def test_mask_outliers():
    pass


def test_process_rows():
    pass


def test_delete_rows():
    pass


def test_byte_size():
    pass


def test_get_mtime():
    pass


def test_file_size():
    pass


def test_read_file():
    pass


def test_save_file():
    pass


def test_sort_rows():
    pass
