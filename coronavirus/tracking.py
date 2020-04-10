# Coronavirus tracking data

import io

import numpy as np
import pandas as pd
import requests

from coronavirus.utils import fill_dates


def get_tracking():
    """Get Coronavirus tracking data"""
    url = "http://covidtracking.com/api/states/daily.csv"
    r = requests.get(url)
    data = io.StringIO(r.text)
    df = pd.read_csv(data)
    df = df[["date", "state", "positive", "hospitalized", "death"]]
    df.columns = ["date", "state_code", "cases", "hospitalized", "deaths"]
    df["date"] = pd.to_datetime(df["date"].astype(str))
    df = fill_dates(df, geo="state_code")
    return df
