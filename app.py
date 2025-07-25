import streamlit as st
import pandas as pd
from utils.forecast import predict_consumption
from utils.visualizer import plot_forecast
from utils.anomaly import detect_anomalies
from utils.visualizer import plot_timeseries_with_anomalies

st.set_page_config(page_title="WattDash", layout="wide")
st.title("⚡ WattDash - Energy Intelligence Dashboard")

use_sample = st.sidebar.checkbox("📂 Gerçek veriyi kullan (Open Power Data)")

df = None

if use_sample:
    df = pd.read_csv("data/time_series_60min_singleindex.csv", index_col=0, parse_dates=True)
    df = df[["DE_load_actual_entsoe_transparency"]]
    df.columns = ["value"]
    df.index.name = "timestamp"

else:
    uploaded_file = st.file_uploader("Bir enerji tüketim CSV dosyası yükleyin (timestamp - value)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Tarih sütunu varsa datetime yap
        for col in df.columns:
            if "time" in col.lower():
                df[col] = pd.to_datetime(df[col])
                timestamp_col = col
                break
        else:
            timestamp_col = df.columns[0]  # ilk kolonu timestamp kabul et

        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox("Tüketim değeri olarak kullanılacak sütunu seçin:", numeric_cols)

            # Yeni dataframe: timestamp + value
            df = df[[timestamp_col, selected_col]]
            df.columns = ['timestamp', 'value']
            df.set_index('timestamp', inplace=True)

        else:
            st.warning("CSV dosyasında sayısal veri içeren sütun bulunamadı.")
            df = None  # Güvenlik için df'yi sıfırla

if df is not None:
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.interpolate().dropna()

    st.subheader("📊 Ham Veri")
    st.dataframe(df.head())

    st.subheader("🚨 Anomali Tespiti")
    anomalies = detect_anomalies(df)
    fig = plot_timeseries_with_anomalies(df, anomalies)
    st.pyplot(fig)

    st.subheader("🔮 Tüketim Tahmini")
    forecast_df = predict_consumption(df)
    fig_forecast = plot_forecast(df, forecast_df)
    st.pyplot(fig_forecast)

