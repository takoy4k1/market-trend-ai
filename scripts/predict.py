import pandas as pd
from prophet import Prophet
import joblib
import os

# Path to the saved model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'prophet_model.pkl')

def load_model():
    """Loads the saved Prophet model from disk"""
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
    return model

def predict_future(days=30):
    """
    Returns forecast for next N days as a list of dicts.
    
    Example output:
    [
        {'date': '2025-11-01', 'predicted_price': 258.3, 'lower_bound': 250.1, 'upper_bound': 266.5},
        ...
    ]
    """
    model = load_model()
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days)
    result = result.rename(columns={
        'ds': 'date',
        'yhat': 'predicted_price',
        'yhat_lower': 'lower_bound',
        'yhat_upper': 'upper_bound'
    })
    result['date'] = result['date'].dt.strftime('%Y-%m-%d')
    
    return result.to_dict(orient='records')


# Test it when you run this file directly
if __name__ == '__main__':
    print("Testing predict_future(5)...")
    output = predict_future(5)
    for row in output:
        print(row)