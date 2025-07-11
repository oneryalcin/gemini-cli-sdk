#!/usr/bin/env python3
"""Quick start example for Gemini CLI SDK."""

import anyio
import os

from gemini_cli_sdk import (
    AssistantMessage,
    GeminiOptions,
    ResultMessage,
    TextBlock,
    CodeBlock,
    query,
)


async def basic_example():
    """Basic example - simple question."""
    print("=== Basic Example ===")

    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Gemini: {block.text}")
    print()


async def with_options_example():
    """Example with custom options."""
    print("=== With Options Example ===")

    options = GeminiOptions(
        model="gemini-2.0-flash",
        system_prompt="You are a helpful assistant that explains things simply.",
    )

    async for message in query(
        prompt="Explain what Python is in one sentence.", options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Gemini: {block.text}")
    print()


async def code_generation_example():
    """Example of code generation."""
    print("=== Code Generation Example ===")

    options = GeminiOptions(
        model="gemini-2.0-flash",
    )

    async for message in query(
        prompt="Write a Python function to calculate factorial",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Gemini: {block.text}")
                elif isinstance(block, CodeBlock):
                    print(f"\nCode ({block.language}):")
                    print(block.code)
                    print()
        elif isinstance(message, ResultMessage):
            if not message.is_error:
                print(f"✓ Completed successfully")
    print()


async def migration_example():
    """Example showing migration from Claude Code SDK."""
    print("=== Migration Example ===")
    print("This code works with both Claude Code SDK and Gemini CLI SDK:")
    print()
    
    # This import style works for both SDKs
    try:
        # For Claude SDK
        from claude_code_sdk import query, ClaudeCodeOptions as Options
    except ImportError:
        # For Gemini SDK
        from gemini_cli_sdk import query, GeminiOptions as Options
    
    options = Options(
        system_prompt="You are a helpful coding assistant",
    )
    
    async for message in query(
        prompt="What's the difference between a list and tuple in Python?",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
    print()


async def main():
    """Run all examples."""
    print("Gemini CLI SDK - Quick Start Examples")
    print("=" * 40)
    print()
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set.")
        print("   The SDK uses OpenAI for parsing Gemini output.")
        print("   Set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print()
        return
    
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        print("⚠️  Warning: GEMINI_API_KEY or GOOGLE_API_KEY not set.")
        print("   Set your Gemini API key:")
        print("   export GEMINI_API_KEY='your-key-here'")
        print()
        return
    
    await basic_example()
    await with_options_example()
    await code_generation_example()
    await migration_example()


if __name__ == "__main__":
    anyio.run(main)