"""LLM-based parser for Gemini CLI output using Gemini's native structured output."""

import logging
import os
import re
from datetime import datetime
from typing import Literal

from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field

from ..._errors import ConfigurationError, ParsingError
from ...types import (
    AssistantMessage,
    CodeBlock,
    ContentBlock,
    Message,
    ResultMessage,
    TextBlock,
)
from . import ParserStrategy

logger = logging.getLogger(__name__)


# Structured schemas for LLM parsing
class ParsedContent(BaseModel):
    """Individual content item parsed from output."""

    type: Literal["text", "code", "error"]
    content: str
    language: str | None = Field(None, description="Language for code blocks")


class ParsedResponse(BaseModel):
    """Structured representation of Gemini output for LLM parsing."""

    contents: list[ParsedContent] = Field(description="List of content blocks in order")
    has_code: bool = Field(description="Whether the response contains code blocks")
    has_error: bool = Field(description="Whether the response indicates an error")
    summary: str = Field(description="Brief summary of the response", max_length=100)


class LLMParser(ParserStrategy):
    """Parser that uses Gemini to extract structured data from plain text."""

    def __init__(self, model: str = "gemini-2.5-flash-lite-preview-06-17"):
        """
        Initialize LLM parser using Gemini.

        Args:
            model: Gemini model to use for parsing
        """
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "Gemini API key required for parsing",
                missing_key="GEMINI_API_KEY or GOOGLE_API_KEY"
            )

        self.model = os.getenv("GEMINI_PARSER_MODEL", model)
        self.client = genai.Client(api_key=api_key)

        # Cache for simple responses
        self._simple_cache = {
            "": [],  # Empty response
        }

    async def parse(self, raw_output: str, stderr: str = "") -> list[Message]:
        """
        Parse Gemini output using Gemini's structured output.

        Args:
            raw_output: The stdout from Gemini CLI
            stderr: The stderr from Gemini CLI

        Returns:
            List of parsed messages
        """
        messages: list[Message] = []

        # Strip common Gemini CLI prefixes/suffixes
        cleaned_output = self._clean_output(raw_output)

        # Check cache for simple responses
        if cleaned_output in self._simple_cache:
            cached = self._simple_cache[cleaned_output]
            if cached:
                return cached.copy()

        # Handle empty responses
        if not cleaned_output or not cleaned_output.strip():
            return messages

        # Quick check for simple numeric/single word responses
        if self._is_simple_response(cleaned_output):
            messages.append(
                AssistantMessage(content=[TextBlock(text=cleaned_output.strip())])
            )
            return messages

        try:
            # Use Gemini to parse the output
            parsed = await self._parse_with_llm(cleaned_output, stderr)

            # Convert parsed response to SDK messages
            content_blocks: list[ContentBlock] = []

            for item in parsed.contents:
                if item.type == "text":
                    content_blocks.append(TextBlock(text=item.content))
                elif item.type == "code":
                    content_blocks.append(CodeBlock(
                        code=item.content,
                        language=item.language or "plaintext"
                    ))
                elif item.type == "error":
                    # For errors, we'll add as text with error prefix
                    content_blocks.append(TextBlock(
                        text=f"Error: {item.content}"
                    ))

            if content_blocks:
                messages.append(AssistantMessage(content=content_blocks))

            # Add result message with basic metadata
            messages.append(ResultMessage(
                subtype="success" if not parsed.has_error else "error",
                duration_ms=100,  # Placeholder
                is_error=parsed.has_error,
                session_id=self._generate_session_id(),
                num_turns=1,
                result=parsed.summary if not parsed.has_error else None
            ))

        except Exception as e:
            logger.error(f"LLM parsing failed: {e}")
            # Fallback: treat entire output as text
            messages.append(AssistantMessage(
                content=[TextBlock(text=cleaned_output)]
            ))
            messages.append(ResultMessage(
                subtype="parsing_fallback",
                duration_ms=100,
                is_error=False,
                session_id=self._generate_session_id(),
                num_turns=1
            ))

        return messages

    async def _parse_with_llm(self, output: str, stderr: str) -> ParsedResponse:
        """Use Gemini to parse the output into structured format."""

        system_prompt = """You are a parser for Gemini CLI output.
        Extract structured information from the CLI output.

        Identify:
        1. Plain text responses
        2. Code blocks (with language if specified) - look for ``` markers
        3. Error messages or warnings
        4. Multiple content sections if present

        Be precise and preserve the exact content."""

        prompt = f"{system_prompt}\n\nParse this Gemini CLI output:\n\n{output}"
        if stderr:
            prompt += f"\n\nStderr output:\n{stderr}"

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ParsedResponse,
                )
            )
            
            # response.parsed already returns the parsed Pydantic object
            return response.parsed
            
        except Exception as e:
            raise ParsingError(
                "Gemini parsing failed",
                raw_output=output,
                original_error=e
            ) from e

    def _clean_output(self, output: str) -> str:
        """Remove common Gemini CLI artifacts from output."""
        # Remove the informational messages Gemini adds
        lines_to_skip = [
            "Both GOOGLE_API_KEY and GEMINI_API_KEY are set",
            "Using GOOGLE_API_KEY",
            "Using GEMINI_API_KEY",
            "Today's date is",
            "My operating system is:",
            "I'm currently working in the directory:",
            "Showing up to",
            "This is the Gemini CLI",
            "We are setting up the context"
        ]

        lines = output.strip().split('\n')
        cleaned_lines = []

        for line in lines:
            # Skip lines that contain setup messages
            if any(skip in line for skip in lines_to_skip):
                continue
            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines).strip()

    def _is_simple_response(self, text: str) -> bool:
        """Check if response is simple enough to not need LLM parsing."""
        # Single line, no code blocks, under 100 chars
        if '\n' not in text and '```' not in text and len(text) < 100:
            return True

        # Just a number or simple calculation result
        return bool(re.match(r'^[\d\s\+\-\*\/\=\.\,]+$', text.strip()))

    def _generate_session_id(self) -> str:
        """Generate a simple session ID."""
        # Simple timestamp-based ID
        return f"gemini-{int(datetime.now().timestamp())}"