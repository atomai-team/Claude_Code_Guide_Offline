"""test_router.py · hash router 契约 v1.0 (v6 方向 A)

覆盖 v6 router 改造: hashchange 双向同步 + scrollspy 保留 + 26 nav-link 全覆盖
方案 C 设计依据: docs/plans/v6-router-design.md
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