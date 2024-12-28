# backtester.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules.strategy import TradingStrategy


class Backtester:
    def __init__(self, historical_data: pd.DataFrame):
        # Historical OHLCV data
        self.data = historical_data
        self.strategy = TradingStrategy()
        self.initial_balance = 10000  # Starting balance in USD
        self.balance = self.initial_balance
        self.position = 0  # Current position (number of coins)
        self.trade_log = []  # Log all trades
    
    def run(self):
        # Run the strategy on each row of historical data
        for index, row in self.data.iterrows():
            price = row['close']
            pair = row['pair']
            
            decision = self.strategy.execute_strategy(pair)
            action = decision['action']
            trade_size = decision['trade_size']
            
            if action == 'buy' and self.balance > 0:
                self.position += (self.balance * trade_size) / price
                self.balance -= (self.balance * trade_size)
                self.trade_log.append({'action': 'buy', 'price': price, 'balance': self.balance})
            
            if action == 'sell' and self.position > 0:
                self.balance += self.position * price * trade_size
                self.position -= self.position * trade_size
                self.trade_log.append({'action': 'sell', 'price': price, 'balance': self.balance})
        
        # Close remaining position at the end of the backtest
        self.balance += self.position * self.data.iloc[-1]['close']
        self.position = 0
    
    def evaluate_performance(self):
        # Analyze trade log for performance metrics
        df = pd.DataFrame(self.trade_log)
        if df.empty:
            print("[WARNING] No trades executed during backtest.")
            return {}
        
        df['pnl'] = df['balance'].diff().fillna(0)
        total_pnl = df['pnl'].sum()
        win_rate = (df['pnl'] > 0).mean()
        max_drawdown = (df['balance'].cummax() - df['balance']).max()
        sharpe_ratio = df['pnl'].mean() / (df['pnl'].std() + 1e-8) * np.sqrt(252)
        
        results = {
            'Total P&L': total_pnl,
            'Win Rate': win_rate,
            'Max Drawdown': max_drawdown,
            'Sharpe Ratio': sharpe_ratio,
            'Final Balance': self.balance
        }
        
        print("[INFO] Backtest Results:")
        for k, v in results.items():
            print(f"{k}: {v}")
        
        return results
    
    def plot_results(self):
        # Plot balance over time
        df = pd.DataFrame(self.trade_log)
        if df.empty:
            print("[WARNING] No trades executed during backtest.")
            return
        
        df['timestamp'] = self.data['timestamp'][:len(df)]
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['balance'], label='Equity Curve')
        plt.title('Backtesting Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Balance (USD)')
        plt.legend()
        plt.show()


# Example Usage
if __name__ == '__main__':
    # Mock historical data
    historical_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-06-01', periods=100, freq='D'),
        'pair': ['ADAUSD'] * 100,
        'open': np.random.uniform(1, 2, 100),
        'high': np.random.uniform(2, 3, 100),
        'low': np.random.uniform(0.5, 1.5, 100),
        'close': np.random.uniform(1, 2.5, 100),
        'volume': np.random.uniform(1000, 5000, 100)
    })
    
    backtester = Backtester(historical_data)
    backtester.run()
    results = backtester.evaluate_performance()
    backtester.plot_results()
