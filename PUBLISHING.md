# Publishing to PyPI

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **API Token**: Generate a token at https://pypi.org/manage/account/token/
   - Scope: "Entire account" for first publish, then create project-specific token
3. **Build Tools**: Install required tools
   ```bash
   uv pip install build twine
   ```

## Pre-publish Checklist

- [ ] Version number is correct in `pyproject.toml`
- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] LICENSE file exists
- [ ] README.md is complete

## Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
uv run python -m build
```

## Test with TestPyPI (Optional but Recommended)

1. Upload to TestPyPI:
   ```bash
   uv run python -m twine upload --repository testpypi dist/*
   ```

2. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ gemini-cli-sdk
   ```

## Publish to PyPI

1. **First Time - Interactive**:
   ```bash
   uv run python -m twine upload dist/*
   ```
   Enter your PyPI username: `__token__`
   Enter your PyPI password: `<your-api-token>`

2. **With .pypirc Configuration**:
   Create `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = <your-api-token>
   ```
   
   Then upload:
   ```bash
   uv run python -m twine upload dist/*
   ```

3. **Using Environment Variable**:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=<your-api-token>
   uv run python -m twine upload dist/*
   ```

## Post-publish

1. Verify on PyPI: https://pypi.org/project/gemini-cli-sdk/
2. Test installation: `pip install gemini-cli-sdk`
3. Create a git tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

## Version Management

For future releases:
1. Update version in `pyproject.toml`
2. Update CHANGELOG (if exists)
3. Commit changes
4. Build and publish
5. Create git tag