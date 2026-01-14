#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "  Retell AI Custom LLM Server (Gemini)"
echo "=========================================="
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$DIR/venv/bin/activate"
else
    echo "Warning: Virtual environment not found. Creating one..."
    python3 -m venv "$DIR/venv"
    source "$DIR/venv/bin/activate"
    echo "Installing requirements..."
    pip install -r "$DIR/requirements.txt"
fi

echo ""
echo "Step 1: Checking libraries..."
pip install -r "$DIR/requirements.txt"

echo ""
echo "Step 2: Starting Ngrok (Tunnel)..."
# Check if ngrok is in path or in current directory
if command -v ngrok &> /dev/null; then
    # Start ngrok in a new terminal window
    osascript -e 'tell application "Terminal" to do script "ngrok http 8080"'
elif [ -f "$DIR/ngrok" ]; then
    # chmod to ensure it is executable
    chmod +x "$DIR/ngrok"
    # Start ngrok from the current directory, handling spaces in path
    osascript -e "tell application \"Terminal\" to do script \"\\\"$DIR/ngrok\\\" http 8080\""
else
    echo "Warning: ngrok not found. Please install ngrok or place it in this directory."
    echo "You can run 'ngrok http 8080' manually in another terminal."
fi

echo ""
echo "Step 3: Starting Servers..."
echo "Server logs will appear below. Press CTRL+C to stop everything."
echo ""

# Start Frontend Server in background to serve the Web UI and API
python3 "$DIR/server.py" &
FRONTEND_PID=$!

echo "Frontend Server started (PID: $FRONTEND_PID) on http://localhost:8000"

# Run the backend python script (LLM Logic)
echo "Starting Backend Server (LLM Logic)..."
python3 "$DIR/custom_llm_server.py"

# Cleanup on exit
kill $FRONTEND_PID
pkill -f "ngrok"
