# Simple Agents - Minimal Sequential AI Workflow

A clean, minimal implementation of a multi-agent AI system using Claude Code CLI. Four specialized agents work together sequentially to plan, test, code, and review software projects.

## 🚀 Quick Start

```bash
# Run the interactive agent system
python3 simple_agents.py

# Give it a task
> Build a REST API for a todo app

# The agents will work sequentially:
# 1. Planner creates a detailed plan
# 2. Test Writer writes comprehensive tests
# 3. Coder implements the solution
# 4. Reviewer checks everything

# Continue with more prompts without losing context
> Add user authentication

# View outputs
> show planner
> show          # Shows all agent outputs

# Save your session
> save

# Exit when done
> exit
```

## 🎯 Philosophy

This implementation follows the KISS (Keep It Simple, Stupid) principle:
- **One file** - Everything in `simple_agents.py`
- **No background processes** - Sequential execution
- **No complex state management** - Simple in-memory context
- **Direct Claude CLI integration** - No API complexity
- **Clear agent roles** - Each agent has one job

## 🤖 The Agents

1. **Planner** - Analyzes requirements and creates detailed implementation plans
2. **Test Writer** - Writes comprehensive tests based on the plan (TDD approach)
3. **Coder** - Implements code that passes all the tests
4. **Reviewer** - Reviews the implementation and suggests improvements

Each agent:
- Sees only what it needs (previous agent's output)
- Maintains its role throughout the session
- Produces clear, focused output

## 📝 Commands

| Command | Description |
|---------|-------------|
| `<any text>` | Run workflow with this prompt |
| `show` | Display all agent outputs |
| `show <agent>` | Display specific agent output (planner/tester/coder/reviewer) |
| `save` | Save session to timestamped JSON file |
| `exit` | Exit the program |

## 🔧 Requirements

- Python 3.6+
- Claude Code CLI (`claude` command must be available)
- Claude model access (default: claude-opus-4-20250514)

## 💡 Use Cases

Perfect for:
- **Rapid Prototyping** - Get from idea to reviewed code quickly
- **Learning** - See how different agents approach the same problem
- **Code Generation** - Generate boilerplate with tests
- **Architecture Design** - Use planner for system design
- **Code Reviews** - Get AI feedback on implementations

## 🎨 Example Session

```
🚀 Simple Agents - Sequential AI Workflow
==================================================
Commands:
  <prompt>    - Run workflow with this prompt
  show        - Show all agent outputs
  show <agent>- Show specific agent output
  save        - Save session to file
  exit        - Exit the program
==================================================

> Create a Python function to calculate fibonacci numbers

🤖 PLANNER is thinking...
✅ Plan created

🤖 TESTER is thinking...
✅ Tests written

🤖 CODER is thinking...
✅ Code implemented

🤖 REVIEWER is thinking...
✅ Review complete

> show coder

============================================================
📄 CODER OUTPUT:
============================================================
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b
============================================================

> Add memoization for performance

[Agents continue with the new requirement...]
```

## 🔄 How It Works

1. **User provides prompt** → Planner creates detailed plan
2. **Plan goes to Test Writer** → Tests are written first (TDD)
3. **Tests go to Coder** → Implementation that passes tests
4. **Code + Tests go to Reviewer** → Final review and suggestions

The context is preserved within each Claude session, so you can keep adding requirements and the agents will build upon previous work.

## 🛠️ Customization

Edit `simple_agents.py` to:
- Change agent prompts (in the `agents` dictionary)
- Modify the workflow order
- Add new agents
- Change the Claude model

## 📦 Minimal Dependencies

- Python standard library only
- No external packages required
- No background process management
- No complex state files

## 🤝 Contributing

This is designed to be a minimal reference implementation. Feel free to:
- Fork and extend for your needs
- Add persistence mechanisms
- Create parallel execution versions
- Build web interfaces on top

Keep the core simple - complexity can always be added in forks!

## 📄 License

MIT - Use freely for any purpose.