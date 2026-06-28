from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from trace_scrub.models import Finding, RedactionResult, ScrubOptions
from trace_scrub.rules import RULES, Rule


def scrub_text(text: str, options: ScrubOptions | None = None, path: str = "$") -> RedactionResult:
    options = options or ScrubOptions()
    findings: list[Finding] = []
    redacted = text

    for rule in RULES:
        count = 0

        def replace(match: object, active_rule: Rule = rule) -> str:
            nonlocal count
            matched = match.group(0)  # type: ignore[attr-defined]
            if active_rule.validator and not active_rule.validator(matched):
                return matched
            count += 1
            return _mask(matched, active_rule.kind, options)

        redacted = rule.pattern.sub(replace, redacted)
        if count:
            findings.append(Finding(kind=rule.kind, path=path, count=count))

    return RedactionResult(value=redacted, findings=findings)


def scrub_value(
    value: Any,
    options: ScrubOptions | None = None,
    path: str = "$",
) -> RedactionResult:
    options = options or ScrubOptions()

    if isinstance(value, str):
        return scrub_text(value, options, path)

    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        findings: list[Finding] = []
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if _is_sensitive_key(str(key), options):
                cleaned[str(key)] = _mask(str(item), "sensitive_key", options)
                findings.append(Finding(kind="sensitive_key", path=child_path))
                continue
            result = scrub_value(item, options, child_path)
            cleaned[str(key)] = result.value
            findings.extend(result.findings)
        return RedactionResult(value=cleaned, findings=findings)

    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        cleaned_list: list[Any] = []
        findings = []
        for index, item in enumerate(value):
            result = scrub_value(item, options, f"{path}[{index}]")
            cleaned_list.append(result.value)
            findings.extend(result.findings)
        return RedactionResult(value=cleaned_list, findings=findings)

    return RedactionResult(value=value)


def _is_sensitive_key(key: str, options: ScrubOptions) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(fragment in normalized for fragment in options.redact_keys)


def _mask(value: str, kind: str, options: ScrubOptions) -> str:
    prefix = options.mask.format(kind=kind)
    if options.keep_last <= 0 or len(value) <= options.keep_last:
        return prefix
    return f"{prefix}{value[-options.keep_last:]}"
