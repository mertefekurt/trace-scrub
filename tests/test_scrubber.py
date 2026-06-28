from trace_scrub.models import ScrubOptions
from trace_scrub.scrubber import scrub_text, scrub_value


def test_redacts_email_and_phone_in_text() -> None:
    result = scrub_text("Email ada@example.com or call (415) 555-0137.")

    assert result.value == "Email [REDACTED:email] or call [REDACTED:phone]."
    assert result.summary() == {"email": 1, "phone": 1}


def test_redacts_sensitive_keys_without_inspecting_value() -> None:
    result = scrub_value({"Authorization": "Bearer sk-testsecret12345678901234567890"})

    assert result.value == {"Authorization": "[REDACTED:sensitive_key]"}
    assert result.summary() == {"sensitive_key": 1}


def test_preserves_json_shape_for_nested_trace() -> None:
    trace = {
        "messages": [
            {"role": "user", "content": "my card is 4111 1111 1111 1111"},
            {"role": "tool", "content": {"ip": "192.168.0.42"}},
        ]
    }

    result = scrub_value(trace)

    assert result.value["messages"][0]["content"] == "my card is [REDACTED:credit_card]"
    assert result.value["messages"][1]["content"]["ip"] == "[REDACTED:ipv4]"
    assert result.summary() == {"credit_card": 1, "ipv4": 1}


def test_credit_card_rule_ignores_non_luhn_numbers() -> None:
    result = scrub_text("ticket 1234 5678 9012 3456 should stay")

    assert result.value == "ticket 1234 5678 9012 3456 should stay"
    assert result.findings == []


def test_keep_last_preserves_suffix_for_debugging() -> None:
    options = ScrubOptions(keep_last=4)
    result = scrub_text("key sk-abcdefghijklmnopqrstuvwxyz123456", options)

    assert result.value == "key [REDACTED:openai_key]3456"
    assert result.summary() == {"openai_key": 1}
