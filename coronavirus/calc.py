# Calc stats

import numpy as np
import pandas as pd


def calc_stats(df, n=7):
    """Calculate per million and average daily percent change"""
    df = df.sort_values(["code", "date"])
    cols = ["cases", "deaths"]
    out = []
    ind = df.groupby("code").indices

    for col in cols:
        df[col + "_pm"] = df[col] / df["pop"] * 1e06

    for k, v in ind.items():
        df1 = df.iloc[v].copy()
        for col in cols:
            df1[col + "_pc"] = calc_percent_change(df1[col], n=n)
        out.append(df1)

    out = pd.concat(out, ignore_index=True)
    return out


def calc_percent_change(x, n=7):
    out = ((x / x.shift(n)) ** (1 / n) - 1) * 100
    return out
