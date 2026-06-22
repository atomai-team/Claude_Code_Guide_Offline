# Claude Code 专业 PM 配置文档
## CMMI Level 3 格式 · 完整配置方案说明
> CLI v2.1.185 · OMC 4.14.7 · 2026-06-22
> 适用对象：项目 PM、技术负责人、CTO、创业团队全员

---

## 一、需求说明（Requirements Specification）

### 1.1 系统总体目标

| 维度 | 目标描述 |
|---|---|
| **效率** | 个人开发效率提升 5-10x；团队协作效率提升 3-5x |
| **质量** | 代码安全性提升（OWASP 自动检测）；文档完整性 >90% |
| **交付** | 从需求到上线平均周期缩短 40-60% |
| **知识** | 项目决策和错误模式 100% 落库，跨会话可复用 |

### 1.2 核心用户角色与需求

**角色 1：CEO/创始人**
- 需求：30分钟内生成完整商业分析（竞品/财务/风险/路线图）
- 触发方式：`/ceo-pipeline` 或 说 "帮我分析这个商业机会"
- 产出物：市场规模报告 + 竞品矩阵 + 财务预测 + 融资材料框架

**角色 2：产品经理**
- 需求：需求文档化、技术拆解、用户故事生成、优先级排序
- 触发方式：说 "帮我把这个需求拆解成开发任务"
- 产出物：PRD、用户故事、RICE 优先级表、验收标准（BDD）

**角色 3：技术负责人**
- 需求：架构决策、代码审查、安全审计、技术债务管理
- 触发方式：`/code-review ultra` 或 `/security-audit`
- 产出物：架构 ADR、安全报告、技术债务清单、重构方案

**角色 4：全栈开发**
- 需求：功能开发、Bug 修复、测试覆盖、部署自动化
- 触发方式：说 "队长，把 XX 功能做完" 或 "tdd 模式开发"
- 产出物：可运行代码 + 测试 + CI/CD 配置 + 部署脚本

**角色 5：增长/运营**
- 需求：内容生产、SEO 优化、数据分析、营销自动化
- 触发方式：`/content-engine` 或 `/marketing`
- 产出物：内容矩阵 + SEO 报告 + 增长实验清单

---

### 1.3 功能需求清单（FR）

#### FR-01 开发能力（必须 MUST）

| ID | 需求 | 验收标准 | 当前状态 |
|---|---|---|---|
| FR-01-01 | 全栈功能开发 | 从描述到可运行代码，覆盖前后端数据库 | ✅ feature-dev skill |
| FR-01-02 | TDD 开发流程 | 红→绿→重构三阶段，有失败测试证据 | ✅ tdd 关键词 |
| FR-01-03 | 自动代码审查 | OWASP + 代码质量 + 逻辑错误，可发 PR 评论 | ✅ /code-review |
| FR-01-04 | 安全审计 | STRIDE 威胁建模 + OWASP Top 10 + P0/P1/P2 | ✅ /security-audit |
| FR-01-05 | 数据库设计 | ER 图 + 建表 SQL + 索引 + 迁移脚本 | ✅ 通用能力 |
| FR-01-06 | CI/CD 配置 | GitHub Actions 自动测试+部署，含回滚 | ✅ /gh-ci-fix |

#### FR-02 调研能力（必须 MUST）

| ID | 需求 | 验收标准 | 当前状态 |
|---|---|---|---|
| FR-02-01 | 深度多渠道调研 | ≥5 渠道，官方文档+社区+视频，有来源有结论 | ✅ /deep-research |
| FR-02-02 | 实时官方文档 | 任何库/框架/API 的最新文档即时查询 | ✅ context7 MCP |
| FR-02-03 | GitHub 仓库分析 | 搜索代码/PR/Issues，深度分析高星仓库 | ✅ github MCP |
| FR-02-04 | 网页抓取分析 | 竞品官网/文档/新闻的深度内容提取 | ✅ firecrawl MCP |
| FR-02-05 | 商业竞品分析 | 功能矩阵/定价/差异化，含★推荐选型 | ✅ /ceo-pipeline |

#### FR-03 协作与管理（应该 SHOULD）

| ID | 需求 | 验收标准 | 当前状态 |
|---|---|---|---|
| FR-03-01 | 项目任务管理 | 与 Linear 双向同步，自动创建/更新 issue | ✅ linear MCP |
| FR-03-02 | GitHub PR 管理 | 创建 PR/审查/发评论/合并，全流程 | ✅ github MCP |
| FR-03-03 | 知识库管理 | 与 Notion 4 个数据库双向同步 | ✅ Notion MCP |
| FR-03-04 | 设计稿读取 | 直接读取 Figma 设计规范，生成代码 | ✅ figma MCP |
| FR-03-05 | 文档生成 | 自动生成 Word/PPT/PDF 格式文档 | ✅ Office MCP + PDF MCP |

#### FR-04 自动化与集成（可以 CAN）

| ID | 需求 | 验收标准 | 当前状态 |
|---|---|---|---|
| FR-04-01 | 浏览器自动化 | E2E 测试 + 截图验证 + 表单操作 | ✅ playwright MCP |
| FR-04-02 | 桌面操作自动化 | macOS 系统操作 + 应用控制 | ✅ computer-use MCP |
| FR-04-03 | 邮件处理 | Gmail 搜索/回复/标记，自动化邮件工作流 | ✅ Gmail MCP |
| FR-04-04 | 日历管理 | Google Calendar 查看/创建，会议材料自动准备 | ✅ Calendar MCP |
| FR-04-05 | 外部 AI 对抗 | 调用 Gemini/Kimi/MiniMax 多模型并发验证 | ✅ ai-panel.sh |

---

### 1.4 非功能性需求（NFR）

| 类别 | 需求 | 指标 |
|---|---|---|
| **性能** | 单任务响应时间 | 简单查询 <10s；复杂开发任务 <5min |
| **并发** | 并行 agent 数 | 默认 8-16，YOLO 模式 15 |
| **准确性** | 事实断言准确率 | 关键数据必须 `gh api`/官方文档核实 |
| **安全** | 配置保护 | settings.local.json 受 hook 保护；API Key 不暴露 |
| **可用性** | 断点续接 | `/compact` 压缩上下文；`/cd` 切目录不重开 |
| **可追溯** | 决策记录 | 所有架构决策生成 ADR；任务产物归档 `archive/tasks/` |

---

## 二、配置方案说明（Configuration Plan）

### 2.1 当前配置总览

```
┌─────────────────────────────────────────────────────┐
│               Claude Code 配置层级                   │
├─────────────────────────────────────────────────────┤
│ L1 模型层  │ sonnet 4.6（标准）/ opus 4.8（深度）    │
│            │ haiku 4.5（快速查询）                   │
├─────────────────────────────────────────────────────┤
│ L2 规则层  │ ~/.claude/CLAUDE.md（全局指令）         │
│            │ ~/.claude/rules/*.md（12 核心铁律）     │
│            │ 项目 CLAUDE.md（项目级规则）            │
├─────────────────────────────────────────────────────┤
│ L3 Hook层  │ 50+ 自动守护钩子（全生命周期覆盖）      │
│            │ 安全/质量/记忆/配置保护/并发防护        │
├─────────────────────────────────────────────────────┤
│ L4 Skill层 │ 151 个专项技能（本地 ~/.claude/skills/）│
│            │ 10 个 Workflow JS 脚本                  │
├─────────────────────────────────────────────────────┤
│ L5 MCP层   │ 4 个核心 MCP（settings.local.json）     │
│            │ 12 个 Desktop Extensions               │
│            │ 插件提供的 ~10 个 MCP                   │
├─────────────────────────────────────────────────────┤
│ L6 外部AI  │ Gemini/Kimi/MiniMax（对抗验证）         │
└─────────────────────────────────────────────────────┘
```

### 2.2 MCP 服务器配置清单

#### 核心 MCP（settings.local.json 配置）

| 服务器 | 用途 | 关键工具 |
|---|---|---|
| **github** | GitHub 全操作 | search_code, list_pull_requests, add_issue_comment, create_pull_request, run_secret_scanning |
| **context7** | 官方文档即时查询 | query-docs, resolve-library-id |
| **playwright** | 浏览器自动化 | browser_navigate, browser_take_screenshot, browser_fill_form, browser_network_requests |
| **linear** | 项目管理 | 创建/更新 issue, sprint 管理 |

#### Desktop Extensions MCP

| 扩展 | 说明 | 最佳用途 |
|---|---|---|
| **chrome-control** | Chrome 浏览器控制 | 网页截图、用户行为模拟 |
| **filesystem** | 文件系统操作 | 批量文件处理、目录管理 |
| **figma** | 设计稿读取 | 设计规范提取、UI 开发 |
| **ms_office_powerpoint** | PPT 创建/编辑 | 投资人 BP、技术汇报 |
| **ms_office_word** | Word 文档 | 合同模板、技术文档 |
| **pdf-server-mcp** | PDF 处理 | 合同/报告内容提取 |
| **macos-mcp** | macOS 系统 | 自动化系统操作 |
| **computer-use** | 桌面控制 | 任何桌面应用操作 |
| **kapture** | 屏幕录制 | 操作录制、培训材料 |
| **iMessage** | iMessage | 消息自动化 |

#### 插件提供的 MCP

| MCP | 来源 | 用途 |
|---|---|---|
| **Notion** | claude-plugins-official | CMMI 4 数据库（任务/需求/错误/版本）|
| **firecrawl** | claude-plugins-official | 深度网页抓取/竞品分析 |
| **semgrep** | claude-plugins-official | SAST 安全扫描 |
| **chrome-devtools** | claude-plugins-official | 性能分析/前端调试 |
| **Gmail** | claude.ai | 邮件自动化 |
| **Google Calendar** | claude.ai | 日程管理 |
| **Google Drive** | claude.ai | 文件协作 |
| **memory** | OMC | 知识图谱记忆 |
| **sequential-thinking** | OMC | 结构化推理 |
| **qmd** | OMC | 本地文档搜索（264页）|

---

### 2.3 Hook 守护体系（50+ 钩子）

| 类别 | 关键 Hook | 守护对象 |
|---|---|---|
| **安全守护** | block-sensitive-files.sh | 禁止意外修改 settings.local.json 等敏感文件 |
| | direct-connect-guard.sh | 防止代理污染（CC Switch 自动修复）|
| | env-sentinel.sh | SubagentStart 前扫描环境变量污染 |
| | config-protection.sh | 防止弱化 linter/安全配置 |
| **质量守护** | llm-judge-completion.sh | Stop 时校验完成证据质量 |
| | uncertainty-detector.sh | 检测"应该可以了"等不确定词 |
| | error-circuit-breaker.sh | 同方法失败 2 次触发方法论切换 |
| **记忆守护** | drift-check.sh | SessionStart 时扫配置漂移 |
| | session-archive-spec.sh | 任务完成后自动归档产物 |
| **并发守护** | serial-bash-circuit.sh | 超过 3 次串行 Bash 触发警告 |
| | multi-session-guard.sh | 多 Session 同时编辑同一文件防冲突 |
| **提示守护** | clarity_scorer.py | 模糊度评分，高歧义触发澄清 |
| | retrieval-precheck.sh | 问题类 prompt 先查本地记忆 |
| | official-paradigm-guard.sh | 改原生机制前提醒查官方文档 |

---

### 2.4 权限与安全配置

#### 核心安全原则

```
✅ 官方直连：不设 ANTHROPIC_BASE_URL / ANTHROPIC_API_KEY
✅ 敏感文件保护：settings.local.json 受 block-sensitive-files.sh 保护
✅ 配置白名单保护：deny 规则 29 条（OWASP + 高危系统操作）
✅ 环境变量清洁：设 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS + ENABLE_TOOL_SEARCH
✅ 多端同步：CLI 主力(100%) + Desktop 辅助(~70%)
```

#### 权限模式说明

| 模式 | 适用场景 | 风险 | 触发方式 |
|---|---|---|---|
| **默认模式** | 日常开发，需要精细控制 | 最低 | 直接启动 |
| **acceptEdits** | 文件编辑密集型任务 | 低 | 系统自动 |
| **YOLO L4** | 信任完整工作流，全自动 | 中 | "火力全开" |
| **bypassPermissions** | 极限档，生产不建议 | 高 | 显式启动参数 |

---

## 三、专业能力说明（Capabilities Specification）

### 3.1 核心能力矩阵

| 能力域 | 具体能力 | 成熟度 | 触发方式 |
|---|---|---|---|
| **代码开发** | 全栈开发 / TDD / 重构 / 调试 | ★★★★★ | 直接描述需求 |
| **安全** | OWASP / STRIDE / 代码扫描 / 合规 | ★★★★☆ | /security-audit |
| **调研分析** | 多渠道调研 / 竞品分析 / 技术选型 | ★★★★★ | /deep-research |
| **文档产出** | PRD / 架构文档 / API 文档 / ADR | ★★★★★ | 直接描述 |
| **项目管理** | 任务拆解 / 进度追踪 / Linear 同步 | ★★★★☆ | /cmmi-tracker |
| **商业分析** | 市场/竞品/财务/风险/路线图 | ★★★★☆ | /ceo-pipeline |
| **UI/UX** | 设计稿读取 / 组件开发 / 设计系统 | ★★★★☆ | /ui-ux-pro-max |
| **部署运维** | CI/CD / 容器化 / 云部署 / 监控 | ★★★★☆ | /deploy-ship |
| **内容创作** | SEO / 营销文案 / 技术文章 | ★★★★☆ | /content-engine |
| **测试** | E2E / 压测 / 安全测试 / 混沌 | ★★★★☆ | /ultraqa |

---

### 3.2 工作流程规范（Process Workflows）

#### WF-01 标准功能开发流程

```
1. 需求澄清（铁律 11）
   └─ clarity_scorer.py 评分 → 模糊度 <0.5 先澄清

2. 规划阶段（Step 1）
   └─ 影响 ≥3 文件 → 生成 plans/{slug}.md
   └─ 包含：Why/关键文件/执行顺序/验证方法/回滚路径

3. 并行实现（Step 2）
   └─ ≥2 独立子任务 → Agent/Workflow 并行
   └─ 前端+后端 → OMC team 协作

4. 质量门控（Step 4）
   ├─ Gate 1: 测试/lint/typecheck
   ├─ Gate 2: 实际运行证据（截图/CLI 输出）
   ├─ Gate 3: 边界检查（空值/超限/并发）
   └─ Gate 4: git diff --stat 确认影响面

5. 代码审查（铁律 10, Writer≠Reviewer）
   └─ /code-review --fix（独立 reviewer agent）

6. 归档（铁律 4）
   └─ archive-task.py 归档产物到 archive/tasks/
   └─ 重要决策 → 推送 Notion 任务库
```

#### WF-02 Bug 修复流程

```
1. 问题定位
   └─ 系统性错误分析（说"又报错"触发）
   └─ 5-Why 根因分析

2. 假说验证（铁律 8：先查再断言）
   └─ 禁止推测，必须 ls/grep/实跑取证据

3. 精准修复（铁律 8 K2）
   └─ 只改必要的，禁止顺手重构

4. 变更闭环（铁律 3 六步）
   PRE-SCAN → EXECUTE → PROPAGATE →
   ADVERSARIAL → EVIDENCE → SUBAGENT-EVIDENCE

5. 失败 2 次切方法论（铁律 9）
   └─ error-circuit-breaker.sh 自动触发
```

#### WF-03 商业分析流程（/ceo-pipeline）

```
Phase 1：市场分析
  └─ TAM/SAM/SOM 市场规模
  └─ 市场趋势 + 时机分析

Phase 2：竞品分析
  └─ 10 个主要竞品功能矩阵
  └─ 定价策略对比
  └─ 差异化机会识别

Phase 3：产品策略
  └─ 用户画像 + Jobs-to-be-Done
  └─ MVP 功能清单 + RICE 排序
  └─ 产品路线图（3 个月/6 个月/12 个月）

Phase 4：财务建模
  └─ 单位经济学（CAC/LTV/Payback）
  └─ 三情景预测（悲/基/乐）
  └─ 融资需求测算

Phase 5：风险评估
  └─ SWOT 分析
  └─ 关键假设 + 风险矩阵
  └─ 应对预案

Phase 6：执行路线图
  └─ 里程碑拆解
  └─ 团队需求
  └─ 融资时间线
```

---

### 3.3 质量保证体系（QA Framework）

#### 代码质量层级

```
L1 静态分析
  ├─ semgrep MCP（SAST 扫描）
  ├─ /security-review（OWASP）
  └─ linter/formatter（config-protection.sh 防弱化）

L2 动态测试
  ├─ /code-review（逻辑/安全/性能三维）
  ├─ playwright MCP（E2E 自动化）
  └─ chrome-devtools MCP（性能/内存）

L3 审查验证
  ├─ /code-review ultra（云端多 agent 审查）
  ├─ /judge-panel（多视角评审面板）
  └─ ai-panel.sh（跨模型对抗验证）

L4 持续监控
  ├─ /canary-monitor（指标监控）
  ├─ /observability-and-instrumentation
  └─ /self-evolve-loop（月度自我进化）
```

#### 验收标准（CMMI Level 3）

每个任务完成前必须满足：
- [ ] 有实际运行证据（截图/CLI输出/API响应）
- [ ] 有单元/集成测试（或明确说明为何豁免）
- [ ] 有回滚路径（git stash / git revert）
- [ ] 有变更影响面说明（git diff --stat）
- [ ] 复杂任务有 ADR（Architecture Decision Record）
- [ ] 产物已归档（archive/tasks/ 或 Notion 任务库）

---

### 3.4 知识管理体系

#### 四层记忆架构

```
L1 会话记忆（当前 session）
  └─ 对话上下文 + /compact 压缩保留

L2 项目记忆（跨会话）
  ├─ CLAUDE.md（项目级指令）
  ├─ .omc/project-memory.json
  └─ .omc/notepad.md

L3 全局记忆（跨项目）
  ├─ ~/.claude/projects/*/memory/MEMORY.md
  └─ ~/.remember/*.md（自动叙述）

L4 云端记忆（持久化协作）
  ├─ Notion 任务库（CMMI PP/PMC）
  ├─ Notion 需求库
  ├─ Notion 错误库
  └─ Notion 版本库
```

#### 知识检索顺序（检索前置，铁律 5）

```
L1 本机检索（自动）
  ├─ retrieval-precheck.sh hook（自动注入）
  └─ qmd search（264 页 Markdown 本地库）

L2 云端检索（按需）
  ├─ Notion CMMI 4DB
  └─ .omc/wiki/（801 页 wiki）

L3 官方文档（按需）
  └─ context7 MCP（任何库的最新文档）

L4 网络调研（按需）
  └─ firecrawl MCP + /v29-deep-research
```

---

## 四、配置验证清单（Verification Checklist）

### 快速健康检查

```bash
# 1. 版本一致性检查
python3 ~/.claude/lib/version-consistency-check.py --json

# 2. 环境变量清洁度
python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('ENV keys:', list(d.get('env',{}).keys()))"
# 期望：只有 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 和 ENABLE_TOOL_SEARCH

# 3. Hook 可执行性检查
find ~/.claude/hooks -name "*.sh" ! -perm -111

# 4. 配置漂移检查
python3 ~/.claude/lib/unify-config-drift.py --dry-run

# 5. Skills 可用性
# 在 Claude Code 中说 "帮我列出所有可用 skills"
```

### 配置分级评分（Harness 六层）

| 层级 | 检查点 | 评分方法 |
|---|---|---|
| L1 配置完整性 | settings.json / settings.local.json 规范 | /config-audit-better |
| L2 Hook 覆盖率 | 50+ 生命周期钩子注册数 | version-consistency-check.py |
| L3 Skill 健康度 | 151 skills 可达率 | /omc-doctor |
| L4 MCP 连通性 | 4+12 MCP 在线状态 | claude --safe-mode 测试 |
| L5 记忆完整性 | MEMORY.md + Notion 同步状态 | grep MEMORY.md 行数 |
| L6 进化能力 | /self-evolve-loop 可运行 | /self-evolve-loop 测试运行 |

---

## 五、常见配置问题 FAQ

**Q：Agent 调用立即失败怎么办？**
```bash
# 检查是否是 CC Switch 污染
python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print([k for k in d.get('env',{}) if k.startswith('ANTHROPIC')])"
# 有输出 = 污染，需要清理后重启 Claude
```

**Q：/code-review ultra 和普通 /code-review 区别？**
- 普通：本地单 agent 审查，快（30s），覆盖主要问题
- ultra：云端多 agent 并行审查，慢（3-5min），覆盖率更高

**Q：什么时候用 /compact 什么时候用 /clear？**
- `/compact`：对话太长，但还在同一个任务里，保留压缩摘要继续
- `/clear`：完全换了个任务，或对话上下文已经混乱，干净重开

**Q：飞书集成怎么配？**
- 通过 Claude Code 写集成脚本：飞书 Webhook → 触发 Claude → 回调飞书群
- 暂无原生飞书 MCP，通过 osascript MCP 或自写脚本实现

**Q：怎么让团队所有人用同一套配置？**
```bash
# 1. 将 ~/.claude/CLAUDE.md 和 rules/ 提交到团队 git 仓库
# 2. 项目根目录的 CLAUDE.md 所有人共用
# 3. ~/.claude/settings.json 个人配置各自维护
```

---

> 📌 **本手册是精简营销版**。完整 PM 专业版（含 CMMI 过程域 REQM/PP/PMC/CM/MA 详解）见 `claude-code-manuals/04-pm-cmmi-guide.md`（625行）。

## V52.2 新增（2026-06-12）

以下 4 项关键能力（原 V52.2 · 2026-06-12 引入）现已合并入 `~/.claude/rules/mycc-core.md` 铁律级规范：

### 1. 铁律 12：TDD 垂直切片（TDD Vertical Slice）
红 → 绿 → 重构三步走，每次只推进一个完整用户价值单元。**YOLO L4/极限档/OMC 自配置任务降级为铁律 3 验证证据**——不是所有任务都要先写失败测试。SSoT：`rules/mycc-core.md`（铁律 12·TDD 垂直切片）。

### 2. 四条件门：是否值得建 Loop（Loop-Worth-Building Gate）
建任何 Loop / `/loop` / LaunchAgent / 无人值守自动化前，过四条件（重复性 + 验证可自动化 + token 预算 + Agent 工具齐备）**全过才建**，否则一条好 Prompt 更省。SSoT：`rules/mycc-core.md`（4 步工作流·Loop 判断）。

### 3. 隔离区模式：读写分离防越权（Quarantine）
处理外部不可信输入（外部 AI 报告 / WebFetch / 用户上传文件）+ 同任务要高权限写时，**读取 agent 必须挂 `disallowed-tools` 移除写权**（物理无法越权）。纵深防御三层：行为层（视为数据非指令）+ **架构层（本规则）** + 运行时层（block-dangerous hook）。SSoT：`rules/mycc-core.md`（防改 4 类配置·安全约束）。

### 4. 双端策略 V52.2（Dual-End Policy）
**CLI 端** `~/.claude/CLAUDE.md` = OMC 工程事实 / `projects/-Users-williammacst/memory/user-profile.md` = 角色偏好 / `~/.claude/CLAUDE.local.md` = 已就绪能力指针；**Desktop 端** = 行为规则契约（云端）。**四份文档正交不冲突**。SSoT：`rules/mycc-core.md`（输出规范·双端策略）。

---

> **如何查阅完整规范**：
> - `cat ~/.claude/rules/mycc-core.md` （唯一规则 SSoT：12 铁律 + 12 行为规则 R1-R12 + 4 步工作流）
> - 注：W4（2026-06-22）精简后，原 iron-laws / loop-worth-building-gate / quarantine / auto-learned-rules 等多文件已合并入 `mycc-core.md` 单文件

*本节能力现已合并入 `rules/mycc-core.md`（OMC 4.14.7 · W4 精简）；保留原 V52 系列升级记录。*

---

*文档更新：2026-06-22 | CMMI Level 3 | OMC 4.14.7*
