# Local Development Setup

## ✅ Setup Complete!

Your local development environment is ready. Here's what has been configured:

### What's Been Set Up

1. **Virtual Environment**: `venv/` - Python 3.13 virtual environment
2. **Dependencies**: All Python packages installed (updated to Python 3.13 compatible versions)
3. **Environment File**: `.env` - Configuration template created
4. **Startup Script**: `run_local.sh` - Quick start script

---

## 🔑 Next Steps: Configure Your API Keys

Open the `.env` file and add your API keys:

```bash
# Edit the .env file
code .env  # or use your preferred editor
```

### Required Configuration:

You need **at least ONE** of these LLM API keys:

#### Option 1: OpenAI (Recommended - Default Configuration)
```env
OPENAI_API_KEY=sk-proj-...your_actual_openai_key...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
```

#### Option 2: Anthropic Claude
```env
ANTHROPIC_API_KEY=sk-ant-...your_actual_anthropic_key...
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

### Optional Configuration:

The following are **optional** for local testing:

```env
# Database (optional - not required for basic portfolio analysis)
DATABASE_URL=postgresql://user:password@localhost:5432/portfoliodb

# Stock Data API (optional - yfinance is used by default)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

---

## 🚀 Running the Application

### Method 1: Using the startup script (Recommended)

```bash
./run_local.sh
```

### Method 2: Manual start

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload
```

The server will start on **http://localhost:8000**

---

## 📚 Testing the API

Once the server is running:

1. **API Documentation**: http://localhost:8000/docs
2. **Alternative Docs**: http://localhost:8000/redoc
3. **Health Check**: http://localhost:8000/api/v1/health

### Example Test Request

Use the Swagger UI at http://localhost:8000/docs or curl:

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "AAPL", "allocation": 30.0, "shares": 100},
      {"symbol": "MSFT", "allocation": 25.0, "shares": 50},
      {"symbol": "GOOGL", "allocation": 20.0, "shares": 30},
      {"symbol": "JPM", "allocation": 15.0, "shares": 40},
      {"symbol": "JNJ", "allocation": 10.0, "shares": 20}
    ],
    "total_value": 100000
  }'
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError"
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### "API key not found"
Check that you've added your API key to `.env` file

### "Cannot connect to database"
Database is optional for local testing. You can ignore database connection errors.

---

## 📦 Dependency Updates

The dependencies have been updated to support Python 3.13:
- `psycopg2-binary` → `psycopg[binary]` (v3.2+)
- `pandas` and `numpy` → Latest compatible versions
- All other packages updated to latest versions

---

## 🚢 Deployment

Once local testing is successful, refer to:
- [QUICK_DEPLOY_OPENAI.md](QUICK_DEPLOY_OPENAI.md) - Quick deployment guide
- [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md) - Full deployment checklist

---

## 📝 Project Structure

```
portfolioanalyzerbackend/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   └── config.py          # Configuration
│   ├── models/
│   │   └── portfolio.py       # Data models
│   ├── services/
│   │   ├── portfolio_analyzer.py  # Analysis logic
│   │   ├── stock_data_service.py  # Stock data
│   │   └── llm_service.py         # LLM integration
│   └── main.py                # FastAPI app
├── venv/                      # Virtual environment
├── .env                       # Your configuration
├── run_local.sh              # Startup script
└── requirements.txt          # Python dependencies
```

---

## 🆘 Need Help?

- Check the logs in the terminal for error messages
- Review the API documentation at /docs
- Ensure all required environment variables are set
