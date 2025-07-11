.PHONY: help install install-dev clean test lint format build publish publish-test check-version tag examples

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       Install package in development mode"
	@echo "  make install-dev   Install package with dev dependencies"
	@echo "  make clean         Clean build artifacts"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linting (ruff)"
	@echo "  make format        Format code with ruff"
	@echo "  make build         Build distribution packages"
	@echo "  make publish       Publish to PyPI"
	@echo "  make publish-test  Publish to TestPyPI"
	@echo "  make check-version Check package version"
	@echo "  make tag           Create git tag for current version"
	@echo "  make examples      Run all examples"

# Install package in development mode
install:
	uv pip install -e .

# Install with development dependencies
install-dev:
	uv pip install -e ".[dev]"

# Clean build artifacts
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run tests
test:
	uv run pytest tests/

# Run linting
lint:
	uv run ruff check src/ tests/ examples/

# Format code
format:
	uv run ruff format src/ tests/ examples/

# Build distribution packages
build: clean
	uv run python -m build
	uv run python -m twine check dist/*

# Publish to PyPI
publish: build
	@echo "Publishing to PyPI..."
	uv run python -m twine upload dist/*

# Publish to TestPyPI
publish-test: build
	@echo "Publishing to TestPyPI..."
	uv run python -m twine upload --repository testpypi dist/*

# Check current version
check-version:
	@echo "Current version:"
	@grep "^version" pyproject.toml | cut -d'"' -f2

# Create git tag for current version
tag:
	@VERSION=$$(grep "^version" pyproject.toml | cut -d'"' -f2); \
	echo "Creating tag v$$VERSION..."; \
	git tag -a "v$$VERSION" -m "Release version $$VERSION"; \
	echo "Tag created. Push with: git push origin v$$VERSION"

# Run all examples
examples:
	@echo "Running quick_start.py..."
	uv run python examples/quick_start.py
	@echo "\n\nRunning claude_compatible_examples.py..."
	uv run python examples/claude_compatible_examples.py

# Development workflow shortcuts
.PHONY: dev-test dev-check release

# Run tests and linting
dev-check: lint test

# Full development test (format, lint, test)
dev-test: format lint test

# Full release process (test, build, publish, tag)
release: dev-check build
	@echo "Ready to release. Run 'make publish' to upload to PyPI"
	@echo "After publishing, run 'make tag' to create git tag"