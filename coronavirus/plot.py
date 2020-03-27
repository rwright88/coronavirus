# Plotting and mapping
# TODO: plot_forecast() shouldn't change state

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

        obs = df1[val].to_numpy()
        pred = forecast(obs, n=h, log=True, trend="add", damped=True)
        obs_len = len(obs)
        x_obs = np.arange(obs_len)
        x_pred = np.arange(obs_len, obs_len + h)

        pop = df1["pop"].to_numpy()[0]
        obs = obs / pop
        pred = pred / pop

        ax[row, col].plot(x_obs, obs, color="#1f77b4", label=item)
        ax[row, col].plot(x_pred, pred, color="#1f77b4", linestyle="--")
        ax[row, col].set_title(item)
        ax[row, col].set_xlim(-5, 105)
        ax[row, col].set_ylim(10 ** y_range[0], 10 ** y_range[1])
        ax[row, col].set_yscale("log")
        ax[row, col].grid()

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
    plt.savefig(file_out)


def map_by_date(country, state, val="cases", z_range=[-6, 0]):
    """Return dict to make Plotly map of val per person by country and date"""
    country = country[(country[val] > 0) & (country["country_code"] != "USA")].copy()
    state = state[state[val] > 0].copy()
    dates_country = country["date"].unique()
    dates_state = state["date"].unique()
    dates = dates_country[np.in1d(dates_country, dates_state)]
    data = []

    for date in dates:
        country1 = country[country["date"] == date]
        state1 = state[state["date"] == date]
        z_country = np.log10(country1[val].to_numpy() / country1["pop"].to_numpy())
        z_state = np.log10(state1[val].to_numpy() / state1["pop"].to_numpy())

        name_country = country1["country_name"].tolist()
        disp_country = np.round(10 ** -z_country)
        text_country = [
            n + ": 1 in " + f"{v:,.0f}" for n, v in zip(name_country, disp_country)
        ]
        name_state = state1["state_name"].tolist()
        disp_state = np.round(10 ** -z_state)
        text_state = [
            str(n) + ": 1 in " + f"{v:,.0f}" for n, v in zip(name_state, disp_state)
        ]

        data1 = {
            "type": "choropleth",
            "locations": country1["country_code"],
            "locationmode": "ISO-3",
            "z": z_country,
            "zmin": z_range[0],
            "zmax": z_range[1],
            "text": text_country,
            "hoverinfo": "text",
            "colorscale": "Reds",
            "colorbar_title": "log10(" + val + ")",
        }
        data2 = {
            "type": "choropleth",
            "locations": state1["state_code"],
            "locationmode": "USA-states",
            "z": z_state,
            "zmin": z_range[0],
            "zmax": z_range[1],
            "text": text_state,
            "hoverinfo": "text",
            "colorscale": "Reds",
            "colorbar_title": "log10(" + val + ")",
        }
        data.append(data1)
        data.append(data2)

    data_len = len(data)
    steps_len = len(dates)
    steps = []

    for i in range(steps_len):
        step = {
            "method": "restyle",
            "args": ["visible", [False] * data_len],
            "label": np.datetime_as_string(dates[i], unit="D"),
        }
        step["args"][1][i * 2] = True
        step["args"][1][i * 2 + 1] = True
        steps.append(step)

    sliders = [{"active": steps_len - 1, "pad": {"t": 25}, "steps": steps}]

    geo = {
        "countrywidth": 0.5,
        "subunitwidth": 0.5,
        "landcolor": "#888",
        "projection": {"type": "natural earth"},
        "showcountries": True,
        "showsubunits": True,
        "showlakes": False,
    }
    layout = {
        "geo": geo,
        "sliders": sliders,
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    }
    fig = {"data": data, "layout": layout}
    return fig
