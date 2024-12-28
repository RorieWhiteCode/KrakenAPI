# aggregator.py
import pandas as pd
from typing import Dict, Any



#Composite Sentiment Formula
#CSS=(N×Wn)+(SM×Wsm)+(EX×Wex)



# Aggregates sentiment scores and generates a composite score
class SentimentAggregator:
    def __init__(self):
        # Define default weights for each sentiment source
        self.weights = {
            'news': 0.3,
            'social': 0.25,
            'expert': 0.45
        }
        self.thresholds = {
            'strong_buy': 0.7,
            'buy': 0.3,
            'hold': -0.3,
            'sell': -0.7
        }
    
    # Calculate weighted sentiment score for each row
    def calculate_weighted_score(self, row: Dict[str, Any]) -> float:
        sentiment = row['sentiment']
        confidence = row['confidence']
        weight = self.weights.get(row['type'], 0.1)
        
        score = 0.0
        if sentiment == 'positive':
            score = 1.0
        elif sentiment == 'negative':
            score = -1.0
        
        # Adjust sentiment by weight and confidence
        return score * confidence * weight
    
    # Generate a composite sentiment score
    def aggregate_sentiment(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {'composite_score': 0.0, 'signal': 'hold'}
        
        # Calculate weighted sentiment scores
        df['weighted_score'] = df.apply(self.calculate_weighted_score, axis=1)
        
        # Calculate the composite score
        composite_score = df['weighted_score'].sum()
        
        # Classify the signal based on thresholds
        if composite_score >= self.thresholds['strong_buy']:
            signal = 'Strong Buy'
        elif composite_score >= self.thresholds['buy']:
            signal = 'Buy'
        elif composite_score <= self.thresholds['sell']:
            signal = 'Sell'
        elif composite_score <= self.thresholds['hold']:
            signal = 'Strong Sell'
        else:
            signal = 'Hold'
        
        return {
            'composite_score': composite_score,
            'signal': signal,
            'details': df[['source', 'type', 'sentiment', 'confidence', 'weighted_score']].to_dict(orient='records')
        }


# Example Usage
if __name__ == '__main__':
    # Mock sentiment data
    raw_data = {
        'source': ['CryptoPanic', 'Twitter', 'TradingView'],
        'type': ['news', 'social', 'expert'],
        'sentiment': ['positive', 'neutral', 'positive'],
        'confidence': [0.8, 0.5, 0.9]
    }
    
    df = pd.DataFrame(raw_data)
    aggregator = SentimentAggregator()
    result = aggregator.aggregate_sentiment(df)
    
    print("[INFO] Composite Sentiment Result:")
    print(result)
