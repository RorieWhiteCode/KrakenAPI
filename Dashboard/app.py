# app.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import pandas as pd
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Mock Data (Replace with live data feeds later)
portfolio = {
    "balance": 10000,
    "equity": 12000,
    "open_positions": [
        {"pair": "ADAUSD", "type": "buy", "size": 1.2, "entry_price": 1.5, "current_price": 1.7},
        {"pair": "LTCUSD", "type": "sell", "size": 0.8, "entry_price": 90, "current_price": 85}
    ]
}

sentiment_signals = [
    {"pair": "ADAUSD", "signal": "Strong Buy", "score": 0.8},
    {"pair": "LTCUSD", "signal": "Hold", "score": 0.1}
]

trade_log = pd.DataFrame({
    "timestamp": pd.date_range(start='2024-06-01', periods=20, freq='D'),
    "pair": ["ADAUSD", "LTCUSD"] * 10,
    "action": ["buy", "sell"] * 10,
    "price": [random.uniform(1, 2) for _ in range(20)],
    "profit_loss": [random.uniform(-50, 100) for _ in range(20)]
})

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/portfolio')
def get_portfolio():
    return jsonify(portfolio)


@app.route('/api/sentiment')
def get_sentiment():
    return jsonify(sentiment_signals)


@app.route('/api/trade_log')
def get_trade_log():
    return trade_log.to_json(orient='records')


@socketio.on('connect')
def handle_connect():
    print('[INFO] Client connected to the dashboard')


@socketio.on('disconnect')
def handle_disconnect():
    print('[INFO] Client disconnected from the dashboard')


if __name__ == '__main__':
    socketio.run(app, debug=True)
