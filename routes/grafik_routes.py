from flask import Blueprint, render_template
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from services.data_service import load_data

grafik_bp = Blueprint("grafik_page", __name__, url_prefix="/grafik")

@grafik_bp.route("/")
def index():
    df = load_data()
    chart_data = {"historical": {"x": [], "y": []}, "forecast": {"x": [], "y": []}}

    if not df.empty:
        df = df.sort_values("Tanggal")
        chart_data["historical"]["x"] = df["Tanggal"].dt.strftime("%Y-%m-%d").tolist()
        chart_data["historical"]["y"] = df["IHK"].tolist()

        if len(df) > 12:
            model = ExponentialSmoothing(df["IHK"], trend="add", seasonal="add", seasonal_periods=12)
            fit = model.fit()
            forecast = fit.forecast(12)

            forecast_dates = [(df["Tanggal"].iloc[-1] + pd.DateOffset(months=i+1)).strftime("%Y-%m-%d") for i in range(12)]
            chart_data["forecast"]["x"] = forecast_dates
            chart_data["forecast"]["y"] = forecast.tolist()

    return render_template("grafik.html", chart_data=chart_data, page="grafik")
