#!/bin/bash
# TridenGuard Mock Builder
# This script compiles the Lobster Trap mock for the current architecture.

echo "🏗️ Building Lobster Trap Mock..."

if ! command -v go &> /dev/null
then
    echo "❌ Error: Go is not installed. Please install Go to build the mock."
    exit 1
fi

go build -o ../lobstertrap main.go

if [ $? -eq 0 ]; then
    chmod +x ../lobstertrap
    echo "✅ Success! 'lobstertrap' binary created in the root directory."
    echo "🚀 You can now run the n8n workflow with full DPI simulation."
else
    echo "❌ Build failed."
    exit 1
fi
