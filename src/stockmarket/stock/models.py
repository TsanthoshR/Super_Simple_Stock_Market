"""Models for the stock market database.

This module defines the data models for stocks and trades in the stock market
application, including the abstract base class `Stock`, and its concrete
subclasses `CommonStock` and `PreferredStock`. It also defines the `Trade` class
to represent individual trades.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from stockmarket.stock.enums import StockType, TradeType


class Stock(ABC):
    """Abstract base class for a stock.

    Represents common behaviour shared by all stock types.

    Parameters
    ----------
    symbol : str
        Ticker symbol for the stock.
    stock_type : StockType
        The enumeration value for the stock type (COMMON or PREFERRED).
    last_dividend : float
        The last dividend value for the stock.
    fixed_dividend : float
        The fixed dividend (as a decimal) for preferred stock; otherwise 0.
    par_value : float
        The par value of the stock.
    """

    def __init__(
        self,
        symbol: str,
        stock_type: StockType,
        last_dividend: float,
        fixed_dividend: float,
        par_value: float,
    ):
        """Initialize a Stock instance.

        Parameters
        ----------
        symbol : str
            Ticker symbol for the stock.
        stock_type : StockType
            The enumeration value for the stock type (COMMON or PREFERRED).
        last_dividend : float
            The last dividend value for the stock.
        fixed_dividend : float
            The fixed dividend (as a decimal) for preferred stock; otherwise 0.
        par_value : float
            The par value of the stock.
        """

        self.symbol: str = symbol
        self.stock_type: StockType = stock_type
        self.last_dividend: float = last_dividend
        self.fixed_dividend: float = fixed_dividend
        self.par_value: float = par_value
        self.trades: List[Trade] = []

    @abstractmethod
    def calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield for the stock.

        Parameters
        ----------
        price : float
            The market price of the stock.

        Returns
        -------
        float
            The dividend yield.
        """
        pass

    def calculate_pe_ratio(self, price: float) -> float:  # Task a, ii
        """Calculate the P/E Ratio for the stock.

        Parameters
        ----------
        price : float
            The market price of the stock.

        Returns
        -------
        float
            The price-to-earnings ratio.
        """
        dividend = self.calculate_dividend_yield(price) * price
        # last dividend vs fixed dividend * par value
        if dividend == 0:
            raise ValueError("Dividend is zero, P/E Ratio is undefined.")
        return price / dividend

    def record_trade(
        self, trade_type: TradeType, quantity: int, price: float, timestamp: datetime | None = None
    ) -> "Trade":  # Task a, iii
        """Record a trade for the stock.

        Parameters
        ----------
        trade_type : TradeType
            The type of trade (buy or sell).
        quantity : int
            Number of shares traded.
        price : float
            Price per share for the trade.
        timestamp : datetime or None, optional
            The time the trade occurred. If None, current time is used.

        Returns
        -------
        Trade
            The recorded Trade instance.
        """

        timestamp = timestamp or datetime.now()

        trade = Trade(
            stock_symbol=self.symbol,
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            timestamp=timestamp,
        )
        self.trades.append(trade)

        return trade

    def get_trades_in_last_minutes(self, minutes: int) -> List["Trade"]:
        """Get trades recorded in the last given minutes.

        Parameters
        ----------
        minutes : int
            Lookback window in minutes.

        Returns
        -------
        List[Trade]
            Trades that occurred within the lookback window.
        """
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [trade for trade in self.trades if trade.timestamp >= cutoff_time]

    def calculate_volume_weighted_stock_price(self, minutes: int = 5) -> float:
        """Calculate the Volume Weighted Stock Price based on recent trades.

        Parameters
        ----------
        minutes : int, optional
            Lookback window in minutes (default is 5).

        Returns
        -------
        float
            The volume weighted stock price computed from recent trades.
        """
        recent_trades = self.get_trades_in_last_minutes(minutes)
        total_trade_price_quantity = sum(trade.price * trade.quantity for trade in recent_trades)
        total_quantity = sum(trade.quantity for trade in recent_trades)

        if total_quantity == 0:
            raise ValueError(
                "No trades in the given time frame to calculate Volume Weighted Stock Price."
            )

        return total_trade_price_quantity / total_quantity


class CommonStock(Stock):
    """Class representing a common stock.

    Common stocks calculate dividend yield from last_dividend.
    """

    def calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield for common stock.

        Parameters
        ----------
        price : float
            The market price of the stock.

        Returns
        -------
        float
            The dividend yield for a common stock.
        """
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return self.last_dividend / price


class PreferredStock(Stock):
    """Class representing a preferred stock.

    Preferred stocks use fixed_dividend and par_value to compute yield.
    """

    # def __init__(self, symbol, stock_type, last_dividend, fixed_dividend, par_value):
    #     super().__init__(symbol, stock_type, last_dividend, fixed_dividend, par_value)
    #     self.fixed_dividend = float(fixed_dividend)  # as a decimal (e.g., 0.02 for 2%)

    def calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield for preferred stock.

        Parameters
        ----------
        price : float
            The market price of the stock.

        Returns
        -------
        float
            The dividend yield for a preferred stock.
        """
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return (self.fixed_dividend * self.par_value) / price


@dataclass(frozen=True)
class Trade:
    """Class representing a trade in the stock market."""

    stock_symbol: str
    trade_type: TradeType  # 'buy' or 'sell'
    quantity: int
    price: float
    timestamp: datetime


# class StockFactory:
#     """Factory class to create stock instances based on stock type."""

#     @staticmethod
#     def create_stock(symbol: str,
#                      stock_type: StockType,
#                      last_dividend: float,
#                      fixed_dividend: float,
#                      par_value: float) -> Stock:
#         """Create a stock instance based on the stock type."""
#         if stock_type == StockType.COMMON:
#             return CommonStock(symbol, stock_type, last_dividend, fixed_dividend, par_value)
#         elif stock_type == StockType.PREFERRED:
#             return PreferredStock(symbol, stock_type, last_dividend, fixed_dividend, par_value)
#         else:
#             raise ValueError(f"Unknown stock type: {stock_type}")


# @dataclass
# class StockMarket:
#     """Class representing the stock market."""
#     stocks: List[Stock] = field(default_factory=list)

#     def add_stock(self, stock: Stock):
#         """Add a stock to the stock market."""
#         self.stocks.append(stock)

#     def get_stock(self, symbol: str) -> Stock:
#         """Retrieve a stock by its symbol."""
#         for stock in self.stocks:
#             if stock.symbol == symbol:
#                 return stock
#         raise ValueError(f"Stock with symbol {symbol} not found.")

#     def list_stocks(self) -> List[Stock]:
#         """List all stocks in the stock market."""
#         return self.stocks
