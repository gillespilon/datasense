#! /usr/bin/env python3
'''
Test help for datasense.

time -f '%e' ./datasense_help_test.py
./datasense_help_test.py

Typical input:
ds.stats.random_data
'''

import datasense as ds

output_url = 'datasense_help_test.html'
header_title = 'datasense help'
header_id = 'datasense-help'


def main():
    input_value = eval(input(r'module.file.function name? > '))
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    help(input_value)
    print('</pre>')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
