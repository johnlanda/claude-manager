#!/usr/bin/env python3
"""
Workflow monitor with timeout detection and recovery
"""
import time
import sys
from datetime import datetime, timedelta
from state_manager import StateManager
from typing import Dict, Optional

class WorkflowMonitor:
    def __init__(self, state_manager: StateManager):
        self.state = state_manager
        self.agent_timeouts = {
            "planner": 300,      # 5 minutes
            "test_writer": 300,  # 5 minutes  
            "coder": 600,        # 10 minutes
            "reviewer": 300      # 5 minutes
        }
        self.retry_counts = {}
        self.max_retries = 2
    
    def check_agent_timeout(self, agent: str, agent_data: Dict) -> bool:
        """Check if an agent has timed out"""
        if agent_data["status"] != "in_progress":
            return False
        
        last_update = agent_data.get("last_update")
        if not last_update:
            return False
        
        last_update_time = datetime.fromisoformat(last_update)
        timeout_seconds = self.agent_timeouts.get(agent, 300)
        
        return datetime.now() - last_update_time > timedelta(seconds=timeout_seconds)
    
    def handle_timeout(self, agent: str):
        """Handle agent timeout"""
        retry_count = self.retry_counts.get(agent, 0)
        
        if retry_count >= self.max_retries:
            print(f"❌ Agent {agent} failed after {self.max_retries} retries")
            self.state.update_agent_status(agent, "failed")
            self.state.add_error(agent, f"Timed out after {self.max_retries} retries")
            return False
        
        print(f"⚠️  Agent {agent} timed out, retrying ({retry_count + 1}/{self.max_retries})")
        self.retry_counts[agent] = retry_count + 1
        self.state.update_agent_status(agent, "pending")
        return True
    
    def get_next_agent(self, current_phase: str) -> Optional[str]:
        """Determine next agent based on workflow phase"""
        phase_agents = {
            "planning": "planner",
            "test-writing": "test_writer",
            "coding": "coder",
            "review": "reviewer"
        }
        return phase_agents.get(current_phase)
    
    def update_workflow_phase(self, completed_agent: str) -> str:
        """Update workflow phase based on completed agent"""
        transitions = {
            "planner": "test-writing",
            "test_writer": "coding",
            "coder": "review",
            "reviewer": "complete"
        }
        return transitions.get(completed_agent, "idle")
    
    def monitor_workflow(self):
        """Main monitoring loop"""
        print("🔍 Monitoring workflow...")
        last_status = {}
        
        while True:
            try:
                state = self.state.read()
                current_phase = state["workflow"]["current_phase"]
                
                # Check for completion
                if current_phase == "complete":
                    print("✅ Workflow completed successfully!")
                    break
                
                # Check each agent
                for agent, data in state["agents"].items():
                    status = data["status"]
                    
                    # Print status changes
                    if last_status.get(agent) != status:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        symbol = self._get_status_symbol(status)
                        print(f"[{timestamp}] {symbol} {agent}: {status}")
                        last_status[agent] = status
                    
                    # Check for timeouts
                    if self.check_agent_timeout(agent, data):
                        self.handle_timeout(agent)
                    
                    # Handle completed agents
                    if status == "completed" and agent == self.get_next_agent(current_phase):
                        next_phase = self.update_workflow_phase(agent)
                        self.state.set_workflow_phase(next_phase)
                        
                        # Activate next agent
                        next_agent = self.get_next_agent(next_phase)
                        if next_agent:
                            self.state.update_agent_status(next_agent, "pending")
                
                # Check for failed agents
                failed_agents = [a for a, d in state["agents"].items() if d["status"] == "failed"]
                if failed_agents and not any(d["status"] == "in_progress" for d in state["agents"].values()):
                    print(f"❌ Workflow failed due to agent failures: {', '.join(failed_agents)}")
                    break
                
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\n⏹️  Monitoring stopped")
                break
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(5)
    
    def _get_status_symbol(self, status: str) -> str:
        """Get visual symbol for status"""
        symbols = {
            "idle": "○",
            "pending": "⏸",
            "in_progress": "⟳",
            "completed": "✓",
            "failed": "✗"
        }
        return symbols.get(status, "?")
    
    def print_summary(self):
        """Print workflow summary"""
        state = self.state.read()
        print("\n📊 Workflow Summary")
        print("=" * 50)
        
        # Project info
        project = state["project"]
        print(f"Project: {project.get('name', 'Unnamed')}")
        print(f"Requirements: {len(project.get('requirements', []))}")
        print(f"Started: {project.get('started_at', 'Unknown')}")
        
        # Agent status
        print("\nAgent Status:")
        for agent, data in state["agents"].items():
            symbol = self._get_status_symbol(data["status"])
            print(f"  {symbol} {agent}: {data['status']}")
        
        # Recent events
        print("\nRecent Events:")
        for event in state["events"][-5:]:
            print(f"  [{event['timestamp']}] {event['type']}")
        
        # Errors
        if state["errors"]:
            print("\n⚠️  Errors:")
            for error in state["errors"][-3:]:
                print(f"  [{error['timestamp']}] {error['agent']}: {error['error']}")

if __name__ == "__main__":
    state_manager = StateManager()
    monitor = WorkflowMonitor(state_manager)
    
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        monitor.print_summary()
    else:
        monitor.monitor_workflow()
        monitor.print_summary()