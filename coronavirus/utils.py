# Utilities

import numpy as np
import pandas as pd


def fill_dates(df, fill_0=False):
    """Fill missing dates in data frame, and sort dates"""
    dates = df["date"]
    dates = pd.date_range(dates.min(), dates.max())
    template = pd.DataFrame(dates, columns=["date"])
    df = pd.merge(template, df, how="left", on="date")
    if fill_0 == True:
        df = df.fillna(0)
    return df
