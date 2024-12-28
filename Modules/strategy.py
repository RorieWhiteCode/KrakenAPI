# strategy.py
import pandas as pd
import numpy as np
from data_handler import KrakenDataHandler


class Strategy:
    def __init__(self):
        # Initialize data handler for fetching market data
        self.data_handler = KrakenDataHandler()

    # Calculate RSI (Relative Strength Index)
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    # Calculate Moving Averages
    def calculate_moving_averages(self, df: pd.DataFrame, short_window: int = 50, long_window: int = 200):
        df['short_ma'] = df['close'].rolling(window=short_window).mean()
        df['long_ma'] = df['close'].rolling(window=long_window).mean()

    # Simple RSI-based strategy
    def rsi_strategy(self, pair: str) -> str:
        df = self.data_handler.get_ohlc(pair, interval=60)
        if df.empty:
            print("[ERROR] No data available for RSI strategy.")
            return "hold"

        df['rsi'] = self.calculate_rsi(df)

        latest_rsi = df['rsi'].iloc[-1]
        print(f"[INFO] Latest RSI for {pair}: {latest_rsi:.2f}")

        if latest_rsi < 30:
            return "buy"
        elif latest_rsi > 70:
            return "sell"
        else:
            return "hold"

    # Moving Average Crossover Strategy
    def ma_strategy(self, pair: str) -> str:
        df = self.data_handler.get_ohlc(pair, interval=60)
        if df.empty:
            print("[ERROR] No data available for MA strategy.")
            return "hold"

        self.calculate_moving_averages(df)

        if df['short_ma'].iloc[-1] > df['long_ma'].iloc[-1] and df['short_ma'].iloc[-2] <= df['long_ma'].iloc[-2]:
            return "buy"
        elif df['short_ma'].iloc[-1] < df['long_ma'].iloc[-1] and df['short_ma'].iloc[-2] >= df['long_ma'].iloc[-2]:
            return "sell"
        else:
            return "hold"

    # Combine Multiple Strategies
    def combined_strategy(self, pair: str) -> str:
        rsi_signal = self.rsi_strategy(pair)
        ma_signal = self.ma_strategy(pair)

        print(f"[INFO] RSI Signal: {rsi_signal}, MA Signal: {ma_signal}")

        if rsi_signal == "buy" and ma_signal == "buy":
            return "buy"
        elif rsi_signal == "sell" and ma_signal == "sell":
            return "sell"
        else:
            return "hold"


# Example usage
if __name__ == '__main__':
    strategy = Strategy()
    
    # Run RSI strategy
    print("\nRunning RSI Strategy on ADA/USD...")
    rsi_decision = strategy.rsi_strategy('ADAUSD')
    print(f"RSI Strategy Decision: {rsi_decision}")
    
    # Run MA strategy
    print("\nRunning Moving Average Strategy on ADA/USD...")
    ma_decision = strategy.ma_strategy('ADAUSD')
    print(f"MA Strategy Decision: {ma_decision}")
    
    # Run Combined Strategy
    print("\nRunning Combined Strategy on ADA/USD...")
    combined_decision = strategy.combined_strategy('ADAUSD')
    print(f"Combined Strategy Decision: {combined_decision}")
