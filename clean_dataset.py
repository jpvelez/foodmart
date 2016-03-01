#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd

def clean_string(series):
    '''
    Attempt to strip apostrophes from any series with string
    processing methods.
    TODO: Make sure you don't accidentally remove apostrophes
    inside strings.
    '''
    try:
        return series.str.replace("'", "").strip()
    except AttributeError:  # Ask forgiveness, not permission.
        return series


def string_to_float(series):
    if series.dtype == np.dtype('O'):
        try:
            return series.astype(np.dtype('float64'))
        except ValueError:
            return series
    else:
        return series

def string_to_date(series):
    if series.dtype == np.dtype('O'):
        return pd.to_datetime(series)
    else:
        return series


# Load input stream into in-memory DataFrame.
dataset = pd.read_csv(sys.stdin)

# Remove whitespace from column names.
dataset.columns = [col_name.strip() for col_name in dataset.columns]

# Remove apostrophe from string column values, cast numerical
# string columns as floats, and cast datetime string columns
# to datetime.
dataset.apply(clean_string)    \
       .apply(string_to_float) \
       .apply(string_to_date)  \
       .to_csv(sys.argv[1])


