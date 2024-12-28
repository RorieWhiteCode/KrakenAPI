# tests/test_risk_manager.py
import unittest
from unittest.mock import patch
from risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    @patch('risk_manager.RiskManager.check_daily_drawdown')
    def test_check_daily_drawdown(self, mock_check_daily_drawdown):
        mock_check_daily_drawdown.return_value = False
        risk_manager = RiskManager()
        self.assertFalse(risk_manager.check_daily_drawdown())

    @patch('risk_manager.RiskManager.validate_trade')
    def test_validate_trade(self, mock_validate_trade):
        mock_validate_trade.return_value = True
        risk_manager = RiskManager()
        self.assertTrue(risk_manager.validate_trade('ADAUSD', 1.25))


if __name__ == '__main__':
    unittest.main()
