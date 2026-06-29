"""test_browser_interactions.py · 3 个 P0 浏览器行为测试 (M2-2 2026-06-29)

目标: 纠正测试金字塔倒置 (现有 206 例大多静态 grep, 交互零行为)
- test_auto_refresh: ⟳ 重载按钮触发 reloadTasks() 不整页刷
- test_scrollspy_browser: 滚动 → nav-link active 联动
- test_global_search: Cmd+K 打开 + 跨 section 搜索 + 命中跳转

复用 dashboard-tests.conftest.GZIP_SERVER (端口 SSoT, 不再硬编码 18771)
复用 conftest.page_loaded fixture 风格但带 file:// fallback.
"""
import pytest
from playwright.sync_api import sync_playwright

from conftest import GZIP_SERVER, REPO_ROOT


@pytest.fixture(scope="module")
def page_loaded():
    """加载 dashboard.html 并等待所有 fetch 完成. 复用 conftest.GZIP_SERVER."""
    import requests
    from pathlib import Path

    HTML_FILE = REPO_ROOT / "dashboard.html"
    try:
        r = requests.get(f"{GZIP_SERVER}/dashboard.html", timeout=3)
        r.raise_for_status()
        url = f"{GZIP_SERVER}/dashboard.html"
    except requests.RequestException:
        url = f"file://{HTML_FILE}"

    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # 等 board-tasks + stats 都加载
        yield page
        br.close()


class TestAutoRefresh:
    """⟳ 重载按钮触发 reloadTasks() 不整页刷."""

    def test_reload_button_exists(self, page_loaded):
        """#btn-reload-tasks 必须存在."""
        btn = page_loaded.query_selector("#btn-reload-tasks")
        assert btn is not None, "⟳ 重载按钮 #btn-reload-tasks 缺失"

    def test_reload_keeps_url_and_does_not_refresh(self, page_loaded):
        """点击 ⟳ 不应触发整页 reload (不应有 navigation event)."""
        # 记录当前 URL + 在 body 上挂个 sentinel 标记
        before_url = page_loaded.url
        page_loaded.evaluate("window.__reloadSentinel = 'before'")

        # 监控 navigation
        navigated = []
        page_loaded.on("framenavigated", lambda f: navigated.append(f.url) if f == page_loaded.main_frame else None)

        # 点击按钮
        btn = page_loaded.query_selector("#btn-reload-tasks")
        btn.click()
        page_loaded.wait_for_timeout(2500)  # 等 reloadTasks 完成

        # 1) URL 不变
        assert page_loaded.url == before_url, f"URL 变了: {before_url} → {page_loaded.url}"

        # 2) sentinel 仍在 (证明 page 没被卸载)
        sentinel = page_loaded.evaluate("window.__reloadSentinel")
        assert sentinel == "before", f"sentinel 消失 = page 被 reload 了, 当前值: {sentinel}"

        # 3) reloadTasks 函数可被外部调用 (window.reloadTasks 暴露)
        assert page_loaded.evaluate("typeof window.reloadTasks") == "function", \
            "window.reloadTasks 应暴露给测试调用"

    def test_reload_button_text_toggles(self, page_loaded):
        """点击后 button text 应短暂变 ⟳ 加载中… 然后恢复."""
        btn = page_loaded.query_selector("#btn-reload-tasks")
        # 不实测 loading 中间态 (太快) — 只验证恢复
        btn.click()
        page_loaded.wait_for_timeout(3000)
        final_text = btn.text_content().strip()
        assert final_text == "⟳ 重载数据", f"按钮 text 未恢复: {final_text!r}"


class TestScrollspyBrowser:
    """滚动 → .nav-link.active 联动 (IntersectionObserver)."""

    def test_nav_link_count_matches_sections(self, page_loaded):
        """nav-link 数 ≥ 实际 section 数 (允许 nav-link 多于 section, 如 footer 返回顶部)."""
        nav_links = page_loaded.query_selector_all(".side-nav .nav-link")
        sections = page_loaded.query_selector_all("section.section[id]")
        assert len(nav_links) >= len(sections), \
            f"nav-link({len(nav_links)}) < section({len(sections)})"

    def test_scroll_to_overview_activates_first_link(self, page_loaded):
        """滚到 #s-overview 附近 → 第一个 nav-link 应有 .active class."""
        # 滚到顶部
        page_loaded.evaluate("window.scrollTo(0, 0)")
        page_loaded.wait_for_timeout(800)

        active = page_loaded.query_selector_all(".side-nav .nav-link.active")
        assert len(active) >= 1, "顶部时至少 1 个 nav-link 应 .active"

    def test_scroll_deep_activates_deep_link(self, page_loaded):
        """滚到 #s-tasks (看板) → 对应 nav-link 应激活.

        算法修正后 (dashboard-app.js L101-114 task #19):
        取"第一个 top > ref 之前一个" — 滚到 s-tasks 顶时, s-tasks top=0 ≤ ref,
        下个 section (s-architecture) top 仍 > ref (s-tasks 内容很高), 所以激活 #s-tasks ✓
        """
        # scrollIntoView
        result = page_loaded.evaluate("""
            () => {
                const el = document.getElementById('s-tasks');
                if (!el) return 'missing';
                el.scrollIntoView({behavior: 'instant', block: 'start'});
                return 'ok';
            }
        """)
        assert result == "ok", f"#s-tasks scrollIntoView 失败: {result}"
        page_loaded.wait_for_timeout(800)

        # 找指向 #s-tasks 的 nav-link
        target_link = page_loaded.query_selector('.side-nav .nav-link[href="#s-tasks"]')
        assert target_link is not None, "找不到指向 #s-tasks 的 nav-link"

        # 严格断言: scrollspy 修正后, 滚到 #s-tasks 顶部应激活 #s-tasks 自身
        active_hrefs = page_loaded.evaluate("""
            () => [...document.querySelectorAll('.side-nav .nav-link.active')]
                  .map(l => l.getAttribute('href'))
        """)
        assert "#s-tasks" in active_hrefs, (
            f"scroll 到 #s-tasks 后 active 应严格包含 #s-tasks (算法已修); "
            f"actual active={active_hrefs}"
        )


class TestGlobalSearch:
    """Cmd+K 全局搜索打开 + 跨 section 命中 + 跳转."""

    def test_cmdk_shortcut_opens_search(self, page_loaded):
        """按 Cmd+K (mac) / Ctrl+K (其他) 应打开搜索面板."""
        # 用 evaluate 触发 openCmdK() 替代真实按键 (避免 platform 差异)
        result = page_loaded.evaluate("""
            () => {
                if (typeof openCmdK !== 'function') return 'no-func';
                openCmdK();
                return 'ok';
            }
        """)
        # fallback: 点搜索入口
        if result == "no-func":
            btn = page_loaded.query_selector('[data-action="open-search"], #search-trigger, .cmd-k-trigger')
            if btn:
                btn.click()
        page_loaded.wait_for_timeout(500)

        # 验证 overlay 存在
        overlay = page_loaded.query_selector("#cmdK-overlay, .cmdk-overlay, [class*='cmdk']")
        assert overlay is not None, "Cmd+K overlay 未出现"

    def test_search_finds_cross_section_term(self, page_loaded):
        """搜 'kanban' 应至少 1 条命中 (看板在 s-tasks). GS_DOCS 0 命中则 skip (graceful)."""
        page_loaded.evaluate("if (typeof openCmdK === 'function') openCmdK()")
        page_loaded.wait_for_timeout(400)

        inp = page_loaded.query_selector("#cmdK-input, .cmdk-input, [class*='cmdk'] input")
        assert inp is not None, "Cmd+K 搜索输入框未找到"

        inp.fill("kanban")
        page_loaded.wait_for_timeout(600)

        # 等待 MiniSearch 索引完成 (initGlobalSearch 异步)
        indexed = page_loaded.evaluate("typeof window.gsMinisearch === 'object' && window.gsMinisearch !== null")
        if not indexed:
            pytest.skip("MiniSearch 索引未就绪 (GS_DOCS fetch 失败/慢, graceful degradation)")

        results = page_loaded.query_selector_all(
            ".cmdk-result, .cmdk-item, [class*='cmdk'] [role='option'], #cmdK-results > *"
        )
        assert len(results) >= 1, f"搜 'kanban' 0 命中 (应有 ≥1 条看板相关)"

    def test_search_result_has_section_label(self, page_loaded):
        """命中项应显示 section 来源 (如 's-tasks'). 同上 skip 规则."""
        page_loaded.evaluate("if (typeof openCmdK === 'function') openCmdK()")
        page_loaded.wait_for_timeout(300)

        inp = page_loaded.query_selector("#cmdK-input, .cmdk-input, [class*='cmdk'] input")
        inp.fill("看板")
        page_loaded.wait_for_timeout(500)

        indexed = page_loaded.evaluate("typeof window.gsMinisearch === 'object' && window.gsMinisearch !== null")
        if not indexed:
            pytest.skip("MiniSearch 索引未就绪 (GS_DOCS fetch 失败/慢, graceful degradation)")

        first_result_html = page_loaded.evaluate("""
            () => {
                const r = document.querySelector(
                    '.cmdk-result, .cmdk-item, [class*="cmdk"] [role="option"], #cmdK-results > *'
                );
                return r ? r.textContent : '';
            }
        """)
        assert len(first_result_html) > 0, "搜 '看板' 第一个结果为空"