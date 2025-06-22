# Example: Building a Calculator Feature

## Step 1: Initialize Project
```bash
# Update agent-state.json with requirements
claude code --prompt "Update agent-state.json with project: 'calculator-app', requirements: ['Create a Calculator class with add, subtract, multiply, divide methods', 'Handle division by zero', 'Support decimal numbers']"
```

## Step 2: Planning Phase
```bash
claude code --prompt "You are the PLANNER agent. Analyze the calculator requirements in agent-state.json and create a detailed implementation plan including:
- Class structure
- Method signatures
- Error handling approach
- Test scenarios to consider
Update agent-state.json with your plan."
```

## Step 3: Test Writing Phase
```bash
claude code --prompt "You are the TEST WRITER agent. Based on the plan in agent-state.json:
1. Create test_calculator.py with comprehensive tests
2. Test normal operations, edge cases, and error conditions
3. Ensure tests fail initially
4. Update agent-state.json with test file location"
```

## Step 4: Implementation Phase
```bash
claude code --prompt "You are the CODER agent. Read agent-state.json and:
1. Run the tests to confirm they fail
2. Create calculator.py implementing the Calculator class
3. Make all tests pass
4. Update agent-state.json with implementation status"
```

## Step 5: Review Phase
```bash
claude code --prompt "You are the REVIEWER agent. Review the implementation:
1. Check code quality and style
2. Verify test coverage
3. Suggest improvements for maintainability
4. Update agent-state.json with review comments"
```

## Step 6: Iteration (if needed)
```bash
claude code --prompt "Read the reviewer comments in agent-state.json and implement the suggested improvements. Run tests to ensure nothing breaks."
```

## Benefits of This Approach:
1. **Separation of Concerns**: Each agent focuses on one aspect
2. **Quality Assurance**: Built-in review process
3. **TDD Enforcement**: Tests written before code
4. **Traceability**: All decisions recorded in agent-state.json
5. **Iterative Improvement**: Easy to refine based on feedback