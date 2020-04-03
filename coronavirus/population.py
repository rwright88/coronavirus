# Get population data

import numpy as np
import pandas as pd
import requests


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
