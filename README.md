# Portfolio Analyzer Backend

AI-powered portfolio analysis service built with FastAPI and deployed on Azure Kubernetes Service (AKS).

## Features

- **Portfolio Analysis**: Analyze stock portfolios with detailed sector breakdown
- **Risk Metrics**: Calculate risk scores, diversification, and volatility
- **AI Insights**: Generate intelligent insights using Claude or GPT models
- **Recommendations**: Provide actionable portfolio recommendations
- **RESTful API**: FastAPI-based REST API with automatic OpenAPI documentation

## Architecture

- **Framework**: FastAPI
- **LLM Integration**: LangChain with Claude/OpenAI
- **Stock Data**: yfinance for real-time stock information
- **Database**: PostgreSQL with pgvector (for future enhancements)
- **Deployment**: Azure Kubernetes Service (AKS)
- **CI/CD**: GitHub Actions

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL (optional for development)
- Anthropic API key or OpenAI API key

### Setup

1. Clone the repository:
```bash
cd /path/to/Repository
git clone https://github.com/YOUR_USERNAME/portfolioanalyzerbackend.git
cd portfolioanalyzerbackend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/v1/analyze

Analyze a portfolio and get comprehensive insights.

**Request Body:**
```json
{
  "holdings": [
    {
      "symbol": "AAPL",
      "allocation": 30.0,
      "shares": 100
    },
    {
      "symbol": "MSFT",
      "allocation": 25.0,
      "shares": 50
    },
    {
      "symbol": "GOOGL",
      "allocation": 20.0,
      "shares": 30
    },
    {
      "symbol": "JPM",
      "allocation": 15.0,
      "shares": 40
    },
    {
      "symbol": "JNJ",
      "allocation": 10.0,
      "shares": 20
    }
  ],
  "total_value": 100000
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "timestamp": "2025-10-31T...",
  "portfolio_summary": {
    "total_stocks": 5,
    "total_sectors": 3,
    "largest_holding": "AAPL",
    "largest_holding_pct": 30.0
  },
  "sector_breakdown": [...],
  "risk_metrics": {
    "risk_score": 45.2,
    "diversification_score": 72.5,
    "volatility_level": "Medium",
    "concentration_risk": "Medium"
  },
  "diversification_analysis": "...",
  "recommendations": [...],
  "ai_insights": "...",
  "stock_details": [...]
}
```

### GET /api/v1/health

Health check endpoint.

## Deployment to AKS

### Prerequisites

- Azure account with AKS cluster
- Azure Container Registry (ACR)
- kubectl configured for your cluster
- GitHub repository secrets configured

### Required GitHub Secrets

- `ACR_USERNAME`: Azure Container Registry username
- `ACR_PASSWORD`: Azure Container Registry password
- `AZURE_CREDENTIALS`: Azure service principal credentials

### Kubernetes Secrets

Create secrets in your AKS cluster:

```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:password@postgres-service:5432/portfoliodb' \
  --from-literal=anthropic-api-key='your_anthropic_api_key' \
  --from-literal=openai-api-key='your_openai_api_key'
```

### Update Configuration

1. Update `k8s/deployment.yaml`:
   - Replace `YOUR_ACR_NAME` with your ACR name

2. Update `.github/workflows/deploy.yaml`:
   - Set `ACR_NAME`
   - Set `AKS_CLUSTER_NAME`
   - Set `AKS_RESOURCE_GROUP`

### Deploy

Push to main branch to trigger deployment:

```bash
git add .
git commit -m "Deploy to AKS"
git push origin main
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `development` |
| `DEBUG` | Enable debug mode | `True` |
| `API_PREFIX` | API prefix path | `/api/v1` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:5000` |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `ANTHROPIC_API_KEY` | Claude API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `LLM_PROVIDER` | LLM provider (`anthropic` or `openai`) | `anthropic` |
| `LLM_MODEL` | Model name | `claude-3-5-sonnet-20241022` |

## Project Structure

```
portfolioanalyzerbackend/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   └── config.py          # Configuration
│   ├── models/
│   │   └── portfolio.py       # Pydantic models
│   ├── services/
│   │   ├── portfolio_analyzer.py  # Main analysis logic
│   │   ├── stock_data_service.py  # Stock data fetching
│   │   └── llm_service.py         # LLM integration
│   └── main.py                # FastAPI application
├── k8s/
│   ├── deployment.yaml        # Kubernetes deployment
│   ├── ingress.yaml          # Ingress configuration
│   ├── hpa.yaml              # Horizontal Pod Autoscaler
│   └── secrets-template.yaml # Secrets template
├── .github/
│   └── workflows/
│       └── deploy.yaml       # GitHub Actions workflow
├── Dockerfile
├── requirements.txt
└── README.md
```

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
