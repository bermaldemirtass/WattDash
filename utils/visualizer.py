# utils/visualizer.py
import matplotlib.pyplot as plt

def plot_timeseries_with_anomalies(df, anomalies, column='value'):
    """
    Anomalileri zaman serisinde işaretleyerek grafiği çizer.
    """
    fig, ax = plt.subplots(figsize=(12, 4))

    # Normal veri çiz
    ax.plot(df.index, df[column], label='Tüketim', color='blue')

    # Anomalileri kırmızı ile işaretle
    ax.scatter(df.index[anomalies], df[column][anomalies], color='red', label='Anomali', marker='x')

    ax.set_title('Tüketim Zaman Serisi ve Anomaliler')
    ax.set_xlabel('Zaman')
    ax.set_ylabel('Değer')
    ax.legend()
    plt.tight_layout()

    return fig

def plot_forecast(original_df, forecast_df, column='value'):
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(original_df.index, original_df[column], label='Gerçek Veri', color='blue')
    ax.plot(forecast_df['timestamp'], forecast_df[column], label='Tahmin', color='orange', linestyle='--')

    ax.set_title('Tüketim Tahmini (Forecast)')
    ax.set_xlabel('Zaman')
    ax.set_ylabel('Değer')
    ax.legend()
    plt.tight_layout()

    return fig

