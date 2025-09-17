from fastmcp import FastMCP
import yfinance as yf
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime

# Set up logging to logs/ directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Create log filename with timestamp
log_filename = os.path.join(
    log_dir, f"stockbroker_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    filename=log_filename,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="stockbroker")

# provide functionality with tools - similar to POST endpoints; we use tools to execute code/do tasks
# the llm will scan the tools (indicated by decorator @mcp.tool() and decide on the most appropriate tool for the user's query
# The llm reads the function signature (arguments and return value), and reads the docstring - these are considered by the llm before deciding on the tool to call and arguments to provide


@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """
    Retrieve the current price of a stock given a ticker symbol
    """
    stock = yf.Ticker(ticker)
    return stock.info["regularMarketPrice"]


@mcp.tool()
def get_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive information about a stock given a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')

    Returns:
        Dictionary containing stock information including price, market cap, volume, etc.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        if not info:
            raise ValueError(f"No data available for ticker: {ticker}")

        # Extract key information
        stock_data = {
            'ticker': ticker.upper(),
            'name': info.get('longName', 'N/A'),
            'current_price': info.get('regularMarketPrice', 'N/A'),
            'previous_close': info.get('previousClose', 'N/A'),
            'day_change': info.get('regularMarketChange', 'N/A'),
            'day_change_percent': info.get('regularMarketChangePercent', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'volume': info.get('volume', 'N/A'),
            'avg_volume': info.get('averageVolume', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': info.get('dividendYield', 'N/A'),
            '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A')
        }

        logger.info(f"Retrieved comprehensive info for {ticker}")
        return stock_data

    except Exception as e:
        logger.error(f"Error retrieving stock info for {ticker}: {str(e)}")
        raise ValueError(
            f"Failed to retrieve stock information for {ticker}: {str(e)}")


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
