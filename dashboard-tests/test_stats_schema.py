"""test_stats_schema.py · mycc-stats.json 结构契约守护 v1.0

目标: 守护 stats.json 的 schema 完整性 (非 FALLBACK↔live 漂移, 而是 JSON 本身结构).
补位 test_stats_parity.py: parity 测"数字对不对", 本测试测"结构对不对".

保护场景:
- stats 引擎 bug 把 counts.skills 写成 null / string / 0
- hermes 重构后顶层缺失 lists / hooks 键
- version 字段变成数字而非字符串 (版本解析 bug)
- counts 某字段负值 (计数器溢出)
"""
from datetime import datetime, timezone

import pytest

# ─────────── required fields ───────────

REQUIRED_TOPLEVEL = {"generated_at", "version", "counts", "lists", "hooks"}

REQUIRED_COUNTS = {
    "skills", "workflows", "hooks_registered", "hook_events", "hook_files",
    "agents_total", "agents_core", "agents_ceo_roles", "agents_industry",
    "agents_teams", "plugin_skills", "plugin_agents", "mcp_servers",
    "enabled_plugins", "total_plugins", "rules", "intent_words_routes",
    "external_clis",
}

REQUIRED_VERSION_KEYS = {"claude_code", "omc", "stats_engine", "cc_switch"}

# key → expected Python type (实查 2026-06-29: skill_desc/skill_categories/workflow_map 是 dict)
REQUIRED_LISTS_ITEMS: dict[str, type] = {
    "priority_routes": list,
    "all_routes":      list,
    "skill_desc":      dict,
    "workflows":       list,
    "ceo_roles":       list,
    "core_agents":     list,
}

# sane bounds: (min_inclusive, max_inclusive) — wide enough to not need frequent updates
COUNTS_BOUNDS = {
    "skills":              (50, 500),
    "agents_total":        (50, 300),
    "hooks_registered":    (10, 200),
    "plugin_skills":       (100, 2000),
    "plugin_agents":       (50, 1000),
    "mcp_servers":         (1, 50),
    "enabled_plugins":     (5, 200),
    "intent_words_routes": (50, 500),
}

# counts fields that must be strictly positive (=0 → stats engine completely failed)
MUST_BE_POSITIVE = {
    "skills", "agents_total", "hooks_registered", "plugin_skills",
    "plugin_agents", "mcp_servers",
}


class TestStatsSchema:
    """mycc-stats.json 结构完整性守护."""

    def test_required_toplevel_keys(self, stats_json_local):
        """顶层必须含 5 个核心 key."""
        missing = REQUIRED_TOPLEVEL - set(stats_json_local.keys())
        assert not missing, f"stats.json 缺顶层字段: {missing}"

    def test_counts_is_dict(self, stats_json_local):
        """counts 必须是 dict (非 null / list / string)."""
        assert isinstance(stats_json_local["counts"], dict), (
            f"counts 类型错误: {type(stats_json_local['counts']).__name__}"
        )

    def test_required_counts_fields_present(self, stats_json_local):
        """counts 必须包含所有 18 个标准字段."""
        counts = stats_json_local["counts"]
        missing = REQUIRED_COUNTS - set(counts.keys())
        assert not missing, (
            f"counts 缺字段: {missing} — hermes 引擎可能重命名/删字段"
        )

    def test_all_counts_values_are_int(self, stats_json_local):
        """counts 每个值必须是 int (防止引擎 bug 写 null / string)."""
        counts = stats_json_local["counts"]
        bad = {k: type(v).__name__ for k, v in counts.items() if not isinstance(v, int)}
        assert not bad, (
            f"counts 字段类型非 int: {bad} — stats 引擎解析/写入 bug"
        )

    def test_counts_no_negative(self, stats_json_local):
        """counts 所有值 ≥ 0 (负值 = 计数器溢出或符号错)."""
        counts = stats_json_local["counts"]
        neg = {k: v for k, v in counts.items() if isinstance(v, int) and v < 0}
        assert not neg, f"counts 出现负值: {neg}"

    def test_must_be_positive_fields(self, stats_json_local):
        """核心展示字段必须 > 0 (=0 意味着 stats 引擎彻底失败)."""
        counts = stats_json_local["counts"]
        zeros = {k for k in MUST_BE_POSITIVE if counts.get(k, 1) == 0}
        assert not zeros, (
            f"核心字段为 0: {zeros} — stats 引擎计数失效, dashboard 会展示 0"
        )

    def test_counts_sane_bounds(self, stats_json_local):
        """关键字段必须在合理区间 (防 stats 引擎离谱偏差)."""
        counts = stats_json_local["counts"]
        violations = []
        for key, (lo, hi) in COUNTS_BOUNDS.items():
            val = counts.get(key)
            if val is not None and isinstance(val, int):
                if not (lo <= val <= hi):
                    violations.append(f"{key}={val} 超出合理区间 [{lo}, {hi}]")
        assert not violations, (
            "counts 字段超合理区间:\n  " + "\n  ".join(violations)
        )

    def test_version_structure(self, stats_json_local):
        """version 是 dict 且含 4 个标准 key, 值均为 string."""
        ver = stats_json_local.get("version", {})
        assert isinstance(ver, dict), f"version 类型错误: {type(ver).__name__}"
        missing = REQUIRED_VERSION_KEYS - set(ver.keys())
        assert not missing, f"version 缺 key: {missing}"
        bad_type = {
            k: type(ver[k]).__name__
            for k in REQUIRED_VERSION_KEYS
            if k in ver and not isinstance(ver[k], str)
        }
        assert not bad_type, f"version 字段非 string: {bad_type}"

    def test_lists_structure(self, stats_json_local):
        """lists 是 dict 且含必须 key, 每个 key 的值类型与 schema 一致."""
        lst = stats_json_local.get("lists", {})
        assert isinstance(lst, dict), f"lists 类型错误: {type(lst).__name__}"
        missing = set(REQUIRED_LISTS_ITEMS) - set(lst.keys())
        assert not missing, f"lists 缺 key: {missing}"
        wrong_type = {
            k: f"期望 {expected.__name__}, 实际 {type(lst[k]).__name__}"
            for k, expected in REQUIRED_LISTS_ITEMS.items()
            if k in lst and not isinstance(lst[k], expected)
        }
        assert not wrong_type, f"lists 字段类型错误: {wrong_type}"

    def test_generated_at_iso_format(self, stats_json_local):
        """generated_at 必须是合法 ISO 8601 字符串 (非空, 能被 datetime 解析)."""
        ts = stats_json_local.get("generated_at", "")
        assert isinstance(ts, str) and ts, "generated_at 空或非 string"
        try:
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError as e:
            pytest.fail(f"generated_at={ts!r} 无法解析为 ISO 8601: {e}")

    def test_hooks_field_type(self, stats_json_local):
        """hooks 顶层字段存在且类型合法 (list 或 dict)."""
        hooks = stats_json_local.get("hooks")
        assert hooks is not None, "stats.json 缺 hooks 顶层字段"
        assert isinstance(hooks, (list, dict)), (
            f"hooks 类型错误: {type(hooks).__name__}"
        )
