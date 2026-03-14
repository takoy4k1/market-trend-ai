import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from anomaly import detect_anomalies

def test_large_spike_is_flagged():
    """A very large price spike should be detected as anomaly"""
    data = {
        'date': pd.date_range('2025-01-01', periods=20),
        'close_price': [100]*19 + [999]  # last day is a huge spike
    }
    df = pd.DataFrame(data)
    anomalies = detect_anomalies(df, threshold=1.5)
    assert len(anomalies) > 0
    print("✅ Spike detection test passed!")

def test_stable_data_has_no_anomalies():
    """Perfectly stable prices should have no anomalies"""
    data = {
        'date': pd.date_range('2025-01-01', periods=20),
        'close_price': [100.0] * 20  # completely flat
    }
    df = pd.DataFrame(data)
    anomalies = detect_anomalies(df, threshold=2.5)
    assert len(anomalies) == 0
    print("✅ Stable data test passed!")

def test_returns_dataframe():
    """detect_anomalies should always return a DataFrame"""
    data = {
        'date': pd.date_range('2025-01-01', periods=10),
        'close_price': [100]*10
    }
    df = pd.DataFrame(data)
    result = detect_anomalies(df)
    assert isinstance(result, pd.DataFrame)
    print("✅ Return type test passed!")