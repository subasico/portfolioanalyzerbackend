from typing import List, Dict
import logging
from app.core.config import settings
from app.models.portfolio import SectorBreakdown, RiskMetrics, StockHolding

logger = logging.getLogger(__name__)


class LLMService:
    """Service for generating AI insights using LLMs"""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        try:
            if self.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.client = ChatAnthropic(
                    model=self.model,
                    anthropic_api_key=settings.ANTHROPIC_API_KEY
                )
            elif self.provider == "openai":
                from langchain_openai import ChatOpenAI
                self.client = ChatOpenAI(
                    model=self.model,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            else:
                logger.warning(f"Unknown LLM provider: {self.provider}")
                self.client = None
        except Exception as e:
            logger.error(f"Error initializing LLM client: {str(e)}")
            self.client = None

    async def generate_portfolio_insights(
        self,
        portfolio_summary: Dict,
        sector_breakdown: List[SectorBreakdown],
        risk_metrics: RiskMetrics,
        stock_details: List[Dict],
        holdings: List[StockHolding]
    ) -> str:
        """Generate AI-powered portfolio insights"""

        if not self.client:
            return self._generate_fallback_insights(
                portfolio_summary, sector_breakdown, risk_metrics
            )

        try:
            # Build context for the LLM
            prompt = self._build_analysis_prompt(
                portfolio_summary, sector_breakdown, risk_metrics, stock_details, holdings
            )

            # Get response from LLM
            response = await self.client.ainvoke(prompt)

            return response.content

        except Exception as e:
            logger.error(f"Error generating LLM insights: {str(e)}")
            return self._generate_fallback_insights(
                portfolio_summary, sector_breakdown, risk_metrics
            )

    def _build_analysis_prompt(
        self,
        portfolio_summary: Dict,
        sector_breakdown: List[SectorBreakdown],
        risk_metrics: RiskMetrics,
        stock_details: List[Dict],
        holdings: List[StockHolding]
    ) -> str:
        """Build the prompt for LLM analysis"""

        holdings_str = "\n".join([
            f"- {h.symbol}: {h.allocation}%"
            for h in holdings
        ])

        sector_str = "\n".join([
            f"- {sb.sector}: {sb.allocation}% ({', '.join(sb.stocks)})"
            for sb in sector_breakdown
        ])

        stock_info_str = "\n".join([
            f"- {s['symbol']} ({s['name']}): {s['sector']}, Beta: {s.get('beta', 'N/A')}, "
            f"P/E: {s.get('pe_ratio', 'N/A')}"
            for s in stock_details
        ])

        prompt = f"""You are an expert financial advisor analyzing an investment portfolio. Provide a comprehensive,
professional analysis with actionable insights. Be specific and reference actual holdings.

Portfolio Overview:
- Total Holdings: {portfolio_summary['total_stocks']}
- Largest Position: {portfolio_summary['largest_holding']} ({portfolio_summary['largest_holding_pct']}%)
- Sectors Represented: {portfolio_summary['total_sectors']}

Holdings:
{holdings_str}

Sector Breakdown:
{sector_str}

Stock Details:
{stock_info_str}

Risk Metrics:
- Overall Risk Score: {risk_metrics.risk_score}/100
- Diversification Score: {risk_metrics.diversification_score}/100
- Volatility Level: {risk_metrics.volatility_level}
- Concentration Risk: {risk_metrics.concentration_risk}

Please provide:
1. A brief overview of the portfolio's composition and strategy
2. Key strengths and potential concerns
3. Market positioning and exposure analysis
4. Specific insights about the holdings and their relationships
5. Forward-looking considerations based on current market conditions

Keep the analysis concise (3-4 paragraphs), professional, and actionable. Focus on practical insights
rather than generic advice."""

        return prompt

    def _generate_fallback_insights(
        self,
        portfolio_summary: Dict,
        sector_breakdown: List[SectorBreakdown],
        risk_metrics: RiskMetrics
    ) -> str:
        """Generate basic insights when LLM is unavailable"""

        insights = f"""Portfolio Analysis Summary:

Your portfolio consists of {portfolio_summary['total_stocks']} holdings across {portfolio_summary['total_sectors']} sectors.
The largest position is {portfolio_summary['largest_holding']} at {portfolio_summary['largest_holding_pct']}% allocation.

Risk Profile: With a risk score of {risk_metrics.risk_score}/100 and diversification score of {risk_metrics.diversification_score}/100,
your portfolio shows {risk_metrics.volatility_level.lower()} volatility characteristics. The concentration risk is {risk_metrics.concentration_risk.lower()}.

Sector Allocation: Your portfolio is most heavily weighted toward {sector_breakdown[0].sector} ({sector_breakdown[0].allocation}%),
followed by {sector_breakdown[1].sector if len(sector_breakdown) > 1 else 'other sectors'}.

Considerations: Regular rebalancing and monitoring of individual holdings is recommended to maintain your target allocation
and risk profile. Consider your investment time horizon and risk tolerance when making portfolio adjustments."""

        return insights
