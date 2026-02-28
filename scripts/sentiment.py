from transformers import pipeline

# Load the sentiment model (downloads once, then cached)
sentiment_analyzer = pipeline('sentiment-analysis')

def analyze_sentiment(texts):
    """
    Takes a list of text strings.
    Returns a list of scores: +1 for positive, -1 for negative.
    
    Example:
        analyze_sentiment(['Great earnings!', 'Terrible quarter'])
        → [1, -1]
    """
    results = sentiment_analyzer(texts)
    scores = []
    for r in results:
        if r['label'] == 'POSITIVE':
            scores.append(1)
        else:
            scores.append(-1)
    return scores


# Test it when you run this file directly
if __name__ == '__main__':
    test_texts = [
        'Apple had a great quarter with record profits',
        'Stock market crash worries investors',
        'iPhone sales exceeded expectations',
        'Supply chain issues hurt Apple revenue',
        'Strong demand for Apple products worldwide'
    ]
    results = analyze_sentiment(test_texts)
    for text, score in zip(test_texts, results):
        label = '✅ POSITIVE' if score == 1 else '❌ NEGATIVE'
        print(f"{label}: {text}")