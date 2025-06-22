# Claude Manager - Multi-Agent Development System

A production-ready multi-agent system for coordinating multiple Claude Code instances to work together on software development tasks following a plan → test → code → review workflow.

## 🚀 Quick Start

```bash
cd claude-manager

# Start all agents with one command
./start-agents.sh

# In the coordinator window, start a workflow:
# Type: start workflow: ["Create a REST API", "Add authentication", "Include tests"]

# Monitor progress (in another terminal)
./start-agents.sh monitor

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
└── logs/                     # Agent output logs (created at runtime)
```

## 🤖 Agent Roles

1. **Coordinator** - Manages workflow and user interaction
2. **Planner** - Analyzes requirements and creates implementation plans
3. **Test Writer** - Writes comprehensive tests (TDD approach)
4. **Coder** - Implements code to pass all tests
5. **Reviewer** - Reviews code quality and suggests improvements

## ✨ Key Features

### Core Capabilities
- **Thread-safe State Management**: File locking prevents race conditions
- **Automatic Recovery**: Failed agents retry up to 2 times
- **Timeout Detection**: Configurable timeouts (5-10 min per agent)
- **Comprehensive Logging**: All output saved to `logs/` directory
- **Clean Process Management**: PID tracking for reliable shutdown
- **Dependency Auto-installation**: Checks and installs goreman if needed

### Monitoring & Control
- **Real-time Progress Tracking**: Visual status updates in terminal
- **Workflow Summary Reports**: Get overview with `workflow_monitor.py summary`
- **Event Logging**: Last 100 events tracked for debugging
- **Error Tracking**: Automatic error capture and reporting

## 🔧 Advanced Usage

### Test the System
```bash
./start-agents.sh test
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
- `agent-templates.md` - Agent prompt templates
- `example-workflow.md` - Example workflow walkthrough

## 🛠️ Customization

### Change Claude Model
```bash
# Use different models for different agents based on their needs
export CLAUDE_MODEL=claude-3-7-sonnet-20241220  # Default for most agents
./start-agents.sh

# Or use the latest Opus 4 for maximum capability
export CLAUDE_MODEL=claude-opus-4-20250514
./start-agents.sh
```

### Modify Agent Prompts
Edit `agent_prompts.py` to customize agent behaviors.

### Adjust Timeouts
Edit `workflow_monitor.py` to change agent timeout values:
```python
self.agent_timeouts = {
    "planner": 300,      # 5 minutes
    "test_writer": 300,  # 5 minutes  
    "coder": 600,        # 10 minutes
    "reviewer": 300      # 5 minutes
}
```

## 🔧 Architecture Benefits

1. **Modularity**: Each component is independent and replaceable
2. **Reliability**: Automatic recovery from failures with retry logic
3. **Observability**: Comprehensive logging and event tracking
4. **Extensibility**: Easy to add new agents or modify workflows
5. **Performance**: Efficient state management without polling

## 📈 Future Enhancements

### Planned Features
- **Message Queue Integration**: Replace file-based communication with Redis/RabbitMQ
- **Web Dashboard**: Real-time visualization of workflow progress
- **Distributed Execution**: Run agents across multiple machines
- **Workflow Templates**: Reusable patterns for common tasks
- **Cost Tracking**: Monitor token usage per workflow

### Security Roadmap
- Agent authentication and authorization
- Encrypted inter-agent communication
- Audit logging for compliance
- Role-based access control

## 🐛 Troubleshooting

### Common Issues

**Agents not starting**: 
- Ensure Claude Code CLI is installed
- Check `claude --version` works
- Verify Python 3 is available

**State conflicts**:
- Run `python3 -c "from state_manager import StateManager; StateManager().start_new_workflow([], 'reset')"`
- Delete `agent-state.json.lock` if it exists

**Performance issues**:
- Adjust sleep delays in `start-agents-improved.sh`
- Reduce retry counts in `workflow_monitor.py`
- Check system resources with `top` or `htop`