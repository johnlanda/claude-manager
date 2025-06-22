# Claude Manager - Multi-Agent Development System

A production-ready multi-agent system for coordinating multiple Claude Code instances to work together on software development tasks following a plan → test → code → review workflow.

## 🚀 Quick Start

```bash
cd claude-manager

# Start all agents with one command
./start-agents-improved.sh

# In the coordinator window, start a workflow:
# Type: start workflow: ["Create a REST API", "Add authentication", "Include tests"]

# Monitor progress (in another terminal)
./start-agents-improved.sh monitor

# Stop all agents
./stop-agents.sh
```

## 📁 Project Structure

```
claude-manager/
├── start-agents-improved.sh    # Main launcher with dependency management
├── state_manager.py           # Thread-safe state management with file locking
├── agent_prompts.py           # Agent role definitions and prompts
├── workflow_monitor.py        # Real-time monitoring with timeout detection
├── agent-coordinator.py       # Original coordinator (legacy)
├── IMPROVEMENTS.md           # Detailed improvement documentation
└── logs/                     # Agent output logs (created at runtime)
```

## 🤖 Agent Roles

1. **Coordinator** - Manages workflow and user interaction
2. **Planner** - Analyzes requirements and creates implementation plans
3. **Test Writer** - Writes comprehensive tests (TDD approach)
4. **Coder** - Implements code to pass all tests
5. **Reviewer** - Reviews code quality and suggests improvements

## ✨ Key Features

- **Thread-safe communication** via locked state file
- **Automatic retry** on agent failures (2x max)
- **Timeout detection** (5-10 minutes per agent)
- **Comprehensive logging** to `logs/` directory
- **Clean process management** with PID tracking
- **Dependency auto-installation**

## 🔧 Advanced Usage

### Test the System
```bash
./start-agents-improved.sh test
```

### View Current State
```bash
python3 -m json.tool agent-state.json
```

### Watch Logs in Real-time
```bash
tail -f logs/*.log
```

### Get Workflow Summary
```bash
python3 workflow_monitor.py summary
```

## 📚 Documentation

- `README-multiagent.md` - Original design documentation
- `IMPROVEMENTS.md` - Detailed improvement notes
- `agent-templates.md` - Agent prompt templates
- `example-workflow.md` - Example workflow walkthrough

## 🛠️ Customization

### Change Claude Model
```bash
export CLAUDE_MODEL=claude-3-opus-20240229
./start-agents-improved.sh
```

### Modify Agent Prompts
Edit `agent_prompts.py` to customize agent behaviors.

### Adjust Timeouts
Edit `workflow_monitor.py` to change agent timeout values.

## 📈 Future Enhancements

See `IMPROVEMENTS.md` for planned features including:
- Message queue integration
- Web dashboard
- Distributed execution
- Workflow templates