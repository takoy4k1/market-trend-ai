import pandas as pd
import os
import sys
sys.path.insert(0, "..")   # so we can import from parent folder

from data_clean import clean_market_data

def test_clean_data_has_required_columns():
    """The clean CSV must have these exact columns"""
    df = pd.read_csv("data/clean/AAPL_clean.csv")
    required = ["date", "open_price", "close_price", "volume"]
    for col in required:
        assert col in df.columns, f"Missing column: {col}"

def test_clean_data_no_missing_values():
    """No NaN values allowed in the clean file"""
    df = pd.read_csv("data/clean/AAPL_clean.csv")
    assert df.isnull().sum().sum() == 0, "Clean data has missing values!"

def test_clean_data_prices_are_positive():
    """All prices must be greater than zero"""
    df = pd.read_csv("data/clean/AAPL_clean.csv")
    assert (df["close_price"] > 0).all(), "Some prices are zero or negative!"

def test_clean_data_has_enough_rows():
    """Must have at least 100 rows of data"""
    df = pd.read_csv("data/clean/AAPL_clean.csv")
    assert len(df) >= 100, f"Only {len(df)} rows — need at least 100"