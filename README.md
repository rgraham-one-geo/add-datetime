# add-datetime

A small Python package with simple datetime helper utilities.

## Requirements

- Python 3.10+

## Quick start

```bash
pip install -e .
```

## Development setup

```bash
pip install -e ".[dev]"
pytest
ruff check .
mypy src
```

## Project layout

- `src/` contains package code
- `tests/` contains test suite
- `.github/workflows/ci.yml` runs tests, linting, and type checks
