#!/bin/bash

# Start Appwrite Proxy Server
echo "🚀 Starting Appwrite Proxy Server..."
echo ""
echo "Requirements:"
echo "  ✓ Appwrite running at http://localhost/v1"
echo ""

# Set environment variables (optional - uses defaults if not set)
export APPWRITE_ENDPOINT=${APPWRITE_ENDPOINT:-"http://localhost/v1"}
export APPWRITE_PROJECT_ID=${APPWRITE_PROJECT_ID:-"689107c288885e90c039"}
export APPWRITE_DATABASE_ID=${APPWRITE_DATABASE_ID:-"6864aed388d20c69a461"}
export APPWRITE_API_KEY=${APPWRITE_API_KEY:-"0f3a08c2c4fc98480980cbe59cd2db6b8522734081f42db3480ab2e7a8ffd7c46e8476a62257e429ff11c1d6616e814ae8753fb07e7058d1b669c641012941092ddcd585df802eb2313bfba49bf3ec3f776f529c09a7f5efef2988e4b4821244bbd25b3cd16669885c173ac023b5b8a90e4801f3584eef607506362c6ae01c94"}
export PORT=${PORT:-3000}

echo "📡 Appwrite Endpoint: $APPWRITE_ENDPOINT"
echo "🔐 Project ID: $APPWRITE_PROJECT_ID"
echo "📦 Port: $PORT"
echo ""

# Run the proxy server
python3 appwrite_proxy.py
