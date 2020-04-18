# Average daily change in last n days

import numpy as np
import pandas as pd


def calc_changes(country, state, n=7):
    """Calculate average daily change in last n days"""
    country = country.copy()
    state = state.copy()
    country.columns = [x if x != "country_code" else "code" for x in country.columns]
    country.columns = [x if x != "country_name" else "geo" for x in country.columns]
    state.columns = [x if x != "state_code" else "code" for x in state.columns]
    state.columns = [x if x != "state_name" else "geo" for x in state.columns]

    df = pd.concat([state, country], ignore_index=True)
    df = df[["date", "code", "geo", "pop", "cases", "hospitalized", "deaths"]]
    df = df.sort_values(["date", "code"])

    for x in ["cases", "hospitalized", "deaths"]:
        df[x + "_pc"] = df[x] / df["pop"]

    out = []

    for code in df["code"].unique():
        df1 = df[df["code"] == code].copy()
        df1["cases_chg"] = calc_change(df1["cases"], n=n)
        df1["hospitalized_chg"] = calc_change(df1["hospitalized"], n=n)
        df1["deaths_chg"] = calc_change(df1["deaths"], n=n)
        out.append(df1)

    out = pd.concat(out)
    col = [
        "date",
        "code",
        "geo",
        "pop",
        "cases",
        "cases_pc",
        "cases_chg",
        "deaths",
        "deaths_pc",
        "deaths_chg",
        "hospitalized",
        "hospitalized_pc",
        "hospitalized_chg",
    ]
    out = out[col]
    return out


def calc_change(x, n=7):
    return (x / x.shift(n)) ** (1 / n) - 1
