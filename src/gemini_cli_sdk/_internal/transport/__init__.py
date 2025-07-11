"""Transport implementations for Gemini SDK."""

from abc import ABC, abstractmethod
from typing import Tuple

from ...types import GeminiOptions


class Transport(ABC):
    """Abstract transport for Gemini communication."""

    @abstractmethod
    async def connect(self) -> None:
        """Initialize connection."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection."""
        pass

    @abstractmethod
    async def execute(self, prompt: str, options: GeminiOptions) -> Tuple[str, str]:
        """
        Execute a prompt and return output.
        
        Args:
            prompt: The prompt to send to Gemini
            options: Configuration options
            
        Returns:
            Tuple of (stdout, stderr)
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if transport is connected."""
        pass


__all__ = ["Transport"]