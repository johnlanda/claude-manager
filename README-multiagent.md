# Claude Code Multi-Agent System

## Quick Start

### 1. Install Dependencies
```bash
# Install goreman (process manager)
go install github.com/mattn/goreman@latest
# or
brew install goreman

# Ensure Python 3 is installed for coordinator
python3 --version
```

### 2. Launch All Agents
```bash
./start-agents.sh
```

This will:
- Initialize the agent state file
- Launch all 5 Claude instances (coordinator + 4 specialized agents)
- Each agent monitors `agent-state.json` for tasks

### 3. Start a Development Task
In the coordinator Claude instance, type:
```
Update agent-state.json with project requirements: ["Create a REST API endpoint for user registration", "Include email validation", "Store users in SQLite database"]
```

The agents will automatically:
1. **Planner**: Analyze codebase and create implementation plan
2. **Test Writer**: Write comprehensive tests (TDD approach)
3. **Coder**: Implement code to pass tests
4. **Reviewer**: Review code quality and suggest improvements

### 4. Monitor Progress
```bash
# In a separate terminal
python3 agent-coordinator.py monitor
```

## Alternative Launch Methods

### Using tmux (visual separation)
```bash
tmuxinator start -p Procfile.tmux
```

### Manual Launch (for debugging)
```bash
# Terminal 1
python3 agent-coordinator.py init

# Terminal 2-6 (run each command in separate terminal)
claude code --model claude-opus-4-20250514 --prompt "You are the COORDINATOR..."
claude code --model claude-opus-4-20250514 --prompt "You are the PLANNER..."
# ... etc
```

## Workflow States

Agents communicate through `agent-state.json`:
- `idle`: Agent waiting for work
- `pending`: Agent should start working
- `in_progress`: Agent currently working
- `completed`: Agent finished task
- `waiting`: Agent waiting for dependencies

## Tips

1. **Parallel Execution**: Agents run concurrently but respect dependencies
2. **Iteration**: After review, update requirements to trigger another cycle
3. **Debugging**: Check `agent-state.json` to see what each agent produced
4. **Custom Prompts**: Modify agent prompts in Procfile for different behaviors

## Troubleshooting

- **Agents not starting**: Check if Claude Code is properly installed
- **State conflicts**: Run `python3 agent-coordinator.py init` to reset
- **Performance**: Adjust sleep delays in Procfile based on your system