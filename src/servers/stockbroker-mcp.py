from fastmcp import FastMCP
import yfinance as yf

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


if __name__ == "__main__":
    # This runs the server. Transport parameter allows you to specify STDIO transport (local filesystem) and HTTPS ()
    mcp.run()
