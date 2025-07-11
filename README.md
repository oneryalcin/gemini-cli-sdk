# Gemini CLI SDK for Python

> ⚠️ **EXPERIMENTAL**: This SDK is in early development and uses LLM-based parsing as a temporary solution. The API may change as Gemini CLI evolves.

Python SDK for [Gemini CLI](https://github.com/google-gemini/gemini-cli), providing programmatic access to Gemini with an API compatible with [Claude Code SDK](https://github.com/anthropics/claude-code-sdk-python).

## Installation

```bash
pip install gemini-cli-sdk
```

**Prerequisites:**
- Python 3.10+
- Gemini CLI installed: `npm install -g @google/gemini-cli`
- OpenAI API key (for LLM-based parsing)

## Quick Start

```python
import anyio
from gemini_cli_sdk import query

async def main():
    async for message in query(prompt="What is 2 + 2?"):
        print(message)

anyio.run(main)
```

## Migration from Claude Code SDK

This SDK is designed to be API-compatible with Claude Code SDK. In most cases, you can migrate by simply changing imports:

### Option 1: Update imports (recommended)
```python
# Before
from claude_code_sdk import query, ClaudeCodeOptions

# After  
from gemini_cli_sdk import query, GeminiOptions
```

### Option 2: Use compatibility aliases (zero code changes!)
```python
# This works with Gemini SDK!
from gemini_cli_sdk import query, ClaudeCodeOptions
```

### Complete example
```python
# This Claude SDK code works unchanged with Gemini SDK
from gemini_cli_sdk import (
    query,
    ClaudeCodeOptions,  # Compatibility alias
    AssistantMessage,
    TextBlock
)

options = ClaudeCodeOptions(
    system_prompt="You are helpful",
    max_turns=1
)

async for message in query(prompt="Hello", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

See [MIGRATION.md](MIGRATION.md) for detailed migration guide.

## Current Limitations

As Gemini CLI doesn't yet support structured JSON output, this SDK uses LLM-based parsing:

- ✅ Structured message types (compatible with Claude SDK)
- ✅ Async iteration pattern
- ✅ Basic error handling
- ⚠️ Additional latency from parsing (~100-500ms)
- ⚠️ Requires OpenAI API key for parsing
- ❌ Tool use blocks (not yet supported)
- ❌ Session management (not exposed by Gemini CLI)
- ❌ Cost tracking (no data available)

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Your Gemini API key
- `OPENAI_API_KEY`: Required for LLM-based parsing
- `GEMINI_PARSER_MODEL`: LLM model for parsing (default: `gpt-4o-mini`)

## Examples

### Basic Query

```python
from gemini_cli_sdk import query, GeminiOptions, AssistantMessage, TextBlock

async for message in query(prompt="Hello Gemini"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

### With Options

```python
options = GeminiOptions(
    model="gemini-2.0-flash",
    system_prompt="You are a helpful assistant"
)

async for message in query(prompt="Explain Python", options=options):
    print(message)
```

## How It Works

1. **Subprocess Execution**: Runs Gemini CLI as a subprocess
2. **LLM Parsing**: Uses Instructor + OpenAI to parse plain text output into structured messages
3. **Type Safety**: Provides Pydantic models compatible with Claude SDK

When Gemini CLI adds native JSON output support, the SDK will automatically switch to use it without requiring code changes.

## Contributing

This is an experimental project. Contributions, issues, and feedback are welcome!

## License

MIT