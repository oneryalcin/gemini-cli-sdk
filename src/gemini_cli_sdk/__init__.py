"""Gemini SDK for Python - Compatible with Claude Code SDK."""

import os
from collections.abc import AsyncIterator

from ._errors import (
    GeminiSDKError,
    CLIConnectionError,
    CLIJSONDecodeError,
    CLINotFoundError,
    ProcessError,
    ParsingError,
    ConfigurationError,
    # Compatibility aliases
    ClaudeSDKError,
)
from ._internal.client import InternalClient
from .types import (
    # Main types
    AssistantMessage,
    GeminiOptions,
    ContentBlock,
    Message,
    PermissionMode,
    ResultMessage,
    SystemMessage,
    TextBlock,
    CodeBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    # Compatibility alias
    ClaudeCodeOptions,
)

__version__ = "0.1.0"

__all__ = [
    # Main function
    "query",
    # Types
    "PermissionMode",
    "UserMessage",
    "AssistantMessage",
    "SystemMessage",
    "ResultMessage",
    "Message",
    "GeminiOptions",
    "ClaudeCodeOptions",  # Compatibility alias
    "TextBlock",
    "CodeBlock",
    "ToolUseBlock",
    "ToolResultBlock",
    "ContentBlock",
    # Errors
    "GeminiSDKError",
    "ClaudeSDKError",  # Compatibility alias
    "CLIConnectionError",
    "CLINotFoundError",
    "ProcessError",
    "CLIJSONDecodeError",
    "ParsingError",
    "ConfigurationError",
]


async def query(
    *, prompt: str, options: GeminiOptions | None = None
) -> AsyncIterator[Message]:
    """
    Query Gemini CLI.

    Python SDK for interacting with Gemini CLI, with an API compatible
    with Claude Code SDK.

    Args:
        prompt: The prompt to send to Gemini
        options: Optional configuration (defaults to GeminiOptions() if None).
                 Set options.model to choose Gemini model (default: gemini-2.5-pro).
                 Set options.yolo=True to auto-accept all actions.
                 Set options.sandbox=True to run in sandbox mode.
                 Set options.cwd for working directory.

    Yields:
        Messages from the conversation

    Example:
        ```python
        # Simple usage
        async for message in query(prompt="Hello"):
            print(message)

        # With options
        async for message in query(
            prompt="Hello",
            options=GeminiOptions(
                model="gemini-2.0-flash",
                yolo=True,
                cwd="/home/user"
            )
        ):
            print(message)
        ```
    
    Note:
        This SDK uses LLM-based parsing to convert Gemini's plain text output
        into structured messages. This adds some latency and requires an
        OpenAI API key to be set in the OPENAI_API_KEY environment variable.
        
        When Gemini CLI adds native JSON output support, this SDK will
        automatically switch to use it without requiring code changes.
    """
    if options is None:
        options = GeminiOptions()

    # Set SDK identifier
    os.environ["GEMINI_CODE_SDK"] = "python"

    client = InternalClient()

    async for message in client.process_query(prompt=prompt, options=options):
        yield message