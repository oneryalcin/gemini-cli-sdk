"""Type definitions for Gemini SDK - Compatible with Claude Code SDK."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Union

# Permission modes (matching Claude SDK)
PermissionMode = Literal["default", "acceptEdits", "bypassPermissions"]


# Content block types
@dataclass
class TextBlock:
    """Text content block."""

    text: str
    type: Literal["text"] = "text"


@dataclass
class CodeBlock:
    """Code content block with language."""

    code: str
    language: str = "plaintext"
    type: Literal["code"] = "code"


# Tool blocks - simplified for initial implementation
@dataclass
class ToolUseBlock:
    """Tool use content block (placeholder for future)."""

    id: str
    name: str
    input: dict[str, Any]
    type: Literal["tool_use"] = "tool_use"


@dataclass
class ToolResultBlock:
    """Tool result content block (placeholder for future)."""

    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
    type: Literal["tool_result"] = "tool_result"


# Union type for all content blocks
ContentBlock = Union[TextBlock, CodeBlock, ToolUseBlock, ToolResultBlock]


# Message types
@dataclass
class UserMessage:
    """User message."""

    content: str
    type: Literal["user"] = "user"


@dataclass
class AssistantMessage:
    """Assistant message with content blocks."""

    content: list[ContentBlock]
    type: Literal["assistant"] = "assistant"


@dataclass
class SystemMessage:
    """System message with metadata."""

    subtype: str
    data: dict[str, Any]
    type: Literal["system"] = "system"


@dataclass
class ResultMessage:
    """Result message with execution information."""

    subtype: str
    duration_ms: int
    is_error: bool
    session_id: str
    num_turns: int = 1
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    type: Literal["result"] = "result"
    # Note: duration_api_ms not available from Gemini CLI


# Union type for all messages
Message = Union[UserMessage, AssistantMessage, SystemMessage, ResultMessage]


@dataclass
class GeminiOptions:
    """Query options for Gemini SDK (compatible with ClaudeCodeOptions)."""

    # Core options
    model: str | None = None
    system_prompt: str | None = None
    append_system_prompt: str | None = None

    # Gemini-specific options
    sandbox: bool = False
    sandbox_image: str | None = None
    debug: bool = False
    all_files: bool = False
    yolo: bool = False  # Auto-accept all actions
    checkpointing: bool = False
    extensions: list[str] | None = None

    # Claude compatibility options (some not implemented yet)
    allowed_tools: list[str] = field(default_factory=list)
    disallowed_tools: list[str] = field(default_factory=list)
    permission_mode: PermissionMode | None = None
    max_turns: int | None = None
    max_thinking_tokens: int = 8000  # Not used by Gemini

    # Session management (future)
    continue_conversation: bool = False
    resume: str | None = None

    # MCP support (future)
    mcp_servers: dict[str, Any] = field(default_factory=dict)
    allowed_mcp_server_names: list[str] | None = None

    # Working directory
    cwd: str | Path | None = None

    # Permission prompt tool (future)
    permission_prompt_tool_name: str | None = None


# Compatibility alias for migration from Claude SDK
ClaudeCodeOptions = GeminiOptions


# Export all public types
__all__ = [
    # Permission modes
    "PermissionMode",
    # Content blocks
    "TextBlock",
    "CodeBlock",
    "ToolUseBlock",
    "ToolResultBlock",
    "ContentBlock",
    # Messages
    "UserMessage",
    "AssistantMessage",
    "SystemMessage",
    "ResultMessage",
    "Message",
    # Options
    "GeminiOptions",
    "ClaudeCodeOptions",  # Compatibility alias
]
