"""Type definitions for Gemini SDK - Compatible with Claude Code SDK."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, TypedDict, Optional, List, Union

from typing_extensions import NotRequired  # For Python < 3.11 compatibility

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
    content: List[ContentBlock]
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
    total_cost_usd: Optional[float] = None
    usage: Optional[dict[str, Any]] = None
    result: Optional[str] = None
    type: Literal["result"] = "result"
    # Note: duration_api_ms not available from Gemini CLI


# Union type for all messages
Message = Union[UserMessage, AssistantMessage, SystemMessage, ResultMessage]


@dataclass
class GeminiOptions:
    """Query options for Gemini SDK (compatible with ClaudeCodeOptions)."""
    
    # Core options
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    append_system_prompt: Optional[str] = None
    
    # Gemini-specific options
    sandbox: bool = False
    sandbox_image: Optional[str] = None
    debug: bool = False
    all_files: bool = False
    yolo: bool = False  # Auto-accept all actions
    checkpointing: bool = False
    extensions: Optional[List[str]] = None
    
    # Claude compatibility options (some not implemented yet)
    allowed_tools: List[str] = field(default_factory=list)
    disallowed_tools: List[str] = field(default_factory=list)
    permission_mode: Optional[PermissionMode] = None
    max_turns: Optional[int] = None
    max_thinking_tokens: int = 8000  # Not used by Gemini
    
    # Session management (future)
    continue_conversation: bool = False
    resume: Optional[str] = None
    
    # MCP support (future)
    mcp_servers: dict[str, Any] = field(default_factory=dict)
    allowed_mcp_server_names: Optional[List[str]] = None
    
    # Working directory
    cwd: Union[str, Path, None] = None
    
    # Permission prompt tool (future)
    permission_prompt_tool_name: Optional[str] = None


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