import pandas as pd
from scipy import stats

def detect_anomalies(csv_path='../data/clean/AAPL_clean.csv', threshold=2.5):
    """
    Detects unusual price days using z-scores.
    Any day where the z-score is above the threshold is flagged as anomalous.
    
    Returns a list of dicts with anomaly date and deviation %.
    """
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Calculate z-scores
    df['z_score'] = stats.zscore(df['close_price'])
    df['is_anomaly'] = df['z_score'].abs() > threshold

    # Get anomaly rows
    anomalies = df[df['is_anomaly'] == True][['date', 'close_price', 'z_score']].copy()
    
    # Calculate % deviation from mean
    mean_price = df['close_price'].mean()
    anomalies['deviation_pct'] = ((anomalies['close_price'] - mean_price) / mean_price * 100).round(2)
    anomalies['date'] = anomalies['date'].dt.strftime('%Y-%m-%d')

    result = anomalies[['date', 'close_price', 'deviation_pct']].to_dict(orient='records')
    return result


# Test it when you run this file directly
if __name__ == '__main__':
    anomalies = detect_anomalies()
    
    if len(anomalies) == 0:
        print("No anomalies detected in the data.")
    else:
        print(f"Found {len(anomalies)} anomalies:\n")
        for a in anomalies:
            print(f"📅 {a['date']} — Price: ${a['close_price']} — Deviation: {a['deviation_pct']}%")