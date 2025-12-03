"""Enums for stock types and trade types."""

from enum import Enum


class StockType(str, Enum):
    """Enumeration for different types of stocks."""

    COMMON = "common"
    PREFERRED = "preferred"


class TradeType(str, Enum):
    """Enumeration for different types of trades."""

    BUY = "buy"
    SELL = "sell"
