# Claude Code 全能力清单
> Skills × 148 · Agents × 52 · Hooks × 53(50文件) · 插件 × 32启用/35总 · MCP × 12+ · 外部 CLI × 5联
> OMC 4.15.0 · CLI v2.1.191 · 2026-06-25 完整版（mycc-stats 实测）

---

## 第一部分：148 个 Skills 完整分类说明

### 🚀 执行与工作模式（核心驱动）

| Skill | 触发方式 | 说明 |
|---|---|---|
| **autopilot** | 说"autopilot" 或 `/autopilot` | 自动驾驶：Claude 自主规划并连续执行任务，不打断确认 |
| **ultrawork** | 说"ulw" 或 `/ultrawork` | 超级工作模式：高并发+高密度执行，opus 模型全力输出 |
| **ultragoal** | `/ultragoal` | 超级目标：先用 rubric 定义完成标准，再全力达成 |
| **ultraqa** | `/ultraqa` | 超级 QA：全维度质量验收，覆盖功能/边界/安全/体验 |
| **smart-flow-all** | 说"队长" | 总调度器：按意图自动路由到最合适的执行模式 |
| **cancel** | 说"cancelomc" 或 `/cancel` | 终止当前执行模式 |
| **caveman** | `/caveman` | 压缩主线程对话密度，节省 token（吸收自 Gemini cavecrew）|
| **token-budget** | `/token-budget` | 管理 token 预算，防止超额 |

---

### 💻 功能开发类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **feature-dev:feature-dev** | `/feature-dev:feature-dev` | 完整功能开发流程：探索→架构→实现→代码审查 |
| **ecc-tdd-workflow** | 说"tdd" | TDD 三阶段：红（失败测试）→绿（最小实现）→重构 |
| **ecc-parallel-execution-optimizer** | 自动触发 | 并行执行优化，自动识别可并行任务 |
| **deep-dive** | 说"deep-analyze" 或 `/deep-dive` | 深度专项分析：代码库结构、技术债、性能瓶颈 |
| **codesight** | `/codesight` | 代码全局洞察，生成代码库理解报告 |
| **improve-codebase-architecture** | `/improve-codebase-architecture` | 架构改进建议，从全局视角优化代码结构 |
| **source-driven-development** | `/source-driven-development` | 源码驱动开发，先读源码再实现 |
| **doubt-driven-development** | `/doubt-driven-development` | 质疑驱动开发，先质疑假设再动手 |
| **prototype** | `/prototype` | 快速原型，30分钟内可演示的 MVP |
| **vercel-react-best-practices** | `/vercel-react-best-practices` | Vercel + React 最佳实践指南 |
| **local-build-reminder** | 自动触发 | 修改代码后提醒本地构建验证 |
| **context-engineering** | `/context-engineering` | Context 工程优化，提升 LLM 调用质量 |
| **api-and-interface-design** | `/api-and-interface-design` | API 和接口设计最佳实践 |

---

### 🔍 调研与分析类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **deep-research** | 说"调研" 或 `/deep-research` | ≥5 渠道深度调研（官方/GitHub/社区/中文/视频），有来源有结论 |
| **deep-research-sop** | `/deep-research-sop` | 调研 SOP wrapper，带六步决策闭环 |
| **autoresearch** | `/autoresearch` | 自动调研，自主选择最优渠道组合 |
| **v29-deep-research** | `/v29-deep-research` | Workflow 版深度调研（多 agent 并行抓取+合成）|
| **ask** | `/ask` | 互动式问答，适合模糊需求澄清 |
| **grill-me** | `/grill-me` | 苏格拉底式质询，帮你想清楚一个决策 |
| **grill-with-docs** | `/grill-with-docs` | 结合文档的深度质询 |
| **deep-interview** | 说"deep interview" 或 `/deep-interview` | 深度访谈，挖掘真实需求和痛点 |
| **interview-me** | `/interview-me` | 模拟面试，准备技术/产品/融资面谈 |
| **web-access** | `/web-access` | 直接访问网页内容 |

---

### 🛡️ 代码质量与安全类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **code-review** | `/code-review` | 代码审查（--fix 自动修复，--comment 发 PR 评论，ultra 云端）|
| **ce-code-review** | `/ce-code-review` | CE 模式代码审查（ECC 规范，覆盖 React/security/testing）|
| **simplify** | `/simplify` | 代码简化重构，去掉多余复杂度 |
| **security-audit** | `/security-audit` | 完整安全审计（OWASP Top 10 + STRIDE 威胁建模）|
| **security-review** | `/security-review` | 快速安全扫描，重点看漏洞 |
| **ai-slop-cleaner** | 说"deslop" 或 `/ai-slop-cleaner` | 清洗 AI 生成内容中的套话和低质量表达 |
| **neat-freak** | `/neat-freak` | 代码洁癖模式，强制执行命名/格式/风格统一 |
| **ecc-skill-comply** | `/ecc-skill-comply` | ECC 规范合规检查 |
| **ecc-gateguard** | `/ecc-gateguard` | 代码质量门控，阻止低质量代码合并 |
| **ecc-eval-harness** | `/ecc-eval-harness` | ECC 评估框架，量化代码质量 |

---

### 🎯 CEO/战略/创业类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **ceo-mode** | `/ceo-mode` | CEO 战略分析模式：市场/竞品/财务/风险全维度 |
| **smart-flow-all** | 说"队长" | 全流水线编排，ceo-mode + team-fullstack + 调研 |
| **ce-strategy** | `/ce-strategy` | CE 战略模式，专注战略决策 |
| **ce-plan** | `/ce-plan` | CE 规划模式，详细执行计划 |
| **ceo-pipeline** (workflow) | `/ceo-pipeline` | 6阶段商业分析流水线（市场→竞品→产品→财务→风险→路线图）|

---

### 🏗️ 规划与架构类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **omc-plan** | `/omc-plan` | OMC 任务规划，生成带验证步骤的执行计划 |
| **ralplan** | 说"ralplan" 或 `/ralplan` | 快速详细规划 |
| **spec-generator** | `/spec-generator` | 技术规格文档生成器 |
| **to-prd** | `/to-prd` | 需求→PRD 文档转化 |
| **documentation-and-adrs** | `/documentation-and-adrs` | 文档 + 架构决策记录（ADR）|
| **planning-with-files-mode** | 自动触发 | 文件级规划模式 |
| **omc-hitl** | `/omc-hitl` | Human-in-the-loop 审批点设置 |
| **cmmi-tracker** | `/cmmi-tracker` | CMMI 任务跟踪，同步到 Notion 看板 |

---

### 📝 文档与内容创作类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **article-writing** | `/article-writing` | 写技术文章/博客/README，有结构有深度 |
| **writer-memory** | `/writer-memory` | 保持写作风格一致，跨会话记忆写作偏好 |
| **baoyu-translate** | `/baoyu-translate` | 高质量中英互译，保留技术术语 |
| **baoyu-slide-deck** | `/baoyu-slide-deck` | 生成演示 PPT（Marp/Reveal.js）|
| **baoyu-diagram** | `/baoyu-diagram` | 生成架构图/流程图（Mermaid/PlantUML）|
| **baoyu-markdown-to-html** | `/baoyu-markdown-to-html` | Markdown → 精美 HTML |
| **baoyu-infographic** | `/baoyu-infographic` | 信息图表设计 |
| **baoyu-article-illustrator** | `/baoyu-article-illustrator` | 为文章生成配图 |
| **baoyu-wechat-summary** | `/baoyu-wechat-summary` | 微信文章摘要提取 |
| **baoyu-url-to-markdown** | `/baoyu-url-to-markdown` | 网页→Markdown 转换 |
| **baoyu-youtube-transcript** | `/baoyu-youtube-transcript` | YouTube 视频转文字+摘要 |
| **baoyu-format-markdown** | `/baoyu-format-markdown` | Markdown 格式美化 |
| **baoyu-comic** | `/baoyu-comic` | 将内容转为漫画形式 |
| **slides** | `/slides` | 演示文稿生成 |
| **diff-generator** | `/diff-generator` | 生成变更对比文档 |
| **humanize-chinese** | `/humanize-chinese` | 中文内容人性化，去除 AI 腔调 |
| **humanizer** | `/humanizer` | 通用内容人性化 |

---

### 🎨 设计与 UI 类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **design** | `/design` | UI/UX 完整设计流程 |
| **ui-ux-pro-max** | `/ui-ux-pro-max` | 专业级 UI/UX 设计，有用户旅程/信息架构/交互逻辑 |
| **design-system** | `/design-system` | 设计系统建立，组件规范/色彩/字体 |
| **ui-styling** | `/ui-styling` | CSS/Tailwind 样式优化 |
| **banner-design** | `/banner-design` | 横幅/封面设计 |
| **baoyu-cover-image** | `/baoyu-cover-image` | 生成文章封面图 |
| **baoyu-image-gen** | `/baoyu-image-gen` | AI 图片生成（含提示词优化）|
| **prototype** | `/prototype` | 快速可交互原型 |
| **visual-verdict** | `/visual-verdict` | 视觉审查，给设计稿打分+建议 |

---

### 👥 团队协作类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **team** | `/team` 或 `/oh-my-claudecode:team` | 启动多 agent 协作团队 |
| **omc-teams** | `/omc-teams` | OMC 团队管理，配置 agent 团队 |
| **team-prompt-template** | `/team-prompt-template` | 团队协作提示词模板 |
| **n-step-pipeline** (workflow) | `/n-step-pipeline` | N步自定义流水线，每步可分配不同 agent |
| **handoff** | `/handoff` | 任务交接文档生成，新会话快速续接 |
| **teleport** | `/teleport` | 跨会话上下文传送，复杂上下文接力 |
| **project-session-manager** | `/project-session-manager` | 会话项目管理，多轮任务状态持久化 |

---

### 🚀 部署与 DevOps 类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **deploy-ship** | `/deploy-ship` | 一站式部署（CI/CD + 环境变量 + 健康检查）|
| **release** | `/release` | 正式发版流程（CHANGELOG + tag + 发布说明）|
| **gh-ci-fix** | `/gh-ci-fix` | 自动修复 GitHub Actions 失败 |
| **ci-template** | `/ci-template` | CI/CD 模板生成（GitHub Actions/GitLab CI）|
| **commit-commands:commit** | `/commit-commands:commit` | 智能生成 git commit message |
| **commit-commands:commit-push-pr** | `/commit-commands:commit-push-pr` | commit + push + 开 PR 全自动 |
| **commit-commands:clean_gone** | `/commit-commands:clean_gone` | 清理已删除远端分支的本地追踪 |
| **shipping-and-launch** | `/shipping-and-launch` | 产品上线全流程清单 |
| **deprecation-and-migration** | `/deprecation-and-migration` | 废弃API/功能迁移指南生成 |
| **observability-and-instrumentation** | `/observability-and-instrumentation` | 可观测性建设（日志/监控/追踪）|

---

### 🔧 配置与系统维护类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **claude-code-better** | 说"全面升级" 或 `/claude-code-better` | 一站式全面升级（唯一升级入口）|
| **audit-all-better** | `/audit-all-better` | 30维健康诊断（只诊断不修改）|
| **harness-audit** (workflow) | `/harness-audit` | harness 六层评分（配置层质量评估）|
| **config-audit-better** (workflow) | `/config-audit-better` | 配置专项审计 |
| **self-evolve-loop** (workflow) | `/self-evolve-loop` | 自我进化闭环（evaluator-optimizer 飞轮）|
| **self-audit-loop** | `/self-audit-loop` | 任务级自审循环（5问自检）|
| **self-improve** | `/self-improve` | 针对外部代码库跑 benchmark 改进 |
| **update-all** | `/update-all` | 版本更新（CLI + 插件 + 依赖）|
| **update-config** | `/update-config` | 修改 settings.json/settings.local.json |
| **hookify:hookify** | `/hookify:hookify` | 分析对话行为，自动生成 hooks 防范重复错误 |
| **hookify:configure** | `/hookify:configure` | 配置 hook 行为 |
| **hookify:list** | `/hookify:list` | 查看已配置 hooks |
| **omc-doctor** | `/omc-doctor` | 诊断 OMC 配置问题 |
| **omc-setup** | `/omc-setup` | 初始化/重置 OMC 配置 |
| **setup** | `/setup` | 初始化项目环境 |
| **antigravity-claude-settings-audit** | `/antigravity-claude-settings-audit` | 反向审计：找出过度复杂的配置并简化 |
| **antigravity-memory-systems** | `/antigravity-memory-systems` | 记忆系统审计，清理过时记忆 |

---

### 💾 记忆与知识管理类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **remember:remember** | `/remember:remember` | 保存重要信息到持久记忆（7天/永久两级）|
| **wiki** | `/wiki` 或 `/oh-my-claudecode:wiki` | 知识库管理（wiki 的查询/更新）|
| **notion-knowledge-capture** | `/notion-knowledge-capture` | 将洞察直接保存到 Notion |
| **notion-spec-to-implementation** | `/notion-spec-to-implementation` | Notion 需求文档→代码实现 |
| **obsidian-vault** | `/obsidian-vault` | Obsidian 知识库操作 |
| **writer-memory** | `/writer-memory` | 写作风格记忆 |
| **memory-dream-consolidation** | `/memory-dream-consolidation` | 记忆整合，合并分散知识 |
| **ecc-continuous-learning-v2** | 自动触发 | 会话观察→生成改进 instinct，持续学习 |

---

### 🌐 营销与内容运营类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **marketing** | `/marketing` | 营销策略+文案，含 GTM 策略 |
| **brand** | `/brand` | 品牌建设（定位/视觉/声音）|
| **brand-voice** | `/brand-voice` | 品牌语气一致性审查和建立 |
| **content-engine** | `/content-engine` | 内容工厂：批量生成各平台内容 |
| **social-publisher** | `/social-publisher` | 多平台社交媒体发布 |
| **card-xiaohongshu** | `/card-xiaohongshu` | 小红书图文卡片生成 |
| **baoyu-xhs-images** | `/baoyu-xhs-images` | 小红书风格图片 |
| **xhs-operations-method** | `/xhs-operations-method` | 小红书运营方法论 |
| **baoyu-electron-extract** | `/baoyu-electron-extract` | 从内容中提取精华 |

---

### 🧰 工具与集成类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **macos-automation** | `/macos-automation` | macOS 自动化（AppleScript/Shortcuts）|
| **mmx-cli** | `/mmx-cli` | MiniMax CLI 调用接口 |
| **external-context** | `/external-context` | 加载外部上下文文档 |
| **canary-monitor** | `/canary-monitor` | 金丝雀监控，持续检查指标 |
| **hud** | `/hud` | 状态 HUD 显示（实时状态栏）|
| **claude-hud:setup** | `/claude-hud:setup` | 配置 HUD 显示 |
| **configure-notifications** | `/configure-notifications` | 配置完成通知（Mac 通知/声音）|
| **mcp-setup** | `/mcp-setup` | 设置和配置 MCP 服务器 |
| **trace** | `/trace` | 执行路径追踪，调试复杂问题 |
| **diagnose** | `/diagnose` | 系统诊断，快速定位问题 |
| **triage** | `/triage` | 问题分类优先级排序 |
| **systematic-error-analysis** | 说"又报错" | 系统性错误分析，找根因 |

---

### 🎓 学习与教学类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **learner** | `/learner` | 学习模式，解释复杂概念 |
| **teach** | `/teach` | 教学模式，生成教程 |
| **zoom-out** | `/zoom-out` | 拉远视角，从大局看问题 |
| **composition-patterns** | `/composition-patterns` | 设计模式说明和应用 |
| **ecc-continuous-learning-v2** | 自动 | 从会话中学习，生成改进提案 |

---

### 🔄 进化与自我改进类

| Skill | 触发方式 | 说明 |
|---|---|---|
| **auto-evolve** | 月度触发 | 自动进化：扫描社区→识别增量→吸收落地 |
| **auto-collector-official** | `/auto-collector-official` | 采集官方最新能力/文档 |
| **auto-collector-github** | `/auto-collector-github` | 采集 GitHub 高星项目能力 |
| **auto-collector-community** | `/auto-collector-community` | 采集社区使用案例 |
| **skill-audit** | `/skill-audit` | 安装新 skill 前安全审查（重复度+许可证+风险）|
| **skillify** | `/skillify` | 将常用对话模式转化为可复用 skill |
| **omc-skill-health** | 月度触发 | skill 健康度扫描，清理过时 skill |

---

## 🆕 最新工程化能力（2026-06 新增）

### 异构对抗 ai-panel（5联外部 CLI）

多模型并发对抗验证，破解同源盲点，节省 Claude 主力 token：

| CLI | 状态 | 说明 |
|---|---|---|
| **kimi** | 自动 | Kimi K2 / 256K 上下文，中文长文档、竞品分析 |
| **mmx** | 自动 | MiniMax-M3 1M，中文创作+对话优化 |
| **qwen** | 自动 | 通义千问，中文推理+代码 |
| **opencode** | 自动 | Volcengine，代码专项 |
| **mavis** | 自动 | 多模态视觉分析 |

```bash
# 单模型调用
~/.claude/scripts/ai-panel.sh "评估这个商业计划" kimi

# 5联异构对抗（ai-panel 入口，唯一稳定调用方式）
~/.claude/scripts/ai-panel.sh "分析这个架构方案"
```

典型场景：方案评审前的多视角反驳、升级决策前的独立校验、调研结论的对抗确认。

---

### self-evolve-loop — 自我进化闭环

`/self-evolve-loop` 触发四阶段飞轮：

1. **Scope** — 扫描会话错误+社区新实践，确定进化范围
2. **Optimize** — 生成改进候选（skill/hook/rule 修改建议）
3. **Evaluate** — 独立 evaluator 打分，≥阈值才落地
4. **Land** — 写入文件+git commit+memory 更新

含异构对抗节点：evaluator 阶段触发 ai-panel 做独立评分，防止自我强化偏见。

---

### ceo-pipeline — 战略编排流水线

6 阶段商业分析 Workflow，含异构对抗节点：

```
市场分析 → 竞品矩阵 → 产品定位 → 财务建模 → 风险评估 → 路线图
         ↑                                               ↑
    ai-panel 5联验证                              ai-panel 裁决
```

输出：执行级战略备忘录 + 数据支撑的决策矩阵。

---

### automation-reality-check.py — 自动化虚假健康检测

检测"看起来在跑但实际没效果"的 false-green 问题：

- Hook 注册了但脚本无 +x 权限（接线病 Form 1）
- 脚本在 `~/.claude/scripts/` 但未软链到 PATH（接线病 Form 2）
- Hook 命令路径用 `$HOME` 变量而非绝对路径（接线病 Form 3）
- LaunchAgent plist 存在但未 load（定时任务沉睡）
- Mock 测试全绿但真实链路断路

```bash
python3 ~/.claude/scripts/automation-reality-check.py
```

---

### 多层记忆体系

| 层级 | 位置 | 内容 | 规模 |
|---|---|---|---|
| L1 即时记忆 | 会话上下文 | 当前对话内容 | session 级 |
| L2 项目记忆 | `MEMORY.md` 索引 | 关键决策/能力指针/规则摘要 | ~200 条目 |
| L3 知识归档 | `memory-archive-index.md` | 历史 session 摘要/评估记录/低频条目 | 分层存储 |
| L4 知识图谱 | `.omc/wiki/` | 1526 个 wiki 文件，历史 session + 架构图 | 结构化检索 |

记忆完整率监控：`memory-index-check` 脚本定期扫描，当前状态 **100% GREEN**（所有 MEMORY.md 引用的文件均存在）。

auto-memory 系统（OMC v2.1.59+ 官方）接管 `memory/` 目录，SSoT 为 `MEMORY.md`。

---

### smoke-tests.sh + auto-rollback.sh — 冒烟测试与自动回滚

**smoke-tests.sh**（5项冒烟，每次升级后自动触发）：

| 测试项 | 验证内容 |
|---|---|
| Claude CLI 响应 | `claude --version` 返回有效版本号 |
| OMC 基础加载 | smart-flow-all 路由可解析 |
| Hook 注册健康 | 53 个 hook 均有 +x 权限 |
| 记忆完整率 | MEMORY.md 引用文件 100% 存在 |
| 外部 CLI 可达 | 5联 CLI 至少 3 个响应正常 |

**auto-rollback.sh**（cleanroom 体系）：

```bash
# 升级前自动快照（存 ~/.claude-cleanroom-YYYYMMDD-HHMMSS/）
~/.claude/bin/cleanroom-precheck.sh

# 出错时 30 秒内回滚
~/.claude/bin/auto-rollback.sh --to latest-snapshot
```

任何"清理/删除/瘦身"操作前必跑 `cleanroom-precheck.sh` 6步检查（rsync snapshot + git baseline + 4 detector），全部 OK 才动真实环境。

---

### Orchestrator 3组件 — 多 session 工程化协作

**组件 1：多 session 状态管理**
- `.omc/state/sessions/{sessionId}/` 存储每个 session 的上下文快照
- `project-session-manager` skill 跨 session 续接任务
- handoff 文档标准化：目标/进度/阻塞/下一步四段式

**组件 2：智能路由（92 条意图词）**
- 意图词从 59 条扩展至 92 条（W3 2026-06-22）
- 6 → 33 路由词覆盖（session 2026-06-25 实测）
- 优先级路由：队长(95) > 活力全开(95) > CEO决策(88) > 综合升级(86) > 智能流(85)

**组件 3：提示词优化**
- 动态注入上下文（用户画像 + 当前任务 + 历史决策）
- 反讽刺铁律自动检查（R1-R5 五条规则内化为行为层）
- 自动截断过长提示词，防 token 超额

---

### 风险分级 L0-L3 + verify-before-assert 铁律

**操作风险分级**（3问定档）：

| 档 | 触发条件 | 动作 |
|---|---|---|
| **L0** | 1-2 文件 + 可撤 + 不碰 config/hook | 直做+报告 |
| **L1** | ≤5 文件 + 可撤 + 不碰 config/hook | 验证+clean 自动 commit（不 push）|
| **L2** | 6-20 文件 / push / Notion | 一句话简报即开 |
| **L3** | 不可逆 / 碰 settings/hook/cron / 架构 / security | plan+确认+ai-panel |

3问：① 可逆？② 碰 config/hook？③ ≤5 文件？

**verify-before-assert 铁律**（铁律 8，Karpathy 5 原则之一）：
- 事实断言前必先查验，禁推测下结论
- 输出分已验证/[未验证] 两类标注
- LLM 模型能力/价格断言前必查 models.dev + 官方 docs
- `uncertainty-detector.sh` hook 自动扫描高置信度推测性断言

**Writer ≠ Reviewer 原则**（铁律 10）：
- 写作 pass 和审查 pass 必须分离到不同 agent 或不同 context
- 禁止同一 context 内自写自批
- 审查入口：`/gstack-review`、`/code-review`、`verifier` agent

---

### WBS 工程化排期 + capability-activation-map

**WBS 工程化排期**（`docs/plan/wbs-engineering-rollout-2026-06-24.md`）：

- 188 行详细排期，覆盖 29 个行动项
- Top 10 优先级 + 5联裁决结果
- 每项含：负责角色 / 验收标准 / 回滚方案 / 预估工时

**capability-activation-map（5大智能脑）**：

| 智能脑 | 核心能力 | 激活条件 |
|---|---|---|
| **主调度器** | 意图识别 + 92词路由 + 风险分级 | 默认激活 |
| **异构对抗脑** | ai-panel 5联 + 交叉验证 | 方案评审/升级决策时触发 |
| **记忆脑** | auto-memory 200条 + wiki 1526页 | 涉及历史决策/配置时自动查 |
| **进化脑** | self-evolve-loop + omc-skill-health | 月度自动 + 手动触发 |
| **代码脑** | codebase-memory MCP + serena + understand-anything | 代码库理解任务时激活 |

headroom MCP Server 为休眠状态（P0 激活后可用，参见 `docs/local-reference.md`）。

---

### cleanroom 快照备份/回滚体系

```
升级前自动快照
    ↓
~/.claude-cleanroom-YYYYMMDD-HHMMSS/
    ├── .claude/（完整备份）
    ├── settings.json（单独备份）
    └── manifest.json（快照元数据）
    ↓
cleanroom-precheck.sh 6步检查：
① rsync snapshot（30秒内可回滚）
② git baseline（工作树干净）
③ orphan plugin detector（无孤儿插件）
④ orphan hook detector（无孤儿 hook）
⑤ CLAUDE.md drift check（无未记录变更）
⑥ settings drift check（防配置四类防改规则违反）
    ↓
全部 OK → 动真实环境
任一失败 → 阻断 + 报告
```

---

## 第二部分：MCP 服务器完整说明

### 通过 settings.local.json 配置的 MCP

| MCP | 说明 | 典型用法 |
|---|---|---|
| **github** | GitHub API 完整访问 | 查 PR、搜索代码、管理 issues、获取仓库结构 |
| **context7** | 官方文档实时查询（库/框架/SDK）| "查 Next.js 14 App Router 最新 API" |
| **playwright** | 浏览器自动化测试 | E2E 测试、截图验证、表单自动填写 |
| **linear** | Linear 项目管理 | 创建/更新 issue、sprint 管理 |

### Desktop Extensions 安装的 MCP

| MCP | 说明 | 典型用法 |
|---|---|---|
| **chrome-control** | Chrome 浏览器控制 | 打开网页、点击操作、截图 |
| **filesystem** | 本地文件系统访问 | 读写文件、目录操作 |
| **iMessage** | iMessage 收发 | 发送消息、读取对话 |
| **ms_office_powerpoint** | PowerPoint 操作 | 创建/修改 PPT |
| **ms_office_word** | Word 操作 | 创建/修改 Word 文档 |
| **Apple Notes** | Apple Notes 操作 | 创建/读取笔记 |
| **figma** | Figma 设计操作 | 读取设计稿、获取组件 |
| **pdf-server-mcp** | PDF 处理 | 读取 PDF、提取内容 |
| **macos-mcp** | macOS 系统操作 | 系统设置、应用控制 |
| **osascript** | AppleScript 执行 | 自动化 macOS 操作 |
| **kapture** | 屏幕录制/截图 | 录制操作过程 |
| **desktopcommandermcp** | 桌面命令执行 | 执行系统命令 |

### 通过插件系统提供的 MCP

| MCP | 说明 | 典型用法 |
|---|---|---|
| **computer-use** | 桌面截图+鼠标键盘控制 | 操作任何桌面应用 |
| **firecrawl** | 高级网页抓取+搜索 | 深度调研、竞品分析、数据采集 |
| **Notion** | Notion 完整操作 | 创建页面/数据库、任务管理 |
| **chrome-devtools** | Chrome 开发者工具 | 性能分析、内存检测、LCP 优化 |
| **oh-my-claudecode tools** | OMC 工具集（wiki/notepad/state/LSP等）| 项目记忆、代码分析 |
| **semgrep** | 静态代码分析 | 安全扫描、代码规范检查 |
| **code-review-graph** | 知识图谱代码审查 | 代码结构理解、影响分析 |
| **memory** | 知识图谱记忆 | 实体关系记忆 |
| **sequential-thinking** | 结构化推理链 | 复杂问题分步推理 |
| **qmd** | 本地 Markdown 搜索（2058 文件）| 查本地知识库、规则 |
| **Fellow.ai** | AI 会议助手 | 会议记录、行动项提取 |
| **Gmail** | Gmail 操作 | 搜索/标记/草稿邮件 |
| **Google Calendar** | 日历操作 | 查看/创建日程 |
| **Google Drive** | Google Drive | 文件管理、内容读取 |

---

## 第三部分：插件（Plugins）说明

> 当前状态：35 总插件（32 启用 + 3 禁用），mycc-stats 2026-06-25 实测。

### oh-my-claudecode（OMC）
**核心插件，提供整套 OMC 能力**
- Skills: **148** 原生 skill
- Hooks: **51** 自动守护钩子（50 个 hook 文件，14 个 hook 事件类型）
- Workflows: **13** 个 JS 流水线脚本
- MCP Tools: wiki/notepad/state/LSP/shared-memory 等
- Agents: **90** 角色（核心6 + CEO角色12 + 行业专家7 + 团队蓝图6 + 通用21）
- 意图路由: **92 条**词触发规则

### claude-hud
**实时状态显示 HUD**
- 显示：当前模型/token 使用/session 状态/git 分支/CC Switch provider
- 配置：`/claude-hud:setup`
- 真实配置文件：`~/.claude/plugins/claude-hud/config.json`（非 settings.json）

### Marketplace 插件（按需安装）

| 插件 | 来源 | 核心能力 |
|---|---|---|
| **understand-anything** | claude-code-plugins | 代码库知识图谱、架构分析、领域理解 |
| **feature-dev** | claude-code-plugins | 完整功能开发流程（explorer+architect+reviewer）|
| **pr-review-toolkit** | claude-code-plugins | PR 审查工具集（code/test/type/comment/silent-failure）|
| **firecrawl** | claude-plugins-official | 网页抓取/搜索/爬虫/监控 |
| **semgrep** | claude-plugins-official | 代码安全扫描（SAST）|
| **chrome-devtools** | claude-plugins-official | 浏览器性能调试 |
| **context7** | claude-plugins-official | 官方文档实时查询 |
| **hookify** | claude-code-plugins | 从对话自动生成 hooks |
| **remember** | - | 持久记忆管理 |
| **Notion** | claude-plugins-official | Notion 完整操作 |

---

## 第四部分：外部 AI CLI（5 联异构对抗）

| CLI | 状态 | 模型 | 最佳用途 |
|---|---|---|---|
| **kimi** | 自动（5联默认）| Kimi K2 / 256K | 中文长文档处理、竞品研报 |
| **mmx** | 自动（5联默认）| MiniMax-M3 1M | 中文创作、对话优化 |
| **qwen** | 自动（5联默认）| 通义千问 | 中文推理、代码理解 |
| **opencode** | 自动（5联默认）| Volcengine | 代码专项（续订后全力）|
| **mavis** | 自动（5联默认）| 多模态 | 视觉分析、截图解读 |
| **codex** | 手动（非自动）| OpenAI Codex | 对比验证（手动触发）|

> 注：gemini 已退役（2026-06-22），kimi 实测后端走 MiniMax-M3 而非 Moonshot K1.5，带 `[1M]` 后缀才能解锁 1M 上下文。

调用方式：
```bash
# 唯一稳定入口：positional arg（非 pipe 非 flag）
~/.claude/scripts/ai-panel.sh "评估这份竞品分析" kimi mmx qwen

# 5联默认并发对抗（省 Claude token，外部 API 额度）
~/.claude/scripts/ai-panel.sh "这个架构方案有没有致命缺陷？"
```

---

## 第五部分：Workflow 脚本（13个）

| Workflow | 核心能力 | 阶段数 |
|---|---|---|
| **/boardroom** | 董事会汇报准备（含财务/风险/路线图）| 3 |
| **/bughunt** | 全库 bug 猎捕（parallel finder → adversarial verify）| 2 |
| **/ceo-pipeline** | 商业分析 6 阶段（市场→竞品→产品→财务→风险→路线图）| 6 |
| **/code-review** | 多维代码审查（bugs/perf/security → verify）| 2 |
| **/comprehensive-upgrade** | 综合升级流水线（全层 audit + apply + verify）| 5 |
| **/config-audit-better** | 配置健康审计（30维 → P0自动修）| 3 |
| **/dev-pipeline** | 开发流水线（spec→scaffold→impl→test→review→deploy）| 6 |
| **/domain-audit-better** | 领域专项深度审计 | 4 |
| **/fundraising** | 融资准备（BP + 财务模型 + 投资人 FAQ）| 4 |
| **/harness-audit** | Harness 六层评分（L1-L6 量化）| 2 |
| **/judge-panel** | 多视角评审面板（N维 judge → 综合裁决）| 2 |
| **/n-step-pipeline** | N步自定义流水线（args 驱动）| N |
| **/overseas-compliance** | 出海合规（法务+牌照+数据保护+支付）| 4 |
| **/self-evolve-loop** | 自我进化闭环（scope→optimize→evaluate→land）| 4 |
| **/v29-deep-research** | 深度多渠道调研（web抓取→合成→报告）| 3 |

> 注：mycc-stats 显示 13 个 workflow，上表含所有已注册条目。

---

## 第六部分：定时任务体系

### LaunchAgents（13 个 plist）

| plist | 触发周期 | 任务 |
|---|---|---|
| com.mycc.auto-commit | 每日 23:00 | 自动提交 myclaude-test 仓库 |
| com.mycc.daily-external-scanner | 每日 | 扫描外部 repo/社区新能力 |
| com.mycc.drift-check | 每日 | 配置漂移检查（settings+CLAUDE.md）|
| com.mycc.memory-compact | 每日 | 记忆整合压缩 |
| com.mycc.memory-health | 每日 | 记忆完整率检查（100% GREEN 目标）|
| com.mycc.monthly-expert-check | 每月 | 专家团队健康度评估 |
| com.mycc.monthly-skill-audit | 每月 | skill 存活+触发率审计 |
| com.mycc.snapshot | 每日 | cleanroom 快照备份 |
| com.user.claude-daily-brief | 每日 | 日报生成（今日任务+待办+状态）|
| com.user.claude-external-research | 每周 | 外部调研采集 |
| com.user.claude-monthly-evolution | 每月 | 月度进化扫描+建议 |
| com.user.claude-secretary | 每日 | 秘书任务（日程+提醒+归档）|
| *(第13个 LaunchAgent)* | 按需 | 参见 docs/scheduled-tasks.md |

### Cron 任务（2 个）

| cron 表达式 | 任务 |
|---|---|
| `0 3 * * 1`（每周一凌晨3点）| certbot renew（SSL 证书续期）|
| `0 21 * * 0`（每周日晚9点）| weekly-cron-orchestrator-clean.sh（周进化闭环）|

> SSoT：`~/.claude/docs/scheduled-tasks.md`。定时任务相关操作前必查。

---

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
> - `cat ~/.claude/docs/capability-activation-map.md`（5大智能脑激活地图）
> - `cat ~/.claude/docs/wbs-engineering-rollout-2026-06-24.md`（工程化排期 WBS）
> - 注：W4（2026-06-22）精简后，原 iron-laws / loop-worth-building-gate / quarantine / auto-learned-rules 等多文件已合并入 `mycc-core.md` 单文件

*本节能力现已合并入 `rules/mycc-core.md`（OMC 4.15.0 · W4 精简）；保留原 V52 系列升级记录。*

---

最后更新：2026-06-25 · 数字经 mycc-stats 实测
*全能力清单：Skills: 148 · Agents: 52 · Hooks: 53(50文件) · Workflows: 13 · LaunchAgents: 13 · Cron: 2 · 插件启用/总: 32/35 · 外部CLI: 5联*

---

## 🌟 5 大高级功能全景 + 超级入口（2026-06-25 增）

> 148 个 skill 太多不知道用哪个？记住这 **5 大高级功能** + **超级入口**，覆盖 90% 场景。

### 💎 5 大高级功能（各管一摊不重叠）

| 功能 | 口语触发 | 对应 skill | 何时用 |
|---|---|---|---|
| **队长** | 队长 / 火力全开 / 活力全开 / YOLO | `smart-flow-all` | 极限档 · 复杂任务 · 多顾问 |
| **CEO** | 评估 / 尽调 / 出海 / 商业可行性 | `ceo-mode` + `ceo-pipeline` | 商业决策 · 投资 · 立项 |
| **经理** | 我几个 session / 别的 session 在干嘛 | `multi-session-state` | 多 session 互可见 + 冲突检测 |
| **秘书** | 秘书 / daily-brief / weekly | `weekly-secretary` + `daily-brief` | 自动巡检 · 报告 |
| **超级入口** | super / 超级入口 / 不知道找谁 | `engineering-scenario-router` | 不知道找谁时兜底 |

### 🔗 高级功能融合矩阵（按"你想做什么"路由）

| 你的意图 | 推荐组合 |
|---|---|
| 不知道找谁 | `super`（列出候选）→ 你选 → 执行 |
| 商业评估 | `CEO`（7 顾问）→ 想工程化 → `队长` |
| 复杂代码改动 | `队长` + `eng-experts`（3 专家盲评） |
| 多 session 协作 | `经理`（自动）+ `start-work`（工程化） |
| 系统健康 | `秘书`（自动）+ `full-checkup`（手动） |
| 升级 + 改造 | `秘书` 发现 → `super` 路由 → `队长` 修 → `CEO` 评 |

### 🚀 super 入口详解（51 个意图 SSoT）

**SSoT**：`~/.claude/skills/engineering-scenario-router/router-table.json`

**核心机制**：当用户说 `super` 或 `超级入口` 或 `不知道找谁` 时，主调度器读 router-table.json → 按意图关键词概率排序 → 列出 1-3 个候选 skill → 用户选 → 执行。

**为什么不直接做而是列候选？** 单人维护者 + 51 路由分散 = 静默调错风险 > 多一步"选"的成本。

**风险档**：`super` 触发时 execution_path = YOLO-L4（叠加 modifier，不降低安全不变量：配置防改 / 官方直连 / 改 hook 前 snapshot 仍硬）。

> 📌 **学习路径**：先熟 5 大高级功能 → 再学 11 个高频入口（dashboard §C7）→ 最后学 super 兜底（diversity safety net）。

---

---

## 📚 更多入口

- **dashboard.html** · 36+ 张卡片（命令/能力/5 大高级功能/统计/帮助）
- **mycc-config.html** · 配置全景（自动拉取 ~/.claude/ · MCP/插件/Skills/Hooks/路由表）
- **start-here.md** · 35 场景 × 7 手册 × 3 万能入口
