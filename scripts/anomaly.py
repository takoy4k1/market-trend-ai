import pandas as pd
from scipy import stats


def detect_anomalies(history_df, threshold=1.5):
    """
    Takes a history DataFrame directly.
    Returns a DataFrame with anomaly rows — date, close_price, deviation_pct.
    """
    try:
        df = history_df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Calculate z-scores on the column only (not whole DataFrame)
        df['z_score'] = stats.zscore(df['close_price'].values)
        df['is_anomaly'] = df['z_score'].abs() > threshold

        # Get anomaly rows
        anomalies = df[df['is_anomaly'] == True][['date', 'close_price', 'z_score']].copy()

        # Calculate % deviation from mean
        mean_price = df['close_price'].mean()
        anomalies['deviation_pct'] = ((anomalies['close_price'] - mean_price) / mean_price * 100).round(2)
        anomalies['date'] = anomalies['date'].dt.strftime('%Y-%m-%d')

        return anomalies[['date', 'close_price', 'deviation_pct']].reset_index(drop=True)

    except Exception as e:
        print(f"Anomaly detection error: {e}")
        return pd.DataFrame(columns=['date', 'close_price', 'deviation_pct'])