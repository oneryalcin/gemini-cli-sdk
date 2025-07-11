"""Subprocess transport implementation using Gemini CLI."""

import os
import shutil
import logging
from pathlib import Path
from subprocess import PIPE
from typing import Tuple, Optional

import anyio
from anyio.abc import Process

from ...types import GeminiOptions
from ..._errors import CLINotFoundError, CLIConnectionError, ProcessError
from . import Transport


logger = logging.getLogger(__name__)


class SubprocessCLITransport(Transport):
    """Subprocess transport using Gemini CLI."""
    
    def __init__(self, cli_path: Optional[str | Path] = None):
        """
        Initialize subprocess transport.
        
        Args:
            cli_path: Path to Gemini CLI executable (auto-detected if None)
        """
        self._cli_path = str(cli_path) if cli_path else self._find_cli()
        self._process: Optional[Process] = None
        
    def _find_cli(self) -> str:
        """Find Gemini CLI binary."""
        # First check if 'gemini' is in PATH
        if cli := shutil.which("gemini"):
            return cli
        
        # Common installation locations
        locations = [
            Path.home() / ".npm-global/bin/gemini",
            Path("/usr/local/bin/gemini"),
            Path.home() / ".local/bin/gemini",
            Path.home() / "node_modules/.bin/gemini",
            Path.home() / ".yarn/bin/gemini",
            # Also check @google/gemini-cli
            Path.home() / ".npm-global/bin/@google/gemini-cli",
        ]
        
        for path in locations:
            if path.exists() and path.is_file():
                return str(path)
        
        # Check if Node.js is installed
        node_installed = shutil.which("node") is not None
        
        if not node_installed:
            error_msg = "Gemini CLI requires Node.js, which is not installed.\n\n"
            error_msg += "Install Node.js from: https://nodejs.org/\n"
            error_msg += "\nAfter installing Node.js, install Gemini CLI:\n"
            error_msg += "  npm install -g @google/gemini-cli"
            raise CLINotFoundError(error_msg)
        
        raise CLINotFoundError(
            "Gemini CLI not found. Install with:\n"
            "  npm install -g @google/gemini-cli\n"
            "\nIf already installed locally, try:\n"
            '  export PATH="$HOME/node_modules/.bin:$PATH"\n'
            "\nOr specify the path when creating the SDK:\n"
            "  # In your code, pass cli_path parameter"
        )
    
    def _build_command(self, prompt: str, options: GeminiOptions) -> list[str]:
        """Build CLI command with arguments."""
        cmd = [self._cli_path]
        
        # Model selection
        if options.model:
            cmd.extend(["-m", options.model])
        
        # Gemini-specific options
        if options.sandbox:
            cmd.append("-s")
        
        if options.sandbox_image:
            cmd.extend(["--sandbox-image", options.sandbox_image])
        
        if options.debug:
            cmd.append("-d")
        
        if options.all_files:
            cmd.append("-a")
        
        if options.yolo:
            cmd.append("-y")
        
        if options.checkpointing:
            cmd.append("-c")
        
        if options.extensions:
            cmd.extend(["-e", *options.extensions])
        
        if options.allowed_mcp_server_names:
            cmd.extend(["--allowed-mcp-server-names", *options.allowed_mcp_server_names])
        
        # Add prompt (non-interactive mode)
        cmd.extend(["-p", prompt])
        
        return cmd
    
    async def connect(self) -> None:
        """No persistent connection needed for CLI invocation."""
        # Verify CLI exists
        if not Path(self._cli_path).exists():
            raise CLINotFoundError(f"Gemini CLI not found at: {self._cli_path}")
    
    async def disconnect(self) -> None:
        """No persistent connection to close."""
        self._process = None
    
    async def execute(self, prompt: str, options: GeminiOptions) -> Tuple[str, str]:
        """
        Execute Gemini CLI with prompt and return output.
        
        Args:
            prompt: The prompt to send
            options: Configuration options
            
        Returns:
            Tuple of (stdout, stderr)
        """
        cmd = self._build_command(prompt, options)
        
        # Set up environment
        env = os.environ.copy()
        env["GEMINI_SDK"] = "gemini-cli-sdk-python"
        
        # Handle working directory
        cwd = str(options.cwd) if options.cwd else None
        if cwd and not Path(cwd).exists():
            raise CLIConnectionError(f"Working directory does not exist: {cwd}")
        
        try:
            # Run the command
            logger.debug(f"Running command: {' '.join(cmd)}")
            
            self._process = await anyio.open_process(
                cmd,
                stdin=None,  # No stdin for non-interactive mode
                stdout=PIPE,
                stderr=PIPE,
                cwd=cwd,
                env=env,
            )
            
            # Wait for completion and collect output
            stdout_data = b""
            stderr_data = b""
            
            # Read stdout
            if self._process.stdout:
                try:
                    async for chunk in self._process.stdout:
                        stdout_data += chunk
                except anyio.EndOfStream:
                    pass
            
            # Read stderr
            if self._process.stderr:
                try:
                    async for chunk in self._process.stderr:
                        stderr_data += chunk
                except anyio.EndOfStream:
                    pass
            
            # Wait for process to complete
            returncode = await self._process.wait()
            
            # Decode output
            stdout = stdout_data.decode('utf-8', errors='replace')
            stderr = stderr_data.decode('utf-8', errors='replace')
            
            # Debug logging
            logger.debug(f"Process completed with return code: {returncode}")
            logger.debug(f"Stdout length: {len(stdout)}")
            logger.debug(f"Stderr length: {len(stderr)}")
            if stdout:
                logger.debug(f"Stdout preview: {stdout[:200]}...")
            if stderr:
                logger.debug(f"Stderr preview: {stderr[:200]}...")
            
            # Check for errors
            if returncode != 0:
                raise ProcessError(
                    f"Gemini CLI failed with exit code {returncode}",
                    exit_code=returncode,
                    stderr=stderr
                )
            
            return stdout, stderr
            
        except FileNotFoundError as e:
            raise CLINotFoundError(f"Gemini CLI not found at: {self._cli_path}") from e
        except Exception as e:
            if isinstance(e, (ProcessError, CLIConnectionError, CLINotFoundError)):
                raise
            raise CLIConnectionError(f"Failed to execute Gemini CLI: {e}") from e
        finally:
            self._process = None
    
    def is_connected(self) -> bool:
        """Check if subprocess is running."""
        return self._process is not None and self._process.returncode is None