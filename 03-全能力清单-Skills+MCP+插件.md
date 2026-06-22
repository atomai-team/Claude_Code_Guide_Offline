# Claude Code 全能力清单
> Skills × 130 · Agents × 38 · Hooks × 47 · 插件 × 10/58 · MCP × 12+ · 外部 CLI × 6
> OMC 4.14.7 · CLI v2.1.185 · 2026-06-22 完整版

---

## 第一部分：130 个 Skills 完整分类说明

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
| **autoresearch** | `/autoresearch` | 自动选择最优调研策略 |

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
| **wiki** | `/wiki` 或 `/oh-my-claudecode:wiki` | 知识库管理（797页 wiki 的查询/更新）|
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
| **qmd** | 本地 Markdown 搜索（264页）| 查本地知识库、规则 |
| **Fellow.ai** | AI 会议助手 | 会议记录、行动项提取 |
| **Gmail** | Gmail 操作 | 搜索/标记/草稿邮件 |
| **Google Calendar** | 日历操作 | 查看/创建日程 |
| **Google Drive** | Google Drive | 文件管理、内容读取 |

---

## 第三部分：插件（Plugins）说明

### oh-my-claudecode（OMC）
**核心插件，提供整套 OMC 能力**
- Skills: **130** 原生 skill
- Hooks: **48** 自动守护钩子
- Workflows: **15** 个 JS 流水线脚本
- MCP Tools: wiki/notepad/state/LSP/shared-memory 等
- Agents: **38** 角色（含多领域专家 + 团队蓝图）

### claude-hud
**实时状态显示 HUD**
- 显示：当前模型/token 使用/session 状态/git 分支
- 配置：`/claude-hud:setup`

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

## 第四部分：外部 AI CLI

| CLI | 状态 | 模型 | 最佳用途 |
|---|---|---|---|
| **gemini** | ✅ 在线 | Gemini 2.0 Flash | 快速调研、多模态、Google 搜索集成 |
| **kimi** | ✅ 在线 | Kimi k1.5 | 256K 超长文档处理、中文内容 |
| **mmx** | ✅ 在线 | MiniMax | 中文创作、对话优化 |
| **opencode** | ⚠️ 订阅过期 | volcengine | 代码专项（续订后启用）|

调用方式：
```bash
# 单模型
scripts/ai-cli.sh gemini "分析这份竞品报告"
scripts/ai-cli.sh kimi "帮我处理这 200 页 PDF"

# 多模型并发对抗验证（烧外部 API 额度，省 Claude token）
scripts/ai-panel.sh "评估这个商业计划书" gemini kimi mmx
```

---

## 第五部分：Workflow 脚本（10个）

| Workflow | 核心能力 | 阶段数 |
|---|---|---|
| **/bughunt** | 全库 bug 猎捕（parallel finder → adversarial verify）| 2 |
| **/ceo-pipeline** | 商业分析 6 阶段（市场→竞品→产品→财务→风险→路线图）| 6 |
| **/code-review** | 多维代码审查（bugs/perf/security → verify）| 2 |
| **/config-audit-better** | 配置健康审计（30维 → P0自动修）| 3 |
| **/domain-audit-better** | 领域专项深度审计 | 4 |
| **/harness-audit** | Harness 六层评分（L1-L6 量化）| 2 |
| **/judge-panel** | 多视角评审面板（N维 judge → 综合裁决）| 2 |
| **/n-step-pipeline** | N步自定义流水线（args 驱动）| N |
| **/self-evolve-loop** | 自我进化闭环（scope→optimize→evaluate→land）| 4 |
| **/v29-deep-research** | 深度多渠道调研（web抓取→合成→报告）| 3 |

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
> - 注：W4（2026-06-22）精简后，原 iron-laws / loop-worth-building-gate / quarantine / auto-learned-rules 等多文件已合并入 `mycc-core.md` 单文件

*本节能力现已合并入 `rules/mycc-core.md`（OMC 4.14.7 · W4 精简）；保留原 V52 系列升级记录。*

---

*全能力清单更新：2026-06-23 | Skills: 130 · MCP: 12+ · Plugins: 10 · Workflows: 15 · Hooks: 48 · Agents: 38*
