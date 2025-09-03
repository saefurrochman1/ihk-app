import pandas as pd
import os

DATA_PATH = "data/ihk.xlsx"

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        return df
    else:
        return pd.DataFrame(columns=["Tanggal", "IHK"])

def save_data(df):
    df.to_excel(DATA_PATH, index=False)
