"""Basic tests for Gemini SDK."""

import pytest
import anyio
from unittest.mock import Mock, AsyncMock, patch

from gemini_cli_sdk import (
    query,
    GeminiOptions,
    AssistantMessage,
    TextBlock,
    CodeBlock,
    CLINotFoundError,
    ConfigurationError,
)


@pytest.mark.asyncio
async def test_query_basic():
    """Test basic query functionality with mocked transport."""
    # Mock the subprocess transport
    with patch("gemini_cli_sdk._internal.client.SubprocessCLITransport") as MockTransport:
        # Set up mock
        mock_transport = Mock()
        mock_transport.connect = AsyncMock()
        mock_transport.disconnect = AsyncMock()
        mock_transport.execute = AsyncMock(return_value=("42", ""))
        MockTransport.return_value = mock_transport
        
        # Mock the LLM parser to return simple response
        with patch("gemini_cli_sdk._internal.client.LLMParser") as MockParser:
            mock_parser = Mock()
            mock_parser.parse = AsyncMock(return_value=[
                AssistantMessage(content=[TextBlock(text="42")])
            ])
            MockParser.return_value = mock_parser
            
            # Run query
            messages = []
            async for message in query(prompt="What is 40 + 2?"):
                messages.append(message)
            
            # Verify we got messages
            assert len(messages) >= 2  # At least system init and assistant message
            
            # Find assistant message
            assistant_messages = [m for m in messages if isinstance(m, AssistantMessage)]
            assert len(assistant_messages) == 1
            assert assistant_messages[0].content[0].text == "42"


@pytest.mark.asyncio
async def test_query_with_options():
    """Test query with custom options."""
    with patch("gemini_cli_sdk._internal.client.SubprocessCLITransport") as MockTransport:
        mock_transport = Mock()
        mock_transport.connect = AsyncMock()
        mock_transport.disconnect = AsyncMock()
        mock_transport.execute = AsyncMock(return_value=("Hello from Gemini", ""))
        MockTransport.return_value = mock_transport
        
        with patch("gemini_cli_sdk._internal.client.LLMParser") as MockParser:
            mock_parser = Mock()
            mock_parser.parse = AsyncMock(return_value=[
                AssistantMessage(content=[TextBlock(text="Hello from Gemini")])
            ])
            MockParser.return_value = mock_parser
            
            options = GeminiOptions(
                model="gemini-2.0-flash",
                yolo=True,
                sandbox=True,
            )
            
            messages = []
            async for message in query(prompt="Hello", options=options):
                messages.append(message)
            
            # Verify execute was called with options
            mock_transport.execute.assert_called_once()
            call_args = mock_transport.execute.call_args
            assert call_args[0][0] == "Hello"  # prompt
            assert call_args[0][1].model == "gemini-2.0-flash"
            assert call_args[0][1].yolo is True
            assert call_args[0][1].sandbox is True


def test_error_hierarchy():
    """Test that error classes are properly defined."""
    # Test inheritance
    assert issubclass(CLINotFoundError, ConfigurationError.__bases__[0])
    
    # Test error creation
    err = CLINotFoundError("Test error", cli_path="/usr/bin/gemini")
    assert "Test error: /usr/bin/gemini" in str(err)
    
    # Test configuration error
    config_err = ConfigurationError("Missing API key", missing_key="OPENAI_API_KEY")
    assert "Missing OPENAI_API_KEY" in str(config_err)


def test_compatibility_imports():
    """Test that compatibility aliases work."""
    from gemini_cli_sdk import ClaudeCodeOptions, ClaudeSDKError
    
    # These should be aliases
    assert ClaudeCodeOptions is GeminiOptions
    
    # Error alias
    from gemini_cli_sdk import GeminiSDKError
    assert ClaudeSDKError is GeminiSDKError