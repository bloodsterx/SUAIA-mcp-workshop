from fastmcp import Context, FastMCP
import yfinance as yf
import json

mcp = FastMCP(name="stockbroker")


@mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """
    Retrieve the current price of a stock given a ticker symbol
    """
    stock = yf.Ticker(ticker)
    return stock.info["regularMarketPrice"]


@mcp.tool()
def summarize_portfolio(portfolio: list[str]) -> dict:
    """Summarizes the portfolio of stocks in the user's portfolio"""

    portfolio_summary = {}
    for ticker in portfolio:
        stock = yf.Ticker(ticker)
        summary = {}
        summary["closing price"] = stock.info["regularMarketPrice"]
        summary["previous close"] = stock.info["regularMarketPreviousClose"]
        summary["change"] = stock.info["regularMarketPrice"] - \
            stock.info["regularMarketPreviousClose"]
        summary["news"] = stock.news

        portfolio_summary[ticker] = summary

    return portfolio_summary


@mcp.resource("myportfolio://portfolio")
def get_portfolio() -> dict:
    """Retrieves and returns stocks in the user's portfolio"""
    return {
        "portfolio": ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "CSCO", "INTC"]
    }


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
