"""Parser implementations for Gemini output."""

from abc import ABC, abstractmethod
from typing import List

from ...types import Message


class ParserStrategy(ABC):
    """Abstract base class for parsing strategies."""
    
    @abstractmethod
    async def parse(self, raw_output: str, stderr: str = "") -> List[Message]:
        """
        Parse raw Gemini CLI output into structured messages.
        
        Args:
            raw_output: The stdout from Gemini CLI
            stderr: The stderr from Gemini CLI (for error detection)
            
        Returns:
            List of parsed messages
        """
        pass


__all__ = ["ParserStrategy"]