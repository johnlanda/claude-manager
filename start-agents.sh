#!/bin/bash
# Improved multi-agent launcher with better process management

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLAUDE_MODEL="${CLAUDE_MODEL:-claude-opus-4-20250514}"
LOG_DIR="./logs"
PID_FILE=".agent-pids"
STATE_FILE="agent-state.json"

# Function to print colored output
print_status() {
    echo -e "${2}${1}${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..." "$BLUE"
    
    # Check for Python 3
    if ! command -v python3 &> /dev/null; then
        print_status "❌ Python 3 is required but not installed" "$RED"
        exit 1
    fi
    
    # Check for goreman
    if ! command -v goreman &> /dev/null; then
        print_status "⚠️  goreman not found. Installing..." "$YELLOW"
        if command -v go &> /dev/null; then
            go install github.com/mattn/goreman@latest
        elif command -v brew &> /dev/null; then
            brew install goreman
        else
            print_status "❌ Please install goreman manually" "$RED"
            exit 1
        fi
    fi
    
    # Check for Claude
    if ! command -v claude &> /dev/null; then
        print_status "❌ Claude Code CLI not found. Please install it first" "$RED"
        exit 1
    fi
    
    print_status "✅ All dependencies satisfied" "$GREEN"
}

# Function to create log directory
setup_logging() {
    mkdir -p "$LOG_DIR"
    print_status "📁 Log directory created: $LOG_DIR" "$BLUE"
}

# Function to initialize state
init_state() {
    print_status "🔧 Initializing agent state..." "$BLUE"
    python3 -c "from state_manager import StateManager; StateManager().start_new_workflow([], 'multi-agent-project')"
    print_status "✅ State initialized" "$GREEN"
}

# Function to create improved Procfile
create_procfile() {
    cat > Procfile.improved <<EOF
# Enhanced Procfile with proper Python path and error handling
coordinator: PYTHONPATH=. claude code --model $CLAUDE_MODEL --prompt "\$(python3 agent_prompts.py coordinator)" 2>&1 | tee $LOG_DIR/coordinator.log
planner: sleep 3 && PYTHONPATH=. claude code --model $CLAUDE_MODEL --prompt "\$(python3 agent_prompts.py planner)" 2>&1 | tee $LOG_DIR/planner.log
tester: sleep 6 && PYTHONPATH=. claude code --model $CLAUDE_MODEL --prompt "\$(python3 agent_prompts.py test_writer)" 2>&1 | tee $LOG_DIR/tester.log
coder: sleep 9 && PYTHONPATH=. claude code --model $CLAUDE_MODEL --prompt "\$(python3 agent_prompts.py coder)" 2>&1 | tee $LOG_DIR/coder.log
reviewer: sleep 12 && PYTHONPATH=. claude code --model $CLAUDE_MODEL --prompt "\$(python3 agent_prompts.py reviewer)" 2>&1 | tee $LOG_DIR/reviewer.log
monitor: sleep 1 && python3 workflow_monitor.py 2>&1 | tee $LOG_DIR/monitor.log
EOF
    print_status "✅ Enhanced Procfile created" "$GREEN"
}

# Function to start agents
start_agents() {
    print_status "🚀 Starting multi-agent system..." "$BLUE"
    
    # Save PIDs for cleanup
    echo "# Agent PIDs - $(date)" > "$PID_FILE"
    
    # Start goreman in background and save PID
    goreman -f Procfile.improved start &
    GOREMAN_PID=$!
    echo "goreman=$GOREMAN_PID" >> "$PID_FILE"
    
    print_status "✅ Agents started (PID: $GOREMAN_PID)" "$GREEN"
    print_status "📊 Monitor logs in real-time: tail -f $LOG_DIR/*.log" "$BLUE"
    print_status "🛑 Stop all agents: ./stop-agents.sh" "$BLUE"
}

# Function to create stop script
create_stop_script() {
    cat > stop-agents.sh <<'EOF'
#!/bin/bash
# Stop all running agents

if [ -f .agent-pids ]; then
    echo "Stopping agents..."
    while IFS='=' read -r name pid; do
        if [ ! -z "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
            echo "Stopping $name (PID: $pid)"
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done < .agent-pids
    rm .agent-pids
    echo "✅ All agents stopped"
else
    echo "No running agents found"
fi

# Also kill any remaining claude or python processes related to agents
pkill -f "claude code.*agent" 2>/dev/null || true
pkill -f "workflow_monitor.py" 2>/dev/null || true
EOF
    chmod +x stop-agents.sh
}

# Function to show usage
show_usage() {
    cat <<EOF
🤖 Claude Code Multi-Agent System
=================================

Commands:
  ./start-agents.sh          - Start all agents
  ./start-agents.sh monitor  - Start monitoring only
  ./start-agents.sh test     - Run system test
  ./stop-agents.sh                    - Stop all agents

Workflow Control:
  In the coordinator terminal, type:
  - "start workflow: [requirement1, requirement2, ...]" to begin
  - "status" to check progress
  - "retry [agent]" to retry failed agent

Monitoring:
  - Watch logs: tail -f logs/*.log
  - View state: python3 -m json.tool agent-state.json
  - Summary: python3 workflow_monitor.py summary

EOF
}

# Main execution
main() {
    case "${1:-}" in
        "monitor")
            python3 workflow_monitor.py
            ;;
        "test")
            print_status "🧪 Running system test..." "$BLUE"
            check_dependencies
            init_state
            python3 -c "from state_manager import StateManager; sm = StateManager(); sm.start_new_workflow(['Create a hello world function', 'Add unit tests'], 'test-project')"
            python3 workflow_monitor.py
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            check_dependencies
            setup_logging
            init_state
            create_procfile
            create_stop_script
            start_agents
            show_usage
            ;;
    esac
}

# Cleanup on exit
cleanup() {
    print_status "\n🛑 Shutting down agents..." "$YELLOW"
    if [ -f stop-agents.sh ]; then
        ./stop-agents.sh
    fi
}

trap cleanup EXIT INT TERM

# Run main
main "$@"