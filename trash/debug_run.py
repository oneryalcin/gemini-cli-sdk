#!/usr/bin/env python3
"""Debug version to see what's happening"""

import anyio
import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from gemini_cli_sdk import (
    query,
    GeminiOptions,
    AssistantMessage,
    TextBlock,
)


async def debug_example():
    """Debug example with error handling"""
    print("=== Debug Example ===")
    print(f"Working directory: {os.getcwd()}")
    print(f"GEMINI_API_KEY set: {bool(os.getenv('GEMINI_API_KEY'))}")
    print(f"OPENAI_API_KEY set: {bool(os.getenv('OPENAI_API_KEY'))}")
    print()
    
    try:
        message_count = 0
        async for message in query(prompt="What is 2 + 2?"):
            message_count += 1
            print(f"Message {message_count}: {type(message).__name__}")
            print(message)
            print("-" * 30)
            
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Assistant says: {block.text}")
        
        if message_count == 2:  # Only system and user message
            print("⚠️ No assistant message received!")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    anyio.run(debug_example)