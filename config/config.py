# ============================================
# Kraken API Credentials
# ============================================
API_KEY = "your_api_key_here"  # Replace with your Kraken API Key
API_SECRET = "your_api_secret_here"  # Replace with your Kraken API Secret

# ============================================
# Portfolio and Leverage Settings
# ============================================
LEVERAGE = {
    "ADA": 4,  # 4x leverage for ADA
    "LTC": 3   # 3x leverage for LTC
}
MAX_PORTFOLIO_EXPOSURE = 0.3  # 30% max exposure per position
RESERVE_BALANCE = 0.1  # 10% reserved as cash buffer
BASE_CURRENCY = "USD"  # Choose 'USD' or 'GBP'
ALLOWED_PAIRS = ["ADA/USD", "LTC/USD", "DOT/USD"]

# ============================================
# Strategy Settings
# ============================================
TIMEFRAME = "1h"  # Trading timeframe (e.g., 1h, 4h, 1d)
TAKE_PROFIT = 0.1  # 10% take-profit per trade
STOP_LOSS = 0.05  # 5% stop-loss per trade
MAX_CONCURRENT_POSITIONS = 5  # Max number of simultaneous positions

# ============================================
# Risk Management
# ============================================
MAX_DAILY_DRAWDOWN = 0.05  # Stop trading after 5% loss in a day
TRAILING_STOP = 0.02  # 2% trailing stop
RISK_PER_TRADE = 0.02  # 2% risk per trade

# ============================================
# Logging and Monitoring
# ============================================
ENABLE_LOGGING = True  # Enable or disable logging
LOG_FILE = "./logs/tradebot.log"  # Log file location
NOTIFICATIONS = {
    "email": False,
    "telegram": True,
    "sms": False
}

# ============================================
# Execution and Throttling
# ============================================
ORDER_TYPE = "market"  # Default order type ('market' or 'limit')
API_CALL_DELAY = 1  # Delay between API calls (in seconds)
TRADING_MODE = "live"  # Modes: 'live', 'paper_trade', 'backtest'
