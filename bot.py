# bot.py
import time
from strategy import Strategy
from portfolio import PortfolioManager
from trade_executor import TradeExecutor
from risk_manager import RiskManager
from config import TRADING_MODE, API_CALL_DELAY

class TradingBot:
    def __init__(self):
        # Initialize all modules
        self.strategy = Strategy()
        self.portfolio = PortfolioManager()
        self.executor = TradeExecutor()
        self.risk_manager = RiskManager()
        self.running = True  # Control flag for the bot loop

    # Run pre-trade checks (risk and drawdown validation)
    def pre_trade_checks(self) -> bool:
        if self.risk_manager.check_daily_drawdown():
            print("[HALT] Trading halted due to daily drawdown limit.")
            return False
        return True

    # Execute a trade based on strategy signals
    def execute_trade(self, pair: str):
        signal = self.strategy.combined_strategy(pair)
        print(f"[INFO] Strategy Signal for {pair}: {signal}")
        
        if signal == "buy":
            entry_price = float(self.strategy.data_handler.get_ticker(pair)[pair]['c'][0])
            if self.risk_manager.validate_trade(pair, entry_price):
                volume = self.risk_manager.calculate_position_size(entry_price)
                self.executor.place_market_order(pair, volume, 'buy')
                self.portfolio.add_position(pair, volume)
        
        elif signal == "sell":
            self.executor.place_market_order(pair, 1.0, 'sell')  # Placeholder volume
            self.portfolio.close_position(pair)
        
        else:
            print(f"[INFO] No trade action for {pair} (Signal: {signal}).")

    # Monitor and manage active trades
    def monitor_trades(self):
        print("[INFO] Monitoring active positions for risk triggers...")
        self.risk_manager.monitor_positions()

    # Main bot loop
    def run(self):
        print(f"[START] Trading Bot running in {TRADING_MODE.upper()} mode.")
        try:
            while self.running:
                if not self.pre_trade_checks():
                    print("[HALT] Bot shutting down due to failed pre-trade checks.")
                    break

                for pair in self.portfolio.positions.keys() or ['ADAUSD', 'LTCUSD']:
                    print(f"\n[INFO] Processing pair: {pair}")
                    self.execute_trade(pair)
                    time.sleep(API_CALL_DELAY)
                
                self.monitor_trades()
                print("[INFO] Cycle complete. Sleeping before next iteration.")
                time.sleep(10)  # Pause before the next cycle

        except KeyboardInterrupt:
            print("[STOP] Bot stopped manually.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")
        finally:
            self.shutdown()

    # Clean shutdown procedure
    def shutdown(self):
        self.running = False
        print("[SHUTDOWN] Trading Bot has been stopped. All systems are offline.")


# Example usage
if __name__ == '__main__':
    bot = TradingBot()
    bot.run()
