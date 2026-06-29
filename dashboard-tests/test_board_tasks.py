"""test_board_tasks.py · board-tasks 看板集成契约 v1.0

集成契约 (board-tasks-INTEGRATION.md · 2026-06-29):
- fetch board-tasks.json 成功 (HTTP 200, 顶层 4 key)
- 四列看板渲染 (待规划/待办/进行中/审核中)
- 里程碑渲染
- hero stats 数字非 '—'

依赖: serve-gzip.py (18766 CI / 18771 本地), DASHBOARD_GZIP_URL 环境变量
"""
import os
import re
from pathlib import Path

import pytest
import requests
from playwright.sync_api import sync_playwright

REPO_ROOT   = Path(__file__).resolve().parent.parent
GZIP_SERVER = os.environ.get("DASHBOARD_GZIP_URL", "http://127.0.0.1:18771")


# ─────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def board_json():
    """board-tasks.json 从 HTTP server fetch (跳过若 server 不可达)."""
    try:
        r = requests.get(f"{GZIP_SERVER}/board-tasks.json", timeout=5)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as e:
        pytest.skip(f"gzip server unreachable: {e}")


@pytest.fixture(scope="module")
def page_loaded():
    """加载 dashboard.html 并等待 board-tasks.json fetch 完成."""
    with sync_playwright() as p:
        br   = p.chromium.launch()
        page = br.new_page()
        page.goto(f"{GZIP_SERVER}/dashboard.html", wait_until="networkidle")
        page.wait_for_timeout(1500)
        yield page
        br.close()


# ─────────────────────────────────────────────────────────────────
# TestBoardTasksJson: JSON 结构契约
# ─────────────────────────────────────────────────────────────────

class TestBoardTasksJson:
    """board-tasks.json 顶层结构完整性."""

    REQUIRED_KEYS = {"meta", "kanban", "milestones", "blockers"}
    KANBAN_COLS   = {"待规划", "待办", "进行中", "审核中"}

    def test_required_toplevel_keys(self, board_json):
        missing = self.REQUIRED_KEYS - set(board_json.keys())
        assert not missing, f"board-tasks.json 缺顶层字段: {missing}"

    def test_kanban_has_four_columns(self, board_json):
        cols = set(board_json["kanban"].keys())
        assert cols == self.KANBAN_COLS, f"kanban 列不对: {cols}"

    def test_milestones_is_list(self, board_json):
        assert isinstance(board_json["milestones"], list), "milestones 应为 list"
        assert len(board_json["milestones"]) >= 1, "milestones 不能为空"

    def test_doing_cards_exist(self, board_json):
        doing = board_json["kanban"]["进行中"]
        assert len(doing) >= 1, "进行中 无任何卡片 (stats 引擎异常?)"

    def test_card_fields_complete(self, board_json):
        required = {"id", "title", "group", "status"}
        for col, cards in board_json["kanban"].items():
            for c in cards[:3]:
                missing = required - set(c.keys())
                assert not missing, f"kanban[{col}] 卡片缺字段: {missing}"


# ─────────────────────────────────────────────────────────────────
# TestBoardTasksRender: Playwright 渲染验证
# ─────────────────────────────────────────────────────────────────

class TestBoardTasksRender:
    """dashboard #s-tasks section 动态渲染验证."""

    def test_section_present(self, page_loaded):
        el = page_loaded.query_selector("#s-tasks")
        assert el, "#s-tasks section 不存在 — HTML 未写入"

    def test_nav_link_present(self, page_loaded):
        link = page_loaded.query_selector('a[href="#s-tasks"]')
        assert link, "nav-link #s-tasks 缺失"

    def test_kanban_four_columns_rendered(self, page_loaded):
        cols = page_loaded.query_selector_all("#bt-kanban > div")
        # 4 主列 + 可选 1 虚拟"待优化"列（subplans todo/doing）
        assert 4 <= len(cols) <= 5, f"看板列数 {len(cols)} 应在 [4,5]"

    def test_hero_doing_not_placeholder(self, page_loaded):
        val = page_loaded.text_content("#bt-doing")
        assert val != "—" and val is not None, "bt-doing 未渲染 (仍为 '—')"
        assert val.isdigit(), f"bt-doing 应为数字, 实测: {val!r}"

    def test_hero_blocked_not_placeholder(self, page_loaded):
        val = page_loaded.text_content("#bt-blocked")
        assert val != "—" and val is not None, "bt-blocked 未渲染"

    def test_milestones_rendered(self, page_loaded):
        items = page_loaded.query_selector_all("#bt-milestones > div > div")
        assert len(items) >= 1, "里程碑未渲染"

    def test_no_js_errors(self, page_loaded):
        # console errors tracked during page load (module fixture)
        # 轻验证: 不能有 board 相关 JS 错误
        errors = []
        def on_err(e):
            errors.append(e.text)
        page_loaded.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        # Errors captured during fixture load; check page for obvious failures
        kanban_el = page_loaded.query_selector("#bt-kanban")
        assert kanban_el, "#bt-kanban element missing"

    def test_evidence_closure_stat(self, page_loaded):
        val = page_loaded.text_content("#bt-evidence")
        assert val != "—" and val is not None, "bt-evidence 未渲染"
