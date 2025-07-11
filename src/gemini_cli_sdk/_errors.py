"""Error types for Gemini SDK - Compatible with Claude SDK errors."""


class GeminiSDKError(Exception):
    """Base exception for all Gemini SDK errors."""
    pass


class CLIConnectionError(GeminiSDKError):
    """Raised when unable to connect to Gemini CLI."""
    pass


class CLINotFoundError(CLIConnectionError):
    """Raised when Gemini CLI is not found or not installed."""

    def __init__(
        self, message: str = "Gemini CLI not found", cli_path: str | None = None
    ):
        if cli_path:
            message = f"{message}: {cli_path}"
        super().__init__(message)


class ProcessError(GeminiSDKError):
    """Raised when the CLI process fails."""

    def __init__(
        self, message: str, exit_code: int | None = None, stderr: str | None = None
    ):
        self.exit_code = exit_code
        self.stderr = stderr

        if exit_code is not None:
            message = f"{message} (exit code: {exit_code})"
        if stderr:
            message = f"{message}\nError output: {stderr}"

        super().__init__(message)


class CLIJSONDecodeError(GeminiSDKError):
    """Raised when unable to decode JSON from CLI output."""

    def __init__(self, line: str, original_error: Exception):
        self.line = line
        self.original_error = original_error
        super().__init__(f"Failed to decode JSON: {line[:100]}...")


class ParsingError(GeminiSDKError):
    """Raised when LLM-based parsing fails."""
    
    def __init__(
        self, 
        message: str = "Failed to parse Gemini output", 
        raw_output: str | None = None,
        original_error: Exception | None = None
    ):
        self.raw_output = raw_output
        self.original_error = original_error
        
        if original_error:
            message = f"{message}: {str(original_error)}"
        if raw_output and len(raw_output) < 200:
            message = f"{message}\nRaw output: {raw_output}"
        
        super().__init__(message)


class ConfigurationError(GeminiSDKError):
    """Raised when SDK is misconfigured."""
    
    def __init__(self, message: str, missing_key: str | None = None):
        self.missing_key = missing_key
        if missing_key:
            message = f"{message}: Missing {missing_key}"
        super().__init__(message)


# Compatibility aliases for Claude SDK
ClaudeSDKError = GeminiSDKError


__all__ = [
    "GeminiSDKError",
    "CLIConnectionError",
    "CLINotFoundError",
    "ProcessError",
    "CLIJSONDecodeError",
    "ParsingError",
    "ConfigurationError",
    "ClaudeSDKError",  # Compatibility alias
]