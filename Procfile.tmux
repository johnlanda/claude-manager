# Alternative Procfile for tmux-based launch (if you prefer tmux over goreman)
# Usage: tmuxinator start -p Procfile.tmux

name: claude-agents
root: .

windows:
  - coordinator:
      layout: tiled
      panes:
        - claude code --model claude-opus-4-20250514 --prompt "You are the COORDINATOR. Monitor agent-state.json and orchestrate the workflow. When user provides requirements, update agent statuses to trigger the pipeline. Provide status updates."
  - planner:
      layout: tiled
      panes:
        - sleep 2 && claude code --model claude-opus-4-20250514 --prompt "You are the PLANNER agent. Monitor agent-state.json for new requirements. When your status is 'pending', analyze codebase, create plan, update agent-state.json."
  - tester:
      layout: tiled
      panes:
        - sleep 5 && claude code --model claude-opus-4-20250514 --prompt "You are the TEST WRITER agent. Monitor agent-state.json. When planner completes and your status is 'pending', write tests, update agent-state.json."
  - coder:
      layout: tiled
      panes:
        - sleep 8 && claude code --model claude-opus-4-20250514 --prompt "You are the CODER agent. Monitor agent-state.json. When test_writer completes and your status is 'pending', implement code, update agent-state.json."
  - reviewer:
      layout: tiled
      panes:
        - sleep 11 && claude code --model claude-opus-4-20250514 --prompt "You are the REVIEWER agent. Monitor agent-state.json. When coder completes and your status is 'pending', review code, update agent-state.json."