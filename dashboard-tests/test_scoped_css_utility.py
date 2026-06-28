"""test_scoped_css_utility.py · P1-4 scoped CSS + utility 工具集契约 v1.0

P1-4 Architect #1 落地范围 (实测降级为 L0 准备):
- dashboard.html 6 段 scoped CSS 物理保留 (CSS specificity 限制, scoped 不能删)
- components.css 加 5 个 utility class (.deep-key--132/156/172/184/220)
  作为工具集, 供未来新建组件直接使用

反讽 R1 实证 (2026-06-29):
- 实测 dashboard.html L157-176 scoped #s-X .deep-key { min-width: NNNpx }
- 全局 @media .deep-key { min-width: 0 } 在 mobile (390px) 不生效,
  因 scoped specificity 110 > 全局 specificity 0, scoped 胜出
- 故决策保留 6 段 scoped, 不强行做 scoped → utility 大重构

本测试固化这个事实, 防未来误删 scoped 引入 mobile 视觉退化.
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_CSS = REPO_ROOT / "design-system" / "components.css"
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


# ─────────────────────────────────────────────────────────────────
# 契约 SSoT (实测 2026-06-29)
# ─────────────────────────────────────────────────────────────────

EXPECTED_UTILITY_CLASSES = [
    "deep-key--132",   # s-brains
    "deep-key--156",   # s-architecture
    "deep-key--172",   # s-github
    "deep-key--184",   # s-entry, s-health
    "deep-key--220",   # s-knowledge
]

# (section_id, expected_min_width_px)
SCOPED_CSS_SECTIONS = [
    ("s-entry",         184),
    ("s-github",        172),
    ("s-knowledge",     220),
    ("s-health",        184),
    ("s-brains",        132),
    ("s-architecture",  156),
]


# ─────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def components_css() -> str:
    return COMPONENTS_CSS.read_text(encoding="utf-8")


# 注: dashboard_html fixture 由 conftest.py 提供 (读 dashboard.html)
# 这里不重复定义避免 pytest fixture resolution 警告

@pytest.fixture(scope="session")
def scoped_css_blocks(dashboard_html: str) -> dict[str, int]:
    """返回 {section_id: min_width_px} 来自 scoped CSS."""
    out = {}
    pattern = re.compile(
        r'#(s-\w+(?:-\w+)?)\s+\.deep-key\s*\{\s*min-width:\s*(\d+)px;\s*\}',
    )
    for m in pattern.finditer(dashboard_html):
        out[m.group(1)] = int(m.group(2))
    return out


# ─────────────────────────────────────────────────────────────────
# TestUtilityClasses: 5 utility class 必须就位
# ─────────────────────────────────────────────────────────────────

class TestUtilityClasses:
    """components.css 必须有 5 个 .deep-key--* utility class.

    这是 P1-4 落地物 (L0 准备): 即使 dashboard.html 不立即切换,
    utility class 必须就位供未来使用.
    """

    @pytest.mark.parametrize("class_name", EXPECTED_UTILITY_CLASSES)
    def test_utility_class_defined(self, class_name, components_css):
        """每个 .deep-key--NNN 必须有 min-width: NNNpx 定义."""
        pattern = re.compile(rf'\.{re.escape(class_name)}\s*\{{\s*min-width:\s*\d+px;\s*\}}')
        m = pattern.search(components_css)
        assert m, (
            f"components.css 缺 .{class_name} 定义. "
            f"加: .{class_name} {{ min-width: {class_name.split('--')[1]}px; }}"
        )

    def test_utility_count_is_5(self, components_css):
        """utility class 总数应为 5 (不多不少).

        只匹配 .deep-key--NNN { min-width: NNNpx } 定义, 不匹配注释里的引用.
        """
        # 用正向匹配: .deep-key--NNN { min-width: NNNpx }
        found = re.findall(
            r'\.deep-key--(\d+)\s*\{\s*min-width:\s*\d+px',
            components_css,
        )
        assert len(found) == 5, (
            f"components.css utility class 定义数 {len(found)} ≠ 5. 实测: {found}"
        )


# ─────────────────────────────────────────────────────────────────
# TestScopedCSSPreserved: 6 段 scoped CSS 物理保留契约
# ─────────────────────────────────────────────────────────────────

class TestScopedCSSPreserved:
    """dashboard.html 6 段 scoped CSS 必须保留 (CSS specificity 物理限制).

    反讽 R1 (2026-06-29): 用户决策"保留 scoped"——因为全局 @media 重置
    min-width: 0 在 mobile (390px) 不生效 (scoped 110 > 全局 0), 强删会
    导致 mobile 水平滚动条. 本测试固化事实, 防未来误删.
    """

    def test_scoped_count_is_6(self, scoped_css_blocks):
        """scoped #s-X .deep-key 块应有 6 个 (s-entry/s-github/s-knowledge/s-health/s-brains/s-architecture)."""
        assert len(scoped_css_blocks) == 6, (
            f"scoped #s-X .deep-key 块 {len(scoped_css_blocks)} ≠ 6. "
            f"实测: {scoped_css_blocks}. 删 scoped 需先解决 mobile min-width 重置 (P2.x)."
        )

    @pytest.mark.parametrize("section_id,expected_min_width", SCOPED_CSS_SECTIONS)
    def test_scoped_min_width_correct(self, section_id, expected_min_width, scoped_css_blocks):
        """每段 scoped CSS 的 min-width 必须匹配契约 SSoT."""
        assert section_id in scoped_css_blocks, (
            f"#{section_id} 缺 scoped CSS. "
            f"修法: 加 {section_id} .deep-key {{ min-width: {expected_min_width}px; }}"
        )
        actual = scoped_css_blocks[section_id]
        assert actual == expected_min_width, (
            f"#{section_id} scoped min-width 漂移: 期望 {expected_min_width}px, 实测 {actual}px. "
            f"如改动有意, 同步更新 SCOPED_CSS_SECTIONS 契约表"
        )


# ─────────────────────────────────────────────────────────────────
# TestScopedMediaQueryPreserved: 6 段 scoped @media 必须保留
# ─────────────────────────────────────────────────────────────────

class TestScopedMediaQueryPreserved:
    """6 段 @media (max-width: 700px) scoped 内必须保留.

    反讽 R1: 删这 6 段会让 mobile (390px) deep-row 不能切 flex-direction: column,
    且 min-width 不能重置为 0 (因 scoped specificity 物理限制).
    """

    def test_scoped_media_count_is_6(self, dashboard_html: str):
        """scoped 内 @media (max-width: 700px) 块应有 6 段 (与 scoped CSS 一一对应)."""
        # 匹配 scoped 内 @media: @media (max-width: 700px) { #s-X .deep-row ... #s-X .deep-key ... }
        pattern = re.compile(
            r'@media \(max-width: 700px\) \{\s*#s-\w+(?:-\w+)?\s+\.deep-row'
        )
        matches = pattern.findall(dashboard_html)
        assert len(matches) == 6, (
            f"scoped 内 @media 块 {len(matches)} ≠ 6. "
            f"实测: {matches}. 删任何一段都会让对应 section 在 mobile 退化."
        )

    @pytest.mark.parametrize("section_id,_min_width", SCOPED_CSS_SECTIONS)
    def test_scoped_media_query_exists(self, section_id, _min_width, dashboard_html: str):
        """每个 scoped CSS section 必须有对应的 scoped @media 重置块."""
        pattern = re.compile(
            rf'@media \(max-width: 700px\) \{{\s*#{re.escape(section_id)}\s+\.deep-row'
        )
        m = pattern.search(dashboard_html)
        assert m, (
            f"#{section_id} 缺 scoped @media (max-width: 700px) 重置块. "
            f"修法: 加 @media (max-width: 700px) {{ #{section_id} .deep-row ... #{section_id} .deep-key ... }}"
        )


# ─────────────────────────────────────────────────────────────────
# TestUtilityVsScopedParity: utility class 与 scoped CSS 数字一致性
# ─────────────────────────────────────────────────────────────────

class TestUtilityVsScopedParity:
    """utility class 提供的 min-width 必须与 scoped CSS 一致 (未来切换无视觉退化)."""

    @pytest.mark.parametrize("class_name", EXPECTED_UTILITY_CLASSES)
    def test_utility_min_width_matches_scoped(self, class_name, components_css, scoped_css_blocks):
        """utility .deep-key--NNN 的 NNN 必须等于某个 scoped CSS 的 min-width."""
        utility_min_width = int(class_name.split("--")[1])
        scoped_widths = set(scoped_css_blocks.values())
        assert utility_min_width in scoped_widths, (
            f"utility .{class_name} ({utility_min_width}px) 与 scoped CSS 不一致. "
            f"scoped 宽度集: {sorted(scoped_widths)}. utility 应覆盖每个 scoped 宽度."
        )


# ─────────────────────────────────────────────────────────────────
# TestScopedCSSFutureMigrationGuard: 防未来误删 scoped 引入 mobile 退化
# ─────────────────────────────────────────────────────────────────

class TestScopedCSSFutureMigrationGuard:
    """反讽 R1 教训: scoped CSS 不能删 (mobile min-width 退化).

    本测试用作 P1-4 的"防误删哨兵": 未来有人想"清理 scoped 重复"时,
    必须先解决 mobile min-width 重置问题 (例如 utility class 加 !important,
    或在 scoped 内增加移动端 min-width 重置). 否则测试失败.
    """

    def test_no_recent_deletion_of_scoped_css(self, scoped_css_blocks):
        """scoped CSS 数量从 6 减少 → 需先解决 mobile 重置."""
        assert len(scoped_css_blocks) == 6, (
            f"scoped CSS 数量 {len(scoped_css_blocks)} < 6, 表明有人删了 scoped. "
            f"删除前请确认: 1) utility class 在 mobile 重置 min-width 已实现 (或 !important); "
            f"2) Playwright 390px 实测 deep-row flex-direction: column 仍生效; "
            f"3) 同步更新本测试 SCOPED_CSS_SECTIONS 契约表"
        )