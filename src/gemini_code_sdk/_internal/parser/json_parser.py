"""JSON parser for future Gemini CLI structured output."""

import json
from typing import List

from ...types import Message
from ..._errors import CLIJSONDecodeError
from . import ParserStrategy


class JSONParser(ParserStrategy):
    """
    Parser for native JSON output from Gemini CLI.
    
    This is a placeholder for when Gemini CLI supports --output-format json.
    It will parse streaming JSON similar to Claude Code SDK.
    """
    
    async def parse(self, raw_output: str, stderr: str = "") -> List[Message]:
        """
        Parse JSON output from Gemini CLI.
        
        This is not yet implemented as Gemini CLI doesn't support JSON output.
        When it does, this will parse newline-delimited JSON messages.
        """
        raise NotImplementedError(
            "JSON parsing not yet available. "
            "Gemini CLI does not currently support structured JSON output. "
            "Use LLMParser instead."
        )
    
    def _parse_json_line(self, line: str) -> dict:
        """Parse a single JSON line."""
        try:
            return json.loads(line)
        except json.JSONDecodeError as e:
            raise CLIJSONDecodeError(line, e)