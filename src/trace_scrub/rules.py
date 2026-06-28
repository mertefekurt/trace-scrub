from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    kind: str
    pattern: re.Pattern[str]
    validator: Callable[[str], bool] | None = None


def looks_like_credit_card(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    if not 13 <= len(digits) <= 19:
        return False

    total = 0
    reverse_digits = list(map(int, reversed(digits)))
    for index, digit in enumerate(reverse_digits):
        if index % 2:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


RULES: tuple[Rule, ...] = (
    Rule("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    Rule("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    Rule(
        "jwt",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    ),
    Rule(
        "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ),
    Rule(
        "phone",
        re.compile(r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\w)"),
    ),
    Rule("ipv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    Rule(
        "credit_card",
        re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        validator=looks_like_credit_card,
    ),
)
