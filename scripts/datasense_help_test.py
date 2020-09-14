#! /usr/bin/env python3

'''
Test help for datasense.

time -f '%e' ./datasense_help_test.py
./datasense_help_test.py
'''

import webbrowser
import sys


import datasense as ds


output_url = 'datasense_help_test.html'
header_title = 'datasense help'
header_id = 'datasense-help'


def main():
    input_value = eval(input(r'module.file.function name? > '))
    original_stdout = sys.stdout
    sys.stdout = open(output_url, 'w')
    ds.html_header(
        headertitle=header_title,
        headerid=header_id
    )
    help(input_value)
    ds.html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout
    webbrowser.open_new_tab(output_url)


if __name__ == '__main__':
    main()
