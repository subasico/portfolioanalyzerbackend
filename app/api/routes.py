from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from app.models.portfolio import (
    PortfolioRequest, PortfolioAnalysis, HealthCheckResponse
)
from app.services.portfolio_analyzer import PortfolioAnalyzer
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
analyzer = PortfolioAnalyzer()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )


@router.post("/analyze", response_model=PortfolioAnalysis)
async def analyze_portfolio(portfolio: PortfolioRequest):
    """
    Analyze a portfolio and return comprehensive insights

    This endpoint accepts a list of stock holdings with their allocations
    and returns:
    - Sector breakdown
    - Risk metrics
    - Diversification analysis
    - AI-powered insights
    - Actionable recommendations
    """
    try:
        logger.info(f"Analyzing portfolio with {len(portfolio.holdings)} holdings")

        analysis = await analyzer.analyze_portfolio(portfolio)

        logger.info(f"Portfolio analysis completed: {analysis.request_id}")
        return analysis

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while analyzing the portfolio"
        )


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Portfolio Analyzer API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
