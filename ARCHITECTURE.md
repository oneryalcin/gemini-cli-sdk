# Gemini CLI SDK Architecture

## Overview

The Gemini CLI SDK provides a Python interface to Gemini CLI that's API-compatible with Claude Code SDK. It uses LLM-based parsing to convert Gemini's plain text output into structured messages.

## Directory Structure

```
gemini-cli-sdk/
├── src/gemini_cli_sdk/
│   ├── __init__.py              # Public API (query function)
│   ├── types.py                 # Type definitions (Message, Options, etc.)
│   ├── _errors.py               # Error hierarchy
│   ├── py.typed                 # Type checking marker
│   └── _internal/
│       ├── __init__.py
│       ├── client.py            # Orchestrates transport + parser
│       ├── parser/
│       │   ├── __init__.py      # ParserStrategy ABC
│       │   ├── llm_parser.py    # LLM-based parsing (current)
│       │   └── json_parser.py   # JSON parsing (future)
│       └── transport/
│           ├── __init__.py      # Transport ABC
│           └── subprocess_cli.py # Subprocess execution
├── examples/
│   └── quick_start.py           # Usage examples
├── tests/
│   └── test_basic.py            # Basic unit tests
├── pyproject.toml               # Package configuration
├── README.md                    # User documentation
├── MIGRATION.md                 # Migration guide from Claude SDK
├── ARCHITECTURE.md              # This file
└── LICENSE                      # MIT license
```

## Core Components

### 1. Public API (`__init__.py`)

- Single entry point: `async def query(prompt, options) -> AsyncIterator[Message]`
- Maintains exact same signature as Claude SDK
- Handles environment setup and client creation

### 2. Type System (`types.py`)

Compatible with Claude SDK types:
- **Messages**: `UserMessage`, `AssistantMessage`, `SystemMessage`, `ResultMessage`
- **Content Blocks**: `TextBlock`, `CodeBlock`, `ToolUseBlock`, `ToolResultBlock`
- **Options**: `GeminiOptions` (aliased as `ClaudeCodeOptions`)

### 3. Parser Strategy Pattern

```python
class ParserStrategy(ABC):
    async def parse(self, raw_output: str, stderr: str) -> List[Message]
```

Two implementations:
- **LLMParser**: Uses Instructor + OpenAI to parse plain text (current)
- **JSONParser**: For future native JSON support

### 4. Transport Layer

```python
class Transport(ABC):
    async def connect() -> None
    async def disconnect() -> None
    async def execute(prompt, options) -> Tuple[stdout, stderr]
```

- **SubprocessCLITransport**: Executes Gemini CLI as subprocess
- Handles CLI discovery, command building, error detection

### 5. Internal Client

Orchestrates the flow:
1. Creates transport and parser instances
2. Emits initial system message
3. Executes query via transport
4. Parses output via parser strategy
5. Yields messages to caller

## Data Flow

```
User Code
    ↓
query(prompt, options)
    ↓
InternalClient
    ↓
SubprocessCLITransport.execute()
    ↓
Gemini CLI (subprocess)
    ↓
Plain text output
    ↓
LLMParser.parse()
    ↓
OpenAI API (structured output)
    ↓
Message objects
    ↓
User Code (async iteration)
```

## Key Design Decisions

### 1. Adapter Pattern for Parsing

- Allows seamless switch from LLM to JSON parsing
- No API changes when Gemini adds JSON support
- Clean separation of concerns

### 2. API Compatibility

- Exact same public API as Claude SDK
- Type aliases for migration (`ClaudeCodeOptions` → `GeminiOptions`)
- Compatible error hierarchy

### 3. Async/Await Throughout

- Matches Claude SDK's async patterns
- Uses `anyio` for runtime independence
- Proper async context management

### 4. Pragmatic LLM Parsing

- Reliable extraction of structure from plain text
- Handles code blocks, errors, multi-part responses
- Fallback to simple text on parsing failure

## Configuration

### Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Gemini authentication
- `OPENAI_API_KEY`: Required for LLM parsing
- `GEMINI_PARSER_STRATEGY`: Parser selection (default: "llm")
- `GEMINI_PARSER_MODEL`: LLM model for parsing (default: "gpt-4o-mini")

### Future Enhancements

When Gemini CLI adds JSON output:
1. Implement `JSONParser` with streaming support
2. Auto-detect JSON availability
3. Remove LLM parsing dependency
4. Add tool use and session support

## Testing Strategy

- Unit tests with mocked transport/parser
- Integration tests with real Gemini CLI
- Compatibility tests with Claude SDK examples
- Parser tests for various output formats

## Performance Considerations

- LLM parsing adds 100-500ms latency
- Costs ~$0.0001-0.001 per parse
- Simple responses cached to avoid LLM calls
- Future JSON parsing will eliminate overhead