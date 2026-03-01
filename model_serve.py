import joblib
import pandas as pd
import os
from config import MODEL_PATH, FORECAST_DAYS

def load_model():
    """Load Person B's trained model from disk"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Has Person B run model_train.py yet?")
    return joblib.load(MODEL_PATH)

def predict_forecast(days=None):
    """
    Returns a forecast as a list of dicts.
    Each dict = { "date": "2024-02-01", "predicted_price": 192.5,
                  "lower": 188.0, "upper": 197.0 }
    """
    if days is None:
        days = FORECAST_DAYS

    model = load_model()

    # Prophet needs this exact format
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    # Get only the future rows (not the historical fitted values)
    future_only = forecast.tail(days)[["ds", "yhat", "yhat_lower", "yhat_upper"]]

    # Convert to clean list of dicts for JSON response
    result = []
    for _, row in future_only.iterrows():
        result.append({
            "date":            str(row["ds"]).split(" ")[0],  # just the date part
            "predicted_price": round(float(row["yhat"]),       2),
            "lower":           round(float(row["yhat_lower"]), 2),
            "upper":           round(float(row["yhat_upper"]), 2),
        })
    return result

# Test it
if __name__ == "__main__":
    preds = predict_forecast(7)
    for p in preds:
        print(p)