#!/usr/bin/env python3
"""
Claude SDK quick_start.py example running on Gemini SDK.
Only the import is changed - everything else is identical.
"""

import anyio

# ONLY CHANGE: Import from gemini_cli_sdk instead of claude_code_sdk
from gemini_cli_sdk import (
    query,
    ClaudeCodeOptions,
    AssistantMessage,
    TextBlock,
)


async def main():
    """Claude SDK example code - unchanged except for import."""
    
    # Basic example
    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    
    # With options
    options = ClaudeCodeOptions(
        system_prompt="You are a helpful assistant that explains things simply.",
        max_turns=1,
    )
    
    async for message in query(
        prompt="Explain what Python is in one sentence.", 
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")


if __name__ == "__main__":
    print("CLAUDE SDK EXAMPLE RUNNING ON GEMINI SDK")
    print("This proves API compatibility - only import changed\n")
    anyio.run(main)