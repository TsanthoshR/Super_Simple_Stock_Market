"""Test for Models module."""

import unittest
from datetime import datetime, timedelta

from src.stockmarket.stock.enums import TradeType
from src.stockmarket.stock.exceptions import NoTradeError
from src.stockmarket.stock.models import CommonStock, PreferredStock


class TestStockModels(unittest.TestCase):
    """Unit tests for Stock models.

    Args:
        unittest (_type_): _description_
    """

    def setUp(self) -> None:
        """Setup for the tests."""
        self.commom_stock = CommonStock(
            symbol="TEST", last_dividend=8.0, par_value=100.0
        )
        self.preferred_stock = PreferredStock(
            symbol="PTEST", last_dividend=8.0, fixed_dividend=0.02, par_value=100.0
        )

    def test_dividend_yield_common(self) -> None:
        """Test dividend yield calculation for common stock."""
        price = 100.0
        expected_yield = 0.08  # 8 / 100
        self.assertAlmostEqual(
            self.commom_stock.calculate_dividend_yield(price), expected_yield
        )

    def test_dividend_yield_preferred(self) -> None:
        """Test dividend yield calculation for preferred stock."""
        price = 100.0
        expected_yield = 0.02  # (0.02 * 100) / 100
        self.assertAlmostEqual(
            self.preferred_stock.calculate_dividend_yield(price), expected_yield
        )

    def test_pe_ratio_common(self) -> None:
        """Test P/E ratio calculation for common stock."""
        price = 100.0
        expected_pe = 12.5  # 100 / 8
        self.assertAlmostEqual(self.commom_stock.calculate_pe_ratio(price), expected_pe)

    def test_pe_ratio_preferred(self) -> None:
        """Test P/E ratio calculation for preferred stock."""
        price = 100.0
        expected_pe = 50.0  # 100 / (0.02 * 100)
        self.assertAlmostEqual(
            self.preferred_stock.calculate_pe_ratio(price), expected_pe
        )

    def test_pe_ration_zero_dividend_common_raises(self) -> None:
        """Test that P/E ratio calculation raises ZeroDivisionError for zero
        dividend."""
        zero_dividend_stock = CommonStock(
            symbol="ZERO", last_dividend=0.0, par_value=100.0
        )
        with self.assertRaises(ValueError):
            zero_dividend_stock.calculate_pe_ratio(100.0)

    def test_pe_ration_zero_dividend_raises(self) -> None:
        """Test that P/E ratio calculation raises ZeroDivisionError for zero
        dividend."""
        zero_dividend_stock = CommonStock(
            symbol="ZERO", last_dividend=0.0, par_value=100.0
        )
        with self.assertRaises(ValueError):
            zero_dividend_stock.calculate_pe_ratio(100.0)

    def test_trade_and_vwsp(self) -> None:
        """Test trade recording and VWSP calculation."""
        stock = CommonStock(symbol="TRADE", last_dividend=5.0, par_value=100.0)

        # Record trades
        now = datetime.now()
        stock.record_trade(
            timestamp=now - timedelta(minutes=10),
            quantity=100,
            trade_type=TradeType.BUY,
            price=110.0,
        )
        stock.record_trade(
            timestamp=now - timedelta(minutes=5),
            quantity=50,
            trade_type=TradeType.SELL,
            price=130.0,
        )
        stock.record_trade(
            timestamp=now - timedelta(minutes=20),
            quantity=200,
            trade_type=TradeType.BUY,
            price=120.0,
        )  # Outside 15 min window

        vwsp = stock.calculate_volume_weighted_stock_price(minutes=15)
        expected_vwsp = (100 * 110.0 + 50 * 130.0) / (100 + 50)
        self.assertAlmostEqual(vwsp, expected_vwsp)

    def test_vwsp_no_trades_raises(self) -> None:
        """Test that VWSP calculation raises NoTradeError when no trades exist."""
        stock = CommonStock(symbol="NOTRADE", last_dividend=5.0, par_value=100.0)
        with self.assertRaises(NoTradeError):
            stock.calculate_volume_weighted_stock_price(minutes=15)

    def test_trade_type_enum(self) -> None:
        """Test that TradeType enum works correctly."""
        trade = self.commom_stock.record_trade(
            timestamp=datetime.now(),
            quantity=100,
            trade_type=TradeType.BUY,
            price=50.0,
        )

        self.assertEqual(trade.trade_type.value, "buy")

    if __name__ == "__main__":
        unittest.main()
