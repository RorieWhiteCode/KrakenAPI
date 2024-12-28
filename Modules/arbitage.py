# arbitrage.py
from data_handler import KrakenDataHandler


class Arbitrage:
    def __init__(self):
        self.data_handler = KrakenDataHandler()

    def find_opportunity(self):
        usd_price = float(self.data_handler.get_ticker('ADAUSD')['ADAUSD']['c'][0])
        eur_price = float(self.data_handler.get_ticker('ADAEUR')['ADAEUR']['c'][0])
        eur_usd = float(self.data_handler.get_ticker('EURUSD')['EURUSD']['c'][0])

        implied_usd_price = eur_price * eur_usd
        spread = abs(usd_price - implied_usd_price)

        if spread > 0.5:  # Threshold for profitable arbitrage
            print("[INFO] Arbitrage Opportunity Found!")
            print(f"ADA/USD: {usd_price}, Implied USD from EUR: {implied_usd_price}, Spread: {spread}")
        else:
            print("[INFO] No significant arbitrage opportunities.")


if __name__ == '__main__':
    arb = Arbitrage()
    arb.find_opportunity()
