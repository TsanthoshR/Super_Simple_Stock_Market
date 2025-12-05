"""Simple performance tests for GBCE market operations."""

import timeit
import unittest

from my_logger import daily_logger
from src.stockmarket.exchange.market import GBCE
from src.stockmarket.stock.enums import TradeType
from src.stockmarket.stock.models import CommonStock


class TestGBCEPerformance(unittest.TestCase):
    """Performance tests for GBCE market operations."""

    def setUp(self) -> None:
        self.market = GBCE()
        self.stock_symbols = [f"TEST{i}" for i in range(100)]

        for symbol in self.stock_symbols:
            stock = CommonStock(symbol=symbol, last_dividend=5.0, par_value=100.0)
            self.market.add_Stock(stock)

    def test_record_trade_performance(self):
        """Test performance of recording trades."""

        def record_trades() -> None:
            """Record trades for all test stocks."""
            for symbol in self.stock_symbols:
                self.market.record_trade(
                    symbol=symbol,
                    trade_type=TradeType.BUY,
                    quantity=10,
                    price=100.0,
                )

        duration = timeit.timeit(record_trades, number=10)
        daily_logger.info(
            f"Recording trades for 100 stocks took {duration:.4f} seconds."
        )

        self.assertLess(duration, 0.5, "Recording trades took too long.")

    def test_vwap_performance(self) -> None:
        """Test performance of calculating VWAP for all stocks."""
        # First, record some trades to have data for VWAP calculation
        for symbol in self.stock_symbols:
            self.market.record_trade(
                symbol=symbol,
                trade_type=TradeType.BUY,
                quantity=10,
                price=100.0,
            )

        def calculate_vwap_all() -> None:
            """Calculate VWAP for all test stocks."""
            for symbol in self.stock_symbols:
                stock = self.market.get_stock(symbol)
                if stock:
                    stock.calculate_volume_weighted_stock_price()

        duration = timeit.timeit(calculate_vwap_all, number=10)
        daily_logger.info(
            f"Calculating VWAP for 100 stocks took {duration:.4f} seconds."
        )

        self.assertLess(duration, 0.5, "VWAP calculation took too long.")

    def test_calculate_gbce_performance(self):
        """Test performance of calculating GBCE All Share Index."""
        # First, record some trades to have prices
        for symbol in self.stock_symbols:
            self.market.record_trade(
                symbol=symbol,
                trade_type="BUY",
                quantity=10,
                price=100.0,
            )

        duration = timeit.timeit(self.market.calculate_gbce_all_share_index, number=10)
        daily_logger.info(
            f"Calculating GBCE All Share Index took {duration:.4f} seconds."
        )
        self.assertLess(
            duration, 0.5, "GBCE All Share Index calculation took too long."
        )
