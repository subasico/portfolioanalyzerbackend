from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class StockHolding(BaseModel):
    """Represents a single stock holding in the portfolio"""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")
    allocation: float = Field(..., ge=0, le=100, description="Allocation percentage (0-100)")
    shares: Optional[int] = Field(None, description="Number of shares (optional)")

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper().strip()


class PortfolioRequest(BaseModel):
    """Request model for portfolio analysis"""
    holdings: List[StockHolding] = Field(..., min_items=1, description="List of stock holdings")
    total_value: Optional[float] = Field(None, ge=0, description="Total portfolio value (optional)")

    @validator('holdings')
    def validate_allocations(cls, v):
        total = sum(holding.allocation for holding in v)
        if not (99.0 <= total <= 101.0):  # Allow small rounding errors
            raise ValueError(f"Total allocation must be 100%, got {total}%")
        return v


class SectorBreakdown(BaseModel):
    """Sector breakdown of the portfolio"""
    sector: str
    allocation: float
    stocks: List[str]


class RiskMetrics(BaseModel):
    """Risk assessment metrics"""
    risk_score: float = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    diversification_score: float = Field(..., ge=0, le=100, description="Diversification score (0-100)")
    volatility_level: str = Field(..., description="Low, Medium, or High")
    concentration_risk: str = Field(..., description="Risk level due to concentration")


class PortfolioAnalysis(BaseModel):
    """Complete portfolio analysis response"""
    request_id: str
    timestamp: datetime
    portfolio_summary: Dict[str, Any]
    sector_breakdown: List[SectorBreakdown]
    risk_metrics: RiskMetrics
    diversification_analysis: str
    recommendations: List[str]
    ai_insights: str
    stock_details: Optional[List[Dict[str, Any]]] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
