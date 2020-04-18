# Coronavirus predictions from Good Judgement
# Source: https://goodjudgment.io/covid/dashboard/
# See also: https://pandemic.metaculus.com/questions/
# TODO: us_deaths_rel

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_gl_cases = "out/coronavirus-predict-gl-cases.png"
file_gl_deaths = "out/coronavirus-predict-gl-deaths.png"
file_us_cases = "out/coronavirus-predict-us-cases.png"
file_us_deaths = "out/coronavirus-predict-us-deaths.png"
file_us_deaths_rel = "out/coronavirus-predict-us-deaths-rel.png"


def get_data_manual():
    """Get Coronavirus prediction data from Good Judgement"""
    # TODO: No changes from 2020-04-01 to 2020-04-06
    gl_cases_const = 5.3 * 10 ** np.arange(6, 10)
    gl_deaths_const = 8.0 * 10 ** np.arange(4, 8)
    us_cases_const = 2.3 * 10 ** np.arange(5, 9)
    us_deaths_const = 3.5 * 10 ** np.arange(3, 7)
    us_deaths_rel_const = [1, 10 ** 5, 3 * 10 ** 5, 10 ** 6]

    gl_cases = [
        ["2020-03-20", [0.07, 0.29, 0.50, 0.13], gl_cases_const],
        ["2020-03-21", [0.06, 0.27, 0.50, 0.16], gl_cases_const],
        ["2020-03-22", [0.05, 0.22, 0.46, 0.25], gl_cases_const],
        ["2020-03-23", [0.04, 0.20, 0.46, 0.28], gl_cases_const],
        ["2020-03-24", [0.04, 0.23, 0.47, 0.24], gl_cases_const],
        ["2020-03-25", [0.03, 0.21, 0.49, 0.25], gl_cases_const],
        ["2020-03-26", [0.02, 0.20, 0.52, 0.25], gl_cases_const],
        ["2020-03-27", [0.01, 0.13, 0.49, 0.35], gl_cases_const],
        ["2020-03-28", [0.01, 0.12, 0.48, 0.37], gl_cases_const],
        ["2020-03-29", [0.01, 0.12, 0.48, 0.37], gl_cases_const],
        ["2020-03-30", [0.01, 0.13, 0.53, 0.31], gl_cases_const],
        ["2020-03-31", [0.01, 0.11, 0.53, 0.33], gl_cases_const],
        ["2020-04-01", [0.01, 0.12, 0.54, 0.31], gl_cases_const],
        ["2020-04-07", [0.01, 0.10, 0.56, 0.31], gl_cases_const],
        ["2020-04-08", [0.01, 0.11, 0.57, 0.30], gl_cases_const],
        ["2020-04-09", [0.01, 0.10, 0.57, 0.31], gl_cases_const],
        ["2020-04-10", [0.01, 0.10, 0.57, 0.31], gl_cases_const],
        ["2020-04-11", [0.01, 0.09, 0.58, 0.31], gl_cases_const],
        ["2020-04-12", [0.01, 0.10, 0.60, 0.28], gl_cases_const],
        ["2020-04-13", [0.01, 0.07, 0.61, 0.30], gl_cases_const],
        ["2020-04-14", [0.01, 0.07, 0.61, 0.30], gl_cases_const],
        ["2020-04-15", [0.01, 0.07, 0.61, 0.30], gl_cases_const],
        ["2020-04-16", [0.01, 0.09, 0.61, 0.28], gl_cases_const],
        ["2020-04-17", [0.01, 0.11, 0.60, 0.27], gl_cases_const],
        ["2020-04-18", [0.01, 0.13, 0.58, 0.27], gl_cases_const],
    ]
    gl_deaths = [
        ["2020-03-20", [0.04, 0.33, 0.50, 0.12], gl_deaths_const],
        ["2020-03-21", [0.03, 0.30, 0.52, 0.14], gl_deaths_const],
        ["2020-03-22", [0.03, 0.27, 0.54, 0.14], gl_deaths_const],
        ["2020-03-23", [0.02, 0.32, 0.51, 0.13], gl_deaths_const],
        ["2020-03-24", [0.02, 0.37, 0.46, 0.13], gl_deaths_const],
        ["2020-03-25", [0.02, 0.37, 0.48, 0.11], gl_deaths_const],
        ["2020-03-26", [0.01, 0.31, 0.53, 0.13], gl_deaths_const],
        ["2020-03-27", [0.01, 0.20, 0.55, 0.21], gl_deaths_const],
        ["2020-03-28", [0.01, 0.18, 0.55, 0.24], gl_deaths_const],
        ["2020-03-29", [0.01, 0.18, 0.55, 0.24], gl_deaths_const],
        ["2020-03-30", [0.01, 0.11, 0.54, 0.32], gl_deaths_const],
        ["2020-03-31", [0.01, 0.14, 0.59, 0.24], gl_deaths_const],
        ["2020-04-01", [0.01, 0.16, 0.60, 0.21], gl_deaths_const],
        ["2020-04-07", [0.01, 0.14, 0.65, 0.18], gl_deaths_const],
        ["2020-04-08", [0.01, 0.14, 0.69, 0.15], gl_deaths_const],
        ["2020-04-09", [0.01, 0.14, 0.71, 0.13], gl_deaths_const],
        ["2020-04-10", [0.01, 0.16, 0.70, 0.12], gl_deaths_const],
        ["2020-04-11", [0.01, 0.14, 0.70, 0.14], gl_deaths_const],
        ["2020-04-12", [0.01, 0.13, 0.71, 0.14], gl_deaths_const],
        ["2020-04-13", [0.01, 0.08, 0.68, 0.21], gl_deaths_const],
        ["2020-04-14", [0.00, 0.07, 0.67, 0.24], gl_deaths_const],
        ["2020-04-15", [0.00, 0.09, 0.70, 0.19], gl_deaths_const],
        ["2020-04-16", [0.00, 0.10, 0.71, 0.17], gl_deaths_const],
        ["2020-04-17", [0.00, 0.10, 0.72, 0.16], gl_deaths_const],
        ["2020-04-18", [0.00, 0.09, 0.72, 0.17], gl_deaths_const],
    ]
    us_cases = [
        ["2020-03-20", [0.04, 0.26, 0.41, 0.27], us_cases_const],
        ["2020-03-21", [0.04, 0.31, 0.41, 0.23], us_cases_const],
        ["2020-03-22", [0.03, 0.28, 0.42, 0.26], us_cases_const],
        ["2020-03-23", [0.02, 0.26, 0.41, 0.29], us_cases_const],
        ["2020-03-24", [0.01, 0.27, 0.40, 0.30], us_cases_const],
        ["2020-03-25", [0.01, 0.27, 0.43, 0.27], us_cases_const],
        ["2020-03-26", [0.01, 0.26, 0.48, 0.24], us_cases_const],
        ["2020-03-27", [0.01, 0.18, 0.46, 0.33], us_cases_const],
        ["2020-03-28", [0.01, 0.16, 0.46, 0.35], us_cases_const],
        ["2020-03-29", [0.01, 0.16, 0.46, 0.35], us_cases_const],
        ["2020-03-30", [0.01, 0.11, 0.54, 0.32], us_cases_const],
        ["2020-03-31", [0.01, 0.14, 0.59, 0.24], us_cases_const],
        ["2020-04-01", [0.01, 0.09, 0.58, 0.30], us_cases_const],
        ["2020-04-07", [0.01, 0.03, 0.59, 0.35], us_cases_const],
        ["2020-04-08", [0.01, 0.03, 0.56, 0.39], us_cases_const],
        ["2020-04-09", [0.01, 0.04, 0.55, 0.39], us_cases_const],
        ["2020-04-10", [0.01, 0.04, 0.57, 0.37], us_cases_const],
        ["2020-04-11", [0.01, 0.03, 0.55, 0.39], us_cases_const],
        ["2020-04-12", [0.01, 0.03, 0.56, 0.39], us_cases_const],
        ["2020-04-13", [0.01, 0.03, 0.55, 0.39], us_cases_const],
        ["2020-04-14", [0.00, 0.03, 0.56, 0.39], us_cases_const],
        ["2020-04-15", [0.00, 0.03, 0.55, 0.41], us_cases_const],
        ["2020-04-16", [0.00, 0.03, 0.61, 0.35], us_cases_const],
        ["2020-04-17", [0.00, 0.02, 0.58, 0.39], us_cases_const],
        ["2020-04-18", [0.00, 0.02, 0.58, 0.39], us_cases_const],
    ]
    us_deaths = [
        ["2020-03-20", [0.03, 0.27, 0.53, 0.16], us_deaths_const],
        ["2020-03-21", [0.02, 0.25, 0.57, 0.15], us_deaths_const],
        ["2020-03-22", [0.02, 0.26, 0.54, 0.17], us_deaths_const],
        ["2020-03-23", [0.02, 0.26, 0.52, 0.18], us_deaths_const],
        ["2020-03-24", [0.02, 0.26, 0.53, 0.17], us_deaths_const],
        ["2020-03-25", [0.01, 0.24, 0.56, 0.17], us_deaths_const],
        ["2020-03-26", [0.01, 0.22, 0.58, 0.18], us_deaths_const],
        ["2020-03-27", [0.01, 0.16, 0.59, 0.23], us_deaths_const],
        ["2020-03-28", [0.01, 0.10, 0.62, 0.26], us_deaths_const],
        ["2020-03-29", [0.01, 0.10, 0.62, 0.26], us_deaths_const],
        ["2020-03-30", [0.01, 0.10, 0.64, 0.23], us_deaths_const],
        ["2020-03-31", [0.01, 0.11, 0.56, 0.30], us_deaths_const],
        ["2020-04-01", [0.01, 0.05, 0.69, 0.24], us_deaths_const],
        ["2020-04-07", [0.01, 0.02, 0.67, 0.29], us_deaths_const],
        ["2020-04-08", [0.01, 0.01, 0.70, 0.27], us_deaths_const],
        ["2020-04-09", [0.01, 0.01, 0.74, 0.23], us_deaths_const],
        ["2020-04-10", [0.01, 0.01, 0.72, 0.25], us_deaths_const],
        ["2020-04-11", [0.01, 0.01, 0.73, 0.24], us_deaths_const],
        ["2020-04-12", [0.01, 0.01, 0.73, 0.24], us_deaths_const],
        ["2020-04-13", [0.00, 0.01, 0.74, 0.24], us_deaths_const],
        ["2020-04-14", [0.00, 0.01, 0.72, 0.26], us_deaths_const],
        ["2020-04-15", [0.00, 0.01, 0.75, 0.23], us_deaths_const],
        ["2020-04-16", [0.00, 0.01, 0.72, 0.26], us_deaths_const],
        ["2020-04-17", [0.00, 0.01, 0.72, 0.26], us_deaths_const],
        ["2020-04-18", [0.00, 0.00, 0.76, 0.23], us_deaths_const],
    ]
    us_deaths_rel = [
        ["2020-04-13", [0.02, 0.12, 0.54, 0.29], us_deaths_rel_const],
        ["2020-04-14", [0.02, 0.18, 0.59, 0.19], us_deaths_rel_const],
        ["2020-04-15", [0.01, 0.16, 0.61, 0.20], us_deaths_rel_const],
        ["2020-04-16", [0.03, 0.25, 0.55, 0.16], us_deaths_rel_const],
        ["2020-04-17", [0.04, 0.27, 0.50, 0.17], us_deaths_rel_const],
        ["2020-04-18", [0.04, 0.28, 0.48, 0.18], us_deaths_rel_const],
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


def plot_quantiles(df, p_pred):
    date = df["date"].to_numpy()
    fig, ax = plt.subplots(figsize=(8, 5))

    for i, p in enumerate(p_pred):
        name = "p" + str(int(p * 100))
        q_pred = df[name].to_numpy()
        ax.plot(date, q_pred, label=name, marker=".")
        x_text = ax.lines[i].get_xdata()[-1]
        y_text = ax.lines[i].get_ydata()[-1]
        color = ax.lines[i].get_color()
        ax.annotate(
            f"{np.round(y_text, 6):.6f}", xy=(x_text, y_text), color=color, size=10
        )

    ax.grid()
    ax.legend()
    ax.set_xlim(np.datetime64("2020-03-13"), np.datetime64("2020-05-13"))
    ax.set_ylim(10 ** -6, 10 ** 0)
    ax.set_yscale("log")
    fig.autofmt_xdate()
    return fig


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

plt.close("all")
fig = plot_quantiles(gl_cases, p_pred)
plt.savefig(file_gl_cases)

plt.close("all")
fig = plot_quantiles(gl_deaths, p_pred)
plt.savefig(file_gl_deaths)

plt.close("all")
fig = plot_quantiles(us_cases, p_pred)
plt.savefig(file_us_cases)

plt.close("all")
fig = plot_quantiles(us_deaths, p_pred)
plt.savefig(file_us_deaths)
