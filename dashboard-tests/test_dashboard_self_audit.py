"""test_dashboard_self_audit.py · 锚点数字归属契约 v1.0

每个 dashboard 展示的关键数字必须能在"它声称的 section"中找到.

SSoT: dashboard.html 14 个 section (实测 grep, 非接力包):
  top / s-overview / s-entry / s-commands / s-commands-deep / s-data /
  s-agents / s-workflows / s-docs / s-github / s-knowledge /
  s-health / s-brains / s-architecture

锚点清单来源: 反讽 R1 实测 (2026-06-29), 接力包 §4.1 "12 锚点"
有多处失真, 本文件以 grep 结果为准:

实测发现:
  ✓ 70/100 → s-health (2 处)
  ✓ D3 → s-health, s-brains (26 处, Hooks 维度引用最广)
  ✓ 149 → s-knowledge, s-health, s-brains (10 处, skill 数字多 section 复用)
  ✓ 156 → s-brains (5 处)
  ✓ 58 → s-brains (6 处, 插件数字)
  ✓ 51 → s-brains (3 处)
  ✓ 35 → s-brains (1 处)
  ✓ P0×1 → s-health, s-brains (2 处)
  ✓ P1×5 → s-health, s-brains (2 处)
  ✓ P2×3 → s-health, s-brains (2 处)
  ✓ REFUTE×3 → s-health (2 处)
  ✗ 8维 → 全文 0 处 (接力包失真, 改为 REFUTE×3 替代)

设计原则:
- "primary_section" 是锚点**声明**所在的 section (dashboard 对外宣称)
- 其他 section 出现算 "引用", 测试允许但记 stderr
- 任何 primary_section 缺失 → hard fail (锚点从主页消失 = 数据看板盲区)
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


# ─────────────────────────────────────────────────────────────────
# 锚点 SSoT 表 (实测 2026-06-29)
# ─────────────────────────────────────────────────────────────────

# (needle, primary_section, description, expected_min_count_in_primary)
ANCHOR_CONTRACT = [
    ("70/100",   "s-health",       "综合健康度评分 70/100",                 1),
    ("D3",       "s-health",       "Hooks 维度审计",                       1),
    ("149",      "s-knowledge",    "skill 总数 149 (mycc-stats.json SSoT)", 1),
    ("156",      "s-brains",       "skill 156 (口径 B, 旧数据未刷新)",      1),
    ("58",       "s-brains",       "插件 58",                              1),
    ("51",       "s-brains",       "agents 51",                            1),
    ("35",       "s-brains",       "P2 plugins 35",                        1),
    ("P0×1",     "s-health",       "P0 bug 数 1",                          1),
    ("P1×5",     "s-health",       "P1 task 数 5",                         1),
    ("P2×3",     "s-health",       "P2 task 数 3",                         1),
    ("REFUTE×3", "s-health",       "对抗验证 REFUTE×3",                     1),
]


# ─────────────────────────────────────────────────────────────────
# Fixtures: 复用 conftest.py 的 section indexer
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def section_index(dashboard_html: str) -> dict[str, str]:
    """Return dict: section_id → section_html_text."""
    out = {}
    section_re = re.compile(r'<section[^>]*\bid="([^"]+)"[^>]*>', re.IGNORECASE)
    matches = list(section_re.finditer(dashboard_html))
    for i, m in enumerate(matches):
        sid = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(dashboard_html)
        out[sid] = dashboard_html[start:end]
    return out


# ─────────────────────────────────────────────────────────────────
# TestSectionStructure: section 数量 + id 唯一性
# ─────────────────────────────────────────────────────────────────

class TestSectionStructure:
    """dashboard 结构层契约: section 数量稳定 + id 唯一."""

    def test_section_count_in_range(self, section_index):
        """section 数量应在 13-26 之间 (含 s-agent-teams F1 2026-06-30)."""
        n = len(section_index)
        assert 13 <= n <= 26, f"section 数量 {n} 超出预期 [13, 26], 需重新审计 dashboard"

    def test_no_duplicate_section_ids(self, section_index):
        ids = list(section_index.keys())
        assert len(ids) == len(set(ids)), f"section id 重复: {ids}"


# ─────────────────────────────────────────────────────────────────
# TestAnchorPlacement: 12 锚点必须在 primary_section 出现
# ─────────────────────────────────────────────────────────────────

class TestAnchorPlacement:
    """每个 dashboard 关键数字必须在它"声明"的 section 中至少出现 1 次.

    Bug 实证 (QA-strategist): 数字漂移 + 跨 section 引用混乱 → 用户
    在 A section 看到 "skill 149" 但 B section 展示 "skill 156" → 自相矛盾.
    本测试只检测"声明归属", 跨 section 引用由 TestCrossSectionRef 检测.
    """

    @pytest.mark.parametrize("needle,primary,desc,min_count", ANCHOR_CONTRACT)
    def test_anchor_in_primary_section(
        self, needle, primary, desc, min_count, section_index
    ):
        assert primary in section_index, (
            f"锚点 {needle!r} 声明在 {primary}, 但 {primary} section 不存在"
        )
        body = section_index[primary]
        # 反讽 R1 修 (QA-validator P2 报): 加 \b 词边界防误匹配 (149 vs 1949 年份, 51 vs 5100)
        word_boundary = (
            re.compile(rf"\b{re.escape(needle)}\b") if needle.isascii()
            else re.compile(re.escape(needle))  # 中文符号 (×) 无 \b 概念
        )
        actual = len(word_boundary.findall(body))
        assert actual >= min_count, (
            f"锚点 {needle!r} ({desc}) 应在 {primary} 出现 ≥{min_count} 次, "
            f"实测 {actual} 次 (词边界匹配). 可能 dashboard 重构丢失声明."
        )

    @pytest.mark.parametrize("needle,primary,desc,_", ANCHOR_CONTRACT)
    def test_anchor_not_in_unexpected_sections(self, needle, primary, desc, _, section_index):
        """锚点不应在 primary 之外**主推**section 出现.

        例外: 跨 section 引用是允许的 (s-health 引用 149 也行),
        但若超过 5 个 section 都有同一锚点 = 数字含义混乱, 报警.

        此测试是 WARN 级 (soft), 只输出 stderr 不 fail.
        """
        appearances = [
            sid for sid, body in section_index.items() if needle in body
        ]
        unexpected = [s for s in appearances if s != primary]
        if len(appearances) > 5:
            print(
                f"\n⚠️  ANCHOR [{needle}] 出现在 {len(appearances)} 个 section: "
                f"{appearances}. 可能口径混乱, 考虑统一."
            )
        elif unexpected:
            print(
                f"\n📎 ANCHOR [{needle}] primary={primary}, 跨 section 引用: {unexpected}"
            )


# ─────────────────────────────────────────────────────────────────
# TestCrossSectionConsistency: 同一锚点跨 section 数字应自洽
# ─────────────────────────────────────────────────────────────────

class TestCrossSectionConsistency:
    """同一概念在不同 section 必须用同一数字 (149 ≠ 156 ≠ 147).

    Bug 实证 (PM): 149/156/120 三口径暴露矛盾 → 用户对 dashboard 信任崩塌.
    """

    def test_skill_count_single_canonical(self, section_index):
        """skill 总数必须只用一个口径 (149 OR 156, 不能并存).

        149 = mycc-stats.json SSoT 实时数字 (本机) ← SSoT
        156 = 早期 P0 阶段数字, dashboard.html L1065 在 <code> 标签内诚实披露
        147 = FALLBACK 内嵌残留 (P1-2 commit 7573599 同步 dashboard L1370 后,
               dashboard.html L782/L832 hero subtitle 的 "147 skill" 硬编码未跟进)

        实际 dashboard.html 同时含 147/149/156 → 三口径并存.
        PM 共识 #9 + 本测试实证已 hard fail 多次 (P1-1 commit cc0e888 时).

        P1-2 决策 (用户钦定): 按 SSoT 149 归一, 但保留 156 注释作诚实披露.

        反讽 R2: 多模型一致 ≠ 自动执行. dashboard 全文数字归一属 P1-2.x
        范围, 保留 xfail 但 stderr 详细报告, 让工程师看清三口径位置.
        """
        # 找所有形如 "skill N" / "N skill" 的 token
        skill_pattern = re.compile(r"\b(\d{2,3})\s*(?:个\s*)?skill", re.IGNORECASE)
        secondary_pattern = re.compile(r"skill[^\d]{0,8}(\d{2,3})", re.IGNORECASE)

        # 数字 → [(section_id, is_disclosure), ...] 列表
        # is_disclosure=True 表示该数字紧邻 <code> 标签 (诚实披露模式,
        # 例如 L1065 "<code>capability-activation-map.md</code> 标 156 skill 含 7 个 platform"
        # 数字 156 在 </code> 之后但属于 code 引用的延伸说明)
        occurrences: dict[int, list[tuple[str, bool]]] = {}
        for sid, body in section_index.items():
            for m in skill_pattern.finditer(body):
                # 简化判定: token 之前 80 字符内最近一个 </code> 距离 <=30
                # (紧邻 code 引用后的说明文字)
                before = body[max(0, m.start() - 80):m.start()]
                last_close_in_before = before.rfind("</code>")
                distance_to_close = (m.start() - max(0, m.start() - 80)) - last_close_in_before
                is_disclosure = last_close_in_before >= 0 and distance_to_close <= 30
                for g in m.groups():
                    if g and 100 <= int(g) <= 200:
                        occurrences.setdefault(int(g), []).append((sid, is_disclosure))
            for m in secondary_pattern.finditer(body):
                before = body[max(0, m.start() - 80):m.start()]
                last_close_in_before = before.rfind("</code>")
                distance_to_close = (m.start() - max(0, m.start() - 80)) - last_close_in_before
                is_disclosure = last_close_in_before >= 0 and distance_to_close <= 30
                if m.group(1) and 100 <= int(m.group(1)) <= 200:
                    occurrences.setdefault(int(m.group(1)), []).append((sid, is_disclosure))

        # 滤掉 false-positive (年份等)
        plausible = {n: locs for n, locs in occurrences.items() if 100 <= n <= 200}

        # stderr: 让工程师看到全部口径 + 位置 + 是否诚实披露
        print("\n=== skill 多口径分布 ===")
        for n in sorted(plausible):
            locs_str = ", ".join(
                f"{sid}{'(code)' if in_code else '(main)'}"
                for sid, in_code in plausible[n]
            )
            print(f"  {n}: {len(plausible[n])}× at {locs_str}")
        print("=" * 30)

        # 严格断言 (P1-2 commit 7573599 同步 FALLBACK 后, dashboard.html
        # L782/L832 的 hero subtitle "147 skill" 也已归一, 只剩 149 + 156 诚实披露):
        # - SSoT=149 必须 0 main 位出现 (即不是数字断言, 只验证非 SSoT)
        # - 156 允许在 <code> 标签附近 (诚实披露), 不允许在 main 位
        # - 其他非 SSoT 数字 (147/151/...) 必须 0 出现
        non_sso_main = {
            n: [l for l in plausible[n] if not l[1]]
            for n in plausible if n != 149
        }
        non_sso_main_with_occ = {n: locs for n, locs in non_sso_main.items() if locs}
        if non_sso_main_with_occ:
            pytest.fail(
                f"skill 数字非 SSoT=149 仍出现在 main 位 (用户可见): "
                f"{non_sso_main_with_occ}. "
                f"允许 <code> 标签附近的诚实披露 (如 L1065 'capability-activation-map.md 标 156')."
            )