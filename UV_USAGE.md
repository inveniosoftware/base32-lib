
## Development with uv

This project supports [uv](https://github.com/astral-sh/uv) for modern Python dependency management.

### Running Tests

```bash
# Install test dependencies
uv sync --group test

# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_base32.py
```

### Development Dependencies

```bash
# Install all development dependencies
uv sync --group dev

# Run code quality checks
uv run isort .
uv run pydocstyle base32_lib
uv run check-manifest
```
