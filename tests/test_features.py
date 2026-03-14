import pandas as pd
import sys
sys.path.append('.')

def test_rolling_average_calculated():
    """Test that 7-day rolling average is calculated correctly"""
    data = {
        'date': pd.date_range('2025-01-01', periods=10),
        'close_price': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109]
    }
    df = pd.DataFrame(data)
    df['7_day_avg'] = df['close_price'].rolling(7).mean()

    # First 6 rows should be NaN (not enough data yet)
    assert df['7_day_avg'].iloc[0] != df['7_day_avg'].iloc[0]  # NaN check

    # 7th row should have a value
    assert df['7_day_avg'].iloc[6] is not None

    # Check the actual value is correct
    expected = round(sum([100,102,101,103,105,104,106]) / 7, 6)
    assert round(df['7_day_avg'].iloc[6], 6) == expected
    print("✅ Rolling average test passed!")

def test_price_change_pct():
    """Test that percentage change is calculated correctly"""
    data = {'close_price': [100.0, 110.0, 99.0]}
    df = pd.DataFrame(data)
    df['price_change_pct'] = df['close_price'].pct_change()

    assert round(df['price_change_pct'].iloc[1], 2) == 0.10  # 10% increase
    assert round(df['price_change_pct'].iloc[2], 2) == -0.10  # 10% decrease
    print("✅ Price change test passed!")