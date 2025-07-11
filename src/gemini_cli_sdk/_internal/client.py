"""Internal client implementation."""

import os
import logging
from typing import AsyncIterator, Optional

from ..types import Message, GeminiOptions, SystemMessage, UserMessage
from .transport import Transport
from .transport.subprocess_cli import SubprocessCLITransport
from .parser import ParserStrategy
from .parser.llm_parser import LLMParser
from .parser.json_parser import JSONParser


logger = logging.getLogger(__name__)


class InternalClient:
    """Internal client implementation."""
    
    def __init__(
        self,
        transport: Optional[Transport] = None,
        parser: Optional[ParserStrategy] = None
    ):
        """
        Initialize the internal client.
        
        Args:
            transport: Transport implementation (default: SubprocessCLITransport)
            parser: Parser strategy (default: auto-detect based on env)
        """
        self.transport = transport or SubprocessCLITransport()
        self.parser = parser or self._create_parser()
        
    def _create_parser(self) -> ParserStrategy:
        """Create parser based on environment configuration."""
        parser_type = os.getenv("GEMINI_PARSER_STRATEGY", "llm").lower()
        
        if parser_type == "json":
            # For future when JSON is supported
            logger.warning(
                "JSON parser requested but Gemini CLI doesn't support JSON output yet. "
                "Falling back to LLM parser."
            )
            return LLMParser()
        elif parser_type == "llm":
            return LLMParser()
        else:
            logger.warning(f"Unknown parser type: {parser_type}. Using LLM parser.")
            return LLMParser()
    
    async def process_query(
        self, prompt: str, options: GeminiOptions
    ) -> AsyncIterator[Message]:
        """
        Process a query through transport and parser.
        
        Args:
            prompt: The prompt to send
            options: Configuration options
            
        Yields:
            Messages from the conversation
        """
        try:
            # Connect transport
            await self.transport.connect()
            
            # Emit initial system message
            yield SystemMessage(
                subtype="init",
                data={
                    "model": options.model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
                    "cwd": str(options.cwd) if options.cwd else os.getcwd(),
                    "parser": type(self.parser).__name__,
                    "sandbox": options.sandbox,
                    "yolo": options.yolo,
                }
            )
            
            # Emit user message
            yield UserMessage(content=prompt)
            
            # Execute the query
            stdout, stderr = await self.transport.execute(prompt, options)
            
            # Parse the output
            messages = await self.parser.parse(stdout, stderr)
            
            # Yield all parsed messages
            for message in messages:
                yield message
                
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            # Emit error message before re-raising
            yield ResultMessage(
                subtype="error_during_execution",
                duration_ms=0,
                is_error=True,
                session_id="error",
                num_turns=0,
                result=str(e)
            )
            raise
        finally:
            # Ensure transport is disconnected
            await self.transport.disconnect()