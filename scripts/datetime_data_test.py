#! /usr/bin/env python3
"""
Test for datetime data
"""

import datasense as ds

output_url = 'datetime_data_test.html'
header_title = 'datetime_data_test'
header_id = 'datetime-data-test'


def main():
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    series = ds.datetime_data()
    print('datetime series')
    print(series)
    print('</pre>')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
