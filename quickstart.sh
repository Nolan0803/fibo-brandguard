#!/bin/bash

# FIBO BrandGuard Quick Start Script

echo "🛡️  FIBO BrandGuard Setup"
echo "========================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is required but not found."
    exit 1
fi

echo "✓ Python found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies."
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run demo
echo "Running demo..."
python3 demo.py

if [ $? -ne 0 ]; then
    echo "❌ Error: Demo failed."
    exit 1
fi

echo ""
echo "✓ Demo completed successfully!"
echo ""
echo "========================="
echo "To launch the Streamlit app, run:"
echo "  streamlit run app.py"
echo "========================="
