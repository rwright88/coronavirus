# Get data, forecast, and plot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotly import offline

import coronavirus as cv

file_changes = "out/coronavirus-table-changes.csv"
file_plot_country = "out/coronavirus-trend-country.png"
file_plot_state = "out/coronavirus-trend-state.png"
file_map_cases = "out/coronavirus-map-cases.html"
file_map_deaths = "out/coronavirus-map-deaths.html"
file_map_cases_changes = "out/coronavirus-map-cases-changes.html"
file_map_deaths_changes = "out/coronavirus-map-deaths-changes.html"

np.seterr(all="ignore")

# Data -----

pop_country = cv.get_pop_country()
pop_state = cv.get_pop_state()

country = cv.get_hopkins()
country = pd.merge(country, pop_country, how="left", on="country_name")

state = cv.get_tracking()
state = pd.merge(state, pop_state, how="left", on="state_code")

# Average daily change -----

changes = cv.calc_changes(country, state, n=7)
ind = (changes["date"] == changes["date"].max()) & (changes["pop"] >= 10 ** 6)
changes[ind].to_csv(file_changes, index=False)

# Forecast and plot -----

h = 30
y_range = [-8, 0]

plt.close("all")
geo = "country_name"
vals = ["cases", "deaths"]
fig = cv.plot_forecast(country, geo=geo, vals=vals, h=h, y_range=y_range)
plt.savefig(file_plot_country)

plt.close("all")
geo = "state_name"
vals = ["cases", "deaths", "hospitalized"]
fig = cv.plot_forecast(state, geo=geo, vals=vals, h=h, y_range=y_range)
plt.savefig(file_plot_state)

# Map -----

data = cv.map_by_date(country, state, val="cases", z_range=[-6, 0])
offline.plot(data, filename=file_map_cases)

data = cv.map_by_date(country, state, val="deaths", z_range=[-6, -2])
offline.plot(data, filename=file_map_deaths)

data = cv.map_by_date_changes(changes, val="cases_chg", z_range=[0, 30])
offline.plot(data, filename=file_map_cases_changes)

data = cv.map_by_date_changes(changes, val="deaths_chg", z_range=[0, 30])
offline.plot(data, filename=file_map_deaths_changes)
