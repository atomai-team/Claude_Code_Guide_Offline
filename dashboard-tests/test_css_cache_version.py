"""test_css_cache_version.py · CSS 缓存版本号守门 (2026-06-30, web-perf HIGH + 接力包遗留隐患)。

防 "改了 design-system/*.css 但忘更新 dashboard.html 的 ?v= 版本号" → 浏览器缓存
serve 旧样式。这是 dashboard FALLBACK/freshness 同类的"手维护值易漏"问题, 用 git
最后提交日期对比版本号守门 (git 历史在 CI 可靠, 不依赖 mtime)。

设计哲学: 与 test_stats_parity 一致——能自动的自动(test 守门), 该人工的人工(改 CSS
时手动 bump 版本号), test 在忘 bump 时 fail 提醒。
"""
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


def _is_shallow():
    """shallow clone (CI checkout fetch-depth:1) 下 git log -- <file> 失真:
    只返回 shallow 边界 commit 而非真正改该文件的 commit → 版本号守门会误判。"""
    r = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    return r.stdout.strip() == "true"


def _css_refs():
    """抓 dashboard.html 里 design-system/*.css?v=YYYYMMDD 引用 → [(fname, ver), ...]。"""
    html = DASHBOARD_HTML.read_text()
    return re.findall(r'design-system/([^"?]+\.css)\?v=(\d+)', html)


def _git_last_date(relpath):
    """该文件 git 最后提交日期 (YYYYMMDD int); 无历史返回 None。"""
    r = subprocess.run(
        ["git", "log", "-1", "--format=%cd", "--date=format:%Y%m%d", "--", relpath],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    out = r.stdout.strip()
    return int(out) if out.isdigit() else None


def test_css_refs_present():
    """dashboard.html 应有带版本号的 CSS 引用 (回归基线)。"""
    assert _css_refs(), "dashboard.html 应有 design-system/*.css?v= 引用"


def test_css_version_not_stale():
    """每个 CSS ?v= 版本号必须 >= 该文件 git 最后提交日期 (防忘 bump→缓存 serve 旧样式)。

    ⚠️ shallow clone (CI fetch-depth:1) 下 git log -- <file> 返回 shallow 边界 commit
    而非真正改该文件的 commit → 误判, 故 skip。本地完整克隆守门有效。
    """
    if _is_shallow():
        pytest.skip("shallow clone: git log -- <file> 不可靠, CSS 版本号守门仅本地完整克隆生效")
    stale = []
    for fname, ver in _css_refs():
        git_date = _git_last_date(f"design-system/{fname}")
        if git_date and int(ver) < git_date:
            stale.append(
                f"{fname}: ?v={ver} < git 最后改={git_date} "
                f"(改了 CSS 忘 bump 版本号 → 浏览器缓存会 serve 旧样式)"
            )
    assert not stale, "CSS 缓存版本号过期:\n  " + "\n  ".join(stale)
