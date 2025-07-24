import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def predict_consumption(df, steps=5, column='value'):
    df = df.copy()
    df = df.reset_index()
    
    df['time_step'] = np.arange(len(df))
    
    X = df[['time_step']]
    y = df[column]

    model = LinearRegression()
    model.fit(X, y)

    future_steps = np.arange(len(df), len(df) + steps).reshape(-1, 1)
    future_preds = model.predict(future_steps)

    future_dates = pd.date_range(start=df['timestamp'].iloc[-1], periods=steps+1, freq='H')[1:]

    future_df = pd.DataFrame({
        'timestamp': future_dates,
        column: future_preds
    })

    return future_df

