#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Clean Foodmart dataset csv. Gets input data from stdin,
scrubs it, and outputs to user-provided filename.

Example usage:
cat product.csv | ./clean_dataset.py clean_product.csv
'''

import sys
import numpy as np
import pandas as pd


def clean_string_col(series):
    '''
    Attempt to strip apostrophes from any series with string
    processing methods.
    '''
    try:
        return series.str.replace("'", "")
    except AttributeError:  # Ask forgiveness, not permission.
        return series


def string_to_float(series):
    '''
    Attempt to convert string series to float.
    Only numerical strings should be recast.
    '''
    if series.dtype == np.dtype('O'):
        try:
            return series.astype(np.dtype('float64'))
        except ValueError:
            return series
    else:
        return series

if __name__ == '__main__':
    # IO: Spool stdin data stream into in-memory DataFrame.
    in_stream = sys.stdin
    dataset = pd.read_csv(in_stream)

    # COLUMN NAMES: Remove whitespace from column names.
    dataset.columns = [col_name.strip() for col_name in dataset.columns]

    # COLUMN VALUES: Remove apostrophes from string column values,
    # cast numerical string columns to floats, save to disk.
    out_filename = sys.argv[1]
    dataset.apply(clean_string_col).apply(string_to_float).to_csv(out_filename)
