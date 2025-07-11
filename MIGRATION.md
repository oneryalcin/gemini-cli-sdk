# Migration Guide: Claude Code SDK → Gemini Code SDK

This guide helps you migrate from Claude Code SDK to Gemini Code SDK with minimal code changes.

## Quick Migration

### 1. Install Gemini Code SDK

```bash
# Remove Claude SDK
pip uninstall claude-code-sdk

# Install Gemini SDK
pip install gemini-code-sdk
```

### 2. Update Imports

The Gemini SDK provides compatibility aliases for easy migration:

```python
# Option 1: Change imports (recommended)
# Before
from claude_code_sdk import query, ClaudeCodeOptions

# After
from gemini_code_sdk import query, GeminiOptions

# Option 2: Use compatibility aliases (minimal changes)
from gemini_code_sdk import query, ClaudeCodeOptions  # Works!
```

### 3. Update Environment Variables

```bash
# Claude SDK uses:
export ANTHROPIC_API_KEY="your-key"

# Gemini SDK uses:
export GEMINI_API_KEY="your-key"  # or GOOGLE_API_KEY
export OPENAI_API_KEY="your-key"  # Required for LLM parsing
```

## API Compatibility

### ✅ Fully Compatible APIs

These work exactly the same:

- `query()` function signature
- `AsyncIterator[Message]` pattern
- Message types: `AssistantMessage`, `UserMessage`, `SystemMessage`, `ResultMessage`
- Content blocks: `TextBlock`, `CodeBlock`
- Error types (with aliases)

### ⚠️ Partially Compatible

These work but with differences:

| Feature | Claude SDK | Gemini SDK | Notes |
|---------|------------|------------|-------|
| Models | `claude-3-*` | `gemini-2.0-flash`, `gemini-2.5-pro` | Different model names |
| Options | `ClaudeCodeOptions` | `GeminiOptions` | Additional Gemini-specific options |
| System prompts | Supported | Limited support | Gemini has different prompt handling |

### ❌ Not Yet Supported

These features are not available:

- Tool use blocks (`ToolUseBlock`, `ToolResultBlock`)
- Session management (`continue_conversation`, `resume`)
- MCP server configuration (limited)
- Permission prompt tools
- Cost tracking in `ResultMessage`

## Code Examples

### Basic Query (No Changes Needed)

```python
# This code works with both SDKs!
async for message in query(prompt="Hello AI"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

### With Options (Minor Changes)

```python
# Claude SDK
options = ClaudeCodeOptions(
    system_prompt="You are helpful",
    allowed_tools=["Read", "Write"],
    permission_mode="acceptEdits"
)

# Gemini SDK
options = GeminiOptions(
    system_prompt="You are helpful",  # Works but limited
    yolo=True,  # Similar to permission_mode="acceptEdits"
    model="gemini-2.0-flash"  # Gemini models
)
```

### Error Handling (Compatible)

```python
from gemini_code_sdk import (
    CLINotFoundError,
    ProcessError,
    ClaudeSDKError  # Alias works!
)

try:
    async for message in query(prompt="Hello"):
        pass
except CLINotFoundError:
    print("Please install Gemini CLI")
except ProcessError as e:
    print(f"Process failed: {e.exit_code}")
```

## Gemini-Specific Features

The Gemini SDK adds new options:

```python
options = GeminiOptions(
    # Claude-compatible options
    model="gemini-2.0-flash",
    system_prompt="Assistant prompt",
    
    # Gemini-specific options
    sandbox=True,  # Run in sandbox
    yolo=True,  # Auto-accept actions
    all_files=True,  # Include all files in context
    checkpointing=True,  # Enable checkpointing
    extensions=["extension1", "extension2"],
)
```

## Performance Considerations

### LLM-Based Parsing

The Gemini SDK currently uses LLM-based parsing (via OpenAI) because Gemini CLI doesn't support JSON output:

- **Latency**: Adds 100-500ms per response
- **Cost**: ~$0.0001-0.001 per parse (using GPT-4o-mini)
- **Reliability**: More robust than regex parsing

When Gemini CLI adds JSON support, the SDK will automatically switch without code changes.

### Optimization Tips

1. Use `gemini-2.0-flash` for faster responses
2. Set `GEMINI_PARSER_MODEL=gpt-4o-mini` for cheaper parsing
3. Cache responses when possible

## Migration Checklist

- [ ] Install `gemini-code-sdk`
- [ ] Update imports (use find/replace)
- [ ] Set environment variables (`GEMINI_API_KEY`, `OPENAI_API_KEY`)
- [ ] Update model names in options
- [ ] Test error handling
- [ ] Review any tool use code (not yet supported)
- [ ] Test in development before production

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/gemini-code-sdk/gemini-code-sdk-python/issues)
- **Gemini CLI**: [Official Repo](https://github.com/google-gemini/gemini-cli)
- **API Differences**: See docstrings in `types.py`

## Future Compatibility

When Gemini CLI adds JSON output support:
1. The SDK will auto-detect and use it
2. No code changes required
3. Parsing latency/cost will be eliminated
4. More features (tool use, sessions) may become available