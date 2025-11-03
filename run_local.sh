#!/bin/bash

# Activate virtual environment and run the application locally

echo "🚀 Starting Portfolio Analyzer Backend..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your API keys"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ Error: Dependencies not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Environment loaded"
echo "✅ Virtual environment activated"
echo ""
echo "Starting server on http://localhost:8000"
echo "API docs will be available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
