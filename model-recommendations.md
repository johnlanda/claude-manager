# Model Selection Guide for Multi-Agent System

## 📊 Model Comparison for Your Max Subscription

### Available Models (2024-2025)

| Model | Speed | Intelligence | Cost (Input/Output per MTok) | Best For |
|-------|-------|--------------|------------------------------|----------|
| **Claude 3.5 Haiku** | ⚡⚡⚡ | ★★☆ | $0.80/$4.00 | High-volume, quick tasks |
| **Claude 3.7 Sonnet** | ⚡⚡ | ★★★ | $3.00/$15.00 | Balanced performance |
| **Claude Opus 4** | ⚡ | ★★★★ | $15.00/$75.00 | Complex reasoning & coding |

## 🎯 Recommended Configuration

### For Maximum Performance (Current Setup)
```bash
# All agents use Opus 4 - Best for complex development tasks
export CLAUDE_MODEL=claude-opus-4-20250514
```

### For Cost-Optimized Performance
```bash
# Create a mixed-model configuration file
cat > model-config.sh <<EOF
export COORDINATOR_MODEL=claude-3-7-sonnet-20241220  # Moderate complexity
export PLANNER_MODEL=claude-opus-4-20250514         # Needs deep analysis
export TEST_WRITER_MODEL=claude-opus-4-20250514     # Critical for quality
export CODER_MODEL=claude-opus-4-20250514           # Best coding performance
export REVIEWER_MODEL=claude-3-7-sonnet-20241220    # Can use balanced model
EOF
```

## 💡 Key Considerations

### 1. **Agent-Specific Needs**
- **Planner**: Benefits from Opus 4's superior reasoning for architecture decisions
- **Test Writer**: Opus 4 ensures comprehensive test coverage
- **Coder**: Opus 4 leads in coding benchmarks (72.5% on SWE-bench)
- **Reviewer**: Sonnet 3.7 is sufficient for code review tasks
- **Coordinator**: Sonnet 3.7 handles workflow management well

### 2. **Cost vs Performance Trade-offs**
- **All Opus 4**: ~5x more expensive than Sonnet, but provides best results
- **Mixed Setup**: Can reduce costs by 40-60% with minimal quality impact
- **Development vs Production**: Use Opus 4 for development, consider mixed for production

### 3. **Speed Considerations**
- Sonnet is 2x faster than Opus for most tasks
- Haiku is 3-5x faster but may miss nuances in complex code
- For your multi-agent system, intelligence > speed due to parallel execution

## 🔧 Implementation Options

### Option 1: Modify start-agents.sh
```bash
# Add model selection per agent
PLANNER_MODEL="${PLANNER_MODEL:-$CLAUDE_MODEL}"
CODER_MODEL="${CODER_MODEL:-$CLAUDE_MODEL}"
# ... etc
```

### Option 2: Create agent-specific Procfiles
```bash
# Procfile.mixed-models
coordinator: claude code --model claude-3-7-sonnet-20241220 ...
planner: claude code --model claude-opus-4-20250514 ...
```

## 📈 Recommendations for Max Subscription Users

1. **Start with Opus 4 for all agents** - Maximize quality during development
2. **Profile token usage** after a few workflows to understand costs
3. **Optimize selectively** - Downgrade specific agents if costs are high
4. **Monitor performance** - Track completion rates and quality metrics

## 🎬 Bottom Line

For a Max subscription user focused on code development:
- **Use Opus 4** as your default - it's the world's best coding model
- **Consider Sonnet 3.7** for coordinator and reviewer roles if managing costs
- **Avoid Haiku** for this use case - the intelligence gap is too significant

The 5x cost difference between Opus and Sonnet is justified by:
- Higher success rates (fewer retries needed)
- Better code quality (less debugging later)
- More comprehensive test coverage
- Superior architectural decisions