import os
import pandas as pd
from scipy import stats

def detect_anomalies(threshold=2.5):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data', 'clean', 'AAPL_clean.csv')

    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    df['z_score'] = stats.zscore(df['close_price'])
    df['is_anomaly'] = df['z_score'].abs() > threshold

    anomalies = df[df['is_anomaly'] == True][['date', 'close_price', 'z_score']].copy()
    
    mean_price = df['close_price'].mean()
    anomalies['deviation_pct'] = ((anomalies['close_price'] - mean_price) / mean_price * 100).round(2)
    anomalies['date'] = anomalies['date'].dt.strftime('%Y-%m-%d')

    return anomalies[['date', 'close_price', 'deviation_pct']].to_dict(orient='records')


if __name__ == '__main__':
    anomalies = detect_anomalies()
    if len(anomalies) == 0:
        print("No anomalies detected.")
    else:
        print(f"Found {len(anomalies)} anomalies:\n")
        for a in anomalies:
            print(f"📅 {a['date']} — Price: ${a['close_price']} — Deviation: {a['deviation_pct']}%")