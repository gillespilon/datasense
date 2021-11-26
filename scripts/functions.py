#! /usr/bin/env python3
'''
Syntax for functions
'''

from inspect import signature
from typing import Optional


def function_name_syntax(
    positional_only_parameters,
    /,
    positional_or_keyword_parameters,
    *,
    keyword_only_parameters
):
    pass


def function_name(
    a: float,
    /,
    b: float,
    c: Optional[float] = 6,
    *,
    d: float,
    e: Optional[float] = 4
):
    pass


def main():
    print(signature(function_name))
    for param in signature(function_name).parameters.values():
        print(param, param.kind.description)
    function_name(1, 2, d=3)
    function_name(1, b=2, d=3)
    function_name(1, 2, 13, d=3)
    function_name(1, 2, c=13, d=3)


if __name__ == '__main__':
    main()
