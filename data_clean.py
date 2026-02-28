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
        "4. close":  "close_price",
        "5. volume": "volume"
    })

    # ── STEP 2: Fix the date column ────────────────────────────
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # ── STEP 3: Fix data types ─────────────────────────────────
    for col in ["open_price", "high_price", "low_price", "close_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # ── STEP 4: Remove duplicates ──────────────────────────────
    before = len(df)
    df = df.drop_duplicates(subset="date")
    print(f"Removed {before - len(df)} duplicate rows")

    # ── STEP 5: Handle missing values ─────────────────────────
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"Filling {missing} missing values...")
        df["close_price"] = df["close_price"].ffill()

    # ── STEP 6: Keep only needed columns ──────────────────────
    df = df[[
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
    ]]

    # ── SAVE ──────────────────────────────────────────────────
    os.makedirs("data/clean", exist_ok=True)
    out_path = f"data/clean/{symbol}_clean.csv"
    df.to_csv(out_path, index=False)

    print(f"\nClean data saved: {out_path}")
    print(f"Rows: {len(df)}")
    print(f"Date range: {df['date'].min()} → {df['date'].max()}")
    print(f"Columns: {list(df.columns)}")

    return df


# 🚀 FULL PIPELINE
def run_full_pipeline(symbol="AAPL"):
    """Run the full pipeline: fetch → clean → features"""
    from api_fetch import fetch_market_data

    # Step 1: fetch fresh data
    fetch_market_data(symbol)

    # Step 2: clean it
    df_clean = clean_market_data(symbol)

    # Step 3: add features
    if os.path.exists("features.py"):
        from features import add_features
        df_features = add_features(df_clean)

        os.makedirs("data/features", exist_ok=True)
        df_features.to_csv(f"data/features/{symbol}_features.csv", index=False)
        print("✅ Features file saved!")
    else:
        print("⏳ features.py not ready yet — skipping features step")


# ▶️ ENTRY POINT (only one!)
if __name__ == "__main__":
    run_full_pipeline("AAPL")