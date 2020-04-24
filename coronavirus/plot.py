# Plotting and mapping

import numpy as np
import pandas as pd


def plot_trend(df, val="cases_pm"):
    """Plot trend"""
    params = _get_params_plot(val)
    val_min = params["val_min"]
    text_per = params["text_per"]
    title = params["title"]
    y_type = params["y_type"]
    y_tickvals = params["y_tickvals"]

    if val in ["cases_pm", "deaths_pm"]:
        df = df[df[val] >= val_min].copy()
    elif val == "cases_pc":
        df = df[df["cases_pm"] >= val_min].copy()
    elif val == "deaths_pc":
        df = df[df["deaths_pm"] >= val_min].copy()

    top = df[df["date"] == df["date"].max()].sort_values("pop", ascending=False)
    top = top["code"].tolist()
    data = []

    for i, code in enumerate(top):
        df1 = df[df["code"] == code]
        name = df1["name"].to_numpy()[0]
        x = np.arange(len(df1["date"]))
        y = df1[val].to_numpy()
        text = np.array(
            [f"{name} - day {d}: {v:,.1f} {text_per}" for d, v in zip(x, y)]
        )
        color = "#1f77b4"

        data1 = {
            "type": "scatter",
            "mode": "lines",
            "x": x,
            "y": y,
            "name": name,
            "text": text,
            "hoverinfo": "text",
            "opacity": 0.2,
            "showlegend": False,
            "line": {"color": color},
        }
        data2 = {
            "type": "scatter",
            "mode": "markers+text",
            "x": [x[-1]],
            "y": [y[-1]],
            "name": name,
            "text": name,
            "textposition": "middle right",
            "showlegend": False,
            "hoverinfo": "skip",
            "marker": {"color": color},
            "textfont": {"color": color},
        }
        data.append(data1)
        data.append(data2)

    layout = {
        "title": title,
        "width": 1200,
        "height": 800,
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
        "xaxis": {"gridcolor": "#ddd", "zeroline": False},
        "yaxis": {
            "gridcolor": "#ddd",
            "zeroline": False,
            "type": y_type,
            "tickvals": y_tickvals,
        },
        "paper_bgcolor": "#fff",
        "plot_bgcolor": "#fff",
    }
    fig = {"data": data, "layout": layout}
    return fig


def map_by_date(df, val="cases_pm"):
    """Map by country/state and date"""
    params = _get_params_map(val)
    text_per = params["text_per"]
    title = params["title"]
    z_range = params["z_range"]

    ind_states = df["code"].str.len() == 2
    country = df[~ind_states & (df["code"] != "USA")].copy()
    state = df[ind_states].copy()
    dates_country = country["date"].unique()
    dates_state = state["date"].unique()
    dates = np.sort(dates_country[np.in1d(dates_country, dates_state)])
    data = []

    for date in dates:
        country1 = country[country["date"] == date]
        state1 = state[state["date"] == date]
        name_country = country1["name"].tolist()
        name_state = state1["name"].tolist()

        if val in ["cases_pm", "deaths_pm"]:
            z_country = np.log10(country1[val].to_numpy())
            z_state = np.log10(state1[val].to_numpy())
            disp_country = np.round(10 ** z_country, 1)
            disp_state = np.round(10 ** z_state, 1)
        elif val in ["cases_pc", "deaths_pc"]:
            z_country = country1[val].to_numpy()
            z_state = state1[val].to_numpy()
            disp_country = np.round(z_country, 1)
            disp_state = np.round(z_state, 1)

        text_country = [
            f"{n}: {v:,.1f} {text_per}" for n, v in zip(name_country, disp_country)
        ]
        text_state = [
            f"{n}: {v:,.1f} {text_per}" for n, v in zip(name_state, disp_state)
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
            "colorbar_title": "TODO",
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
            "colorbar_title": "TODO",
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
        "title": title,
        "geo": geo,
        "sliders": sliders,
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    }
    fig = {"data": data, "layout": layout}
    return fig


def _get_params_plot(val):
    if val == "cases_pm":
        text_per = "per million"
        val_min = 10
        title = "Cases per million people, by country and US state"
        y_type = "log"
        y_tickvals = 10 ** np.arange(7)
    elif val == "deaths_pm":
        text_per = "per million"
        val_min = 1
        title = "Deaths per million people, by country and US state"
        y_type = "log"
        y_tickvals = 10 ** np.arange(7)
    elif val == "cases_pc":
        text_per = "percent change"
        val_min = 10
        title = "Average daily percent change of cases in last 7 days, by country and US state"
        y_type = "linear"
        y_tickvals = None
    elif val == "deaths_pc":
        text_per = "percent change"
        val_min = 1
        title = "Average daily percent change of deaths in last 7 days, by country and US state"
        y_type = "linear"
        y_tickvals = None
    else:
        raise ValueError("Invalid val")

    out = {
        "val_min": val_min,
        "text_per": text_per,
        "title": title,
        "y_type": y_type,
        "y_tickvals": y_tickvals,
    }
    return out


def _get_params_map(val):
    if val == "cases_pm":
        text_per = "per million"
        title = "Cases per million people, by country and US state"
        z_range = [1, 5]
    elif val == "deaths_pm":
        text_per = "per million"
        title = "Deaths per million people, by country and US state"
        z_range = [0, 3]
    elif val == "cases_pc":
        text_per = "percent change"
        title = "Average daily percent change of cases in last 7 days, by country and US state"
        z_range = [0, 30]
    elif val == "deaths_pc":
        text_per = "percent change"
        title = "Average daily percent change of deaths in last 7 days, by country and US state"
        z_range = [0, 30]
    else:
        raise ValueError("Invalid val")

    out = {
        "text_per": text_per,
        "title": title,
        "z_range": z_range,
    }
    return out
