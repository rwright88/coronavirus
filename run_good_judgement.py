# Coronavirus predictions from Good Judgement
# https://goodjudgment.io/covid/dashboard/
# See also: https://pandemic.metaculus.com/questions/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_data_manual():
    """Get Coronavirus prediction data from Good Judgement"""
    gl_cases = [
        ["2020-03-20", [0.07, 0.29, 0.50, 0.13], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-21", [0.06, 0.27, 0.50, 0.16], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-22", [0.05, 0.22, 0.46, 0.25], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-23", [0.04, 0.20, 0.46, 0.28], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-24", [0.04, 0.23, 0.47, 0.24], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-25", [0.03, 0.21, 0.49, 0.25], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-26", [0.02, 0.20, 0.52, 0.25], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-27", [0.01, 0.13, 0.49, 0.35], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-28", [0.01, 0.12, 0.48, 0.37], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-29", [0.01, 0.12, 0.48, 0.37], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-30", [0.01, 0.13, 0.53, 0.31], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-03-31", [0.01, 0.11, 0.53, 0.33], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-04-01", [0.01, 0.12, 0.54, 0.31], 5.3 * 10 ** np.arange(6, 10)],
        ["2020-04-02", [0.01, 0.12, 0.54, 0.31], 5.3 * 10 ** np.arange(6, 10)],
    ]
    gl_deaths = [
        ["2020-03-20", [0.04, 0.33, 0.50, 0.12], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-21", [0.03, 0.30, 0.52, 0.14], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-22", [0.03, 0.27, 0.54, 0.14], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-23", [0.02, 0.32, 0.51, 0.13], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-24", [0.02, 0.37, 0.46, 0.13], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-25", [0.02, 0.37, 0.48, 0.11], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-26", [0.01, 0.31, 0.53, 0.13], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-27", [0.01, 0.20, 0.55, 0.21], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-28", [0.01, 0.18, 0.55, 0.24], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-29", [0.01, 0.18, 0.55, 0.24], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-30", [0.01, 0.11, 0.54, 0.32], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-03-31", [0.01, 0.14, 0.59, 0.24], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-04-01", [0.01, 0.16, 0.60, 0.21], 8.0 * 10 ** np.arange(4, 8)],
        ["2020-04-02", [0.01, 0.16, 0.60, 0.21], 8.0 * 10 ** np.arange(4, 8)],
    ]
    us_cases = [
        ["2020-03-20", [0.04, 0.26, 0.41, 0.27], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-21", [0.04, 0.31, 0.41, 0.23], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-22", [0.03, 0.28, 0.42, 0.26], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-23", [0.02, 0.26, 0.41, 0.29], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-24", [0.01, 0.27, 0.40, 0.30], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-25", [0.01, 0.27, 0.43, 0.27], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-26", [0.01, 0.26, 0.48, 0.24], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-27", [0.01, 0.18, 0.46, 0.33], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-28", [0.01, 0.16, 0.46, 0.35], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-29", [0.01, 0.16, 0.46, 0.35], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-30", [0.01, 0.11, 0.54, 0.32], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-03-31", [0.01, 0.14, 0.59, 0.24], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-04-01", [0.01, 0.09, 0.58, 0.30], 2.3 * 10 ** np.arange(5, 9)],
        ["2020-04-02", [0.01, 0.09, 0.58, 0.30], 2.3 * 10 ** np.arange(5, 9)],
    ]
    us_deaths = [
        ["2020-03-20", [0.03, 0.27, 0.53, 0.16], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-21", [0.02, 0.25, 0.57, 0.15], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-22", [0.02, 0.26, 0.54, 0.17], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-23", [0.02, 0.26, 0.52, 0.18], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-24", [0.02, 0.26, 0.53, 0.17], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-25", [0.01, 0.24, 0.56, 0.17], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-26", [0.01, 0.22, 0.58, 0.18], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-27", [0.01, 0.16, 0.59, 0.23], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-28", [0.01, 0.10, 0.62, 0.26], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-29", [0.01, 0.10, 0.62, 0.26], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-30", [0.01, 0.10, 0.64, 0.23], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-03-31", [0.01, 0.11, 0.56, 0.30], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-04-01", [0.01, 0.05, 0.69, 0.24], 3.5 * 10 ** np.arange(3, 7)],
        ["2020-04-02", [0.01, 0.05, 0.69, 0.24], 3.5 * 10 ** np.arange(3, 7)],
    ]
    return [gl_cases, gl_deaths, us_cases, us_deaths]


def calc_quantiles(x, p_pred):
    dates = []
    q_preds = []

    for i in range(len(x)):
        row = x[i]
        date = row[0]
        p_obs = np.cumsum(row[1])
        q_obs = np.log(row[2])
        q_pred = np.exp(np.interp(p_pred, p_obs, q_obs, left=np.nan, right=np.nan))
        dates.append(date)
        q_preds.append(q_pred)

    names = ["p" + str(int(p * 100)) for p in p_pred]
    df = pd.DataFrame(q_preds, columns=names)
    df["date"] = np.array(dates, dtype="datetime64[D]")
    df = df[["date"] + names]
    return df


def plot_quantiles(df, p_pred, file_out):
    date = df["date"].to_numpy()
    plt.close("all")
    fig, ax = plt.subplots(figsize=(8, 5))

    for p in p_pred:
        name = "p" + str(int(p * 100))
        q_pred = df[name].to_numpy()
        ax.plot(date, q_pred, label=name, marker=".")

    ax.grid()
    ax.legend()
    ax.set_xlim(np.datetime64("2020-03-13"), np.datetime64("2020-04-13"))
    ax.set_ylim(10 ** -6, 10 ** 0)
    ax.set_yscale("log")
    fig.autofmt_xdate()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
    plt.savefig(file_out)


# run -----

p_pred = [0.25, 0.5, 0.75]
gl_pop = 7.7 * 10 ** 9
us_pop = 3.3 * 10 ** 8

data = get_data_manual()

gl_cases = calc_quantiles(data[0], p_pred)
gl_deaths = calc_quantiles(data[1], p_pred)
us_cases = calc_quantiles(data[2], p_pred)
us_deaths = calc_quantiles(data[3], p_pred)

gl_cases.iloc[:, 1:] = gl_cases.iloc[:, 1:] / gl_pop
gl_deaths.iloc[:, 1:] = gl_deaths.iloc[:, 1:] / gl_pop
us_cases.iloc[:, 1:] = us_cases.iloc[:, 1:] / us_pop
us_deaths.iloc[:, 1:] = us_deaths.iloc[:, 1:] / us_pop

plot_quantiles(gl_cases, p_pred, file_out="out/coronavirus-predict-gl-cases.png")
plot_quantiles(gl_deaths, p_pred, file_out="out/coronavirus-predict-gl-deaths.png")
plot_quantiles(us_cases, p_pred, file_out="out/coronavirus-predict-us-cases.png")
plot_quantiles(us_deaths, p_pred, file_out="out/coronavirus-predict-us-deaths.png")
