<p align="center">
  <img src="assets/readme-cover.svg" alt="Trace Scrub cover" width="100%" />
</p>

# Trace Scrub

![stack](https://img.shields.io/badge/stack-Python-dc2626?style=flat-square) ![python](https://img.shields.io/badge/python-3.10-7c3aed?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-0891b2?style=flat-square) ![ci](https://img.shields.io/badge/ci-GitHub%20Actions-b45309?style=flat-square)

Redact sensitive values from LLM traces, prompts, and JSONL logs.

## Good for

- quick local checks around trace privacy
- small CI jobs where a readable report is enough
- review workflows that need deterministic output
- examples based on `examples/chat-trace.jsonl`

## Run it

```bash
python -m pip install -e ".[dev]"
trace-scrub examples/chat-trace.jsonl
trace-scrub examples/chat-trace.jsonl --json --fail-on medium
```

## Project notes

- Command: `trace-scrub`
- Language: Python
- Python: `>=3.10`
- Tests: `pytest`

## Layout

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```

## Check locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m trace_scrub --help
```
