#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Clean Foodmart dataset csv. Gets input data from stdin,
scrubs it, and outputs to user-provided filename.

Example usage:
cat product.csv | ./clean_dataset.py clean_product.csv
'''

import sys
from functools import partial
from operator import methodcaller
import numpy as np
import pandas as pd


def clean_string_col(series):
    '''
    Strip apostrophes from string series.
    '''
    try:
        return series.str.replace("'", "")
    except AttributeError:  # Ask forgiveness, not permission.
        return series       # Non-string series.


# Functions that change dtype of ndarrays/pandas series.
converter_functions = {'datetime': pd.to_datetime,
                       # Treat ndarray type casting method as function
                       # with predefined positional argument.
                       'float': methodcaller('astype', 'float64')}


def convert_str_to(dtype, series):
    '''
    Convert string series with "wrong" dtype to specified dtype.

    If dtype is float, numerical string series convert to float.
    If dtype is datetime, string series with dates convert to datetime.
    Other series are not touched.
    '''
    if series.dtype == np.dtype('O'):  # Don't re-cast numeric series.
        try:
            return converter_functions[dtype](series)
        except ValueError:             # String series that can't be re-cast.
            return series
    else:
        return series


# Manufacture string conversion functions using functools.partial,
# a higher-order function that takes in an abstract function
# - convert_str_to, in this case - and returns a parameterized copy.
str_to_float = partial(convert_str_to, 'float')
str_to_date = partial(convert_str_to, 'datetime')

if __name__ == '__main__':
    # IO: Spool stdin data stream into in-memory DataFrame.
    in_stream = sys.stdin
    dataset = pd.read_csv(in_stream)

    # COLUMN NAMES: Remove whitespace from column names.
    dataset.columns = [col_name.strip() for col_name in dataset.columns]

    # COLUMN VALUES: Remove apostrophes from string column values,
    # cast numerical string columns to floats, cast string columns
    # with dates to datetime, pickle dataset to preserve data types.
    out_filename = sys.argv[1]
    dataset.apply(clean_string_col) \
           .apply(str_to_float)     \
           .apply(str_to_date)      \
           .to_pickle(out_filename)
