# strategy.py
import pandas as pd
from modules.sentiment.collector import SentimentCollector
from modules.sentiment.processor import SentimentPreprocessor
from modules.sentiment.model import SentimentAnalyzer
from modules.sentiment.aggregator import SentimentAggregator
from modules.sentiment.signal import SignalGenerator


# Technical Strategy Class (Placeholder)
class TechnicalStrategy:
    def rsi_strategy(self, pair: str) -> str:
        # Placeholder RSI strategy logic
        return 'buy'
    
    def ma_strategy(self, pair: str) -> str:
        # Placeholder MA strategy logic
        return 'hold'


# Combined Strategy with Sentiment Integration
class TradingStrategy:
    def __init__(self):
        self.technical_strategy = TechnicalStrategy()
        self.sentiment_collector = SentimentCollector()
        self.sentiment_preprocessor = SentimentPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.sentiment_aggregator = SentimentAggregator()
        self.signal_generator = SignalGenerator()
        self.weights = {
            'technical': 0.6,
            'sentiment': 0.4
        }
    
    def fetch_sentiment_signal(self) -> Dict[str, Any]:
        # Collect raw sentiment data
        import asyncio
        asyncio.run(self.sentiment_collector.fetch_all_data())
        raw_sentiment_data = self.sentiment_collector.get_data()
        
        # Preprocess sentiment data
        preprocessed_data = self.sentiment_preprocessor.preprocess_all(raw_sentiment_data)
        
        # Analyze sentiment
        sentiment_results = self.sentiment_analyzer.batch_analyze(preprocessed_data)
        
        # Aggregate sentiment
        aggregated_sentiment = self.sentiment_aggregator.aggregate_sentiment(sentiment_results)
        
        # Generate sentiment signal
        sentiment_signal = self.signal_generator.generate_signal(aggregated_sentiment)
        
        return sentiment_signal
    
    def combine_signals(self, technical_signal: str, sentiment_signal: Dict[str, Any]) -> Dict[str, Any]:
        # Map technical signals to numeric values
        signal_mapping = {
            'Strong Buy': 1.0,
            'Buy': 0.5,
            'Hold': 0.0,
            'Sell': -0.5,
            'Strong Sell': -1.0
        }
        
        technical_score = signal_mapping.get(technical_signal, 0.0)
        sentiment_score = signal_mapping.get(sentiment_signal['signal'], 0.0)
        
        # Combine signals with weights
        combined_score = (
            (technical_score * self.weights['technical']) +
            (sentiment_score * self.weights['sentiment'])
        )
        
        # Generate final decision
        if combined_score >= 0.7:
            return {'action': 'buy', 'trade_size': sentiment_signal['trade_size']}
        elif combined_score <= -0.7:
            return {'action': 'sell', 'trade_size': sentiment_signal['trade_size']}
        else:
            return {'action': 'hold', 'trade_size': 0.0}
    
    def execute_strategy(self, pair: str):
        print(f"[INFO] Executing strategy for {pair}...")
        
        # Fetch technical signal
        technical_signal = self.technical_strategy.rsi_strategy(pair)
        print(f"[INFO] Technical Signal: {technical_signal}")
        
        # Fetch sentiment signal
        sentiment_signal = self.fetch_sentiment_signal()
        print(f"[INFO] Sentiment Signal: {sentiment_signal['signal']}")
        
        # Combine signals
        final_decision = self.combine_signals(technical_signal, sentiment_signal)
        print(f"[INFO] Final Decision: {final_decision}")
        
        return final_decision


# Example Usage
if __name__ == '__main__':
    strategy = TradingStrategy()
    final_decision = strategy.execute_strategy('ADAUSD')
    print(f"[INFO] Final Trading Action: {final_decision}")
