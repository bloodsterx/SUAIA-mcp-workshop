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


@mcp.prompt("detailed-stock-analysis-prompt")
def detailed_stock_analysis_prompt(ticker: str, company_name: str = "") -> str:
    """
    Generates a detailed, context-rich prompt for an LLM to perform a professional-grade stock analysis, including recent performance, risk factors, sentiment, and actionable insights.
    """
    return f"""
You are a financial analyst at a leading investment firm. Your task is to provide a comprehensive, data-driven analysis of the stock {ticker}{' (' + company_name + ')' if company_name else ''} for a client considering a significant investment. Your analysis should include:

1. A concise summary of the company's business and its position in the industry.
2. Recent stock price performance (last 6 months), highlighting key trends and volatility.
3. Notable news, events, or earnings reports in the past quarter that have impacted the stock.
4. An assessment of current market sentiment (bullish, bearish, or neutral) with supporting evidence.
5. Identification of major risks and opportunities facing the company.
6. A summary of analyst consensus (if available) and any recent changes in ratings or price targets.
7. Your actionable recommendation (buy, hold, sell) with a brief rationale.

Be objective, cite data where possible, and keep your response under 300 words. Format your answer with clear headings for each section."
"""


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
