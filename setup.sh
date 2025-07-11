#!/bin/bash
# Setup script for Gemini Code SDK development with UV

echo "Setting up Gemini Code SDK development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment with uv
echo "Creating virtual environment..."
uv venv

# Install dependencies
echo "Installing dependencies..."
uv pip install -e ".[dev]"

# Install pre-commit hooks if available
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Installing pre-commit hooks..."
    uv run pre-commit install
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "  uv run pytest"
echo ""
echo "To run examples:"
echo "  export OPENAI_API_KEY='your-key'"
echo "  export GEMINI_API_KEY='your-key'"
echo "  uv run python examples/quick_start.py"