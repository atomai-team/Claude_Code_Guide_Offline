"""test_body_count_parity.py · 正文 agent 计数 ↔ SSoT 守护 v1.0

盲点 (2026-06-29 captain + architect 0.93): dashboard 主展示区多处 hardcoded
agent 数 (89 个专家 / 50 agent) 与 SSoT (mycc-stats.json counts.agents_total)
漂移; test_stats_parity 只测 FALLBACK↔stats.json, 不覆盖正文叙述数字 → 本测试补位.

架构决策 (architect 方案 B): 叙述性数字用 hardcoded + 本测试守护 (CI 强制 == SSoT),
优于 data-rt 运行时填充 (避免给叙述文案加 JS 依赖 + noscript 失效).

范围 (R3 不猜死): 只守护 "agents_total 展示点" (个专家/Agent 团队/agent 全量/agents·).
deep-note 区多口径叙述 (58 含 platform / 51 业务 / 65 架构层) 是有意口径披露,
不在守护范围 — 见盲点债"agent 口径混乱"(91 vs 58 vs 51, 待后续统一).
"""
import re

# 精确锚定 "agents_total 展示点" 的 pattern, 避开 deep-note 多口径叙述
SSOT_AGENT_PATTERNS = [
    (r'(\d+)\s*个专家', "个专家 (hero/卡片/section/SEO)"),
    (r'(\d+)\s*Agent 团队', "Agent 团队 (nav)"),
    (r'(\d+)\s*agents?\s*(?:全量|·)', "catalog (subtitle/muted)"),
]


class TestBodyAgentCountParity:
    """主展示区所有 hardcoded agent 计数必须 == SSoT(agents_total).

    防 89/50 漂移复发: 本测试若早存在, P1 全程的漂移会被立即拦截.
    """

    def test_display_agent_counts_match_ssot(
        self, dashboard_html: str, stats_json_local: dict
    ):
        """所有 agents_total 展示点 == SSoT (从 stats.json 实读, R2 不固化阈值)."""
        ssot = stats_json_local["counts"]["agents_total"]
        violations = []
        for pat, label in SSOT_AGENT_PATTERNS:
            for m in re.finditer(pat, dashboard_html):
                n = int(m.group(1))
                if n != ssot:
                    s = max(0, m.start() - 12)
                    ctx = dashboard_html[s:m.end() + 4].replace("\n", " ")
                    violations.append(f"{label}: {n} != {ssot}  @…{ctx}…")
        assert not violations, (
            f"主展示区 {len(violations)} 处 agent 计数与 SSoT(agents_total={ssot}) 漂移:\n  "
            + "\n  ".join(violations)
        )

    def test_display_agent_count_has_coverage(
        self, dashboard_html: str, stats_json_local: dict
    ):
        """至少命中 N 处展示点 (防 pattern 失效导致守护静默通过)."""
        ssot = stats_json_local["counts"]["agents_total"]
        total_hits = sum(
            len(re.findall(pat, dashboard_html)) for pat, _ in SSOT_AGENT_PATTERNS
        )
        assert total_hits >= 6, (
            f"agents_total 展示点仅命中 {total_hits} 处 (期望 ≥6: SEO×4 + nav + 卡片 + "
            f"section + catalog). pattern 可能失效或展示点被删."
        )

    def test_no_50_agent_typo(self, dashboard_html: str):
        """硬错回归守护: '50 agent(s)' 是历史笔误 (真实=agents_total), 永不再现."""
        hits = re.findall(r'(?<!\d)50\s*agents?\b', dashboard_html)
        assert not hits, (
            f"出现 '50 agent' 历史笔误 ({len(hits)} 处). agent 总数=agents_total, 非 50."
        )

    def test_ssot_sane(self, stats_json_local: dict):
        """SSoT 自身合理性 (防 stats.json 损坏致守护静默失效)."""
        ssot = stats_json_local["counts"]["agents_total"]
        assert isinstance(ssot, int) and 50 <= ssot <= 200, (
            f"agents_total={ssot} 不在合理区间 [50,200], stats.json 可能损坏"
        )
