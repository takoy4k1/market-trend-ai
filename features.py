import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds feature columns to the market DataFrame.
    """
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # ✅ use close_price (NOT price)
    df["7_day_avg"] = df["close_price"].rolling(7).mean()
    df["30_day_avg"] = df["close_price"].rolling(30).mean()
    df["day_of_week"] = df["date"].dt.dayofweek

    return df