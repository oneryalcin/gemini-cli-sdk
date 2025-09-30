# Gemini CLI SDK for Python

> ⚠️ **EXPERIMENTAL**: This SDK is in early development. The API may change as Gemini CLI evolves.
>
> 🎉 **UPDATE (v0.6.1+)**: Gemini CLI now supports JSON output and session recording! See [#9](https://github.com/oneryalcin/gemini-cli-sdk/issues/9) and [#10](https://github.com/oneryalcin/gemini-cli-sdk/issues/10) for details.

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

## Current Status & Limitations

**✅ Recently Unblocked (Gemini CLI v0.6.1+)**
- Native JSON output format available ([#9](https://github.com/oneryalcin/gemini-cli-sdk/issues/9))
- Automatic session recording to disk ([#10](https://github.com/oneryalcin/gemini-cli-sdk/issues/10))
- Token usage and cost tracking data
- API latency metrics

**⚠️ Temporary (Migration in Progress)**
- SDK still uses LLM parsing (adds ~50-200ms latency)
- Migration to native JSON parsing planned

**⚠️ Partially Available**
- Session files recorded but no `--resume` flag yet ([#11](https://github.com/oneryalcin/gemini-cli-sdk/issues/11))

**❌ Not Yet Supported**
- Tool use blocks tracking
- Session resume in non-interactive mode

## Development Status

### Recent Improvements (v0.6.1)

Gemini CLI has made significant progress:

**✅ JSON Output** - [Issue #9](https://github.com/oneryalcin/gemini-cli-sdk/issues/9)
- Native `--output-format json` flag
- Structured response data with token usage
- API latency and tool execution metrics
- Eliminates need for LLM-based parsing

**✅ Session Recording** - [Issue #10](https://github.com/oneryalcin/gemini-cli-sdk/issues/10)
- Automatic conversation history to disk
- Full message history with timestamps
- Token usage per message
- Session IDs for tracking

**⚠️ Session Resume** - [Issue #11](https://github.com/oneryalcin/gemini-cli-sdk/issues/11)
- Recording works, but no `--resume` flag yet
- Upstream [Issue #1530](https://github.com/google-gemini/gemini-cli/issues/1530) tracked (Priority P2)

### Next Steps for This SDK

1. Migrate from LLM parsing to native JSON output ([#9](https://github.com/oneryalcin/gemini-cli-sdk/issues/9))
2. Add session history retrieval ([#10](https://github.com/oneryalcin/gemini-cli-sdk/issues/10))
3. Implement token/cost tracking with real data
4. Wait for upstream session resume support ([#11](https://github.com/oneryalcin/gemini-cli-sdk/issues/11))

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Your Gemini API key
- `GEMINI_MODEL`: Default model for CLI (default: `gemini-2.0-flash`)
- `GEMINI_PARSER_MODEL`: Model for parsing output (default: `gemini-2.5-flash-lite-preview-06-17`)

## Examples

See the `examples/` directory for complete examples:

- **`quick_start.py`** - Comprehensive introduction with all features
- **`claude_quickstart_on_gemini.py`** - Claude SDK code running unchanged
- **`import_switching_demo.py`** - Migration guide from Claude SDK

### Basic Usage

```python
from gemini_cli_sdk import query, AssistantMessage, TextBlock

async for message in query(prompt="Hello Gemini"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

## How It Works

1. **Subprocess Execution**: Runs Gemini CLI as a subprocess
2. **Structured Parsing**: Currently uses Gemini's structured output to parse responses (migration to native JSON planned - see [#9](https://github.com/oneryalcin/gemini-cli-sdk/issues/9))
3. **Type Safety**: Provides Pydantic models compatible with Claude SDK

### Migration to Native JSON (Coming Soon)

Gemini CLI v0.6.1+ supports native JSON output. The SDK will be updated to use this instead of LLM-based parsing, eliminating the ~50-200ms latency overhead.

## Contributing

This is an experimental project. Contributions, issues, and feedback are welcome!

## License

MIT