# Trace Scrub

![Trace Scrub cover](assets/readme-cover.svg)

Redact sensitive values from LLM traces, prompts, and JSONL logs.

`Python`

## Start here

```bash
git clone https://github.com/mertefekurt/trace-scrub.git
cd trace-scrub
python -m pip install -e ".[dev]"
trace-scrub examples/chat-trace.jsonl
```

## Project map

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
```

## Repository

[Open the source on GitHub →](https://github.com/mertefekurt/trace-scrub)

[MIT License](LICENSE)
