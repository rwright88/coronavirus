# Utilities

from itertools import product

import numpy as np
import pandas as pd


def ffill(x):
    """Fill missing values with last non-missing value, 1-d"""
    mask = np.isnan(x)
    ind = np.where(~mask, np.arange(len(mask)), 0)
    np.maximum.accumulate(ind, out=ind)
    out = x[ind]
    return out


def fill_dates(df, geo):
    """Fill missing dates in data frame for each geo"""
    by = [geo, "date"]
    geos = df[geo].unique()
    dates = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    template = list(product(geos, dates))
    template = pd.DataFrame(template, columns=by)
    df = pd.merge(template, df, how="left", on=by)
    df = df.sort_values(by)
    return df
