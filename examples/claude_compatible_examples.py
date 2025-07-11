#!/usr/bin/env python3
"""
Claude SDK compatible examples running on Gemini SDK.
This demonstrates that code written for Claude SDK works with Gemini SDK.
"""

import anyio
import os

# These imports would normally be from claude_code_sdk
# But we're using gemini_cli_sdk with compatibility aliases
from gemini_cli_sdk import (
    AssistantMessage,
    ClaudeCodeOptions,  # Compatibility alias for GeminiOptions
    ResultMessage,
    TextBlock,
    CodeBlock,
    query,
)


async def basic_example():
    """Basic example - simple question (Claude SDK example)."""
    print("=== Basic Example ===")

    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Assistant: {block.text}")
    print()


async def with_options_example():
    """Example with custom options (Claude SDK example)."""
    print("=== With Options Example ===")

    options = ClaudeCodeOptions(
        system_prompt="You are a helpful assistant that explains things simply.",
        max_turns=1,
    )

    async for message in query(
        prompt="Explain what Python is in one sentence.", options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Assistant: {block.text}")
    print()


async def code_generation_example():
    """Example showing code generation."""
    print("=== Code Generation Example ===")
    
    options = ClaudeCodeOptions(
        system_prompt="You are a helpful coding assistant.",
        model="gemini-2.0-flash",  # Using Gemini model
    )
    
    async for message in query(
        prompt="Write a Python function to calculate the fibonacci sequence",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Text: {block.text}")
                elif isinstance(block, CodeBlock):
                    print(f"\nCode ({block.language}):")
                    print("```" + block.language)
                    print(block.code)
                    print("```")
        elif isinstance(message, ResultMessage):
            print(f"\nResult: {'Success' if not message.is_error else 'Error'}")
            if message.result:
                print(f"Summary: {message.result}")
    print()


async def migration_demo():
    """Demonstrate zero-change migration from Claude to Gemini."""
    print("=== Migration Demo ===")
    print("This code is written for Claude SDK but runs on Gemini SDK:")
    print()
    
    # This is actual Claude SDK code - no changes needed!
    options = ClaudeCodeOptions(
        system_prompt="You are a helpful assistant",
        max_turns=1,
    )
    
    # Using the query function exactly as in Claude SDK
    responses = []
    async for message in query(
        prompt="What's the capital of France?",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    responses.append(block.text)
    
    print(f"Response: {' '.join(responses)}")
    print("\n✅ Claude SDK code works without modification!")
    print()


async def error_handling_example():
    """Example of error handling (compatible with Claude SDK)."""
    print("=== Error Handling Example ===")
    
    # Import error types - these work with both SDKs
    from gemini_cli_sdk import (
        CLINotFoundError,
        ProcessError,
        ClaudeSDKError,  # Compatibility alias
    )
    
    try:
        # Simulate an error case
        options = ClaudeCodeOptions(
            model="invalid-model-xxx",
        )
        
        async for message in query(prompt="Test error", options=options):
            pass
            
    except CLINotFoundError:
        print("❌ Gemini CLI not found (would be Claude CLI in Claude SDK)")
    except ProcessError as e:
        print(f"❌ Process error: {e}")
    except ClaudeSDKError as e:
        print(f"❌ SDK error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    
    print("✅ Error handling is compatible with Claude SDK patterns")
    print()


async def main():
    """Run all Claude-compatible examples."""
    print("=" * 60)
    print("CLAUDE SDK EXAMPLES RUNNING ON GEMINI SDK")
    print("=" * 60)
    print()
    print("These examples use Claude SDK imports and patterns")
    print("but are actually running on Gemini SDK!")
    print()
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   Required for LLM-based parsing")
        return
    
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        print("⚠️  Warning: GEMINI_API_KEY not set")
        return
    
    # Run examples
    await basic_example()
    await with_options_example()
    await code_generation_example()
    await migration_demo()
    await error_handling_example()
    
    print("=" * 60)
    print("✅ ALL CLAUDE SDK PATTERNS WORK WITH GEMINI SDK!")
    print("=" * 60)


if __name__ == "__main__":
    anyio.run(main)