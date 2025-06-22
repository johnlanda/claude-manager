#!/usr/bin/env python3
"""
Simple Sequential Multi-Agent System
Minimal, elegant solution for AI agent collaboration
"""
import subprocess
import json
import os
from datetime import datetime

class SimpleAgents:
    def __init__(self):
        self.model = "claude-opus-4-20250514"
        self.agents = {
            'planner': "You are a planning agent. Create a detailed plan for the given task.",
            'tester': "You are a test writer. Write comprehensive tests based on the plan.",
            'coder': "You are a coding agent. Implement code that passes all the tests.",
            'reviewer': "You are a code reviewer. Review the implementation and suggest improvements."
        }
        self.context = {}
        
    def run_agent(self, agent_name, prompt):
        """Run a single agent with Claude Code CLI"""
        print(f"\n🤖 {agent_name.upper()} is thinking...")
        
        # Build the full prompt with role and context
        full_prompt = f"{self.agents[agent_name]}\n\n{prompt}"
        
        # Run Claude Code CLI with --print flag for non-interactive output
        cmd = ['claude', 'code', '--model', self.model, '--print', full_prompt]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            
            # Store in context
            self.context[agent_name] = {
                'prompt': prompt,
                'output': output,
                'timestamp': datetime.now().isoformat()
            }
            
            return output
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running {agent_name}: {e}")
            return None
            
    def run_workflow(self, user_prompt):
        """Run the complete workflow sequentially"""
        print(f"\n📋 Starting workflow: {user_prompt}")
        
        # 1. Planner
        plan = self.run_agent('planner', user_prompt)
        if not plan:
            return
            
        print(f"\n✅ Plan created")
        
        # 2. Test Writer
        test_prompt = f"Based on this plan, write tests:\n\n{plan}"
        tests = self.run_agent('tester', test_prompt)
        if not tests:
            return
            
        print(f"\n✅ Tests written")
        
        # 3. Coder
        code_prompt = f"Implement code to pass these tests:\n\n{tests}"
        code = self.run_agent('coder', code_prompt)
        if not code:
            return
            
        print(f"\n✅ Code implemented")
        
        # 4. Reviewer
        review_prompt = f"Review this implementation:\n\nCode:\n{code}\n\nTests:\n{tests}"
        review = self.run_agent('reviewer', review_prompt)
        
        print(f"\n✅ Review complete")
        
    def show_output(self, agent_name=None):
        """Display output from agents"""
        if agent_name:
            if agent_name in self.context:
                print(f"\n{'='*60}")
                print(f"📄 {agent_name.upper()} OUTPUT:")
                print(f"{'='*60}")
                print(self.context[agent_name]['output'])
                print(f"{'='*60}")
            else:
                print(f"No output found for {agent_name}")
        else:
            # Show all outputs
            for name in ['planner', 'tester', 'coder', 'reviewer']:
                if name in self.context:
                    self.show_output(name)
                    
    def save_session(self, filename=None):
        """Save the current session context"""
        if not filename:
            filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.context, f, indent=2)
        print(f"\n💾 Session saved to {filename}")
        
    def run_interactive(self):
        """Run in interactive mode"""
        print("🚀 Simple Agents - Sequential AI Workflow")
        print("="*50)
        print("Commands:")
        print("  <prompt>    - Run workflow with this prompt")
        print("  show        - Show all agent outputs")
        print("  show <agent>- Show specific agent output")
        print("  save        - Save session to file")
        print("  exit        - Exit the program")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'exit':
                    print("👋 Goodbye!")
                    break
                    
                elif user_input.lower() == 'save':
                    self.save_session()
                    
                elif user_input.lower().startswith('show'):
                    parts = user_input.split()
                    if len(parts) > 1:
                        self.show_output(parts[1])
                    else:
                        self.show_output()
                        
                else:
                    # Run workflow with the prompt
                    self.run_workflow(user_input)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    agents = SimpleAgents()
    agents.run_interactive()