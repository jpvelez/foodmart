#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd

def clean_string(series):
    '''
    Attempt to strip apostrophes from any series with string
    processing methods.
    TODO: Make sure you don't accidentally remove apostrophes
    inside strings.
    '''
    print(series.dtype)
    # series.str.replace("'", "").strip()
    try:
        print('ghf')
        return series.str.replace("'", "")
    except AttributeError as e:  # Ask forgiveness, not permission.
        print(e)
        print('gh')
        return series


def string_to_float(series):
    if series.dtype == np.dtype('O'):
        try:
            return series.astype(np.dtype('float64'))
        except ValueError:
            return series
    else:
        return series

# def string_to_date(series):
#     if series.dtype == np.dtype('O'):
#         return pd.to_datetime(series)
#     else:
#         return series


# Load input stream into in-memory DataFrame.
dataset = pd.read_csv(sys.stdin)

print(dataset.head())
# Remove whitespace from column names.
dataset.columns = [col_name.strip() for col_name in dataset.columns]

print(dataset.dtypes)
# Remove apostrophe from string column values, cast numerical
# string columns as floats, and cast datetime string columns
# to datetime.
dataset.apply(clean_string)    \
       .apply(string_to_float) \
       .to_csv(sys.argv[1])

# print(clean_dataset.head())


