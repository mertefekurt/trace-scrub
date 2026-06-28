from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScrubOptions:
    """Configuration for redacting text and structured values."""

    mask: str = "[REDACTED:{kind}]"
    keep_last: int = 0
    redact_keys: tuple[str, ...] = (
        "api_key",
        "apikey",
        "access_token",
        "authorization",
        "bearer",
        "client_secret",
        "cookie",
        "id_token",
        "password",
        "private_key",
        "refresh_token",
        "secret",
        "session",
        "token",
    )


@dataclass(frozen=True)
class Finding:
    kind: str
    path: str
    count: int = 1


@dataclass
class RedactionResult:
    value: object
    findings: list[Finding] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.findings)

    def summary(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for finding in self.findings:
            totals[finding.kind] = totals.get(finding.kind, 0) + finding.count
        return dict(sorted(totals.items()))
