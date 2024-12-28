# ml_predictor.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from data_handler import KrakenDataHandler


class PricePredictor:
    def __init__(self):
        self.model = GradientBoostingClassifier()
        self.data_handler = KrakenDataHandler()

    def fetch_data(self, pair: str):
        df = self.data_handler.get_ohlc(pair, interval=60)
        if df.empty:
            return pd.DataFrame()
        df['return'] = df['close'].pct_change()
        df['future_return'] = df['close'].shift(-1).pct_change()
        df['target'] = (df['future_return'] > 0).astype(int)
        return df.dropna()

    def train_model(self, pair: str):
        data = self.fetch_data(pair)
        if data.empty:
            print("[ERROR] No data to train model.")
            return

        X = data[['open', 'high', 'low', 'close', 'volume']]
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"[INFO] Model trained with accuracy: {accuracy:.2f}")

    def predict(self, pair: str):
        data = self.fetch_data(pair).tail(1)
        if data.empty:
            return 'hold'
        prediction = self.model.predict(data[['open', 'high', 'low', 'close', 'volume']])
        return 'buy' if prediction[0] == 1 else 'sell'
    

if __name__ == '__main__':
    predictor = PricePredictor()
    predictor.train_model('ADAUSD')
    signal = predictor.predict('ADAUSD')
    print(f"[INFO] Prediction Signal: {signal}")
