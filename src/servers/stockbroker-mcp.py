from fastmcp import Context, FastMCP
import yfinance as yf
import json

mcp = FastMCP(name="stockbroker")


@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """
    Retrieve the current price of a stock given a ticker symbol
    """
    stock = yf.Ticker(ticker)
    return stock.info["regularMarketPrice"]


@mcp.tool()
def list_portfolio_stocks(portfolio: list[str]) -> list[str]:
    """List all stocks in the user's portfolio. If not provided, the portfolio data is retrieved from the URI exposed by the resource `fetch_mcp_resource`."""
    return portfolio

# lets give the llm some context - the client is going to look through the exposed resources before deciding which tool to call and what args


@mcp.tool()
def fetch_latest_news(stock_ticker: str) -> dict:
    """
    Retrieves and returns the latest news for a given stock ticker

    Args:
        stock_ticker (str): The stock ticker to get the latest news for.

    Returns:
        dict: The latest news for the given stock ticker
    """
    stock = yf.Ticker(stock_ticker)
    return stock.news


@mcp.tool()
def summarize_portfolio(portfolio: list[str]) -> dict:
    """Summarizes market data for a given list of stock tickers.

    IMPORTANT: This tool requires a list of tickers as input. To get the user's
    default portfolio (if the portfolio is not provided), you must first call the
    `fetch_mcp_resource` tool with the server `stockbroker` and the URI 'myportfolio://portfolio' to retrieve the list of stocks.
    """

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
def fetch_mcp_portfolio() -> dict:
    """Retrieves and returns stocks in the user's portfolio"""
    return {
        "portfolio": ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "CSCO", "INTC"]
    }


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
