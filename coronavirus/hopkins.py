# Coronavirus Johns Hopkins data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from coronavirus.population import fix_country_name
from coronavirus.utils import fill_dates


def get_hopkins():
    """Get Johns Hopkins coronavirus cases and deaths data"""
    file_cases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    file_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    cases = pd.read_csv(file_cases)
    deaths = pd.read_csv(file_deaths)
    col_geo = ["state_name", "country_name", "lat", "long"]
    cases.columns = col_geo + cases.columns.tolist()[4:]
    deaths.columns = col_geo + deaths.columns.tolist()[4:]
    deaths = deaths.iloc[:, [0, 1] + list(range(4, deaths.shape[1]))]
    cases = pd.melt(cases, id_vars=col_geo, var_name="date", value_name="cases")
    deaths = pd.melt(
        deaths,
        id_vars=["state_name", "country_name"],
        var_name="date",
        value_name="deaths",
    )

    df = pd.merge(cases, deaths, how="left", on=["state_name", "country_name", "date"])
    df["date"] = pd.to_datetime(df["date"])
    df["country_name"] = fix_country_name(df["country_name"])

    agg = {"cases": "sum", "deaths": "sum"}
    df = df.groupby(["date", "country_name"]).agg(agg).reset_index()
    df = df[["date", "country_name", "cases", "deaths"]]
    df = fill_dates(df)
    return df
