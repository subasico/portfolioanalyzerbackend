from typing import List, Dict
import logging
from collections import defaultdict
import numpy as np
from datetime import datetime
import uuid

from app.models.portfolio import (
    PortfolioRequest, PortfolioAnalysis, SectorBreakdown,
    RiskMetrics, StockHolding
)
from app.services.stock_data_service import StockDataService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class PortfolioAnalyzer:
    """Main service for portfolio analysis"""

    def __init__(self):
        self.stock_service = StockDataService()
        self.llm_service = LLMService()

    async def analyze_portfolio(self, portfolio: PortfolioRequest) -> PortfolioAnalysis:
        """Perform complete portfolio analysis"""

        # Extract symbols and allocations
        symbols = [holding.symbol for holding in portfolio.holdings]
        allocations = [holding.allocation for holding in portfolio.holdings]

        # Fetch stock data
        stock_details = await self.stock_service.get_batch_stock_info(symbols)

        # Calculate sector breakdown
        sector_breakdown = self._calculate_sector_breakdown(stock_details, portfolio.holdings)

        # Calculate risk metrics
        risk_metrics = await self._calculate_risk_metrics(
            stock_details, allocations, symbols
        )

        # Generate diversification analysis
        diversification_analysis = self._generate_diversification_analysis(
            sector_breakdown, stock_details, len(portfolio.holdings)
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            sector_breakdown, risk_metrics, stock_details, portfolio.holdings
        )

        # Portfolio summary
        portfolio_summary = {
            "total_stocks": len(portfolio.holdings),
            "total_sectors": len(sector_breakdown),
            "largest_holding": max(portfolio.holdings, key=lambda x: x.allocation).symbol,
            "largest_holding_pct": max(holding.allocation for holding in portfolio.holdings),
        }

        # Generate AI insights using LLM
        ai_insights = await self.llm_service.generate_portfolio_insights(
            portfolio_summary=portfolio_summary,
            sector_breakdown=sector_breakdown,
            risk_metrics=risk_metrics,
            stock_details=stock_details,
            holdings=portfolio.holdings
        )

        return PortfolioAnalysis(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            portfolio_summary=portfolio_summary,
            sector_breakdown=sector_breakdown,
            risk_metrics=risk_metrics,
            diversification_analysis=diversification_analysis,
            recommendations=recommendations,
            ai_insights=ai_insights,
            stock_details=stock_details
        )

    def _calculate_sector_breakdown(
        self, stock_details: List[Dict], holdings: List[StockHolding]
    ) -> List[SectorBreakdown]:
        """Calculate sector allocation breakdown"""

        sector_map = defaultdict(lambda: {"allocation": 0.0, "stocks": []})

        for detail, holding in zip(stock_details, holdings):
            sector = detail.get("sector", "Unknown")
            sector_map[sector]["allocation"] += holding.allocation
            sector_map[sector]["stocks"].append(detail["symbol"])

        return [
            SectorBreakdown(
                sector=sector,
                allocation=round(data["allocation"], 2),
                stocks=data["stocks"]
            )
            for sector, data in sorted(
                sector_map.items(),
                key=lambda x: x[1]["allocation"],
                reverse=True
            )
        ]

    async def _calculate_risk_metrics(
        self, stock_details: List[Dict], allocations: List[float], symbols: List[str]
    ) -> RiskMetrics:
        """Calculate portfolio risk metrics"""

        # Diversification score (based on number of stocks and allocation spread)
        num_stocks = len(stock_details)
        max_allocation = max(allocations)

        # Herfindahl index for concentration
        hhi = sum((alloc / 100) ** 2 for alloc in allocations)
        diversification_score = (1 - hhi) * 100

        # Calculate average beta (market risk)
        betas = [detail.get("beta", 1.0) for detail in stock_details]
        weighted_beta = sum(
            beta * (alloc / 100) for beta, alloc in zip(betas, allocations)
        )

        # Calculate volatility
        weights = [alloc / 100 for alloc in allocations]
        portfolio_volatility = self.stock_service.calculate_portfolio_volatility(
            symbols, weights
        )

        # Overall risk score (0-100, higher = more risky)
        risk_score = min(100, (
            (weighted_beta * 20) +  # Beta contribution
            (portfolio_volatility * 2) +  # Volatility contribution
            (hhi * 30) +  # Concentration risk
            (max(0, 100 - diversification_score) * 0.3)  # Lack of diversification
        ))

        # Determine volatility level
        if portfolio_volatility < 15:
            volatility_level = "Low"
        elif portfolio_volatility < 25:
            volatility_level = "Medium"
        else:
            volatility_level = "High"

        # Concentration risk
        if max_allocation > 40:
            concentration_risk = "High"
        elif max_allocation > 25:
            concentration_risk = "Medium"
        else:
            concentration_risk = "Low"

        return RiskMetrics(
            risk_score=round(risk_score, 2),
            diversification_score=round(diversification_score, 2),
            volatility_level=volatility_level,
            concentration_risk=concentration_risk
        )

    def _generate_diversification_analysis(
        self, sector_breakdown: List[SectorBreakdown], stock_details: List[Dict], num_stocks: int
    ) -> str:
        """Generate textual diversification analysis"""

        num_sectors = len(sector_breakdown)
        top_sector = sector_breakdown[0]

        analysis = f"Your portfolio contains {num_stocks} stocks across {num_sectors} sectors. "

        if top_sector.allocation > 50:
            analysis += f"The portfolio is heavily concentrated in {top_sector.sector} ({top_sector.allocation}%), " \
                       f"which may increase sector-specific risk. "
        elif top_sector.allocation > 30:
            analysis += f"The portfolio has moderate concentration in {top_sector.sector} ({top_sector.allocation}%). "
        else:
            analysis += f"The portfolio shows good sector diversification with {top_sector.sector} as the largest sector at {top_sector.allocation}%. "

        if num_stocks < 5:
            analysis += "Consider adding more holdings to improve diversification."
        elif num_stocks > 20:
            analysis += "The portfolio has many holdings, which provides good diversification but may be challenging to monitor."
        else:
            analysis += "The number of holdings provides a reasonable balance between diversification and manageability."

        return analysis

    def _generate_recommendations(
        self,
        sector_breakdown: List[SectorBreakdown],
        risk_metrics: RiskMetrics,
        stock_details: List[Dict],
        holdings: List[StockHolding]
    ) -> List[str]:
        """Generate actionable recommendations"""

        recommendations = []

        # Concentration recommendations
        max_holding = max(holdings, key=lambda x: x.allocation)
        if max_holding.allocation > 25:
            recommendations.append(
                f"Consider reducing your {max_holding.symbol} position ({max_holding.allocation}%) "
                f"to decrease concentration risk."
            )

        # Sector diversification
        if sector_breakdown[0].allocation > 40:
            recommendations.append(
                f"Your portfolio is heavily weighted toward {sector_breakdown[0].sector}. "
                f"Consider diversifying into other sectors like Healthcare, Consumer Goods, or Utilities."
            )

        # Risk-based recommendations
        if risk_metrics.risk_score > 70:
            recommendations.append(
                "Your portfolio has high risk. Consider adding more stable, dividend-paying stocks "
                "or defensive sector holdings to reduce volatility."
            )
        elif risk_metrics.risk_score < 30:
            recommendations.append(
                "Your portfolio appears conservative. If you have a longer time horizon, "
                "you might consider adding some growth stocks for higher potential returns."
            )

        # Diversification recommendations
        if risk_metrics.diversification_score < 50:
            recommendations.append(
                "Improve diversification by adding stocks from underrepresented sectors "
                "or reducing positions in overweighted holdings."
            )

        # Missing key sectors
        represented_sectors = {sb.sector for sb in sector_breakdown}
        key_sectors = {"Technology", "Healthcare", "Financials", "Consumer Cyclical"}
        missing_sectors = key_sectors - represented_sectors
        if missing_sectors:
            recommendations.append(
                f"Consider adding exposure to: {', '.join(missing_sectors)} for better sector balance."
            )

        # Default recommendation if none generated
        if not recommendations:
            recommendations.append(
                "Your portfolio appears well-balanced. Continue monitoring performance "
                "and rebalance periodically to maintain your target allocations."
            )

        return recommendations[:5]  # Limit to top 5 recommendations
