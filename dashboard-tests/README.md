# dashboard-tests/ · Dashboard 契约测试套件

> P0 立竿见影 (2026-06-29)：QA-strategist #1 数字契约 pytest 占位骨架
> 5 路综合方案接力包：`~/.claude/memory/teleport-20260629-5ways.md`

## 目录结构

```
dashboard-tests/
├── .gitignore           # 排除 venv + pytest cache + omc runtime
├── README.md            # 本文件
├── test_anchor_contract.py   # v0.1 占位契约测试 (11 tests, 全 PASS)
└── .venv/               # 本地 Python 虚拟环境（不入 git）
```

## 快速上手

```bash
# 1. 建 venv (一次性)
python3 -m venv dashboard-tests/.venv

# 2. 激活 + 装依赖
source dashboard-tests/.venv/bin/activate
pip install pytest requests

# 3. 跑测试
pytest dashboard-tests/ -v

# 预期: 11 passed in <1s
```

## 当前覆盖 (v0.1 占位)

`test_anchor_contract.py` 11 个测试:

| Test Class | 数量 | 覆盖 |
|---|---|---|
| `TestAnchorContract` | 5 | dashboard.html 存在 / 13 section / div 锚点 / nav-link 对应 / 无重复 id |
| `TestNumericAnchors` | 5 (parametrized) | 关键数字（70/100 / D3 72 / 149 / 58 / L0）必须在声明它的 section 内 |
| `TestHttpServing` | 1 | serve-gzip server 18766 优雅降级（不在跑则 skip） |

## 已知抓到的真实 bug

v0.1 第一次跑就抓到：
- `s-catalog` 是 `<div>` 不是 `<section>` —— 暴露锚点类型混用

## 下次 session 扩写方向 (P1-1)

按 QA-strategist #1 完整方案扩写到 v1.0：
- `test_stats_parity.py` (新)：mycc-stats.json 实时字段 vs FALLBACK_COUNTS diff
- `test_dashboard_self_audit.py` (新)：12 个锚点数字 + generated_at age ≤ 7d

详见接力包 §4.1。