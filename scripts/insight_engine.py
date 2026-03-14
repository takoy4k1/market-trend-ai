import sys
import os
sys.path.append(os.path.dirname(__file__))
from predict import predict_future

def analyze_trend(forecast):
    """
    Looks at the forecast and figures out if price is going up or down
    and by how much.
    """
    first_price = forecast[0]['predicted_price']
    last_price = forecast[-1]['predicted_price']
    change = last_price - first_price
    pct_change = (change / first_price) * 100

    if pct_change > 0:
        direction = "rise"
    else:
        direction = "fall"

    return {
        'direction': direction,
        'change_amount': round(abs(change), 2),
        'change_pct': round(abs(pct_change), 2),
        'first_price': round(first_price, 2),
        'last_price': round(last_price, 2)
    }


def generate_insight(history_df, forecast_df, anomalies=None):
    try:
        if forecast_df is None or len(forecast_df) == 0:
            return "Forecast data unavailable — please refresh and try again."
        
        trend = analyze_trend(forecast_df)
        insight = (
            f"AAPL stock prices are expected to {trend['direction']} by "
            f"${trend['change_amount']} ({trend['change_pct']}%) "
            f"over the forecast period, moving from "
            f"${trend['first_price']} to ${trend['last_price']}. "
        )
        if trend['direction'] == 'rise':
            insight += "Bullish momentum suggests a favorable buying window may be approaching."
        else:
            insight += "Bearish signals suggest caution for short-term investors."

        if anomalies is not None and len(anomalies) > 0:
            insight += f" Note: {len(anomalies)} unusual price movement(s) were detected in recent data."

        return insight

    except Exception as e:
        return f"Market insight temporarily unavailable. Please try refreshing."


# Test it when you run this file directly
if __name__ == '__main__':
    import pandas as pd
    from anomaly import detect_anomalies
    
    print("Loading history data...")
    history_df = pd.read_csv('../data/clean/AAPL_clean.csv')

    print("Generating forecast...")
    forecast_list = predict_future(30)
    forecast_df = pd.DataFrame(forecast_list)

    print("Detecting anomalies...")
    anomalies = detect_anomalies(history_df)

    print("Generating insight...")
    insight = generate_insight(history_df, forecast_df, anomalies)

    print("\n📊 AI Insight:")
    print(insight)

    print(f"\n🚨 Anomalies found: {len(anomalies)}")
    for _, row in anomalies.iterrows():
        print(f"  {row['date']} — ${row['close_price']} ({row['deviation_pct']}% deviation)")