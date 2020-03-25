# Get data, forecast, and plot
# Plots are currently saved in directory "out"
# Maps are currently opened in a browser
# TODO: Plot and map function shouldn't change state

import numpy as np
import pandas as pd

import coronavirus as cv

np.seterr(all="ignore")

# data -----

pop_country = cv.get_pop_country()
pop_state = cv.get_pop_state()

hopkins = cv.get_hopkins()
hopkins = pd.merge(hopkins, pop_country, how="left", on="country_name")

tracking = cv.get_tracking()
tracking = pd.merge(tracking, pop_state, how="left", on="state_code")

# forecast and plot -----

rc = [-6, 0]
rh = [-6, -2]
rd = [-6, -2]
h = 14

cv.plot_forecast(hopkins, val="cases", geo="country_name", h=h, y_range=rc)
cv.plot_forecast(hopkins, val="deaths", geo="country_name", h=h, y_range=rd)

cv.plot_forecast(tracking, val="cases", geo="state_name", h=h, y_range=rc)
cv.plot_forecast(tracking, val="hospitalized", geo="state_name", h=h, y_range=rh)
cv.plot_forecast(tracking, val="deaths", geo="state_name", h=h, y_range=rd)

cv.map_latest(hopkins, tracking, val="cases", z_range=rc)
# cv.map_latest(hopkins, tracking, val="hospitalized", z_range=rh)
cv.map_latest(hopkins, tracking, val="deaths", z_range=rd)
