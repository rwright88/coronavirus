# Plotting and mapping

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from coronavirus.forecast import forecast


def plot_forecast(df, geo="country_name", vals=["cases"], h=1, y_range=[-8, 0]):
    """Plot observed and forecasted by geo and val"""
    n_rows = 3
    n_cols = 5
    val_min_cases = 100
    n_plots = n_rows * n_cols
    top = df[df["date"] == df["date"].max()]
    top = top[top["cases"].rank(method="first", ascending=False) <= n_plots]
    top = sorted(top[geo].tolist())
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    fig, ax = plt.subplots(n_rows, n_cols, sharex="all", sharey="all", figsize=(14, 7))

    for i, plot in enumerate(top):
        row = np.floor(i / n_cols).astype(int)
        col = i - row * n_cols
        df1 = df[(df[geo] == plot) & (df["cases"] >= val_min_cases)]

        for j, val in enumerate(vals):
            if val == "cases":
                val_min = val_min_cases
            else:
                val_min = 10
            obs = df1[val].to_numpy().astype(float)
            obs[obs < val_min] = np.nan
            pred = forecast(obs[~np.isnan(obs)], h, log=True, trend="add", damped=True)
            obs_len = len(obs)
            x_obs = np.arange(obs_len)
            x_pred = np.arange(obs_len, obs_len + h)
            pop = df1["pop"].to_numpy()[0]
            obs = obs / pop
            pred = pred / pop
            color = colors[j]
            ax[row, col].plot(x_obs, obs, color=color, label=val)
            ax[row, col].plot(x_pred, pred, color=color, linestyle="--")

        ax[row, col].grid()
        ax[row, col].set_title(plot)
        ax[row, col].set_xlim(-5, 95)
        ax[row, col].set_ylim(10 ** y_range[0], 10 ** y_range[1])
        ax[row, col].set_xticks([0, 30, 60, 90])
        ax[row, col].set_yscale("log")

    handles, labels = ax[n_rows - 1, n_cols - 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    return fig


def map_by_date(country, state, val="cases", z_range=[-6, 0]):
    """Return dict to make Plotly map of val per person by country/state and date"""
    country = country[(country[val] > 0) & (country["country_code"] != "USA")].copy()
    state = state[state[val] > 0].copy()
    dates_country = country["date"].unique()
    dates_state = state["date"].unique()
    dates = np.sort(dates_country[np.in1d(dates_country, dates_state)])
    data = []

    for date in dates:
        country1 = country[country["date"] == date]
        state1 = state[state["date"] == date]
        rate_country = country1[val].to_numpy() / country1["pop"].to_numpy()
        rate_state = state1[val].to_numpy() / state1["pop"].to_numpy()
        z_country = np.log10(rate_country)
        z_state = np.log10(rate_state)
        name_country = country1["country_name"].tolist()
        name_state = state1["state_name"].tolist()
        disp_country = np.round(rate_country * 10 ** 6, 1)
        disp_state = np.round(rate_state * 10 ** 6, 1)
        text_country = [
            f"{n}: {v:,.1f} per million" for n, v in zip(name_country, disp_country)
        ]
        text_state = [
            f"{n}: {v:,.1f} per million" for n, v in zip(name_state, disp_state)
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


def map_by_date_changes(df, val="cases_chg", z_range=[0, 30]):
    """Return dict to make Plotly map of average daily changes of val by country/state and date"""
    df = df.copy()
    df[val] = df[val] * 100
    ind_states = df["code"].str.len() == 2
    country = df[~ind_states & (df["code"] != "USA")].copy()
    state = df[ind_states].copy()
    dates_country = country["date"].unique()
    dates_state = state["date"].unique()
    dates = np.sort(dates_country[np.in1d(dates_country, dates_state)])
    dates = dates[7:]  # TODO: Temporary
    data = []

    for date in dates:
        country1 = country[country["date"] == date]
        state1 = state[state["date"] == date]

        z_country = country1[val].to_numpy()
        z_state = state1[val].to_numpy()
        name_country = country1["geo"].tolist()
        name_state = state1["geo"].tolist()
        disp_country = np.round(z_country, 1)
        disp_state = np.round(z_state, 1)
        text_country = [
            f"{n}: {v:,.1f}% daily change" for n, v in zip(name_country, disp_country)
        ]
        text_state = [
            f"{n}: {v:,.1f}% daily change" for n, v in zip(name_state, disp_state)
        ]

        data1 = {
            "type": "choropleth",
            "locations": country1["code"],
            "locationmode": "ISO-3",
            "z": z_country,
            "zmin": z_range[0],
            "zmax": z_range[1],
            "text": text_country,
            "hoverinfo": "text",
            "colorscale": "Reds",
            "colorbar_title": "Percent",
        }
        data2 = {
            "type": "choropleth",
            "locations": state1["code"],
            "locationmode": "USA-states",
            "z": z_state,
            "zmin": z_range[0],
            "zmax": z_range[1],
            "text": text_state,
            "hoverinfo": "text",
            "colorscale": "Reds",
            "colorbar_title": "Percent",
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
