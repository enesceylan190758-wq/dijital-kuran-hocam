#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "  Retell AI Custom LLM Server (Unified)"
echo "=========================================="
echo ""

# 0. Kill existing processes to avoid conflicts
echo "Cleaning up old processes..."
pkill -f "ngrok"
pkill -f "custom_llm_server.py"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Activate virtual environment
if [ -d "$DIR/venv" ]; then
    source "$DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found."
    exit 1
fi

echo "Step 1: Starting Ngrok in background..."
if [ -f "$DIR/ngrok" ]; then
    chmod +x "$DIR/ngrok"
    # Start ngrok in background
    "$DIR/ngrok" http 8080 > /dev/null 2>&1 &
else
    # Try global ngrok
    ngrok http 8080 > /dev/null 2>&1 &
fi

# Wait for ngrok to initialize
echo "Waiting for Ngrok to start..."
sleep 5

echo ""
echo "Step 2: Retrieving Public URL..."
# Get the URL from ngrok's local API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -z "$NGROK_URL" ]; then
    echo "Error: Could not get Ngrok URL. Is Ngrok running?"
    echo "Please try running './ngrok http 8080' manually in a separate window."
    exit 1
fi

# Convert https to wss
WSS_URL="${NGROK_URL/https:\/\//wss://}/llm-websocket"

echo "*********************************************************"
echo "SUCCESS! Enter this URL in Retell Dashboard:"
echo ""
echo "   $WSS_URL"
echo ""
echo "*********************************************************"
echo ""

echo "Step 3: Starting Python server..."
echo "Server logs will appear below. Press CTRL+C to stop everything."
echo ""

# Run the python script
python3 "$DIR/custom_llm_server.py"

# Cleanup on exit
pkill -f "ngrok"
