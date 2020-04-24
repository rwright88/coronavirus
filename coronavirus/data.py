# Get data

import io

import numpy as np
import pandas as pd
import requests

from coronavirus.utils import fill_dates


def get_data():
    country = get_hopkins()
    pop_country = get_pop_country()
    country = pd.merge(country, pop_country, how="left", on="country_name")

    state = get_tracking()
    pop_state = get_pop_state()
    state = pd.merge(state, pop_state, how="left", on="state_code")

    country.columns = [x if x != "country_code" else "code" for x in country.columns]
    country.columns = [x if x != "country_name" else "name" for x in country.columns]
    state.columns = [x if x != "state_code" else "code" for x in state.columns]
    state.columns = [x if x != "state_name" else "name" for x in state.columns]

    df = pd.concat([state, country], ignore_index=True)
    df = df[["code", "name", "date", "pop", "cases", "deaths"]]
    return df


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
    df = fill_dates(df, "country_name")
    return df


def get_tracking():
    """Get Coronavirus tracking data"""
    url = "http://covidtracking.com/api/states/daily.csv"
    r = requests.get(url)
    data = io.StringIO(r.text)
    df = pd.read_csv(data)
    df = df[["date", "state", "positive", "hospitalized", "death"]]
    df.columns = ["date", "state_code", "cases", "hospitalized", "deaths"]
    df["date"] = pd.to_datetime(df["date"].astype(str))
    df = fill_dates(df, "state_code")
    return df


def get_pop_country():
    """Get population by country from worldometers"""
    url_pop = "https://www.worldometers.info/world-population/population-by-country/"
    url_cw = "https://www.worldometers.info/country-codes/"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    r = requests.get(url_pop, headers=header)
    df = pd.read_html(r.text)[0]
    df = df.iloc[:, [1, 2]]
    df.columns = ["country_name", "pop"]
    df["country_name"] = [x.lower() for x in df["country_name"].tolist()]

    r = requests.get(url_cw, headers=header)
    cw = pd.read_html(r.text)[0]
    cw = cw.iloc[:, [3, 0]]
    cw.columns = ["country_code", "country_name"]
    cw["country_name"] = [x.lower() for x in cw["country_name"].tolist()]

    df = pd.merge(df, cw, how="left", on="country_name")
    df = df[["country_code", "country_name", "pop"]]
    return df


def get_pop_state():
    """Get population by state from US Census"""
    file1 = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/SCPRC-EST2019-18+POP-RES.csv"
    df = pd.read_csv(file1)
    df = df[df["SUMLEV"] == 40]
    df = df[["NAME", "POPESTIMATE2019"]]
    df.columns = ["state_name", "pop"]
    df["state_name"] = [x.lower() for x in df["state_name"].tolist()]
    cw = pd.read_csv("data/state-postal.csv")
    df = pd.merge(df, cw, how="left", on="state_name")
    df = df[["state_code", "state_name", "pop"]]
    return df


def fix_country_name(x):
    """Fix country name to be consistent with worldometers"""
    x = pd.Series([str(e).lower() for e in x])
    x[x.str.contains("brazzaville")] = "congo"
    x[x == "cote d'ivoire"] = "côte d'ivoire"
    x[x.str.contains("czechia")] = "czech republic (czechia)"
    x[x.str.contains("kinshasa")] = "dr congo"
    x[x == "burma"] = "myanmar"
    x[x == "korea, south"] = "south korea"
    x[x.str.contains("taiwan")] = "taiwan"
    x[(x == "uk") | x.str.contains("united kingdom")] = "united kingdom"
    x[(x == "us") | x.str.contains("united states")] = "united states"
    return x
