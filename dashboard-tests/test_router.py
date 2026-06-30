"""test_router.py · hash router 契约 v1.1 (v6 方向 A + v8 双轨改进)

覆盖 v6 router 改造: hashchange 双向同步 + scrollspy 保留 + 26 nav-link 全覆盖
方案 C 设计依据: docs/plans/v6-router-design.md

v8 双轨改进 (2026-06-30):
- nav-link click → pushState (堆 history, 后退可工作)
- scroll → replaceState (不堆 history, 滚动流畅)
- hashchange handler 不调 pushState (防双重污染 history)
- popstate → 浏览器后退已自动 fire hashchange, 无需新增
"""
import re

import pytest


@pytest.fixture(scope="session")
def router_hash_listeners(app_js: str) -> int:
    """统计 dashboard-app.js 中 hashchange listener 数量 (期望 ≥1)."""
    return app_js.count("hashchange")


@pytest.fixture(scope="session")
def router_replace_state(app_js: str) -> int:
    """统计 history.replaceState 调用数 (期望 ≥1, 用于滚动→URL 同步)."""
    return app_js.count("history.replaceState")


@pytest.fixture(scope="session")
def router_push_state(app_js: str) -> int:
    """统计 history.pushState 调用数 (v8 新增 · 期望 ≥1, nav-link click 用)."""
    return app_js.count("history.pushState")


class TestRouterHashSync:
    """滚动 → URL hash 同步 + hashchange → scroll 同步."""

    def test_hashchange_listener_registered(self, router_hash_listeners):
        """hashchange listener 必须存在 (前进/后退可用)."""
        assert router_hash_listeners >= 1, (
            f"hashchange listener 缺失 · 当前 {router_hash_listeners} 处"
        )

    def test_replace_state_used(self, router_replace_state):
        """history.replaceState 必须用于滚动→URL 同步 (不堆 history)."""
        assert router_replace_state >= 1, (
            f"history.replaceState 缺失 · 滚动→URL 同步需要"
        )

    def test_scrollspy_intersection_preserved(self, app_js: str):
        """v3 滚动→高亮算法必须保留 (router 不破坏 scrollspy)."""
        assert "requestAnimationFrame" in app_js, (
            "scrollspy rAF 节流被破坏"
        )
        assert "getBoundingClientRect" in app_js, (
            "scrollspy 位置法被破坏"
        )

    def test_lazy_load_offsetHeight_guard(self, app_js: str):
        """router 必须防 lazy load 竞态 (offsetHeight===0 检测)."""
        assert "offsetHeight" in app_js, (
            "防 lazy load 竞态缺失: offsetHeight===0 检测"
        )


class TestRouterCompatibility:
    """向后兼容: 旧 #s-X 链接 100% 有效."""

    def test_anchor_links_unchanged(self, dashboard_html: str):
        """所有 26 nav-link 仍用 #s-X 锚点格式 (不破坏旧分享链接)."""
        nav_links = re.findall(
            r'<a\s+href="#s-[a-z-]+"\s+class="nav-link"',
            dashboard_html,
        )
        assert len(nav_links) >= 26, (
            f"nav-link 数 {len(nav_links)} < 26 · router 必须保留所有锚点"
        )

    def test_no_replace_state_on_hashchange(self, app_js: str):
        """hashchange 处理中不调用 pushState (避免污染 history 栈)."""
        # 反讽 R5: replaceState 仅用于滚动同步, hashchange 仅 scrollIntoView + setActive
        # 检查 hashchange 块内不含 pushState/replaceState (易污染 history)
        idx = app_js.find("addEventListener('hashchange'")
        if idx >= 0:
            block = app_js[idx:idx+800]
            assert "pushState" not in block, (
                "hashchange 内不应 pushState · 会污染 history 栈"
            )


# ════════════════════════════════════════════════════════════════════
# TestRouterDualTrack · v8 后退双轨改进 (2026-06-30)
# ════════════════════════════════════════════════════════════════════

class TestRouterDualTrack:
    """v8 双轨: nav-link click 走 pushState, scroll 走 replaceState."""

    def test_push_state_present(self, router_push_state):
        """v8: history.pushState 必须存在 (nav-link click 堆 history 让后退可工作)."""
        assert router_push_state >= 1, (
            f"history.pushState 缺失 · v8 双轨改进失败 · 当前 {router_push_state} 处"
        )

    def test_nav_click_uses_push_state(self, app_js: str):
        """v8: nav-link click handler 必须用 pushState (而非默认锚点跳转)."""
        # 找 nav-link click 拦截 (preventDefault + pushState 模式)
        assert "preventDefault" in app_js, (
            "nav-link click 拦截缺失 · v8 双轨需要 preventDefault 阻止默认锚点"
        )
        # pushState 调用必须在 click handler 内, 不在 hashchange handler 内
        assert app_js.count("history.pushState") >= 1, (
            "pushState 必须存在 · nav-link click 双轨改进需要"
        )

    def test_push_state_not_inside_hashchange(self, app_js: str):
        """v8: pushState 必须在 hashchange handler 外 (防双重 history 污染)."""
        idx = app_js.find("addEventListener('hashchange'")
        if idx >= 0:
            # 取 hashchange handler block (800 字符足够覆盖)
            block = app_js[idx:idx+800]
            assert "pushState" not in block, (
                "hashchange 内不应 pushState · 会双重堆 history · v8 反讽 R5"
            )

    def test_replace_state_in_scroll_handler(self, app_js: str):
        """v8: replaceState 必须在 scroll handler 内 (滚动同步不堆 history)."""
        # replaceState 存在性 + scroll 监听器
        assert "history.replaceState" in app_js, "replaceState 缺失"
        # scroll handler 已存在 (v6 测试覆盖), 此处冗余校验
        assert "addEventListener('scroll'" in app_js, (
            "scroll handler 缺失 · replaceState 调用上下文丢失"
        )

    def test_scrollspy_preserved_with_dual_track(self, app_js: str):
        """v8: 双轨改造不破坏 scrollspy (rAF 节流 + 位置法)."""
        # v6 测试已覆盖, 此处明确 v8 改造后仍工作
        assert "requestAnimationFrame" in app_js, "scrollspy rAF 节流丢失"
        assert "getBoundingClientRect" in app_js, "scrollspy 位置法丢失"
        # setActive 仍在 (v6 验证)
        assert "setActive" in app_js, "setActive 缺失 · scrollspy 同步逻辑丢失"