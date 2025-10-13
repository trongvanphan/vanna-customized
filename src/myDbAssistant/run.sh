#!/bin/bash
# Quick run script for myDbAssistant
# This script checks dependencies and runs the Flask application

set -e  # Exit on error

echo "============================================================"
echo "  myDbAssistant - Vanna AI Database Assistant"
echo "============================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Check if we're in the right directory
if [ ! -f "config.py" ] || [ ! -f "quick_start_flask.py" ]; then
    echo "❌ Please run this script from the src/myDbAssistant directory"
    exit 1
fi

echo "✅ In correct directory"

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    
    echo ""
    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment exists"
    source venv/bin/activate
fi

echo ""
echo "🧪 Running connection tests..."
echo "   (Press Ctrl+C to skip if you've already tested)"
echo ""

# Give user a chance to skip tests
sleep 2

python test_umbrella_connection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  🚀 Starting Flask Application"
    echo "============================================================"
    echo ""
    echo "📍 Web UI will be available at: http://localhost:8084"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    python quick_start_flask.py
else
    echo ""
    echo "❌ Connection tests failed!"
    echo "   Fix the issues above before running the application."
    exit 1
fi
