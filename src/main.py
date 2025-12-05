""" " Main file for the Super Simple Stock Market application."""

from my_logger import daily_logger
from src.stockmarket.exchange.market import GBCE
from src.stockmarket.stock.enums import TradeType

if __name__ == "__main__":
    StockMarketApp = GBCE()

    # Example usage: calculate the GBCE All Share Index
    StockMarketApp = GBCE()
    gbce_index = StockMarketApp.calculate_gbce_all_share_index()
    daily_logger.info(f"GBCE All Share Index: {gbce_index}")

    # Example 2:
    StockMarketApp2 = GBCE()
    daily_logger.info(StockMarketApp2.list_stocks())
    daily_logger.info(StockMarketApp2.get_stock("TEA"))
    # print(StockMarketApp.get_stock("TEA").calculate_pe_ratio(100.0))

    pop_stock = StockMarketApp2.get_stock("POP")
    if pop_stock is not None:
        daily_logger.info(f"POP P/E Ratio: {pop_stock.calculate_pe_ratio(100.0)}")
        daily_logger.info(
            "POP dividend yield", pop_stock.calculate_dividend_yield(100.0)
        )

    gin_stock = StockMarketApp2.get_stock("GIN")
    if gin_stock is not None:
        daily_logger.info(
            "GIN dividend yield", gin_stock.calculate_dividend_yield(100.0)
        )
        daily_logger.info(
            "GIN dividend yield", gin_stock.calculate_dividend_yield(100.0)
        )

    # print("JOE dVWSP", StockMarketApp.get_stock("GIN").calculate_volume_weighted_stock_price())
    StockMarketApp2.record_trade(
        "JOE", trade_type=TradeType.BUY, quantity=200, price=105.0
    )
    JOE_Stock = StockMarketApp2.get_stock("JOE")
    assert JOE_Stock is not None
    daily_logger.info("JOE VWSP", JOE_Stock.calculate_volume_weighted_stock_price())
    #

    # StockMarketApp2.record_trade("TEA", "buy", 100, 110.0)
    gbce_index = StockMarketApp2.calculate_gbce_all_share_index()
    print(f"GBCE All Share Index: {gbce_index}")

    # Example 3:
    SM3 = GBCE()
    daily_logger.info(SM3.list_stocks())

    # print("JOE dVWSP", StockMarketApp.get_stock("GIN").calculate_volume_weighted_stock_price())
    SM3.record_trade(symbol="JOE", trade_type=TradeType.BUY, quantity=100, price=200.0)
    joe_stock = SM3.get_stock("JOE")
    if joe_stock is not None:
        daily_logger.info(
            "JOE VWSP",
            joe_stock.calculate_volume_weighted_stock_price(),
        )

    SM3.record_trade(symbol="TEA", trade_type=TradeType.SELL, quantity=100, price=100.0)
    gbce_index = SM3.calculate_gbce_all_share_index()
    daily_logger.info(f"GBCE All Share Index: {gbce_index}")  # sqrt 200*100 = 141.42
