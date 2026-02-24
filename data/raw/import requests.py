import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

def fetch_market_data(symbol="AAPL"):
    """
    Fetches daily price data for a stock symbol.
    symbol = the stock ticker (e.g. "AAPL" for Apple, "MSFT" for Microsoft)
    Returns a cleaned pandas DataFrame and saves it to data/raw/
    """
    api_key = os.getenv("ALPHA_VANTAGE_KEY")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",  # get 6+ months of data
        "apikey": api_key
    }

    print(f"Fetching data for {symbol}...")

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    # Check for API errors
    if "Time Series (Daily)" not in data:
        print("API Error:", data)  # will show the error message
        return None

    # Convert nested JSON into a flat table
    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame(time_series).T  # .T = transpose (flip rows/cols)
    df.index.name = "date"
    df = df.reset_index()

    # Save raw data
    os.makedirs("data/raw", exist_ok=True)
    filepath = f"data/raw/{symbol}_raw.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved {len(df)} rows to {filepath}")

    return df


# Run this file directly to test it
if __name__ == "__main__":
    df = fetch_market_data("AAPL")
    if df is not None:
        print(df.head())  # print first 5 rows