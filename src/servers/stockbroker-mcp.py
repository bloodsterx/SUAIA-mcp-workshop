from fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP(name="stockbroker")


@mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """
    Retrieve the current price of a stock given a ticker symbol
    """
    stock = yf.Ticker(ticker)
    return stock.info["regularMarketPrice"]

# lets give the llm some context - the client is going to look through the exposed resources before deciding which tool to call and what args


@mcp.resource("myportfolio://portfolio")
def get_portfolio() -> dict:
    """Retrieves and returns stock tickers in the user's portfolio"""
    return {
        "portfolio": ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "CSCO", "INTC"]
    }


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


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
