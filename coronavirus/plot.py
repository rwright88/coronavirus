# Plotting and mapping
# TODO: Plot function with matplotlib should not change state

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from coronavirus.forecast import forecast


def plot_forecast(df, val="cases", geo="country_name", h=1, y_range=[-6, 0]):
    """Plot observed and forecasted val by geo"""
    file_out = "out/coronavirus-" + val + "-" + geo[:-5] + ".png"
    n_rows = 2
    n_cols = 5
    n_items = n_rows * n_cols
    top = df[df["date"] == df["date"].max()].sort_values(val, ascending=False)
    top = sorted(top.iloc[:n_items][geo].tolist())

    if val == "cases":
        val_min = 100
    else:
        val_min = 10

    plt.close("all")
    fig, ax = plt.subplots(n_rows, n_cols, sharex="all", sharey="all", figsize=(12, 5))

    for count, item in enumerate(top):
        row = np.floor(count / n_cols).astype(int)
        col = count - row * n_cols
        df1 = df[(df[geo] == item) & (df[val] >= val_min)]
        if df1.shape[0] < 3:
            continue
        dates = [df1["date"].min(), df1["date"].max()]
        x_obs = pd.date_range(dates[0], dates[1]).to_numpy()
        x_pred = pd.date_range(
            dates[1] + pd.Timedelta(days=1), dates[1] + pd.Timedelta(days=h)
        ).to_numpy()
        obs = df1[val].to_numpy()
        pred = forecast(obs, n=h, log=True, trend="add", damped=True)

        pop = df1["pop"].to_numpy()[0]
        obs = obs / pop
        pred = pred / pop

        ax[row, col].plot(x_obs, obs, color="#1f77b4", label=item)
        ax[row, col].plot(x_pred, pred, color="#1f77b4", linestyle="--")
        ax[row, col].set_title(item)
        ax[row, col].set_ylim(10 ** y_range[0], 10 ** y_range[1])
        ax[row, col].set_yscale("log")
        ax[row, col].grid()

    fig.autofmt_xdate()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
    plt.savefig(file_out)


def map_latest(country, state, val="cases", z_range=[-6, 0]):
    country = country[
        (country["date"] == country["date"].max())
        & (country[val] > 0)
        & (country["country_code"] != "USA")
    ]
    state = state[(state["date"] == state["date"].max()) & (state[val] > 0)]
    z_country = np.log10(country[val].to_numpy() / country["pop"].to_numpy())
    z_state = np.log10(state[val].to_numpy() / state["pop"].to_numpy())

    data1 = {
        "locations": country["country_code"],
        "locationmode": "ISO-3",
        "z": z_country,
        "zmin": z_range[0],
        "zmax": z_range[1],
        "colorscale": "Blues",
        "colorbar_title": "log10(" + val + ")",
    }
    data2 = {
        "locations": state["state_code"],
        "locationmode": "USA-states",
        "z": z_state,
        "zmin": z_range[0],
        "zmax": z_range[1],
        "colorscale": "Blues",
        "colorbar_title": "log10(" + val + ")",
    }
    geo = {
        "countrywidth": 0.5,
        "subunitwidth": 0.5,
        "landcolor": "#888",
        "projection_type": "natural earth",
        "showcountries": True,
        "showsubunits": True,
        "showlakes": False,
    }
    fig = go.Figure([go.Choropleth(**data1), go.Choropleth(**data2)])
    fig.update_geos(**geo)
    fig.show()
