"""test_validate_stats.py · lib/validate-stats.py 守护 (2026-06-29 M1-2)

补位 dashboard-tests/test_stats_schema.py (静态测结构);
本测试测 validator 函数本身: 输入边界 + 错误信息可读性.
"""
import sys, json, subprocess, tempfile, os, importlib.util
from pathlib import Path

# 直接 importlib 加载 lib/validate-stats.py (绕过 sys.path 顺序问题)
_LIB_PATH = Path(__file__).resolve().parent.parent / "lib" / "validate-stats.py"
_spec = importlib.util.spec_from_file_location("validate_stats", _LIB_PATH)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["validate_stats"] = _mod
_spec.loader.exec_module(_mod)
validate_stats = _mod.validate_stats


def _stats(**overrides):
    """最小有效 stats 字典 + 按需覆盖字段."""
    s = {
        "generated_at": "2026-06-29T10:00:00Z",
        "version": {"claude_code": "2.1.195", "omc": "4.15.0", "stats_engine": "V53", "cc_switch": "OFF"},
        "counts": {
            "skills": 149, "workflows": 14, "hooks_registered": 42, "hook_events": 14, "hook_files": 58,
            "agents_total": 91, "agents_core": 6, "agents_ceo_roles": 12, "agents_industry": 7,
            "agents_teams": 6, "plugin_skills": 419, "plugin_agents": 164, "mcp_servers": 4,
            "enabled_plugins": 32, "total_plugins": 58, "rules": 3, "intent_words_routes": 133,
            "external_clis": 3,
        },
        "lists": {}, "hooks": {},
    }
    # 深度 merge (简化版: 只覆盖顶层)
    for k, v in overrides.items():
        if k in ("missing_toplevel", "missing_counts", "missing_version", "zero_field"):
            continue
        s[k] = v
    if "missing_toplevel" in overrides:
        for k in overrides["missing_toplevel"]:
            s.pop(k, None)
    if "missing_counts" in overrides:
        for k in overrides["missing_counts"]:
            s["counts"].pop(k, None)
    if "missing_version" in overrides:
        for k in overrides["missing_version"]:
            s["version"].pop(k, None)
    if "zero_field" in overrides:
        for k in overrides["zero_field"]:
            s["counts"][k] = 0
    return s


class TestValidateStats:
    def test_valid_stats_returns_empty(self):
        """完整合法 stats 应返回空 errors."""
        assert validate_stats(_stats()) == []

    def test_missing_toplevel_key(self):
        """缺 generated_at 应报错."""
        errs = validate_stats(_stats(missing_toplevel=["generated_at"]))
        assert any("generated_at" in e or "top-level" in e for e in errs), f"unexpected: {errs}"

    def test_missing_counts_field(self):
        """counts 缺 skills 应报错."""
        errs = validate_stats(_stats(missing_counts=["skills"]))
        assert any("counts missing" in e and "skills" in e for e in errs), f"unexpected: {errs}"

    def test_missing_version_field(self):
        """version 缺 cc_switch 应报错."""
        errs = validate_stats(_stats(missing_version=["cc_switch"]))
        assert any("version missing" in e and "cc_switch" in e for e in errs), f"unexpected: {errs}"

    def test_zero_skill_field_caught(self):
        """skills=0 应被 MUST_BE_POSITIVE 捕获."""
        errs = validate_stats(_stats(zero_field=["skills"]))
        assert any("skills must be > 0" in e for e in errs), f"unexpected: {errs}"

    def test_root_not_dict(self):
        """根非 dict 应立刻报错不抛."""
        errs = validate_stats("not a dict")
        assert any("root must be dict" in e for e in errs)

    def test_counts_not_dict(self):
        """counts 被改成 list 应报错."""
        s = _stats(counts=[])
        errs = validate_stats(s)
        assert any("counts must be dict" in e for e in errs)

    def test_cli_runs_on_real_stats(self):
        """CLI 模式对仓库真实 mycc-stats.json 跑通."""
        real = Path(__file__).resolve().parent.parent / "mycc-stats.json"
        if not real.exists():
            import pytest
            pytest.skip("mycc-stats.json 不存在 (hermes 未跑)")
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent / "lib" / "validate-stats.py"), str(real)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"validate-stats CLI failed: {result.stderr}"
        assert "[OK]" in result.stdout

    def test_cli_catches_corrupt_json(self):
        """CLI 对损坏 JSON 应返回非 0 exit code."""
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{invalid json")
            corrupt_path = f.name
        try:
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parent.parent / "lib" / "validate-stats.py"), corrupt_path],
                capture_output=True, text=True,
            )
            assert result.returncode != 0, "corrupt JSON 应该返回非 0"
            assert "cannot parse" in result.stderr
        finally:
            os.unlink(corrupt_path)