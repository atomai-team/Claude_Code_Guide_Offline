"""test_navigation_completeness.py · 导航契约 v1.0

PM 0.72 P1 推荐: 14+1 nav-link href ↔ 滚动目标 (section 或 div) 一一对应.
补 test_dashboard_self_audit.py section_index fixture 漏 <div class="card" id="s-catalog">
的盲区 (s-catalog 是 nav-link 目标但不是 <section>).

SSoT (实测 2026-06-29):
- 15 nav-link href (top + 13 section + 1 div)
- 14 <section id="...">
- 1 <div class="card" id="s-catalog"> (全量能力目录卡片)

设计原则 (反讽 R1-R4):
- R1 显式报问题: nav 死链 → hard fail, 顺序乱 → warn
- R2 baseline 不固化: 数字阈值从实测, 不拍脑袋
- R3 不猜死路径: 用实测数据, 不复用接力包二手转述
- R4 严重缺陷不软化: 死链必须 fail, 不能 xfail 静默放过
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


# ─────────────────────────────────────────────────────────────────
# Fixtures (复用 conftest.py 的 dashboard_html, 增强 nav_index)
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def nav_links(dashboard_html: str) -> list[str]:
    """所有 nav-link 的 href target (去 # 前缀).

    例: '<a href="#s-health" class="nav-link">...</a>' → 's-health'
    """
    hrefs = re.findall(r'<a\s+href="#([^"]+)"\s+class="nav-link"', dashboard_html)
    return hrefs


@pytest.fixture(scope="session")
def scroll_targets(dashboard_html: str) -> dict[str, str]:
    """所有可滚动目标 id → 标签类型 (section / div-card).

    包含:
    - <section id="X"> (主滚动目标)
    - <div class="card" id="X"> (大块卡片, 如 s-catalog 全量目录)
    - <aside class="side-nav" id="X"> (侧栏自身, 也算导航锚点)

    排除: 内部 UI 组件 div (cmdk*/detail*/agentTags*/catalogChips 等),
    这些是 JS 动态插入/隐藏的二级目标, 不应被 nav-link 直接跳转.
    """
    targets = {}
    # <section id="...">
    for m in re.finditer(r'<section\b[^>]*\bid="([^"]+)"', dashboard_html, re.IGNORECASE):
        targets[m.group(1)] = "section"
    # <div class="card" id="..."> (大块卡片, 如 s-catalog)
    for m in re.finditer(
        r'<div\b[^>]*\bclass="[^"]*\bcard\b[^"]*"[^>]*\bid="([^"]+)"',
        dashboard_html,
        re.IGNORECASE,
    ):
        if m.group(1) not in targets:
            targets[m.group(1)] = "div-card"
    # <aside id="..."> (side-nav 自身)
    for m in re.finditer(r'<aside\b[^>]*\bid="([^"]+)"', dashboard_html, re.IGNORECASE):
        if m.group(1) not in targets:
            targets[m.group(1)] = "aside"
    return targets


# ─────────────────────────────────────────────────────────────────
# TestNavigationCompleteness: nav-link ↔ scroll target 一一对应
# ─────────────────────────────────────────────────────────────────

class TestNavigationCompleteness:
    """用户每天点的 15 个 nav-link 必须都能跳到真实存在的目标.

    Bug 实证 (PM 0.72): section_index fixture 漏 <div id="s-catalog">, 锚点
    测试天然漏 catalog 页; 但 nav-link '#s-catalog' 确实存在, 用户点会跳到
    <div>. 本测试强制 nav-link ↔ target 完整映射.
    """

    def test_nav_link_count_in_range(self, nav_links):
        """nav-link 数量应在 13-24 之间 (含 s-evolution D1 2026-06-30)."""
        n = len(nav_links)
        assert 13 <= n <= 24, (
            f"nav-link 数量 {n} 超出预期 [13, 24], 需重新审计 dashboard 导航"
        )

    def test_nav_link_unique(self, nav_links):
        """nav-link href 不重复."""
        assert len(nav_links) == len(set(nav_links)), (
            f"nav-link href 重复: {[h for h in nav_links if nav_links.count(h) > 1]}"
        )

    @pytest.mark.parametrize("href", [
        "top", "s-overview", "s-entry", "s-commands", "s-commands-deep",
        "s-agents", "s-workflows", "s-docs", "s-github", "s-knowledge",
        "s-data", "s-catalog", "s-health", "s-brains", "s-architecture",
    ])
    def test_nav_link_target_exists(self, href, scroll_targets):
        """每个 nav-link href 必须对应一个真实存在的可滚动目标 (section 或 div)."""
        assert href in scroll_targets, (
            f"nav-link #{href} 指向不存在的目标. "
            f"已知目标: {sorted(scroll_targets.keys())[:10]}..."
        )

    def test_s_catalog_is_div_card_not_section(self, scroll_targets):
        """反讽 R1 实证: s-catalog 是 <div class="card">, 不是 <section>.

        这是 PM 0.72 报的 fixture 盲区根源. section_index fixture 只抓
        <section>, 漏 <div id="s-catalog">, 导致锚点测试天然漏 catalog 页.
        本测试固化这个事实, 防止 dashboard 重构时把 s-catalog 改回 <section>
        (会破坏样式) 或忘了保留 id (会让 nav-link 死链).
        """
        assert "s-catalog" in scroll_targets, "s-catalog 目标丢失"
        assert scroll_targets["s-catalog"] == "div-card", (
            f"s-catalog 应该是 <div class='card'>, 实测 <{scroll_targets['s-catalog']}>. "
            f"若 dashboard 重构成 <section>, 需同步更新 section_index fixture."
        )

    def test_all_scroll_targets_reachable_via_nav(
        self, nav_links, scroll_targets
    ):
        """每个 scroll target 都应有 ≥1 个 nav-link 指向 (主导航 100% 覆盖).

        例外: aside (side-nav 自身) 是 nav 的容器, 不需指向自身.
        """
        reachable = set(nav_links)
        unreachable_targets = {
            sid: tag for sid, tag in scroll_targets.items()
            if sid not in reachable and tag != "aside"
        }
        assert not unreachable_targets, (
            f"scroll target (section/div-card) 无 nav-link 指向: "
            f"{unreachable_targets}. 用户的 nav 死了 = 跳不过去."
        )


# ─────────────────────────────────────────────────────────────────
# TestScrollSpyContract: scroll-spy JS 高亮行为契约
# ─────────────────────────────────────────────────────────────────

class TestScrollSpyContract:
    """JS scroll-spy 必须高亮当前 section 对应的 nav-link.

    Bug 实证 (PM 0.72): scroll-spy 行为无任何契约测试, 用户每天点的功能.
    本测试只验证 JS 代码存在 + 关键 hook 注册, 不模拟浏览器 (Playwright
    MCP 不可用时由 task-closer 加 Playwright 实测).
    """

    def test_scrollspy_handler_exists(self, app_js: str):
        """JS 滚动监听 + nav-link 高亮逻辑必须存在 (P3-1: 改读 app_js)."""
        assert "IntersectionObserver" in app_js, (
            "scroll-spy 用 IntersectionObserver, 代码缺失 = 整页导航高亮失效"
        )
        assert "nav-link" in app_js and "classList.add('active')" in app_js, (
            "scroll-spy 添加 .active 类的逻辑缺失"
        )

    def test_scrollspy_selects_correct_link(self, app_js: str):
        """scroll-spy 必须用 '.side-nav .nav-link' 选择器 (P3-1: 改读 app_js)."""
        assert "'.side-nav .nav-link'" in app_js or '".side-nav .nav-link"' in app_js, (
            "scroll-spy 应限定在 .side-nav 内的 .nav-link, 避免误命中 cmdK/footer 等"
        )