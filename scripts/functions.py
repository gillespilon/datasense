#! /usr/bin/env python3
'''
Syntax for functions

- Parameters without a default argument must explicitly called
'''

from inspect import signature
from typing import List, Tuple, Union


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
    c: float = 6,
    d: Union[float, None] = None,
    e: Union[float, int, None] = None,
    *,
    f: float,
    g: float = 4,
    h: Union[float, None] = None,
    i: Union[float, int, None] = None,
    j: Union[List[str], Tuple[float, int], float, int, None] = None,
):
    pass


def main():
    print(signature(function_name))
    for param in signature(function_name).parameters.values():
        print(param, param.kind.description)
    # function_name(1, 2, f=3)
    # function_name(1, b=2, f=3)
    # function_name(1, 2, 13, f=3)
    # function_name(1, 2, c=13, f=3)


if __name__ == '__main__':
    main()
