# Get data, forecast, and plot
# Plots are currently saved in directory "out"
# Maps are currently opened in a browser

import numpy as np
import pandas as pd
from plotly import offline

import coronavirus as cv

np.seterr(all="ignore")

# data -----

pop_country = cv.get_pop_country()
pop_state = cv.get_pop_state()

country = cv.get_hopkins()
country = pd.merge(country, pop_country, how="left", on="country_name")

state = cv.get_tracking()
state = pd.merge(state, pop_state, how="left", on="state_code")

# forecast and plot -----

rc = [-6, 0]
rh = [-6, -2]
rd = [-6, -2]
h = 14

cv.plot_forecast(country, val="cases", geo="country_name", h=h, y_range=rc)
cv.plot_forecast(country, val="deaths", geo="country_name", h=h, y_range=rd)

cv.plot_forecast(state, val="cases", geo="state_name", h=h, y_range=rc)
cv.plot_forecast(state, val="hospitalized", geo="state_name", h=h, y_range=rh)
cv.plot_forecast(state, val="deaths", geo="state_name", h=h, y_range=rd)

# map -----

offline.plot(
    cv.map_by_date(country, state, val="cases", z_range=rc),
    filename="out/coronavirus-map-cases.html",
)
offline.plot(
    cv.map_by_date(country, state, val="deaths", z_range=rd),
    filename="out/coronavirus-map-deaths.html",
)
