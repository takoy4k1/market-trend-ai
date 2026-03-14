import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from sentiment import analyze_sentiment

def test_positive_text_returns_positive():
    """Positive text should return +1"""
    result = analyze_sentiment(['Apple had record breaking profits this quarter'])
    assert result[0] == 1
    print("✅ Positive sentiment test passed!")

def test_negative_text_returns_negative():
    """Negative text should return -1"""
    result = analyze_sentiment(['Stock market crash causes massive losses'])
    assert result[0] == -1
    print("✅ Negative sentiment test passed!")

def test_multiple_texts():
    """Should handle a list of multiple texts"""
    texts = ['Great earnings!', 'Terrible results', 'Strong growth']
    result = analyze_sentiment(texts)
    assert len(result) == 3
    assert all(r in [1, -1] for r in result)
    print("✅ Multiple texts test passed!")