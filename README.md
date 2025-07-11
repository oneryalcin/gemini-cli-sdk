# Gemini CLI SDK for Python

> ⚠️ **EXPERIMENTAL**: This SDK is in early development and uses Gemini's structured output for parsing. The API may change as Gemini CLI evolves.

Python SDK for [Gemini CLI](https://github.com/google-gemini/gemini-cli), providing programmatic access to Gemini with an API compatible with [Claude Code SDK](https://github.com/anthropics/claude-code-sdk-python).

## Installation

```bash
pip install gemini-cli-sdk
```

**Prerequisites:**
- Python 3.10+
- Gemini CLI installed: `npm install -g @google/gemini-cli`
- Gemini API key (for both CLI and parsing)

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

As Gemini CLI doesn't yet support structured JSON output, this SDK uses Gemini's structured output for parsing:

- ✅ Structured message types (compatible with Claude SDK)
- ✅ Async iteration pattern
- ✅ Basic error handling
- ⚠️ Additional latency from parsing (~50-200ms)
- ⚠️ Uses same Gemini API key for both CLI and parsing
- ❌ Tool use blocks (not yet supported)
- ❌ Session management (not exposed by Gemini CLI)
- ❌ Cost tracking (no data available)

## Why These Limitations?

The limitations of this SDK stem from the current architecture of Gemini CLI, not from the SDK design. We're actively monitoring Gemini CLI's development and will add features as they become available.

### Tracking CLI Development

**Structured Output & JSON Format**
- 🚧 [Issue #3674](https://github.com/google-gemini/gemini-cli/issues/3674): JSON output format for non-interactive mode (Priority P1)
- 🚧 [Issue #2023](https://github.com/google-gemini/gemini-cli/issues/2023): TypeScript SDK and structured output support (Priority P2)  
- 🔨 [PR #3699](https://github.com/google-gemini/gemini-cli/pull/3699): Partial JSON logging implementation (In Progress)

**Session Management**
- 🚧 [Issue #2222](https://github.com/google-gemini/gemini-cli/issues/2222): Resume conversation support (`--resume` flag)
- 🚧 [Issue #2384](https://github.com/google-gemini/gemini-cli/issues/2384): Session selection in non-interactive mode

**Tool Use Protocol**
- Currently, Gemini CLI doesn't expose a structured tool use protocol in its output
- Tool execution results are mixed with LLM responses in plain text
- No way to distinguish between tool calls and regular text responses

### What This Means

Until these CLI features land:
- We use Gemini's structured output to parse plain text (adds ~50-200ms latency)
- No session persistence between queries
- No detailed tool execution tracking
- Limited metadata (no token counts, costs, or timing)

### Future Roadmap

Once Gemini CLI implements JSON output (PR #3699 shows active work):
1. We'll switch from LLM parsing to native JSON parsing
2. Session management will be added when CLI exposes it
3. Tool use tracking will be implemented if/when available
4. Performance will improve significantly (no parsing overhead)

The SDK is designed to seamlessly adopt these features without breaking changes to your code.

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Your Gemini API key
- `GEMINI_MODEL`: Default model for CLI (default: `gemini-2.0-flash`)
- `GEMINI_PARSER_MODEL`: Model for parsing output (default: `gemini-2.5-flash-lite-preview-06-17`)

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
2. **Structured Parsing**: Uses Gemini's native structured output to parse plain text into structured messages
3. **Type Safety**: Provides Pydantic models compatible with Claude SDK

When Gemini CLI adds native JSON output support, the SDK will automatically switch to use it without requiring code changes.

## Contributing

This is an experimental project. Contributions, issues, and feedback are welcome!

## License

MIT