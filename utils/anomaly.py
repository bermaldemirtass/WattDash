from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df, column='value'):
    """
    Enerji tüketim verisinde anomali tespiti yapar.
    Varsayılan olarak 'value' sütununa bakar.
    """
    if column not in df.columns:
        raise ValueError(f"'{column}' sütunu bulunamadı.")

    model = IsolationForest(contamination=0.05, random_state=42)
    df = df.copy()
    df['anomaly'] = model.fit_predict(df[[column]])
    return df['anomaly'] == -1  # -1 anomali demek

