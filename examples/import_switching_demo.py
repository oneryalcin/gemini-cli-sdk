#!/usr/bin/env python3
"""
Migration guide: How to switch from Claude SDK to Gemini SDK.
"""

import anyio

# Try to use rich for better output
try:
    from rich import print
    from rich.syntax import Syntax
except ImportError:
    pass


async def main():
    print("\n[bold]Migration from Claude SDK to Gemini SDK[/bold]\n" if "rich" in globals() else "\nMigration from Claude SDK to Gemini SDK\n")
    
    # Option 1: Update imports
    code1 = """# Before (Claude SDK)
from claude_code_sdk import query, ClaudeCodeOptions

# After (Gemini SDK)  
from gemini_cli_sdk import query, GeminiOptions"""
    
    if "rich" in globals():
        print(Syntax(code1, "python", theme="monokai"))
    else:
        print(code1)
    
    print("\n[bold]Option 2: Use compatibility aliases (zero code changes)[/bold]\n" if "rich" in globals() else "\nOption 2: Use compatibility aliases (zero code changes)\n")
    
    # Option 2: Use aliases
    code2 = """# This Claude SDK code works unchanged with Gemini SDK
from gemini_cli_sdk import query, ClaudeCodeOptions  # Just change the module name!

# Your existing code continues to work
options = ClaudeCodeOptions(
    system_prompt="You are helpful",
    max_turns=1
)

async for message in query(prompt="Hello", options=options):
    # ... process messages ..."""
    
    if "rich" in globals():
        print(Syntax(code2, "python", theme="monokai"))
    else:
        print(code2)
    
    # Live demo
    print("\n[bold]Live Demo[/bold]\n" if "rich" in globals() else "\nLive Demo\n")
    
    from gemini_cli_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
    
    # This is Claude SDK code but runs on Gemini
    options = ClaudeCodeOptions(max_turns=1)
    
    async for message in query(prompt="Say 'Migration successful!'", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Result: {block.text}")


if __name__ == "__main__":
    anyio.run(main)