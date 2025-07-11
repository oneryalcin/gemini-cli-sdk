import anyio
import os
import rich

os.environ["GEMINI_MODEL"] = "gemini-2.0-flash"

from gemini_cli_sdk import (
    AssistantMessage,
    ResultMessage,
    TextBlock,
    CodeBlock,
    query,
)


async def basic_example():
    """Basic example - simple question (Claude SDK example)."""
    print("=== Basic Example ===")

    async for message in query(prompt="What is 2 + 2?"):
        rich.print(message)

    print('-' * 30)


async def main():
    """Run all Claude-compatible examples."""

    await basic_example()
    


if __name__ == "__main__":
    anyio.run(main)