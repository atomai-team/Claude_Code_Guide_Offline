"""test_render_stats_field_mapping.py · renderStats 字段映射契约 v1.0

PM 0.72 P1 推荐: 6 hero stat ID ↔ STATS.counts 字段名映射契约.
若 mycc-stats.json 改名 (例如 hooks_registered → hooks_active), fetch 成功
路径会静默 '?' (test_stats_parity 只比 3 个字段无法捕获), 本测试强制契约.

SSoT (实测 2026-06-29, dashboard.html L1389-1394 附近):
  hs-skills    ↔ c.skills                  (skill 总数)
  hs-agents    ↔ c.agents_total            (agent 总数, 不是 agents_core)
  hs-hooks     ↔ c.hooks_registered        (注册的 hook 数)
  hs-mcp       ↔ c.mcp_servers             (MCP server 数)
  hs-routes    ↔ c.intent_words_routes     (intent-words 路由数)
  hs-plugins   ↔ c.enabled_plugins         (启用的 plugin 数, 不是 total_plugins)

设计原则 (反讽 R1-R4):
- R1 显式报问题: 字段改名 → hard fail, 不静默 '?'
- R2 baseline 固化: 映射表是契约 SSoT, 改 dashboard.html hs() 调用也算违约
- R3 不猜: hs-plugins 用 enabled_plugins 不是 total_plugins 是反讽 R1 实证
- R4 不软化: '?' 兜底会让用户以为 dashboard 坏了, 不如直接 fail
"""
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_HTML = REPO_ROOT / "dashboard.html"


# ─────────────────────────────────────────────────────────────────
# 映射契约 SSoT (实测 2026-06-29)
# ─────────────────────────────────────────────────────────────────

# (hero_stat_id, expected_field, label)
HERO_STAT_MAPPING = [
    ("hs-skills",   "skills",              "本地 Skills"),
    ("hs-agents",   "agents_total",        "本地 Agents"),  # 反讽 R1: 是 total 不是 core
    ("hs-hooks",    "hooks_registered",    "已注册 Hooks"),
    ("hs-mcp",      "mcp_servers",         "MCP Servers"),
    ("hs-routes",   "intent_words_routes", "意图路由"),
    ("hs-plugins",  "enabled_plugins",     "启用插件"),  # 反讽 R1: 是 enabled 不是 total
]


# ─────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def hs_calls(dashboard_html: str) -> dict[str, str]:
    """解析 dashboard.html 全部 hs(id, field) 调用, 返回 {id: field}."""
    out = {}
    # hs('hs-skills', c.skills || '?') → ('hs-skills', 'skills')
    for m in re.finditer(
        r"hs\(\s*['\"]([^'\"]+)['\"]\s*,\s*c\.([a-zA-Z_][a-zA-Z0-9_]*)",
        dashboard_html,
    ):
        out[m.group(1)] = m.group(2)
    return out


@pytest.fixture(scope="session")
def hero_stat_ids(dashboard_html: str) -> set[str]:
    """所有 hero stat DOM id (id='hs-xxx')."""
    return set(re.findall(r'\bid="(hs-[a-z]+)"', dashboard_html))


# ─────────────────────────────────────────────────────────────────
# TestRenderStatsMapping: 6 hero stat ID ↔ STATS.counts 字段映射
# ─────────────────────────────────────────────────────────────────

class TestRenderStatsMapping:
    """hero stat DOM ID 与 STATS.counts 字段名映射契约.

    Bug 实证 (PM 0.72): 若 mycc-stats.json 改名 hooks_registered → hooks_active,
    fetch 成功路径会静默显示 '?' (test_stats_parity 只比 3 个字段). 本测试
    强制 dashboard.html 的 hs() 调用必须用契约规定的字段名, 否则 fail loud.
    """

    @pytest.mark.parametrize("hero_id,field,label", HERO_STAT_MAPPING)
    def test_hero_stat_call_uses_expected_field(
        self, hero_id, field, label, hs_calls
    ):
        """hs('X', c.Y) 必须用契约规定的 Y 字段."""
        assert hero_id in hs_calls, (
            f"hero stat {hero_id} ({label}) 的 hs() 调用缺失 in dashboard.html"
        )
        actual_field = hs_calls[hero_id]
        assert actual_field == field, (
            f"hero stat {hero_id} 字段映射错: 期望 c.{field}, 实测 c.{actual_field}. "
            f"改名会显示 '?'. 修法: dashboard.html 内 hs('{hero_id}', c.{field} ...)"
        )

    def test_all_hero_stats_have_mapping(self, hero_stat_ids):
        """每个 hero stat DOM id 都必须在契约 SSoT 表中登记."""
        contracted = {h[0] for h in HERO_STAT_MAPPING}
        missing = hero_stat_ids - contracted
        assert not missing, (
            f"hero stat DOM id {missing} 未在 HERO_STAT_MAPPING 契约表中登记. "
            f"新增 hero stat 时必须同步更新契约."
        )

    def test_no_orphan_hs_calls(self, hs_calls):
        """hs() 调用都必须对应一个真实 hero stat DOM id (无 orphan)."""
        contracted = {h[0] for h in HERO_STAT_MAPPING}
        orphan = set(hs_calls.keys()) - contracted
        assert not orphan, (
            f"hs() 调用了未登记的 hero stat id: {orphan}. "
            f"可能 dashboard 加了新 hero stat 但忘了登记契约."
        )


# ─────────────────────────────────────────────────────────────────
# TestRenderStatsFallback: fetch 失败降级契约
# ─────────────────────────────────────────────────────────────────

class TestRenderStatsFallback:
    """stats.json fetch 失败时, 6 hero stat 必须降级到 FALLBACK_COUNTS 对应字段.

    Bug 实证 (PM 0.72): fetch 失败路径用 '?' 兜底, 但 hs() 调用有 'c.X || \\'?\\''
    写法, 如果 c 里没 X 字段就显示 '?'. FALLBACK_COUNTS 必须有完整字段集.
    """

    def test_fallback_has_all_hero_stat_fields(self, fallback_counts):
        """FALLBACK_COUNTS 必须包含所有 6 hero stat 映射字段."""
        contracted = {h[1] for h in HERO_STAT_MAPPING}
        missing = contracted - set(fallback_counts.keys())
        assert not missing, (
            f"FALLBACK_COUNTS 缺 hero stat 字段 {missing}. "
            f"fetch 失败时这些 hero stat 会显示 '?', 破坏用户信任."
        )

    def test_hero_stat_calls_have_question_mark_fallback(self, dashboard_html: str):
        """每个 hs() 调用都必须有 '... || \\'?\\'' 兜底 (防 undefined)."""
        # 反讽 R1: 兜底逻辑必须存在, 否则 fetch 失败 → TypeError, 全页崩
        hs_pattern = re.compile(
            r"hs\(\s*['\"]([^'\"]+)['\"]\s*,\s*c\.[a-zA-Z_][a-zA-Z0-9_]*[^)]*\)"
        )
        calls = list(hs_pattern.finditer(dashboard_html))
        assert len(calls) >= 6, (
            f"hs() 调用数 {len(calls)} < 6, hero stat 渲染缺失"
        )
        for m in calls:
            call_text = m.group(0)
            assert "'?'" in call_text or '"?"' in call_text, (
                f"hs() 调用 {call_text[:50]}... 缺 '?' 兜底, "
                f"fetch 失败时 fetch 成功路径有值但 fallback 路径会显示 undefined"
            )