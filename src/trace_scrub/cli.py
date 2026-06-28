from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trace_scrub.io import process_file, render_report
from trace_scrub.models import ScrubOptions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trace-scrub",
        description="Redact PII and secrets from LLM traces, prompts, JSON, JSONL, and text logs.",
    )
    parser.add_argument("input", type=Path, help="file to scrub")
    parser.add_argument("-o", "--output", type=Path, help="write redacted content to this file")
    parser.add_argument(
        "--report",
        type=Path,
        help="write a findings report; defaults to stderr when omitted",
    )
    parser.add_argument(
        "--keep-last",
        type=int,
        default=0,
        help="keep the final N characters after each redaction marker",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="exit with status 2 when any sensitive value was found",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.keep_last < 0:
        parser.error("--keep-last must be zero or greater")

    options = ScrubOptions(keep_last=args.keep_last)
    try:
        processed = process_file(args.input, options)
    except FileNotFoundError:
        print(f"trace-scrub: file not found: {args.input}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"trace-scrub: failed to parse {args.input}: {exc}", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(processed.content, encoding="utf-8")
    else:
        print(processed.content, end="")

    report = render_report(processed.findings)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    else:
        print(report, file=sys.stderr, end="")

    if args.fail_on_findings and processed.findings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
