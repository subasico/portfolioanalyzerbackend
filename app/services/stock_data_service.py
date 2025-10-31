import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class StockDataService:
    """Service to fetch stock data using yfinance"""

    @staticmethod
    async def get_stock_info(symbol: str) -> Optional[Dict]:
        """Fetch stock information for a given symbol"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "beta": info.get("beta", 1.0),
                "dividend_yield": info.get("dividendYield", 0),
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return None

    @staticmethod
    async def get_batch_stock_info(symbols: List[str]) -> List[Dict]:
        """Fetch stock information for multiple symbols"""
        results = []
        for symbol in symbols:
            info = await StockDataService.get_stock_info(symbol)
            if info:
                results.append(info)
        return results

    @staticmethod
    def calculate_portfolio_volatility(symbols: List[str], weights: List[float], period: str = "1y") -> float:
        """Calculate portfolio volatility based on historical data"""
        try:
            # Download historical data
            data = yf.download(symbols, period=period, progress=False)['Close']

            # Calculate returns
            returns = data.pct_change().dropna()

            # Calculate weighted volatility
            if len(symbols) == 1:
                return returns.std() * 100

            # Portfolio variance calculation
            cov_matrix = returns.cov()
            portfolio_variance = 0

            for i, symbol_i in enumerate(symbols):
                for j, symbol_j in enumerate(symbols):
                    portfolio_variance += weights[i] * weights[j] * cov_matrix.iloc[i, j]

            portfolio_volatility = (portfolio_variance ** 0.5) * 100
            return portfolio_volatility

        except Exception as e:
            logger.error(f"Error calculating portfolio volatility: {str(e)}")
            return 15.0  # Default moderate volatility
