# Coronavirus data analysis

import numpy as np
import pandas as pd
from plotly import offline

import coronavirus as cv
from coronavirus.utils import profile, summary

np.seterr(all="ignore")

h = 30
n = 7

file_stats = "out/coronavirus-stats.csv"
file_stats_now = "out/coronavirus-stats-now.csv"

file_plot_cases = "out/coronavirus-plot-cases.html"
file_plot_deaths = "out/coronavirus-plot-deaths.html"
file_plot_cases_changes = "out/coronavirus-plot-cases-changes.html"
file_plot_deaths_changes = "out/coronavirus-plot-deaths-changes.html"

file_map_cases = "out/coronavirus-map-cases.html"
file_map_deaths = "out/coronavirus-map-deaths.html"
file_map_cases_changes = "out/coronavirus-map-cases-changes.html"
file_map_deaths_changes = "out/coronavirus-map-deaths-changes.html"

# Data and stats -----

df = cv.get_data()
df = cv.forecast_all(df, h=h)
df = cv.calc_stats(df, n=n)

df.to_csv(file_stats, index=False)

obs = df[df["type"] == "observed"]
now = obs[(obs["date"] == obs["date"].max()) & (obs["pop"] >= 1e06)]
now.to_csv(file_stats_now, index=False)

# Plot -----

obs_plot = obs[obs["pop"] >= 5e6]

data = cv.plot_trend(obs_plot, val="cases_pm")
offline.plot(data, filename=file_plot_cases, auto_open=False)

data = cv.plot_trend(obs_plot, val="deaths_pm")
offline.plot(data, filename=file_plot_deaths, auto_open=False)

data = cv.plot_trend(obs_plot, val="cases_pc")
offline.plot(data, filename=file_plot_cases_changes, auto_open=False)

data = cv.plot_trend(obs_plot, val="deaths_pc")
offline.plot(data, filename=file_plot_deaths_changes, auto_open=False)

# Map -----

data = cv.map_by_date(obs, val="cases_pm")
offline.plot(data, filename=file_map_cases, auto_open=False)

data = cv.map_by_date(obs, val="deaths_pm")
offline.plot(data, filename=file_map_deaths, auto_open=False)

data = cv.map_by_date(obs, val="cases_pc")
offline.plot(data, filename=file_map_cases_changes, auto_open=False)

data = cv.map_by_date(obs, val="deaths_pc")
offline.plot(data, filename=file_map_deaths_changes, auto_open=False)
