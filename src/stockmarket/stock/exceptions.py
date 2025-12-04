"""Exceptions for stock market database operations."""


class InvalistStockError(Exception):
    """Exception raised for invalid stock operations."""

    pass


class InvalidTradeError(Exception):
    """Exception raised for invalid trade operations."""

    pass


class NoTradeError(Exception):
    """Exception raised when there are no trades to perform an operation."""

    pass


class InvalidTradeTypeError(Exception):
    """Exception raised for invalid trade type."""

    pass
