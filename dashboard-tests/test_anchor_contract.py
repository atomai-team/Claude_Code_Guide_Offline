#!/usr/bin/env python3
"""
test_anchor_contract.py · dashboard.html section 锚点契约测试（占位版 v0.1）

★ 这是 QA-strategist #1 数字契约 pytest 套件的占位骨架，
   P1 完整版会在 dashboard.html 改后扩写。

v0.1 占位目标：
  1. 证明 venv + pytest 9.1.1 可用
  2. 验证 dashboard.html 13 个 section 锚点存在
  3. 验证 nav-link 与 section id 一一对应
  4. 验证关键数字（70/100 / D3 72 / 149 / 58 / 51）在声明它的 section 内

v0.2 计划：扩写为完整契约测试（参考 QA-strategist 回包 JSON）。
"""

import re
import sys
import urllib.request
from pathlib import Path

import pytest

# dashboard.html 路径（相对本测试文件）
DASHBOARD_PATH = Path(__file__).parent.parent / "dashboard.html"


@pytest.fixture(scope="module")
def dashboard_html():
    """读取 dashboard.html 全文"""
    return DASHBOARD_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def sections(dashboard_html):
    """提取所有 section id"""
    return re.findall(r'<section[^>]*id="(s-[^"]+)"', dashboard_html)


@pytest.fixture(scope="module")
def anchor_ids(dashboard_html):
    """提取所有 id="s-*"（含 section 和 div）"""
    return re.findall(r'id="(s-[^"]+)"', dashboard_html)


@pytest.fixture(scope="module")
def nav_links(dashboard_html):
    """提取所有 nav-link href"""
    return re.findall(r'<a href="#(s-[^"]+)" class="nav-link">', dashboard_html)


class TestAnchorContract:
    """section 锚点契约测试"""

    EXPECTED_SECTIONS = [
        "s-overview",
        "s-entry",
        "s-commands",
        "s-commands-deep",
        "s-data",
        "s-agents",
        "s-workflows",
        "s-docs",
        "s-github",
        "s-knowledge",
        "s-health",
        "s-brains",
        "s-architecture",
    ]

    # s-catalog 是 div 不是 section（s-docs 内嵌），需特殊处理
    EXPECTED_DIV_ANCHORS = ["s-catalog"]

    def test_dashboard_file_exists(self):
        """dashboard.html 必须存在"""
        assert DASHBOARD_PATH.exists(), f"dashboard.html 不存在: {DASHBOARD_PATH}"

    def test_all_expected_sections_present(self, sections):
        """13 个核心 section id 必须全部存在"""
        missing = [s for s in self.EXPECTED_SECTIONS if s not in sections]
        assert not missing, f"缺失 section: {missing}"

    def test_div_anchors_present(self, anchor_ids):
        """s-catalog 等 div 锚点必须存在（不在 section 列表里）"""
        missing = [s for s in self.EXPECTED_DIV_ANCHORS if s not in anchor_ids]
        assert not missing, f"缺失 div 锚点: {missing}"

    def test_nav_links_match_anchors(self, anchor_ids, nav_links):
        """nav-link 目标必须有对应 section 或 div 锚点"""
        orphans = [n for n in nav_links if n not in anchor_ids]
        assert not orphans, f"nav-link 指向不存在的锚点: {orphans}"

    def test_no_duplicate_section_ids(self, sections):
        """section id 唯一"""
        dups = [s for s in set(sections) if sections.count(s) > 1]
        assert not dups, f"重复 section id: {dups}"


class TestNumericAnchors:
    """关键数字契约测试（占位 — 数字必须出现在声明它的 section）"""

    @pytest.mark.parametrize("digit,expected_section,description", [
        ("70/100", "s-health", "综合 70/100 必须在 s-health"),
        ("D3", "s-health", "D3 Hooks 维度在 s-health"),
        ("149 skill", "s-knowledge", "149 skill SSoT 在 s-knowledge"),
        ("58 插件", "s-brains", "58 插件在 s-brains"),
        ("L0 能力底座", "s-architecture", "L0-L4 架构在 s-architecture"),
    ])
    def test_digit_in_declared_section(self, dashboard_html, digit, expected_section, description):
        """关键数字必须出现在它声明的 section 内"""
        # 提取目标 section
        pattern = rf'<section[^>]*id="{expected_section}".*?</section>'
        m = re.search(pattern, dashboard_html, re.DOTALL)
        assert m, f"section {expected_section} 不存在"
        section_text = m.group(0)
        assert digit in section_text, f"数字 '{digit}' 未在 {expected_section} 内找到（{description}）"


class TestHttpServing:
    """HTTP server 健康契约测试（验证 serve-gzip.py 是否在跑）"""

    def test_gzip_server_optional(self):
        """serve-gzip server 在 18766 是可选的（不强依赖）"""
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:18766/dashboard.html",
                headers={"Accept-Encoding": "gzip"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                encoding = resp.headers.get("Content-Encoding")
                body = resp.read()
                if encoding == "gzip":
                    import gzip as gz
                    decoded = gz.decompress(body)
                    assert b"<!DOCTYPE" in decoded, "gzip 解压后内容异常"
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pytest.skip("serve-gzip server 未在 18766 跑（可选依赖）")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))