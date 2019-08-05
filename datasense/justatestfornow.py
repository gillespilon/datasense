#! /usr/bin/env python3

import pandas as pd
import datasense as ds


myseries = pd.Series([30, 171, 184, 201, 212, 250, 265, 270, 272, 289,
                      305, 306, 322, 322, 336, 346, 351, 370, 390, 404,
                      409, 411, 436, 437, 439, 441, 444, 448, 451, 453,
                      470, 480, 482, 487, 494, 495, 499, 503, 514, 521,
                      522, 527, 548, 550, 559, 560, 570, 572, 574, 578,
                      585, 592, 592, 607, 616, 618, 621, 629, 637, 638,
                      640, 656, 668, 707, 709, 719, 737, 739, 752, 758,
                      766, 792, 792, 794, 802, 818, 830, 832, 843, 858,
                      860, 869, 918, 925, 953, 991, 1000, 1005, 1068, 1441])


resultpara = ds.parametric_summary(myseries)


resultnonpara = ds.nonparametric_summary(myseries, alphap=0, betap=0)
print('\nMinitab results')
print(f'\nlower outer fence:   {resultnonpara[0]}\n'
        f'lower inner fence:  {resultnonpara[1]}\n'
        f'lower quartile:      {resultnonpara[2]}\n'
        f'median:              {resultnonpara[3]}\n'
        f'upper quartile:      {resultnonpara[4]}\n'
        f'upper inner fence:   {resultnonpara[5]}\n'
        f'upper outer fence:   {resultnonpara[6]}\n'
        f'interquartile range: {resultnonpara[7]}\n'
        f'inner outliers:      {resultnonpara[8]}\n'
        f'outer outliers:      {resultnonpara[9]}\n'
        f'minimum value:       {resultnonpara[10]}\n'
        f'maximum value:       {resultnonpara[11]}\n'
     )
resultnonpara = ds.nonparametric_summary(myseries, alphap=1/3, betap=1/3)
print('\nIdeal results')
print(f'\nlower outer fence:   {resultnonpara[0]}\n'
        f'lower inner fence:  {resultnonpara[1]}\n'
        f'lower quartile:      {resultnonpara[2]}\n'
        f'median:              {resultnonpara[3]}\n'
        f'upper quartile:      {resultnonpara[4]}\n'
        f'upper inner fence:   {resultnonpara[5]}\n'
        f'upper outer fence:   {resultnonpara[6]}\n'
        f'interquartile range: {resultnonpara[7]}\n'
        f'inner outliers:      {resultnonpara[8]}\n'
        f'outer outliers:      {resultnonpara[9]}\n'
        f'minimum value:       {resultnonpara[10]}\n'
        f'maximum value:       {resultnonpara[11]}\n'
     )
