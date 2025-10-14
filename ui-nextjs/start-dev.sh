#!/bin/bash

# Quick Start Script for Next.js + Flask Development
# Run this after making changes to restart both services

echo "🔄 Restarting Vanna Services..."
echo ""

# Kill existing processes
echo "🛑 Stopping existing processes..."
lsof -ti:8084 | xargs kill -9 2>/dev/null && echo "   ✅ Flask stopped (port 8084)"
lsof -ti:3000 | xargs kill -9 2>/dev/null && echo "   ✅ Next.js stopped (port 3000)"
sleep 2

# Start Flask backend
echo ""
echo "🚀 Starting Flask backend..."
cd "$(dirname "$0")/../src/myDbAssistant"
python3 quick_start_flask_ui.py &
FLASK_PID=$!
echo "   Flask PID: $FLASK_PID"

# Wait for Flask to start
echo "   Waiting for Flask to start..."
sleep 5

# Check if Flask is running
if curl -s http://localhost:8084/api/v0/get_config > /dev/null; then
    echo "   ✅ Flask running on http://localhost:8084"
else
    echo "   ❌ Flask failed to start"
    exit 1
fi

# Start Next.js frontend
echo ""
echo "🚀 Starting Next.js frontend..."
cd "$(dirname "$0")"
npm run dev &
NEXTJS_PID=$!
echo "   Next.js PID: $NEXTJS_PID"

# Wait for Next.js to start
echo "   Waiting for Next.js to start..."
sleep 3

# Check if Next.js is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✅ Next.js running on http://localhost:3000"
else
    echo "   ❌ Next.js failed to start"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📋 Service URLs:"
echo "   Next.js UI:     http://localhost:3000"
echo "   Settings Page:  http://localhost:3000/settings"
echo "   Flask API:      http://localhost:8084"
echo "   Flask Settings: http://localhost:8084/settings"
echo ""
echo "🛑 To stop services:"
echo "   lsof -ti:8084 | xargs kill -9  # Stop Flask"
echo "   lsof -ti:3000 | xargs kill -9  # Stop Next.js"
echo ""
echo "Press Ctrl+C to stop watching logs"
echo ""

# Follow logs (optional - comment out if not needed)
tail -f /dev/null
