#!/usr/bin/env bash
# Render Build Script - Builds both frontend and backend

set -e

echo "🚀 Building JARVIS Full Stack..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements-render.txt

# Build Frontend
echo "🔨 Building React frontend..."
cd ../jarvis-frontend
npm install
npm run build

# Copy dist to jarvis-ai for serving
echo "📁 Copying frontend build..."
cp -r dist ../jarvis-ai/frontend-dist

echo "✅ Build complete!"
