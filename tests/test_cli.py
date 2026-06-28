import json

from trace_scrub.cli import main


def test_cli_writes_redacted_json_and_report(tmp_path) -> None:
    source = tmp_path / "trace.json"
    output = tmp_path / "clean.json"
    report = tmp_path / "report.txt"
    source.write_text(json.dumps({"user": "sam@example.com", "token": "abc123"}), encoding="utf-8")

    status = main([str(source), "-o", str(output), "--report", str(report)])

    assert status == 0
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "user": "[REDACTED:email]",
        "token": "[REDACTED:sensitive_key]",
    }
    assert "email: 1 match(es)" in report.read_text(encoding="utf-8")
    assert "sensitive_key: 1 match(es)" in report.read_text(encoding="utf-8")


def test_cli_can_fail_when_findings_exist(tmp_path) -> None:
    source = tmp_path / "prompt.txt"
    source.write_text("contact root@example.com", encoding="utf-8")

    status = main([str(source), "--fail-on-findings"])

    assert status == 2
