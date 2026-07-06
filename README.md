# Trace Scrub

Redact sensitive values from LLM traces, prompts, and JSONL logs. This repo keeps the work close to the terminal: clear input, predictable output, and no service to babysit.

![Trace Scrub cover](assets/readme-cover.svg)

## Where it fits

- for model evaluation, traces, retrieval, and prompt review
- quick local checks without a service dependency
- review notes that should stay easy to reproduce

## Run it

```bash
git clone https://github.com/mertefekurt/trace-scrub.git
cd trace-scrub
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
trace-scrub examples/chat-trace.jsonl
trace-scrub examples/chat-trace.jsonl --json
```

## Project map

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
