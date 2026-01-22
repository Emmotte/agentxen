#!/bin/bash

echo "🚀 AgentXen Setup Script"
echo "========================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check for Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo ""
    echo "Please install Ollama from: https://ollama.com"
    echo ""
    echo "Quick install:"
    echo "  Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  macOS: brew install ollama"
    echo "  Windows: Download from https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama found: $(ollama --version)"

# Create virtual environment
echo ""
echo "📦 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate and install dependencies
echo ""
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Python dependencies installed"

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install firefox
echo "✅ Firefox browser installed"

# Pull Ollama model
echo ""
echo "🤖 Pulling Gemma 1B model..."
ollama pull gemma:1b

echo ""
echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "To run AgentXen:"
echo "  1. source venv/bin/activate"
echo "  2. python src/agent.py"
echo ""
