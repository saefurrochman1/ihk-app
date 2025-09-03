from flask import Blueprint, render_template
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from services.data_service import load_data

forecast_bp = Blueprint("forecast_page", __name__, url_prefix="/forecast")

@forecast_bp.route("/")
def index():
    df = load_data()
    forecast_dict = None
    if len(df) > 12:
        df = df.sort_values("Tanggal")
        model = ExponentialSmoothing(df["IHK"], trend="add", seasonal="add", seasonal_periods=12)
        fit = model.fit()
        forecast = fit.forecast(12)

        forecast_dict = {
            (df["Tanggal"].iloc[-1] + pd.DateOffset(months=i+1)).strftime("%b-%Y"): round(val, 2)
            for i, val in enumerate(forecast)
        }

    return render_template("forecast.html", forecast=forecast_dict, page="forecast")
