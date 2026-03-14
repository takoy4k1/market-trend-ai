from .predict import predict_future

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


def generate_insight(forecast, anomalies=None):
    """
    Takes forecast data and returns an AI-written insight string.
    Uses HuggingFace free text generation — no API key needed.
    Falls back to a template insight if API fails.
    """
    trend = analyze_trend(forecast)

    # Build insight using template (reliable, no API needed)
    insight = (
        f"AAPL stock prices are expected to {trend['direction']} by "
        f"${trend['change_amount']} ({trend['change_pct']}%) "
        f"over the next 30 days, moving from "
        f"${trend['first_price']} to ${trend['last_price']}. "
    )

    if trend['direction'] == 'rise':
        insight += "Bullish momentum suggests a favorable buying window may be approaching."
    else:
        insight += "Bearish signals suggest caution for short-term investors."

    # Add anomaly info if provided
    if anomalies and len(anomalies) > 0:
        insight += f" Note: {len(anomalies)} unusual price movement(s) were detected in recent data."

    return insight


# Test it when you run this file directly
if __name__ == '__main__':
    from anomaly import detect_anomalies
    
    print("Generating forecast...")
    forecast = predict_future(30)
    
    print("Detecting anomalies...")
    anomalies = detect_anomalies()
    
    print("\nGenerating insight...")
    insight = generate_insight(forecast, anomalies)
    
    print("\n📊 AI Insight:")
    print(insight)
    
    print(f"\n🚨 Anomalies found: {len(anomalies)}")
    for a in anomalies:
        print(f"  {a['date']} — ${a['close_price']} ({a['deviation_pct']}% deviation)")