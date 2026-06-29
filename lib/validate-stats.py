#!/usr/bin/env python3
"""validate-stats.py · mycc-stats.json schema 守护 (runtime + write-time 共用)

来源: 2026-06-29 专家组 plan M1-2 (修正版, 最小可交付)
- 与 dashboard-tests/test_stats_schema.py (157 行, 18+1 字段) 互补
- 该模块用于 runtime/dashboard 启动时 / hermes 写前快速校验
- 返回 errors list (空 = 通过); 不抛异常, 让 caller 决定处置 (warn / 阻断)

设计原则:
- KISS: 不引入 jsonschema 依赖 (避免 pip install)
- YAGNI: 只覆盖 mycc-stats.json (最大文件), 不覆盖 dashboard-details.json / board-tasks.json
- Fail-quietly: errors 留痕到 stderr, 不阻断 hermes 主流程 (灰度期 2 周)
"""
from __future__ import annotations
import sys, json
from typing import Any

# 必须顶层 (SSoT: 与 mycc-stats.py 字段定义同步)
REQUIRED_TOPLEVEL = {"generated_at", "version", "counts", "lists", "hooks"}
REQUIRED_COUNTS = {
    "skills", "workflows", "hooks_registered", "hook_events", "hook_files",
    "agents_total", "agents_core", "agents_ceo_roles", "agents_industry",
    "agents_teams", "plugin_skills", "plugin_agents", "mcp_servers",
    "enabled_plugins", "total_plugins", "rules", "intent_words_routes",
    "external_clis",
}
REQUIRED_VERSION = {"claude_code", "omc", "stats_engine", "cc_switch"}

# 字段必须为正数 (=0 表示 stats engine 完全失败)
MUST_BE_POSITIVE = {
    "skills", "agents_total", "hooks_registered",
    "plugin_skills", "plugin_agents", "mcp_servers",
}


def validate_stats(stats: Any) -> list[str]:
    """校验 stats dict. 返回 errors (空 list = 通过)."""
    errors: list[str] = []
    if not isinstance(stats, dict):
        return [f"root must be dict, got {type(stats).__name__}"]

    # 顶层
    missing = REQUIRED_TOPLEVEL - set(stats.keys())
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")

    # counts
    counts = stats.get("counts")
    if not isinstance(counts, dict):
        errors.append(f"counts must be dict, got {type(counts).__name__}")
    else:
        missing_c = REQUIRED_COUNTS - set(counts.keys())
        if missing_c:
            errors.append(f"counts missing fields: {sorted(missing_c)}")
        # 正数检查
        for k in MUST_BE_POSITIVE:
            v = counts.get(k)
            if v is not None and isinstance(v, (int, float)) and v <= 0:
                errors.append(f"counts.{k} must be > 0, got {v}")

    # version
    version = stats.get("version")
    if not isinstance(version, dict):
        errors.append(f"version must be dict, got {type(version).__name__}")
    else:
        missing_v = REQUIRED_VERSION - set(version.keys())
        if missing_v:
            errors.append(f"version missing keys: {sorted(missing_v)}")

    return errors


def main() -> int:
    """CLI 入口: validate-stats.py <path> [path2 ...]"""
    if len(sys.argv) < 2:
        print("usage: validate-stats.py <stats.json> [stats2.json ...]", file=sys.stderr)
        return 2
    total_errors = 0
    for path in sys.argv[1:]:
        try:
            with open(path) as f:
                stats = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[FAIL] {path}: cannot parse ({type(e).__name__}: {e})", file=sys.stderr)
            total_errors += 1
            continue
        errs = validate_stats(stats)
        if errs:
            print(f"[FAIL] {path}:", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            total_errors += len(errs)
        else:
            print(f"[OK]   {path}")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())