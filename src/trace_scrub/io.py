from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trace_scrub.models import Finding, ScrubOptions
from trace_scrub.scrubber import scrub_text, scrub_value


@dataclass(frozen=True)
class ProcessedDocument:
    content: str
    findings: list[Finding]
    format_name: str


def process_file(path: Path, options: ScrubOptions) -> ProcessedDocument:
    raw = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix == ".json":
        document = json.loads(raw)
        result = scrub_value(document, options)
        return ProcessedDocument(
            content=json.dumps(result.value, indent=2, ensure_ascii=False) + "\n",
            findings=result.findings,
            format_name="json",
        )

    if suffix == ".jsonl":
        return _process_jsonl(raw, options)

    result = scrub_text(raw, options)
    return ProcessedDocument(
        content=str(result.value),
        findings=result.findings,
        format_name="text",
    )


def _process_jsonl(raw: str, options: ScrubOptions) -> ProcessedDocument:
    output: list[str] = []
    findings: list[Finding] = []

    for line_number, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            output.append(line)
            continue
        document: Any = json.loads(line)
        result = scrub_value(document, options, path=f"$[{line_number}]")
        output.append(json.dumps(result.value, ensure_ascii=False))
        findings.extend(result.findings)

    return ProcessedDocument(
        content="\n".join(output) + "\n",
        findings=findings,
        format_name="jsonl",
    )


def render_report(findings: Iterable[Finding]) -> str:
    totals: dict[str, int] = {}
    locations: dict[str, list[str]] = {}
    for finding in findings:
        totals[finding.kind] = totals.get(finding.kind, 0) + finding.count
        locations.setdefault(finding.kind, []).append(finding.path)

    if not totals:
        return "No sensitive values detected.\n"

    lines = ["Sensitive values redacted:"]
    for kind in sorted(totals):
        unique_paths = sorted(set(locations[kind]))
        preview = ", ".join(unique_paths[:4])
        suffix = "" if len(unique_paths) <= 4 else f", +{len(unique_paths) - 4} more"
        lines.append(f"- {kind}: {totals[kind]} match(es) at {preview}{suffix}")
    return "\n".join(lines) + "\n"
