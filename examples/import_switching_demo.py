#!/usr/bin/env python3
"""
Demonstrate import switching between Claude SDK and Gemini SDK.
This shows how users can easily migrate with minimal changes.
"""

import anyio
import os
import sys


async def run_with_sdk(sdk_name: str):
    """Run the same code with different SDK imports."""
    print(f"\n{'=' * 50}")
    print(f"Running with {sdk_name}")
    print('=' * 50)
    
    try:
        if sdk_name == "Claude SDK":
            # Import from Claude SDK
            from claude_code_sdk import (
                query,
                ClaudeCodeOptions as Options,
                AssistantMessage,
                TextBlock,
            )
        else:
            # Import from Gemini SDK (with compatibility aliases)
            from gemini_cli_sdk import (
                query,
                ClaudeCodeOptions as Options,  # Using Claude alias!
                AssistantMessage,
                TextBlock,
            )
        
        # This code is EXACTLY THE SAME for both SDKs
        options = Options(
            system_prompt="You are a helpful assistant",
            max_turns=1,
        )
        
        response_text = []
        async for message in query(
            prompt="What is the Python GIL in one sentence?",
            options=options
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text.append(block.text)
        
        if response_text:
            print(f"✅ Response: {' '.join(response_text)}")
        else:
            print("❌ No response received")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")


async def main():
    """Main demo function."""
    print("IMPORT SWITCHING DEMO")
    print("=" * 70)
    print("The EXACT SAME code works with both Claude SDK and Gemini SDK")
    print("Only the import statements need to change (or use aliases!)")
    
    # Check environment
    has_anthropic = os.getenv("ANTHROPIC_API_KEY") is not None
    has_gemini = os.getenv("GEMINI_API_KEY") is not None
    has_openai = os.getenv("OPENAI_API_KEY") is not None
    
    print("\nEnvironment:")
    print(f"- ANTHROPIC_API_KEY: {'✓' if has_anthropic else '✗'}")
    print(f"- GEMINI_API_KEY: {'✓' if has_gemini else '✗'}")
    print(f"- OPENAI_API_KEY: {'✓' if has_openai else '✗'}")
    
    # Try with Claude SDK (will fail without Claude CLI)
    if has_anthropic:
        await run_with_sdk("Claude SDK")
    else:
        print("\n⚠️  Skipping Claude SDK (ANTHROPIC_API_KEY not set)")
    
    # Try with Gemini SDK
    if has_gemini and has_openai:
        await run_with_sdk("Gemini SDK")
    else:
        print("\n⚠️  Skipping Gemini SDK (requires GEMINI_API_KEY and OPENAI_API_KEY)")
    
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print("""
To migrate from Claude SDK to Gemini SDK:

Option 1 - Update imports:
    # Before
    from claude_code_sdk import query, ClaudeCodeOptions
    
    # After
    from gemini_cli_sdk import query, GeminiOptions

Option 2 - Use compatibility aliases (no code changes!):
    from gemini_cli_sdk import query, ClaudeCodeOptions
    
That's it! Your existing code continues to work!
""")


if __name__ == "__main__":
    anyio.run(main)