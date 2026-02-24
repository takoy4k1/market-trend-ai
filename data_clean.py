import pandas as pd
import os

def clean_market_data(symbol="AAPL"):
    """Cleans raw API data → saves to data/clean/"""

    raw_path = f"data/raw/{symbol}_raw.csv"
    print(f"Loading {raw_path}...")

    df = pd.read_csv(raw_path)

    # ── STEP 1: Rename confusing column names ──────────────────
    df = df.rename(columns={
        "1. open":   "open_price",
        "2. high":   "high_price",
        "3. low":    "low_price",
        "4. close":  "close_price",   # ← this is your main target
        "5. volume": "volume"
    })

    # ── STEP 2: Fix the date column ────────────────────────────
    df["date"] = pd.to_datetime(df["date"])  # string → proper date type
    df = df.sort_values("date")               # oldest first
    df = df.reset_index(drop=True)

    # ── STEP 3: Fix data types ─────────────────────────────────
    for col in ["open_price", "high_price", "low_price", "close_price"]:
        df[col] = df[col].astype(float)        # make sure they're numbers
    df["volume"] = df["volume"].astype(int)

    # ── STEP 4: Remove duplicates ──────────────────────────────
    before = len(df)
    df = df.drop_duplicates(subset="date")
    print(f"Removed {before - len(df)} duplicate rows")

    # ── STEP 5: Handle missing values ─────────────────────────
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"Filling {missing} missing values...")
        df["close_price"] = df["close_price"].fillna(method="ffill") # use previous day's price

    # ── STEP 6: Keep only the columns we need ─────────────────
    df = df[["date", "open_price", "high_price", "low_price", "close_price", "volume"]]

    # ── SAVE ──────────────────────────────────────────────────
    os.makedirs("data/clean", exist_ok=True)
    out_path = f"data/clean/{symbol}_clean.csv"
    df.to_csv(out_path, index=False)

    print(f"\n Clean data saved: {out_path}")
    print(f"   Rows: {len(df)}")
    print(f"   Date range: {df['date'].min()} → {df['date'].max()}")
    print(f"   Columns: {list(df.columns)}")
    return df

if __name__ == "__main__":
    clean_market_data("AAPL")