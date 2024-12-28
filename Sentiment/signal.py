# signal.py
import pandas as pd
from typing import Dict, Any


# Generates actionable trade signals based on sentiment scores
class SignalGenerator:
    def __init__(self):
        # Default thresholds for generating signals
        self.thresholds = {
            'strong_buy': 0.7,
            'buy': 0.3,
            'hold': -0.3,
            'sell': -0.7,
            'strong_sell': -1.0
        }
        
        # Trade size adjustments based on sentiment confidence
        self.trade_adjustments = {
            'strong_buy': 1.5,
            'buy': 1.0,
            'hold': 0.0,
            'sell': 1.0,
            'strong_sell': 1.5
        }
    
    # Map composite sentiment score to actionable signals
    def map_score_to_signal(self, composite_score: float) -> str:
        if composite_score >= self.thresholds['strong_buy']:
            return 'Strong Buy'
        elif composite_score >= self.thresholds['buy']:
            return 'Buy'
        elif composite_score <= self.thresholds['sell']:
            return 'Sell'
        elif composite_score <= self.thresholds['strong_sell']:
            return 'Strong Sell'
        return 'Hold'
    
    # Adjust trade size based on sentiment confidence and type
    def adjust_trade_size(self, signal: str, confidence: float) -> float:
        base_trade_size = 1.0  # Default trade size
        adjustment_factor = self.trade_adjustments.get(signal, 0.0)
        return base_trade_size * adjustment_factor * confidence
    
    # Generate a final trading signal from sentiment data
    def generate_signal(self, sentiment_result: Dict[str, Any]) -> Dict[str, Any]:
        composite_score = sentiment_result.get('composite_score', 0.0)
        confidence = max([item.get('confidence', 0.0) for item in sentiment_result.get('details', [])])
        signal = self.map_score_to_signal(composite_score)
        trade_size = self.adjust_trade_size(signal, confidence)
        
        return {
            'signal': signal,
            'composite_score': composite_score,
            'confidence': confidence,
            'trade_size': trade_size,
            'details': sentiment_result.get('details', [])
        }


# Example Usage
if __name__ == '__main__':
    # Mock aggregated sentiment data
    aggregated_sentiment = {
        'composite_score': 0.75,
        'signal': 'Strong Buy',
        'details': [
            {'source': 'CryptoPanic', 'type': 'news', 'sentiment': 'positive', 'confidence': 0.8, 'weighted_score': 0.24},
            {'source': 'Twitter', 'type': 'social', 'sentiment': 'positive', 'confidence': 0.7, 'weighted_score': 0.175},
            {'source': 'TradingView', 'type': 'expert', 'sentiment': 'positive', 'confidence': 0.9, 'weighted_score': 0.405}
        ]
    }
    
    generator = SignalGenerator()
    final_signal = generator.generate_signal(aggregated_sentiment)
    
    print("[INFO] Final Trade Signal:")
    print(final_signal)
