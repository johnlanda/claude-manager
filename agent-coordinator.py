#!/usr/bin/env python3
"""
Agent Coordinator - Manages the multi-agent workflow state
"""
import json
import time
import sys
from pathlib import Path
from datetime import datetime

STATE_FILE = Path("agent-state.json")

def init_state():
    """Initialize or reset the agent state"""
    initial_state = {
        "project": {
            "name": "",
            "description": "",
            "requirements": [],
            "started_at": datetime.now().isoformat()
        },
        "workflow": {
            "current_phase": "idle",
            "phases": ["planning", "test-writing", "coding", "review", "complete"]
        },
        "agents": {
            "planner": {"status": "idle", "output": {}},
            "test_writer": {"status": "idle", "output": {}},
            "coder": {"status": "idle", "output": {}},
            "reviewer": {"status": "idle", "output": {}}
        },
        "iterations": [],
        "messages": []
    }
    
    with open(STATE_FILE, 'w') as f:
        json.dump(initial_state, f, indent=2)
    
    print(f"Initialized agent state at {STATE_FILE}")

def start_workflow(requirements):
    """Start a new workflow with given requirements"""
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    
    # Update project requirements
    state["project"]["requirements"] = requirements
    state["workflow"]["current_phase"] = "planning"
    
    # Set agent statuses to trigger pipeline
    state["agents"]["planner"]["status"] = "pending"
    state["agents"]["test_writer"]["status"] = "waiting"
    state["agents"]["coder"]["status"] = "waiting"
    state["agents"]["reviewer"]["status"] = "waiting"
    
    # Add message
    state["messages"].append({
        "timestamp": datetime.now().isoformat(),
        "type": "workflow_start",
        "content": f"Starting workflow with {len(requirements)} requirements"
    })
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"Started workflow with {len(requirements)} requirements")

def monitor_progress():
    """Monitor and display workflow progress"""
    print("\nMonitoring agent progress...")
    last_phase = None
    
    while True:
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            
            current_phase = state["workflow"]["current_phase"]
            
            # Display status update if phase changed
            if current_phase != last_phase:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Phase: {current_phase}")
                for agent, data in state["agents"].items():
                    status = data["status"]
                    symbol = "✓" if status == "completed" else "○" if status == "idle" else "⟳" if status == "in_progress" else "⏸"
                    print(f"  {symbol} {agent}: {status}")
                last_phase = current_phase
            
            # Check if workflow is complete
            if all(agent["status"] == "completed" for agent in state["agents"].values()):
                print("\n✓ Workflow completed!")
                break
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        except Exception as e:
            print(f"Error reading state: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent-coordinator.py <command> [args]")
        print("Commands:")
        print("  init                    - Initialize agent state")
        print("  start <requirement>     - Start workflow with requirement")
        print("  monitor                 - Monitor workflow progress")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_state()
    elif command == "start":
        if len(sys.argv) < 3:
            print("Error: Please provide requirements")
            sys.exit(1)
        requirements = sys.argv[2:]
        start_workflow(requirements)
        monitor_progress()
    elif command == "monitor":
        monitor_progress()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)