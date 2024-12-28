# model.py
import pandas as pd
from typing import List, Dict, Any
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK resources
nltk.download('vader_lexicon')


# Base Sentiment Model Class
class SentimentModel:
    def __init__(self):
        pass
    
    def analyze(self, text: str) -> Dict[str, Any]:
        # Placeholder for sentiment analysis
        return {"sentiment": "neutral", "confidence": 0.0}


# VADER Sentiment Model for Quick Scoring
class VADERModel(SentimentModel):
    def __init__(self):
        super().__init__()
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        # Analyze text sentiment using VADER
        scores = self.analyzer.polarity_scores(text)
        sentiment = "neutral"
        if scores['compound'] >= 0.05:
            sentiment = "positive"
        elif scores['compound'] <= -0.05:
            sentiment = "negative"
        return {"sentiment": sentiment, "confidence": abs(scores['compound'])}


# FinBERT Sentiment Model for Financial Texts
class FinBERTModel(SentimentModel):
    def __init__(self):
        super().__init__()
        self.model = pipeline("text-classification", model="yiyanghkust/finbert-tone")
    
    def analyze(self, text: str) -> Dict[str, Any]:
        # Analyze text sentiment using FinBERT
        result = self.model(text, truncation=True)[0]
        sentiment = result['label'].lower()
        confidence = result['score']
        return {"sentiment": sentiment, "confidence": confidence}


# Unified Sentiment Analyzer
class SentimentAnalyzer:
    def __init__(self):
        # Initialize VADER and FinBERT models
        self.vader = VADERModel()
        self.finbert = FinBERTModel()
    
    def batch_analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        # Analyze sentiment for each row in the DataFrame
        results = []
        for index, row in df.iterrows():
            text = row.get('content', row.get('title', ''))
            if row['type'] == 'news':
                result = self.finbert.analyze(text)
            elif row['type'] == 'social':
                result = self.vader.analyze(text)
            elif row['type'] == 'expert':
                result = self.finbert.analyze(text)
            else:
                result = {"sentiment": "neutral", "confidence": 0.0}
            
            results.append({
                'source': row['source'],
                'type': row['type'],
                'content': text,
                'sentiment': result['sentiment'],
                'confidence': result['confidence'],
                'timestamp': row.get('timestamp', '')
            })
        
        return pd.DataFrame(results)


# Example Usage
if __name__ == '__main__':
    # Mock DataFrame with preprocessed text
    raw_data = {
        'source': ['CryptoPanic', 'Twitter', 'TradingView'],
        'type': ['news', 'social', 'expert'],
        'content': [
            'Bitcoin hits all-time high!',
            'Everyone is talking about ADA going to the moon!',
            'Analyst predicts strong bullish trend for ETH.'
        ],
        'timestamp': ['2024-06-28T10:00:00Z', '2024-06-28T11:00:00Z', '2024-06-28T12:00:00Z']
    }
    
    df = pd.DataFrame(raw_data)
    analyzer = SentimentAnalyzer()
    results = analyzer.batch_analyze(df)
    print(results)
