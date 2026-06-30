# board-tasks.json 集成契约 —— 交 session 6861ca48 集成"任务todo"看板菜单

> 数据层由 session ed0a1389 完成（`~/.claude/lib/board.py` 单向投影）。本文档供 dashboard owner 集成。
> 2026-06-29 · 数据已就绪（`curl http://127.0.0.1:18765/board-tasks.json` → 200）

## 数据源与更新机制
- 数据文件：`board-tasks.json`（本目录，与 `mycc-stats.json` 同级）
- 单向投影：`~/.claude/docs/project-ledger.json`(本机SSoT) → `board-tasks.json`(dashboard只读)
- 自动更新：`board.py` 每次写操作（done/doing/note/add）自动 export；也可 `python3 ~/.claude/lib/board.py export` 手动
- **铁律：dashboard 端只读 fetch，禁反向写**（单向投影）

## JSON 结构（顶层 10 keys）
| key | 内容 | 形式建议 |
|---|---|---|
| `meta` | updated / generated_at / source / counts(各维度统计) | 头部信息 |
| `kanban` | {待规划:[], 待办:[], 进行中:[], 审核中:[]} | **Linear 四列看板**(参考图) |
| `milestones` | [{id,title,status,evidence}] | 里程碑时间线 |
| `blockers` | [{id,title,ref}] | 卡点列表 |
| `requirements` | [card] 30条 | 需求分组表(可折叠) |
| `wbs` / `subplans` | [card] | 表格(可折叠) |
| `notes` | [{date,note}] 最近20 | 思考/决策轨迹 |
| `memory_system` | {total_files:237, categories:[{name,count}], locations:[]} | ⑥记忆系统位置 |
| `closure` | {with_evidence, without_evidence, total} | ⑦闭环收口统计 |

卡片字段：`{id, title, group, status, status_label, evidence, closure_badge, blocker}`
- `closure_badge`：`已验证(commit)` / `有记录` / `待补证据`（从 evidence 自动判定）

## 5 status → 4 列映射
| board status | Linear 列 |
|---|---|
| todo | 待办 |
| doing / partial | 进行中 |
| done | 审核中 |
| blocked | 待规划 |

## 集成步骤（dashboard owner）
1. 加 nav-link "任务todo" → `#s-tasks`（**nav 契约 15→16，更新 nav 测试**）
2. 加 `<section class="section container" id="s-tasks">`（**section rhythm 契约 12→13，更新 section 测试**）
3. JS `fetch('board-tasks.json', {cache:'no-store'})` —— 参考现有 `mycc-stats.json` fetch 模式（dashboard.html L1428）
4. 渲染：四列看板 + 里程碑 + 卡点 + 需求表 + 记忆系统 + 闭环统计
5. 版本号 cache-bust `?v=` 更新
6. Playwright 测试：fetch 成功 + 四列渲染 + 截图为证

## IA 建议（产品专家 · 防信息过载，6861ca48 曾因 IA 过载被打回）
- **三层折叠**：默认展示「四列看板 + 里程碑」；「卡点/需求表/WBS/记忆系统/闭环」折叠可展开
- 非专业用户视角：突出「进行中」+「卡点」（最需关注），需求表默认折叠

## 已验证
- `python3 ~/.claude/lib/board.py export` → board-tasks.json 生成 ✅
- board.smoke.sh 12/12 ✅
- `curl http://127.0.0.1:18765/board-tasks.json` → HTTP 200 ✅
- 字段完整：kanban 四列 / 30需求 / 4里程碑 / 8卡点 / 5记忆分类237文件 / closure 30/30

---

## v7 多维度更新 (2026-06-30)

### 9 字段扩 (board.py _card 自动 fallback)

| 字段 | 类型 | 默认 | 来源 |
|---|---|---|---|
| `session_id` | string | "" | TODO |
| `session_name` | string | "" | TODO |
| `project_id` | string | "" | TODO |
| `parent_id` | string | "" | TODO |
| `created_at` | ISO8601 | "" | TODO |
| `updated_at` | ISO8601 | "" | TODO |
| `due_date` | ISO8601 | "" | TODO |
| `completed_at` | ISO8601 | "" | TODO |
| `priority` | enum | "medium" | TODO |

### 4 维度 UI (v7 Phase 3)
- **session chip**: 卡片头部小字 tag (📍 + session_name)
- **priority 色块**: 左上角 8px 圆点 (urgent 红/high 橙/medium 蓝/low 灰)
- **时间戳**: 卡片底部 (created_at → due_date 格式) + overdue 红高亮
- **filter 栏**: 全部优先级 + 全部 session 下拉 (applyBoardFilters)

### micro-server 写回通道 (v7 Phase 2 · 端口 18767)
- `bin/board-bridge.py` 50 行 stdlib
- POST `/api/board/health` / `update_status` / `add_note` / `create_task`
- 调 board.py 子命令 (done/doing/todo/partial/block/note/add) → 自动 atomic write + 投影
- lockfile: `~/.omc/snapshots/board-bridge.lock` (5min TTL)

### 反讽 R1 铁律
- ⚠️ 直写 `board-tasks.json` 违反单向投影 → 必须走 board.py
- ⚠️ 18767 端口唯一可用 (18765=Playwright / 18766=dashboard conftest)
- ⚠️ board.py 子命令无通用 update → micro-server 简化为 update_status + add_note
- ⚠️ 9 字段 MVP 限制, 不引 labels / assignee / cycle (v8+)

### 测试契约
- 275 passed / 3 skipped (257 + 18 v7 测试)
- Playwright 18765 实测 0 error

### 启动 micro-server
```bash
python3 bin/board-bridge.py --port 18767
# 健康检查
curl -X POST http://127.0.0.1:18767/api/board/health
```
