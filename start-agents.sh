#!/bin/bash
# Start all Claude agents using goreman

echo "🚀 Starting Claude Code Multi-Agent System"
echo "==========================================="

# Check if goreman is installed
if ! command -v goreman &> /dev/null; then
    echo "❌ goreman not found. Install with: go install github.com/mattn/goreman@latest"
    echo "   or: brew install goreman"
    exit 1
fi

# Initialize agent state
echo "📋 Initializing agent state..."
python3 agent-coordinator.py init

# Start all agents
echo "🤖 Launching all agents..."
echo ""
echo "Agents will start in sequence:"
echo "  1. Coordinator (immediate)"
echo "  2. Planner (2s delay)"
echo "  3. Test Writer (5s delay)"
echo "  4. Coder (8s delay)"
echo "  5. Reviewer (11s delay)"
echo ""
echo "Press Ctrl+C to stop all agents"
echo "==========================================="

# Start goreman with our Procfile
goreman start