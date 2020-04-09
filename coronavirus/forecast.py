# Forecast

import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def forecast(y, n, log=False, trend="add", damped=False):
    """Prediction of exponential smoothing forecast"""
    y = np.array(y)
    size = len(y)
    if size < 2:
        return np.full(n, np.nan, float)
    start = size
    end = size + n - 1
    if log == False:
        mod = ExponentialSmoothing(y, trend=trend, damped=damped).fit()
        pred = mod.predict(start=start, end=end)
    elif log == True:
        mod = ExponentialSmoothing(np.log(y), trend=trend, damped=damped).fit()
        pred = np.exp(mod.predict(start=start, end=end))
    return pred
