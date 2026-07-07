import json
from pathlib import Path

REPORT = Path("/app/report.json")

# Ground truth for environment/access.log, which is fixed at image build time.
# Kept here (in tests/, never agent-visible) rather than recomputed from
# /app/access.log, which the agent could modify.
EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _report():
    assert REPORT.exists(), "no /app/report.json found"
    with REPORT.open() as f:
        data = json.load(f)
    assert isinstance(data, dict), "report.json must contain a single JSON object"
    return data


def test_report_is_valid_json_object():
    """The agent produced a parseable JSON object at /app/report.json."""
    _report()


def test_total_requests():
    """total_requests matches the number of non-empty log lines."""
    assert _report()["total_requests"] == EXPECTED_TOTAL_REQUESTS


def test_unique_ips():
    """unique_ips matches the number of distinct client IPs."""
    assert _report()["unique_ips"] == EXPECTED_UNIQUE_IPS


def test_top_path():
    """top_path is the most frequently requested path."""
    assert _report()["top_path"] == EXPECTED_TOP_PATH
