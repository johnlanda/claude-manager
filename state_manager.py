#!/usr/bin/env python3
"""
Thread-safe state manager with file locking for multi-agent coordination
"""
import json
import fcntl
import time
import os
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Optional, Callable

class StateManager:
    def __init__(self, state_file: str = "agent-state.json"):
        self.state_file = Path(state_file)
        self.lock_file = Path(f"{state_file}.lock")
        self._ensure_state_exists()
    
    def _ensure_state_exists(self):
        """Ensure state file exists with valid structure"""
        if not self.state_file.exists():
            initial_state = {
                "project": {
                    "name": "",
                    "description": "",
                    "requirements": [],
                    "started_at": datetime.now().isoformat()
                },
                "workflow": {
                    "current_phase": "idle",
                    "phases": ["planning", "test-writing", "coding", "review", "complete"],
                    "iteration": 0
                },
                "agents": {
                    "planner": {"status": "idle", "output": {}, "last_update": None},
                    "test_writer": {"status": "idle", "output": {}, "last_update": None},
                    "coder": {"status": "idle", "output": {}, "last_update": None},
                    "reviewer": {"status": "idle", "output": {}, "last_update": None}
                },
                "events": [],
                "errors": []
            }
            self._write_state(initial_state)
    
    @contextmanager
    def _file_lock(self, timeout: float = 5.0):
        """Acquire exclusive lock on state file"""
        lock_acquired = False
        lock_fd = None
        start_time = time.time()
        
        try:
            # Create lock file if it doesn't exist
            lock_fd = open(self.lock_file, 'w')
            
            # Try to acquire lock with timeout
            while True:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock_acquired = True
                    break
                except IOError:
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"Could not acquire lock after {timeout}s")
                    time.sleep(0.1)
            
            yield
            
        finally:
            if lock_acquired and lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            if lock_fd:
                lock_fd.close()
    
    def _read_state(self) -> Dict[str, Any]:
        """Read state file safely"""
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def _write_state(self, state: Dict[str, Any]):
        """Write state file safely"""
        # Write to temp file first
        temp_file = self.state_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Atomic rename
        temp_file.replace(self.state_file)
    
    def read(self) -> Dict[str, Any]:
        """Read current state with lock"""
        with self._file_lock():
            return self._read_state()
    
    def update(self, update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """Update state atomically with a function"""
        with self._file_lock():
            state = self._read_state()
            new_state = update_fn(state)
            self._write_state(new_state)
            return new_state
    
    def update_agent_status(self, agent: str, status: str, output: Optional[Dict] = None):
        """Update specific agent status"""
        def _update(state):
            state["agents"][agent]["status"] = status
            state["agents"][agent]["last_update"] = datetime.now().isoformat()
            if output:
                state["agents"][agent]["output"] = output
            
            # Add event
            state["events"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "agent_status_change",
                "agent": agent,
                "status": status
            })
            
            # Keep only last 100 events
            state["events"] = state["events"][-100:]
            
            return state
        
        return self.update(_update)
    
    def add_error(self, agent: str, error: str):
        """Log an error"""
        def _update(state):
            state["errors"].append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent,
                "error": error
            })
            # Keep only last 50 errors
            state["errors"] = state["errors"][-50:]
            return state
        
        return self.update(_update)
    
    def get_agent_status(self, agent: str) -> Dict[str, Any]:
        """Get specific agent status"""
        state = self.read()
        return state["agents"].get(agent, {})
    
    def get_workflow_phase(self) -> str:
        """Get current workflow phase"""
        state = self.read()
        return state["workflow"]["current_phase"]
    
    def set_workflow_phase(self, phase: str):
        """Set workflow phase"""
        def _update(state):
            state["workflow"]["current_phase"] = phase
            state["events"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "phase_change",
                "phase": phase
            })
            return state
        
        return self.update(_update)
    
    def start_new_workflow(self, requirements: list, project_name: str = ""):
        """Initialize a new workflow"""
        def _update(state):
            state["project"]["requirements"] = requirements
            state["project"]["name"] = project_name
            state["project"]["started_at"] = datetime.now().isoformat()
            state["workflow"]["current_phase"] = "planning"
            state["workflow"]["iteration"] += 1
            
            # Reset all agents
            for agent in state["agents"]:
                state["agents"][agent]["status"] = "idle"
                state["agents"][agent]["output"] = {}
                state["agents"][agent]["last_update"] = None
            
            # Set planner to start
            state["agents"]["planner"]["status"] = "pending"
            
            # Add event
            state["events"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "workflow_start",
                "requirements_count": len(requirements)
            })
            
            return state
        
        return self.update(_update)