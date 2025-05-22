#!/usr/bin/env python3
"""
MCP Server for financial data.

This script implements an MCP server that provides tools for accessing
financial data using yfinance.
"""

import logging
from datetime import datetime
from typing import Any, Dict

import yfinance as yf
from mcp.server.fastmcp import Context, FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create a FastMCP server
mcp = FastMCP("Financial Data MCP")


@mcp.tool(description="Get basic information about a stock")
def get_stock_info(ticker: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Get basic information about a stock.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT).
        ctx: Optional context for providing info and progress updates.

    Returns:
        Dict containing basic information about the stock.
    """
    try:
        if ctx:
            ctx.info(f"Fetching information for {ticker}...")

        stock = yf.Ticker(ticker)
        info = stock.info

        # Filter relevant information
        relevant_info = {
            "shortName": info.get("shortName", ""),
            "longName": info.get("longName", ""),
            "symbol": info.get("symbol", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "marketCap": info.get("marketCap", 0),
            "currentPrice": info.get("currentPrice", 0),
            "currency": info.get("currency", "USD"),
        }
        return relevant_info
    except Exception as e:
        logger.error(f"Error getting stock info for {ticker}: {e}")
        return {"error": f"Could not retrieve information for {ticker}: {str(e)}"}


@mcp.tool(description="Get the current price of a stock")
def get_stock_price(ticker: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Get the current price of a stock.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT).
        ctx: Optional context for providing info and progress updates.

    Returns:
        Dict containing the current price of the stock.
    """
    try:
        if ctx:
            ctx.info(f"Fetching current price for {ticker}...")

        stock = yf.Ticker(ticker)
        current_price = stock.info.get(
            "currentPrice", stock.info.get("regularMarketPrice", 0)
        )
        return {
            "symbol": ticker,
            "price": current_price,
            "currency": stock.info.get("currency", "USD"),
            "asOf": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error getting stock price for {ticker}: {e}")
        return {"error": f"Could not retrieve price for {ticker}: {str(e)}"}


@mcp.tool(description="Get financial statements data for a company")
def get_financial_data(
    ticker: str, statement_type: str = "income", ctx: Context = None
) -> Dict[str, Any]:
    """
    Get financial statements data for a company.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT).
        statement_type: Type of financial statement to retrieve.
                        Options: "income", "balance", "cash".
        ctx: Optional context for providing info and progress updates.

    Returns:
        Dict containing the financial data.
    """
    try:
        if ctx:
            ctx.info(f"Fetching {statement_type} statement for {ticker}...")

        stock = yf.Ticker(ticker)

        if statement_type.lower() == "income":
            financials = stock.income_stmt
            statement_name = "Income Statement"
        elif statement_type.lower() == "balance":
            financials = stock.balance_sheet
            statement_name = "Balance Sheet"
        elif statement_type.lower() == "cash":
            financials = stock.cashflow
            statement_name = "Cash Flow Statement"
        else:
            return {
                "error": f"Invalid statement type: {statement_type}. Use 'income', 'balance', or 'cash'."
            }

        # Convert to dict for JSON serialization
        if financials is not None and not financials.empty:
            financial_data = financials.to_dict()

            # Process the nested dictionaries for easier consumption
            processed_data = {}
            for metric, values in financial_data.items():
                processed_data[str(metric)] = {
                    str(date): value for date, value in values.items()
                }

            return {
                "symbol": ticker,
                "statement": statement_name,
                "data": processed_data,
            }
        else:
            return {"error": f"No {statement_name} data available for {ticker}."}
    except Exception as e:
        logger.error(f"Error getting financial data for {ticker}: {e}")
        return {"error": f"Could not retrieve financial data for {ticker}: {str(e)}"}


@mcp.tool(description="Get key financial metrics including EBITDA for a company")
def get_key_metrics(ticker: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Get key financial metrics including EBITDA for a company.

    Args:
        ticker: The stock ticker symbol (e.g., IBM, AAPL).
        ctx: Optional context for providing info and progress updates.

    Returns:
        Dict containing key financial metrics.
    """
    try:
        if ctx:
            ctx.info(f"Fetching key metrics for {ticker}...")

        stock = yf.Ticker(ticker)
        income_stmt = stock.income_stmt

        # Get the most recent financial data
        if income_stmt is not None and not income_stmt.empty:
            # Get the most recent column (latest period)
            latest_data = income_stmt.iloc[:, 0]

            # Extract key metrics
            ebitda = float(latest_data.get("EBITDA", 0))
            total_revenue = float(latest_data.get("Total Revenue", 0))
            net_income = float(latest_data.get("Net Income", 0))

            # Get additional info
            info = stock.info
            market_cap = info.get("marketCap", 0)

            # Calculate some ratios
            ebitda_margin = (ebitda / total_revenue) if total_revenue else 0

            return {
                "symbol": ticker,
                "period": str(income_stmt.columns[0].date())
                if hasattr(income_stmt.columns[0], "date")
                else str(income_stmt.columns[0]),
                "metrics": {
                    "EBITDA": ebitda,
                    "Total Revenue": total_revenue,
                    "Net Income": net_income,
                    "Market Cap": market_cap,
                    "EBITDA Margin": ebitda_margin,
                },
            }
        else:
            return {"error": f"No financial data available for {ticker}."}
    except Exception as e:
        logger.error(f"Error getting key metrics for {ticker}: {e}")
        return {"error": f"Could not retrieve key metrics for {ticker}: {str(e)}"}


# Example resource to demonstrate resource capabilities
@mcp.resource("finance://info/{ticker}")
def get_finance_info(ticker: str) -> str:
    """Get financial information for a ticker symbol as a resource."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return f"""
        Company: {info.get("longName", "Unknown")}
        Symbol: {ticker}
        Sector: {info.get("sector", "Unknown")}
        Industry: {info.get("industry", "Unknown")}
        Current Price: {info.get("currentPrice", "Unknown")} {info.get("currency", "USD")}
        Market Cap: {info.get("marketCap", "Unknown")}
        """
    except Exception as e:
        return f"Error retrieving finance info for {ticker}: {e}"


if __name__ == "__main__":
    logger.info("Starting Financial Data MCP server...")
    mcp.run()
