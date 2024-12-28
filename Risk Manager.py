# risk_manager.py
import time
from typing import Dict, Union
from data_handler import KrakenDataHandler
from trade_executor import TradeExecutor
from portfolio import PortfolioManager
from config import STOP_LOSS, TAKE_PROFIT, MAX_DAILY_DRAWDOWN, RISK_PER_TRADE, BASE_CURRENCY


class RiskManager:
    def __init__(self):
        # Initialize required modules
        self.data_handler = KrakenDataHandler()
        self.trade_executor = TradeExecutor()
        self.portfolio_manager = PortfolioManager()
        self.daily_loss = 0.0  # Track daily losses

    # Monitor portfolio-wide daily drawdown
    def check_daily_drawdown(self) -> bool:
        self.portfolio_manager.update_balance()
        total_balance = float(self.portfolio_manager.balance.get(BASE_CURRENCY, 0))

        if total_balance == 0:
            print("[ERROR] Could not fetch portfolio balance. Cannot calculate drawdown.")
            return False

        drawdown = (self.daily_loss / total_balance) * 100
        print(f"[INFO] Current daily drawdown: {drawdown:.2f}%")

        if drawdown >= (MAX_DAILY_DRAWDOWN * 100):
            print(f"[ALERT] Daily drawdown limit of {MAX_DAILY_DRAWDOWN * 100}% reached. Trading paused.")
            return True

        return False

    # Monitor stop-loss and take-profit levels for open positions
    def monitor_positions(self):
        positions = self.portfolio_manager.get_positions()
        for pair, position in positions.iterrows():
            pair_data = self.data_handler.get_ticker(pair)
            current_price = float(pair_data[pair]['c'][0]) if pair_data else None

            if current_price is None:
                print(f"[WARNING] Could not fetch price data for {pair}. Skipping risk check.")
                continue

            entry_price = position['amount'] / position['leverage']
            stop_loss_price = entry_price * (1 - STOP_LOSS)
            take_profit_price = entry_price * (1 + TAKE_PROFIT)

            print(f"[INFO] Monitoring {pair}: Entry: {entry_price}, SL: {stop_loss_price}, TP: {take_profit_price}, Current: {current_price}")

            if current_price <= stop_loss_price:
                print(f"[ALERT] Stop-loss triggered for {pair}. Closing position.")
                self.trade_executor.place_market_order(pair, position['amount'], 'sell')
                self.portfolio_manager.close_position(pair)
                self.daily_loss += position['amount'] * STOP_LOSS

            elif current_price >= take_profit_price:
                print(f"[SUCCESS] Take-profit reached for {pair}. Closing position.")
                self.trade_executor.place_market_order(pair, position['amount'], 'sell')
                self.portfolio_manager.close_position(pair)

    # Calculate risk for a new trade
    def calculate_position_size(self, entry_price: float) -> float:
        self.portfolio_manager.update_balance()
        total_balance = self.portfolio_manager.get_available_balance()
        max_risk = total_balance * RISK_PER_TRADE

        position_size = max_risk / (entry_price * STOP_LOSS)
        print(f"[INFO] Calculated position size: {position_size:.2f} based on risk per trade.")
        return position_size

    # Validate if new trade complies with risk parameters
    def validate_trade(self, pair: str, entry_price: float) -> bool:
        position_size = self.calculate_position_size(entry_price)
        exposure = self.portfolio_manager.calculate_exposure(pair, position_size * entry_price)

        if exposure > (RISK_PER_TRADE * 100):
            print(f"[WARNING] Trade exposure for {pair} exceeds risk limits.")
            return False

        return True


# Example Usage
if __name__ == '__main__':
    risk_manager = RiskManager()
    
    # Check daily drawdown
    print("\nChecking Daily Drawdown...")
    if risk_manager.check_daily_drawdown():
        print("[HALT] Trading paused due to daily drawdown limit.")
    else:
        print("[INFO] Daily drawdown within safe limits.")
    
    # Monitor active positions
    print("\nMonitoring Active Positions...")
    risk_manager.monitor_positions()
    
    # Validate a new trade
    print("\nValidating New Trade for ADA/USD...")
    if risk_manager.validate_trade(pair='ADAUSD', entry_price=0.50):
        print("[INFO] Trade validated successfully.")
    else:
        print("[ERROR] Trade validation failed.")
