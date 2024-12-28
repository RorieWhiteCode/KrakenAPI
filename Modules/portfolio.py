# portfolio.py
import pandas as pd
from typing import Dict, Union
from data_handler import KrakenDataHandler
from config import LEVERAGE, MAX_PORTFOLIO_EXPOSURE, RESERVE_BALANCE, BASE_CURRENCY


class PortfolioManager:
    # Initialize the portfolio manager with data handling and portfolio tracking
    def __init__(self):
        self.data_handler = KrakenDataHandler()
        self.positions = {}  # Active positions
        self.balance = {}  # Account balances

    # Update portfolio balances from Kraken
    def update_balance(self):
        self.balance = self.data_handler.get_balance()
        if not self.balance:
            print("[ERROR] Could not fetch portfolio balance.")
        else:
            print("[INFO] Portfolio balance updated.")

    # Calculate available balance after reserving a buffer
    def get_available_balance(self) -> float:
        if not self.balance:
            self.update_balance()
        base_currency_balance = float(self.balance.get(BASE_CURRENCY, 0))
        available_balance = base_currency_balance * (1 - RESERVE_BALANCE)
        print(f"[INFO] Available balance: {available_balance} {BASE_CURRENCY}")
        return available_balance

    # Calculate portfolio exposure for a given trade amount
    def calculate_exposure(self, pair: str, amount: float) -> float:
        total_balance = self.get_available_balance()
        exposure = (amount / total_balance) * 100 if total_balance > 0 else 0
        print(f"[INFO] Exposure for {pair}: {exposure:.2f}%")
        return exposure

    # Check if a new position can be opened without breaching exposure limits
    def can_open_position(self, pair: str, amount: float) -> bool:
        current_exposure = self.calculate_exposure(pair, amount)
        if current_exposure > (MAX_PORTFOLIO_EXPOSURE * 100):
            print(f"[WARNING] Cannot open position in {pair}: Exposure would exceed {MAX_PORTFOLIO_EXPOSURE * 100}%")
            return False
        return True

    # Add a new position to the portfolio if exposure rules are met
    def add_position(self, pair: str, amount: float):
        if self.can_open_position(pair, amount):
            leverage = LEVERAGE.get(pair.split('/')[0], 1)  # Default leverage if not specified
            self.positions[pair] = {
                'amount': amount,
                'leverage': leverage,
                'status': 'open'
            }
            print(f"[INFO] Position opened: {pair}, Amount: {amount}, Leverage: {leverage}x")
        else:
            print(f"[ERROR] Failed to open position for {pair}.")

    # Close an existing position
    def close_position(self, pair: str):
        if pair in self.positions:
            del self.positions[pair]
            print(f"[INFO] Position closed: {pair}")
        else:
            print(f"[WARNING] No open position found for {pair}")

    # Display all active positions as a DataFrame
    def get_positions(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.positions, orient='index')


# Example usage for testing
if __name__ == '__main__':
    portfolio = PortfolioManager()
    
    # Update balances
    portfolio.update_balance()
    
    # Check available balance
    portfolio.get_available_balance()
    
    # Open positions
    portfolio.add_position('ADA/USD', 100)
    portfolio.add_position('LTC/USD', 50)
    
    # Display current positions
    print("\nCurrent Positions:")
    print(portfolio.get_positions())
    
    # Close a position
    portfolio.close_position('ADA/USD')
    
    # Display updated positions
    print("\nUpdated Positions:")
    print(portfolio.get_positions())
