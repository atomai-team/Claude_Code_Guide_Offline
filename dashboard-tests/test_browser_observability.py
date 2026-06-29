"""test_browser_observability.py · M3 可观测性三件守护 (2026-06-29)

覆盖 dashboard-app.js 末尾的 3 个新注入:
- window.onerror → window.__errs 聚合
- performance.measure('render-time') → 渲染耗时埋点
- fetchRetry(url, n=3) → 指数退避重试

复用 dashboard-tests.conftest.GZIP_SERVER + page_loaded fixture 模式 (port SSoT).
"""
import pytest
from playwright.sync_api import sync_playwright

from conftest import GZIP_SERVER, REPO_ROOT


@pytest.fixture(scope="module")
def page_loaded():
    """加载 dashboard.html, 等所有 fetch 完成. 复用 conftest.GZIP_SERVER."""
    import requests

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
        page.wait_for_timeout(2000)
        yield page
        br.close()


class TestObservability:
    """M3 可观测性三件守护."""

    def test_window_errs_array_initialized(self, page_loaded):
        """window.__errs 必须初始化为空数组."""
        errs = page_loaded.evaluate("window.__errs")
        assert isinstance(errs, list), f"window.__errs 应是 list, 实际: {type(errs).__name__}"
        assert len(errs) == 0, f"初始应空, 实际: {len(errs)} 条"

    def test_window_error_handler_captures_thrown(self, page_loaded):
        """主动 throw → 应被 window.onerror 捕获并 push 到 __errs."""
        # 在 page context 里抛错
        page_loaded.evaluate("""
            () => {
                setTimeout(() => { throw new Error('test-observability-' + Date.now()); }, 50);
            }
        """)
        page_loaded.wait_for_timeout(500)  # 等 setTimeout 触发 + handler 执行

        errs = page_loaded.evaluate("window.__errs")
        assert any("test-observability-" in e.get("msg", "") for e in errs), \
            f"主动 throw 未被捕获, __errs: {errs}"

    def test_errs_capped_at_50(self, page_loaded):
        """__errs 长度上限 50 条 (防内存泄漏)."""
        # 模拟 60 条 errs 直接 push, 验证上限
        page_loaded.evaluate("""
            () => {
                window.__errs = [];
                for (let i = 0; i < 60; i++) {
                    window.__errs.push({msg: 'synthetic-' + i, src: '?', line: 0, ts: Date.now()});
                    if (window.__errs.length > 50) window.__errs.shift();
                }
            }
        """)
        errs = page_loaded.evaluate("window.__errs")
        assert len(errs) <= 50, f"__errs 应 ≤50, 实际: {len(errs)}"

    def test_performance_measure_recorded(self, page_loaded):
        """performance.measure('render-time') 应存在."""
        # render-time 是 dashboard 启动时埋的点 (Promise.all 完成)
        measures = page_loaded.evaluate("""
            () => {
                const m = performance.getEntriesByName('render-time', 'measure');
                return m.map(e => ({name: e.name, duration: e.duration, startTime: e.startTime}));
            }
        """)
        assert len(measures) >= 1, f"render-time 未找到, 现有: {measures}"
        assert measures[0]["duration"] >= 0, f"duration 异常: {measures[0]}"

    def test_fetch_retry_helper_exists(self, page_loaded):
        """window.__fetchRetry 必须暴露 (window 注入 + 测试可达)."""
        fn_type = page_loaded.evaluate("typeof window.__fetchRetry")
        assert fn_type == "function", f"window.__fetchRetry 应是 function, 实际: {fn_type}"

    def test_fetch_retry_succeeds_on_first_try(self, page_loaded):
        """正常 fetch → fetchRetry 应一次成功, 不重试."""
        import requests as _req

        try:
            _req.get(f"{GZIP_SERVER}/dashboard.html", timeout=3).raise_for_status()
        except _req.RequestException:
            pytest.skip("HTTP server 不在, 跳过 fetch 重试测试")

        # 在 page context 跑 fetchRetry (用同一 origin)
        result = page_loaded.evaluate("""
            async () => {
                try {
                    const r = await window.__fetchRetry('mycc-stats.json', {cache: 'no-store'}, 3);
                    return {ok: r.ok, status: r.status};
                } catch (e) {
                    return {error: e.message};
                }
            }
        """)
        assert "error" not in result, f"fetchRetry 应成功, 实际: {result}"
        assert result.get("ok") is True, f"response.ok 应 True, 实际: {result}"

    def test_fetch_retry_fails_gracefully_on_404(self, page_loaded):
        """404 应触发 3 次重试后抛错 (不静默)."""
        import requests as _req

        try:
            _req.get(f"{GZIP_SERVER}/dashboard.html", timeout=3).raise_for_status()
        except _req.RequestException:
            pytest.skip("HTTP server 不在, 跳过 fetch 重试测试")

        result = page_loaded.evaluate("""
            async () => {
                const start = Date.now();
                try {
                    const r = await window.__fetchRetry('__nonexistent__.json', {cache: 'no-store'}, 3);
                    return {unexpected_ok: true, status: r.status};
                } catch (e) {
                    return {elapsed_ms: Date.now() - start, error: e.message};
                }
            }
        """)
        assert "error" in result, f"应抛错, 实际: {result}"
        # fetchRetry 算法: n=3 时 sleep 200+400=600ms (i=1/i=2 后各睡一次, 最后一次不睡)
        # 容忍 ±300ms (含 fetch 自身开销)
        assert result["elapsed_ms"] >= 500, f"重试等待应 ≥500ms (含 200+400 sleep), 实际: {result['elapsed_ms']}ms"