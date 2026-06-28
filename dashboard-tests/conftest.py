"""Shared pytest fixtures for dashboard-tests.

SSoT (Single Source of Truth) for test data fetching:
- Single HTTP endpoint: http://127.0.0.1:18766 (gzip-capable, see serve-gzip.py)
- Single fixture per resource: avoids 11→N+ redundant fetches
- requests lib auto-decodes gzip via Accept-Encoding header
- Fallback to filesystem read if server down (graceful degradation)
"""
import json
import os
import re
from pathlib import Path

import pytest
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"
STATS_JSON = REPO_ROOT / "mycc-stats.json"
GZIP_SERVER = os.environ.get("DASHBOARD_GZIP_URL", "http://127.0.0.1:18766")


@pytest.fixture(scope="session")
def dashboard_html() -> str:
    """Raw dashboard.html text. Session scope = 1 disk read per test run."""
    assert DASHBOARD_HTML.exists(), f"dashboard.html missing at {DASHBOARD_HTML}"
    return DASHBOARD_HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def stats_json_local() -> dict:
    """mycc-stats.json from disk (always available, no network)."""
    assert STATS_JSON.exists(), f"mycc-stats.json missing at {STATS_JSON}"
    return json.loads(STATS_JSON.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def stats_json_live() -> dict | None:
    """mycc-stats.json fetched from gzip HTTP server.

    Returns None if server unreachable (graceful degradation — parity tests
    skip rather than fail, matching TestHttpServing pattern in anchor_contract).
    """
    try:
        r = requests.get(f"{GZIP_SERVER}/mycc-stats.json", timeout=3)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as e:
        pytest.skip(f"gzip server unreachable: {e}")
        return None  # unreachable, pytest.skip raises


@pytest.fixture(scope="session")
def fallback_counts(dashboard_html: str) -> dict:
    """Parse FALLBACK_COUNTS const block from dashboard.html.

    FALLBACK 块是 JS object literal 风格: 每行 4 个 `key: value,` pair,
    不带尾引号. 解析策略: 移除换行/空白, 按 `,` 切 token, 再按 `:` 切 key/value.

    Returns dict of key→int (or str for non-numeric). Raises if block not found
    (dashboard refactor breakage should fail loudly, not silently fall through).
    """
    m = re.search(
        r"const\s+FALLBACK_COUNTS\s*=\s*\{([^}]+)\}",
        dashboard_html,
        re.DOTALL,
    )
    assert m, "FALLBACK_COUNTS block not found in dashboard.html — refactor broke contract"
    block = m.group(1)
    # 规范化: 移除 JS 注释行 + 压缩空白
    cleaned = re.sub(r"//[^\n]*", "", block)
    cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
    out = {}
    # 按 `,` 切 token (每行 4 对, 尾行无逗号)
    for tok in cleaned.split(","):
        tok = tok.strip()
        if not tok:
            continue
        km = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.+)", tok, re.DOTALL)
        if not km:
            continue
        key, val = km.group(1), km.group(2).strip()
        try:
            out[key] = int(val)
        except ValueError:
            # 非数字值 (string 等) 保留为 str
            out[key] = val.strip("'\"")
    assert len(out) >= 15, (
        f"FALLBACK_COUNTS 仅解析出 {len(out)} 个字段 (期望 ≥15), "
        f"解析器可能漏行. 字段: {list(out.keys())}"
    )
    return out


@pytest.fixture(scope="session")
def fallback_version(dashboard_html: str) -> dict:
    """Parse FALLBACK_VERSION const block from dashboard.html.

    Returns dict of key→str. Used to detect version-string drift like
    '2.1.195' vs '2.1.195 (Claude Code)' (parens suffix pollution).
    """
    m = re.search(
        r"const\s+FALLBACK_VERSION\s*=\s*\{([^}]+)\}",
        dashboard_html,
        re.DOTALL,
    )
    assert m, "FALLBACK_VERSION block not found in dashboard.html"
    out = {}
    for line in m.group(1).splitlines():
        line = line.strip().rstrip(",").rstrip(";")
        km = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*['\"]([^'\"]+)['\"]", line)
        if km:
            out[km.group(1)] = km.group(2)
    return out