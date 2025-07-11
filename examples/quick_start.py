#!/usr/bin/env python3
"""Quick start examples for Gemini CLI SDK."""

import os
import anyio
from gemini_cli_sdk import (
    query,
    GeminiOptions,
    AssistantMessage,
    TextBlock,
    CodeBlock,
    # Compatibility aliases for Claude SDK migration
    ClaudeCodeOptions,
)

# Try to use rich for better output, fallback to regular print
try:
    from rich import print
except ImportError:
    pass


async def basic_example():
    """Basic usage - simple question."""
    print("\n[bold]Basic Example[/bold]" if "rich" in globals() else "\nBasic Example")
    
    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)


async def with_options():
    """Using custom options."""
    print("\n[bold]With Options[/bold]" if "rich" in globals() else "\nWith Options")
    
    options = GeminiOptions(
        model="gemini-2.0-flash",
        system_prompt="You are a helpful assistant. Be concise.",
    )
    
    async for message in query(
        prompt="Explain Python's GIL in one sentence.", 
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)


async def code_generation():
    """Handle code generation responses."""
    print("\n[bold]Code Generation[/bold]" if "rich" in globals() else "\nCode Generation")
    
    async for message in query(prompt="Write a Python fibonacci function"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, CodeBlock):
                    print(f"\n```{block.language}")
                    print(block.code)
                    print("```")


async def claude_compatibility():
    """Show compatibility with Claude SDK code."""
    print("\n[bold]Claude SDK Compatibility[/bold]" if "rich" in globals() else "\nClaude SDK Compatibility")
    
    # This code works unchanged from Claude SDK
    options = ClaudeCodeOptions(  # Claude's class name
        system_prompt="You are helpful",
        max_turns=1,
    )
    
    async for message in query(prompt="Hello", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)


async def error_handling():
    """Demonstrate error handling."""
    print("\n[bold]Error Handling[/bold]" if "rich" in globals() else "\nError Handling")
    
    from gemini_cli_sdk import GeminiSDKError, ProcessError
    
    try:
        options = GeminiOptions(model="invalid-model-xxx")
        async for _ in query(prompt="Test", options=options):
            pass
    except ProcessError as e:
        print(f"Process error: {e}")
    except GeminiSDKError as e:
        print(f"SDK error: {e}")


async def main():
    """Run examples."""
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        print("[red]Error:[/red] GEMINI_API_KEY not set" if "rich" in globals() else "Error: GEMINI_API_KEY not set")
        print("export GEMINI_API_KEY='your-key-here'")
        return
    
    print("[bold]Gemini CLI SDK Examples[/bold]" if "rich" in globals() else "Gemini CLI SDK Examples")
    
    await basic_example()
    await with_options()
    await code_generation()
    await claude_compatibility()
    await error_handling()


if __name__ == "__main__":
    anyio.run(main)