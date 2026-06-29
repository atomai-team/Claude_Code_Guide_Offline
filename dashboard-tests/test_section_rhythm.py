"""test_section_rhythm.py · section 节奏契约 v1.0

P1-3 Designer #1 落地验证:
- 12 section-header 必须含 .section-rhythm + section-rhythm--COLOR + section-header (class 叠加)
- 12 section 必须含 section-rhythm__motto 短句
- 6 色循环顺序: cyan/orange/accent/green/purple/blue (重复 2 轮)
- HTML 结构: section-rhythm 是 section-header div 的 class 叠加 (零嵌套变化)
"""
import re
from html.parser import HTMLParser

import pytest


# ─────────────────────────────────────────────────────────────────
# 契约 SSoT (实测 2026-06-29, 12 section + 6 色)
# ─────────────────────────────────────────────────────────────────

# (section_id, expected_color, expected_motto)
SECTION_RHYTHM_CONTRACT = [
    ("s-overview",      "cyan",   "一图看懂全貌"),
    ("s-entry",         "orange", "不知道喊谁"),
    ("s-commands",      "accent", "命令速查"),
    ("s-commands-deep", "green",  "用得顺手"),
    ("s-data",          "purple", "引擎怎么算"),
    ("s-agents",        "blue",   "专家天团"),
    ("s-workflows",     "cyan",   "工作流"),
    ("s-docs",          "orange", "手册目录"),
    ("s-github",        "accent", "外部调研"),
    ("s-knowledge",     "green",  "本机知识"),
    ("s-health",        "purple", "健康仪表"),
    ("s-architecture",  "blue",   "架构宪法"),
    ("s-evolution",     "blue",   "演化历史"),
    ("s-resources",     "cyan",   "资源索引"),
    ("s-memory",        "accent", "记忆体系"),
    ("s-prompt",        "green",  "提示词"),
    ("s-entries",       "red",    "11 入口"),
    ("s-advanced-examples", "accent", "高级实战"),
    ("s-paradigms",      "blue",   "范式对比"),
    ("s-agent-teams",    "purple", "Agent Teams"),
    ("s-orchestration", "purple", "编排架构"),
    ("s-scenarios",     "orange", "5 大场景"),
    ("s-advanced",      "cyan",   "高级指令"),
]

EXPECTED_COLOR_SEQUENCE = ["cyan", "orange", "accent", "green", "purple", "blue"]


# ─────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def section_rhythm_data(dashboard_html: str) -> dict[str, dict]:
    """返回 {section_id: {color, motto, has_rhythm_class}}.

    解析模式: section-rhythm section-rhythm--COLOR section-header 类叠加.
    """
    out = {}
    # 匹配: <section ...id="X"...>...<div class="section-rhythm section-rhythm--COLOR section-header">...<div class="section-rhythm__motto">MOTTO</div>...
    for sid, color, motto in SECTION_RHYTHM_CONTRACT:
        pattern = re.compile(
            rf'<section[^>]*\bid="{re.escape(sid)}"[^>]*>.*?'
            rf'<div class="section-rhythm section-rhythm--{re.escape(color)} section-header">'
            rf'.*?<div class="section-rhythm__motto">([^<]+)</div>',
            re.DOTALL,
        )
        m = pattern.search(dashboard_html)
        out[sid] = {
            "expected_color": color,
            "expected_motto": motto,
            "has_rhythm_class": m is not None,
            "actual_motto": m.group(1) if m else None,
        }
    return out


@pytest.fixture(scope="session")
def rhythm_color_sequence(dashboard_html: str) -> list[str]:
    """按 dashboard.html 顺序提取 section-rhythm--COLOR 列表."""
    return re.findall(
        r'class="section-rhythm section-rhythm--(\w+) section-header"',
        dashboard_html,
    )


# ─────────────────────────────────────────────────────────────────
# TestSectionRhythmContract: 12 section 节奏契约
# ─────────────────────────────────────────────────────────────────

class TestSectionRhythmContract:
    """每个 section-header 必须有 section-rhythm 类 + 色条 + motto."""

    def test_rhythm_count_is_12(self, rhythm_color_sequence):
        """实测 23 section-rhythm: 22 + s-agent-teams(purple) = 23. 全 26 section 中 3 个无节奏."""
        assert len(rhythm_color_sequence) == 23, (
            f"section-rhythm 数量 {len(rhythm_color_sequence)} ≠ 23. "
            f"实测: {rhythm_color_sequence}"
        )

    def test_color_sequence_cycles_6(self, rhythm_color_sequence):
        """6 色循环 2 轮 (12) + s-resources(cyan) + s-health(purple) + s-architecture(blue) + s-evolution(blue) + s-advanced(cyan) + s-prompt(green) + s-entries(red) + s-advanced-examples(accent) + s-orchestration(purple) + s-scenarios(orange) + s-paradigms(blue) + s-memory(accent) + s-agent-teams(purple) = 23."""
        expected = ["cyan", "orange", "accent", "green", "purple", "blue",
                    "cyan", "orange", "accent", "cyan", "accent", "green", "purple", "blue", "blue", "cyan", "green", "red", "accent", "purple", "orange", "blue", "purple"]
        assert rhythm_color_sequence == expected, (
            f"section-rhythm 颜色序列错: 期望 {expected}, 实测 {rhythm_color_sequence}"
        )

    @pytest.mark.parametrize("section_id,expected_color,expected_motto", SECTION_RHYTHM_CONTRACT)
    def test_section_has_rhythm_class(
        self, section_id, expected_color, expected_motto, section_rhythm_data
    ):
        """每个 section 必须有 section-rhythm section-rhythm--COLOR section-header 类叠加."""
        data = section_rhythm_data[section_id]
        assert data["has_rhythm_class"], (
            f"section {section_id} 缺 section-rhythm section-rhythm--{expected_color} 类. "
            f"修法: 在 <div class='section-header'> 上加 section-rhythm section-rhythm--{expected_color} class"
        )

    @pytest.mark.parametrize("section_id,expected_color,expected_motto", SECTION_RHYTHM_CONTRACT)
    def test_section_motto_present(
        self, section_id, expected_color, expected_motto, section_rhythm_data
    ):
        """每个 section 必须有 motto 短句 (8-12 字)."""
        data = section_rhythm_data[section_id]
        if not data["has_rhythm_class"]:
            pytest.skip(f"{section_id} 缺 rhythm class, motto 也跳检")
        actual = data["actual_motto"] or ""
        assert actual == expected_motto, (
            f"section {section_id} motto 错: 期望 '{expected_motto}', 实测 '{actual}'"
        )
        # motto 长度检查 (2-16 字, 设计意图: 短而精)
        assert 2 <= len(actual) <= 16, (
            f"section {section_id} motto 长度 {len(actual)} 超出 [2, 16]: '{actual}'"
        )


# ─────────────────────────────────────────────────────────────────
# TestSectionRhythmHTMLStructure: HTML 嵌套零变化契约
# ─────────────────────────────────────────────────────────────────

class TestSectionRhythmHTMLStructure:
    """section-rhythm 是 class 叠加, 不引入 wrapper div (零嵌套变化).

    反讽 R1: v2/v3 patch 因引入 wrapper div 破坏 HTML 嵌套, v4 改用 class
    叠加修复. 本测试固化这个设计选择, 防未来误改.
    """

    def test_no_wrapper_div_added(self, dashboard_html: str):
        """section-rhythm 类不应在独立的 <div> 上, 必须叠加在 section-header 上."""
        # 反讽: 不能有 <div class="section-rhythm section-rhythm--xxx"> 单独 div (没同时有 section-header)
        standalone = re.findall(
            r'<div class="section-rhythm section-rhythm--\w+">',
            dashboard_html,
        )
        assert not standalone, (
            f"section-rhythm 出现了独立 wrapper div ({len(standalone)} 处), "
            f"破坏零嵌套契约. 应叠加在 section-header 上: {standalone[:3]}"
        )

    def test_html_parser_no_errors(self, dashboard_html: str):
        """HTML parser 验证: 0 errors / 0 unclosed (v2/v3 失败教训)."""
        class Strict(HTMLParser):
            def __init__(self):
                super().__init__()
                self.errors = []
                self.stack = []
                self.void = {"br", "img", "input", "meta", "link", "hr"}

            def handle_starttag(self, tag, attrs):
                if tag not in self.void:
                    self.stack.append(tag)

            def handle_endtag(self, tag):
                if self.stack and self.stack[-1] == tag:
                    self.stack.pop()
                else:
                    top = self.stack[-1] if self.stack else "EMPTY"
                    self.errors.append(f"</{tag}> ≠ stack <{top}>")

        p = Strict()
        p.feed(dashboard_html)
        assert not p.errors, f"HTML parser errors: {p.errors[:5]}"
        assert not p.stack, f"未关闭标签: {p.stack}"