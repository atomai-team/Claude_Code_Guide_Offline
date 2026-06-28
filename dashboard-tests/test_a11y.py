"""test_a11y.py · a11y 契约 v1.0 (P2-1 Web Dev 0.91 落地)

实测起点 (2026-06-29):
- 0 inert / 0 noscript / 0 img alt (接力包 §5.1 正确)
- 2 modal-overlay 已有 role="dialog" + aria-modal="true" + aria-label
- 2 SVG 已 aria-hidden="true" (装饰性)

修复重点 = Modal 焦点陷阱 (inert) + noscript 降级. SVG/alt/noscript 大部分已就位.

设计原则 (反讽 R1-R4):
- R1 显式报问题: 焦点陷阱缺失 → hard fail (Playwright 验证)
- R2 baseline 不固化: 数字阈值从实测
- R3 不猜死: SVG 必须 aria-hidden 或 role=img, 二选一
- R4 严重缺陷不软化: inert 缺失 → fail loud
"""
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


# ─────────────────────────────────────────────────────────────────
# TestNoscriptFallback: JS 关闭时降级提示
# ─────────────────────────────────────────────────────────────────

class TestNoscriptFallback:
    """JS 关闭时, 用户应看到降级提示 (a11y + Apple HIG)."""

    def test_noscript_tag_present(self, dashboard_html: str):
        """<noscript> 标签必须存在."""
        assert "<noscript>" in dashboard_html, (
            "<noscript> 缺失. 用户 JS 关闭时无降级提示, 看到空白页."
        )

    def test_noscript_has_meaningful_text(self, dashboard_html: str):
        """noscript 必须含提示文本 (不能空标签)."""
        m = re.search(r"<noscript>(.*?)</noscript>", dashboard_html, re.DOTALL)
        assert m, "<noscript> 不完整 (缺闭合标签或内容)"
        content = m.group(1).strip()
        assert len(content) > 20, (
            f"<noscript> 内容太短 ({len(content)} chars): {content!r}"
        )
        # 必须含中英文提示关键词
        assert any(kw in content for kw in ["JavaScript", "Java", "依赖"]), (
            f"<noscript> 缺关键词 (JavaScript/Java/依赖): {content!r}"
        )


# ─────────────────────────────────────────────────────────────────
# TestModalA11y: Modal 焦点陷阱 + role/aria
# ─────────────────────────────────────────────────────────────────

class TestModalA11y:
    """2 个 modal-overlay (detailOverlay + cmdkOverlay) 的 a11y 契约."""

    @pytest.mark.parametrize("overlay_id", ["detailOverlay", "cmdkOverlay"])
    def test_overlay_has_role_dialog(self, overlay_id, dashboard_html: str):
        """每个 modal-overlay 必须 role='dialog'."""
        pattern = re.compile(
            rf'<div[^>]*id="{overlay_id}"[^>]*\brole="dialog"',
            re.IGNORECASE,
        )
        m = pattern.search(dashboard_html)
        assert m, (
            f"#{overlay_id} 缺 role='dialog'. "
            f"screen reader 不知道这是对话框."
        )

    @pytest.mark.parametrize("overlay_id", ["detailOverlay", "cmdkOverlay"])
    def test_overlay_has_aria_modal(self, overlay_id, dashboard_html: str):
        """每个 modal-overlay 必须 aria-modal='true'."""
        pattern = re.compile(
            rf'<div[^>]*id="{overlay_id}"[^>]*\baria-modal="true"',
            re.IGNORECASE,
        )
        m = pattern.search(dashboard_html)
        assert m, (
            f"#{overlay_id} 缺 aria-modal='true'. "
            f"screen reader 不知道这是模态对话框 (背景应被冻结)."
        )

    @pytest.mark.parametrize("overlay_id", ["detailOverlay", "cmdkOverlay"])
    def test_overlay_has_aria_label(self, overlay_id, dashboard_html: str):
        """每个 modal-overlay 必须 aria-label (对话框标题)."""
        pattern = re.compile(
            rf'<div[^>]*id="{overlay_id}"[^>]*\baria-label="[^"]+"',
            re.IGNORECASE,
        )
        m = pattern.search(dashboard_html)
        assert m, (
            f"#{overlay_id} 缺 aria-label. screen reader 读不出对话框用途."
        )


# ─────────────────────────────────────────────────────────────────
# TestInertFocusTrap: body.inert 焦点陷阱契约 (静态源码)
# ─────────────────────────────────────────────────────────────────

def _extract_function_body(html: str, signature: str) -> str | None:
    """从 html 找 `signature` 函数体 (用括号配对, 容忍嵌套 {}).

    signature 例: 'window.openDetail = function' 或 'function openCmdK'.
    """
    # 找到 signature 起点
    sig_idx = html.find(signature)
    if sig_idx < 0:
        return None
    # 找 signature 后第一个 { (函数体起点)
    brace_start = html.find("{", sig_idx)
    if brace_start < 0:
        return None
    # 配对 {} 找函数体终点
    depth = 0
    for i in range(brace_start, len(html)):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                return html[brace_start:i + 1]
    return None


class TestInertFocusTrap:
    """openDetail/openCmdK 必须给 <main> 加 inert; closeDetail/closeCmdK 必须移除.

    反讽 R1 (实测 2026-06-29): 加 inert 到 body 会冻结整个 body, 包括 Modal
    内部, setTimeout focus 失效. 正确做法: 加到 <main> (主内容), Modal 自身
    在 <body> 内但不在 <main> 内, 仍可访问.

    开 Modal → setAttribute('inert', '') on <main>
    关 Modal → removeAttribute('inert') on <main>
    """

    def test_open_detail_sets_inert_on_main(self, dashboard_html: str):
        """openDetail 函数内必须 <main>.setAttribute('inert', ...)."""
        body = _extract_function_body(dashboard_html, "window.openDetail = function")
        assert body, "openDetail 函数体未找到"
        assert "inert" in body, (
            "openDetail 没设 inert, 焦点陷阱失效. "
            "加: const mainEl = document.getElementById('main'); "
            "if (mainEl) mainEl.setAttribute('inert', '');"
        )
        # 反讽 R1 防御: 不应加 inert 到 body (会冻结 Modal 自身)
        assert "document.body.setAttribute('inert'" not in body, (
            "openDetail 把 inert 加到 body 会冻结 Modal 自身. "
            "改: 加到 <main> 而非 <body>."
        )

    def test_close_detail_removes_inert(self, dashboard_html: str):
        """closeDetail 函数内必须 <main>.removeAttribute('inert')."""
        body = _extract_function_body(dashboard_html, "window.closeDetail = function")
        assert body, "closeDetail 函数体未找到"
        assert "inert" in body, (
            "closeDetail 没移除 inert, 下次开 Modal 焦点陷阱失效."
        )
        assert "document.body.removeAttribute('inert')" not in body, (
            "closeDetail 应移除 <main> 的 inert, 不是 body."
        )

    def test_open_cmdk_sets_inert_on_main(self, dashboard_html: str):
        """openCmdK 函数内必须设 inert on <main>."""
        body = _extract_function_body(dashboard_html, "function openCmdK")
        assert body, "openCmdK 函数体未找到"
        assert "inert" in body, (
            "openCmdK 没设 inert. 加到 <main> 而非 <body>."
        )
        assert "document.body.setAttribute('inert'" not in body, (
            "openCmdK 不应加 inert 到 body."
        )

    def test_close_cmdk_removes_inert(self, dashboard_html: str):
        """closeCmdK 函数内必须移除 inert on <main>."""
        body = _extract_function_body(dashboard_html, "function closeCmdK")
        assert body, "closeCmdK 函数体未找到"
        assert "inert" in body, (
            "closeCmdK 没移除 inert."
        )
        assert "document.body.removeAttribute('inert')" not in body, (
            "closeCmdK 应移除 <main> 的 inert."
        )


# ─────────────────────────────────────────────────────────────────
# TestSvgA11y: 装饰性 SVG 必须有 aria-hidden 或 role=img
# ─────────────────────────────────────────────────────────────────

class TestSvgA11y:
    """所有 <svg> 必须有 a11y 属性 (装饰性 aria-hidden 或信息性 role=img+aria-label)."""

    def test_all_svg_have_a11y_attribute(self, dashboard_html: str):
        """每个 <svg> 至少含 aria-hidden='true' 或 role='img' + aria-label."""
        svg_pattern = re.compile(r"<svg\b[^>]*>", re.IGNORECASE)
        svgs = list(svg_pattern.finditer(dashboard_html))
        assert len(svgs) > 0, "<svg> 缺失 (本测试无意义)"

        violations = []
        for m in svgs:
            tag = m.group(0)
            has_decorative = re.search(r'\baria-hidden="true"', tag, re.IGNORECASE)
            has_informative = (
                re.search(r'\brole="img"', tag, re.IGNORECASE)
                and re.search(r'\baria-label="[^"]+"', tag, re.IGNORECASE)
            )
            if not (has_decorative or has_informative):
                violations.append(tag[:80])

        assert not violations, (
            f"{len(violations)} 个 <svg> 缺 a11y 属性 (aria-hidden 或 role=img+aria-label): "
            f"{violations[:3]}"
        )


# ─────────────────────────────────────────────────────────────────
# TestImgAltRequirement: 所有 <img> 必须有 alt 属性
# ─────────────────────────────────────────────────────────────────

class TestImgAltRequirement:
    """若 <img> 缺失或缺 alt → fail. 当前 dashboard 无 <img>, 测试守护未来."""

    def test_all_img_have_alt(self, dashboard_html: str):
        """每个 <img> 必须 alt='...' (装饰性可空 alt='')."""
        img_pattern = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
        imgs = list(img_pattern.finditer(dashboard_html))

        violations = []
        for m in imgs:
            tag = m.group(0)
            if not re.search(r'\balt="[^"]*"', tag, re.IGNORECASE):
                violations.append(tag[:80])

        assert not violations, (
            f"{len(violations)} 个 <img> 缺 alt 属性: {violations[:3]}"
        )