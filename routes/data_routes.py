from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
from services.data_service import load_data, save_data

data_bp = Blueprint("data_page", __name__, url_prefix="/data")

@data_bp.route("/", methods=["GET", "POST"])
def index():
    df = load_data()

    # Tambah data
    if request.method == "POST":
        tanggal = request.form["tanggal"]
        ihk = float(request.form["ihk"])
        new_row = pd.DataFrame({"Tanggal": [pd.to_datetime(tanggal)], "IHK": [ihk]})
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        return redirect(url_for("data_page.index"))

    return render_template(
        "data.html",
        data=df.reset_index().to_dict(orient="records"),
        page="data"
    )

# Hapus data
@data_bp.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    df = load_data()
    if 0 <= index < len(df):
        df = df.drop(index).reset_index(drop=True)
        save_data(df)
    return redirect(url_for("data_page.index"))

# Edit data
@data_bp.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    df = load_data()
    if 0 <= index < len(df):
        tanggal = request.form["tanggal"]
        ihk = float(request.form["ihk"])
        df.at[index, "Tanggal"] = pd.to_datetime(tanggal)
        df.at[index, "IHK"] = ihk
        save_data(df)
    return redirect(url_for("data_page.index"))
