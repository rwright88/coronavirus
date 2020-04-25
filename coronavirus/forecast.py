# Forecast

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from coronavirus.utils import ffill


def forecast_all(df, h=1):
    """Forecast for each code in df"""
    df = df[~df["pop"].isna()]
    df = df.sort_values(["code", "date"])
    cols = ["cases", "deaths"]
    out = []
    ind = df.groupby("code").indices

    for k, v in ind.items():
        df1 = df.iloc[v].copy()
        code = df1["code"].to_numpy()[0]
        name = df1["name"].to_numpy()[0]
        pop = df1["pop"].to_numpy()[0]

        for col in cols:
            val_min = _get_val_min(col, pop)
            dates = pd.date_range(
                df1["date"].min(), df1["date"].max() + pd.Timedelta(h, "D")
            )
            obs = ffill(df1[col].to_numpy())
            obs_fc = obs[obs >= val_min]
            pred = _forecast(obs_fc, h)
            types = ["observed"] * len(obs) + ["predicted"] * len(pred)
            vals = np.concatenate([obs, pred])
            res = {
                "code": code,
                "name": name,
                "date": dates,
                "type": types,
                "pop": pop,
                "col": col,
                "val": vals,
            }
            res = pd.DataFrame(res)
            out.append(res)

    out = pd.concat(out, ignore_index=True)
    by = ["code", "name", "date", "type", "pop"]
    out = pd.pivot_table(out, index=by, columns="col", values="val").reset_index()
    return out


def _get_val_min(col, pop):
    if col == "cases":
        val_min = 10 * pop / 1e06
    elif col == "deaths":
        val_min = 1 * pop / 1e06
    else:
        return ValueError("Invalid column name")
    return val_min


def _forecast(y, h):
    """Prediction of exponential smoothing forecast"""
    size_min = 10
    log = True
    trend = "add"
    damped = True
    smoothing_level = None
    damping_slope = None

    y = np.asarray(y)
    size = len(y)
    if size < size_min:
        return np.full(h, np.nan, float)
    start = size
    end = size + h - 1

    if log == False:
        mod = ExponentialSmoothing(y, trend=trend, damped=damped)
        mod = mod.fit(smoothing_level=smoothing_level, damping_slope=damping_slope)
        pred = mod.predict(start=start, end=end)
    elif log == True:
        mod = ExponentialSmoothing(np.log(y), trend=trend, damped=damped)
        mod = mod.fit(smoothing_level=smoothing_level, damping_slope=damping_slope)
        pred = np.exp(mod.predict(start=start, end=end))

    return pred
