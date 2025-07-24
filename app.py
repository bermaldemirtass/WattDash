import streamlit as st
import pandas as pd
from utils.forecast import predict_consumption
from utils.visualizer import plot_forecast


from utils.anomaly import detect_anomalies
from utils.visualizer import plot_timeseries_with_anomalies

st.set_page_config(page_title="WattDash", layout="wide")
st.title("⚡ WattDash - Energy Intelligence Dashboard")

uploaded_file = st.file_uploader("Bir enerji tüketim CSV dosyası yükleyin", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)

    st.subheader("📊 Ham Veri")
    st.dataframe(df.head())

    st.subheader("🚨 Anomali Tespiti")
    anomalies = detect_anomalies(df)
    fig = plot_timeseries_with_anomalies(df, anomalies)
    st.pyplot(fig)

    # Forecasting
    st.subheader("🔮 Tüketim Tahmini")
    forecast_df = predict_consumption(df)
    fig_forecast = plot_forecast(df, forecast_df)
    st.pyplot(fig_forecast)

