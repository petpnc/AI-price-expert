#!/bin/bash

# ValueAI - Quick Startup Script
# This script checks dependencies and starts the app

echo "🚀 ValueAI - Starting..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    exit 1
fi

echo "✅ pip found"
echo ""

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check if API key is configured
if grep -q "your-google-api-key-here" .streamlit/secrets.toml 2>/dev/null; then
    echo "⚠️  WARNING: API key not configured!"
    echo "Please edit .streamlit/secrets.toml and add your Google API key"
    echo ""
fi

# Start the app
echo "🎉 Starting ValueAI..."
echo "📱 App will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

streamlit run app.py
