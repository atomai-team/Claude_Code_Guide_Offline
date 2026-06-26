# MYCC · Claude Code 全局能力指导书

> **一个仪表盘看懂、用好 Claude Code** —— 从零基础上手到工程化高阶编排，外加唐霜老师权威中文指南全文离线存档。

![Claude Code](https://img.shields.io/badge/Claude_Code-2.1.193-c15f3c)
![OMC](https://img.shields.io/badge/oh--my--claudecode-4.15.0-7a5ba8)
![Skills](https://img.shields.io/badge/Skills-148-3d7a4e)
![Agents](https://img.shields.io/badge/Agents-52-b06a1f)
![Hooks](https://img.shields.io/badge/Hooks-50-2f7d8a)
![License](https://img.shields.io/badge/原版内容-唐霜_©-595650)

---

## 📖 这是什么

本项目是一个**双层知识系统**，把"Claude Code 怎么用"从入门到精通一站式讲透：

| 层 | 内容 | 受众 |
|---|---|---|
| **① 能力指导层**（原创） | 交互式仪表盘 + 配置全景 + 7 本场景手册 + 全局搜索 | 想快速上手 / 工程化用好 CC 的人 |
| **② 权威指南层**（唐霜原版） | 《Claude Code 指南》全文离线存档，9 部分 / 36 章 / 207 节 | 想系统学习 CC 原理与实战的人 |

入口只有一个：**`dashboard.html`** —— 打开它，所有内容按场景串联可达。

---

## ✨ 核心功能

- **🎛️ 交互式仪表盘**（`dashboard.html`）：30+ 能力速查卡，按「新手起步 → 命令参考 → 交互模式 → 高级编排 → 配置全景」分区，左侧导航 + 响应式抽屉 + 明暗主题切换。
- **🔍 全局搜索（⌘K）**：客户端全文索引 13 份文档 / 19 万字符，搜 skill / agent / 口语 / 命令即时高亮。
- **🗂️ 二级详情页下钻**：仪表盘当入口菜单，数据密集卡（Skills / Hooks / Agents / 高级功能）一键下钻到 `mycc-config.html` 对应专区。
- **⚙️ 配置全景**（`mycc-config.html`）：自动从 `~/.claude/` 实时拉取，零手工维护，呈现已装的全部 MCP / 插件 / Skills / Hooks / 定时任务 / 路由表。
- **📚 7 本场景手册**：小白上手、商城项目实战、全能力清单、CMMI 配置、创业分析专家系统、CEO 能力速用、能力全景总册 —— 均提供 Markdown + 渲染版 HTML。
- **⚡ 高级实战示例**：goal 闭环 / loop 巡检 / Dynamic Workflow 编排 / 多 Agent 协同 / Skill 自优化，5 个复制即用的完整范例。
- **📊 实时数据注入**：版本号、各项能力计数由 `mycc-stats.py` 自动生成，仪表盘启动即刷新。

---

## 📊 数据概览

> 数据源：`mycc-stats.json`（由 `mycc-stats.py` 自动生成）· 截至 2026-06-26

| 维度 | 数量 | 说明 |
|---|---:|---|
| **Skills** | 148 | 按 8 大类分组，口语触发 |
| **Agents** | 52 | 6 核心 + 12 CEO 顾问 + 7 行业专家 + 6 交付团队 |
| **Hooks** | 50 | 覆盖 14 类事件（安全 / 质量 / 记忆 / 并发…） |
| **Workflows** | 13 | 多阶段确定性编排 |
| **MCP 服务器** | 4 | 外部工具与数据接入 |
| **权威指南** | 9 部分 / 36 章 / 207 节 | 唐霜《Claude Code 指南》全文 |
| **场景手册** | 7 本 | 原创，Markdown + HTML 双格式 |

运行环境：Claude Code `2.1.193` · oh-my-claudecode `4.15.0` · 官方直连。

---

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/atomai-team/Claude_Code_Guide_Offline.git
cd Claude_Code_Guide_Offline

# 2. 启本地服务（中文路径 + .html 渲染需经 HTTP，勿用 file://）
python3 -m http.server 18765 --bind 127.0.0.1

# 3. 浏览器打开仪表盘
open http://127.0.0.1:18765/dashboard.html
```

从仪表盘的「5 分钟上手」卡开始，按「新手 30 天路径」推进；不确定找哪个能力时，用顶部 **⌘K 全局搜索**或「超级入口」兜底。

---

## 📂 目录结构

```
.
├── dashboard.html              # 🎛️ 主入口：能力仪表盘
├── mycc-config.html            # ⚙️ 配置全景（自动生成）
├── 00-速查表.md ~ 06-CEO能力速用手册.md     # 📚 7 本场景手册（含 .html 渲染版）
├── start-here.md               # 新手第一站
├── MYCC-能力全景总册.md          # 能力总索引
├── mycc-stats.json             # 📊 实时数据源
├── _md-shared.css              # 手册渲染共享样式
└── 第1部分 ~ 第9部分/            # 📖 唐霜《Claude Code 指南》207 节原版
```

---

## 🙏 致谢与版权

本项目分**原创能力层**与**权威指南层**，版权分别归属：

- **权威指南层**（`第N部分/` 下 207 节内容）：原作者 **[唐霜 (Tang Shuang)](https://www.tangshuang.net/)**，来源 <https://claudecode.tangshuang.net/>。本仓库仅作个人学习与非营利备份，所有权 / 版权 / 最终解释权均归唐霜先生所有。转载引用请注明原作者及原始链接。
- **原创能力层**（仪表盘 / 配置全景 / 7 本场景手册 / 数据引擎）：基于实际 Claude Code + oh-my-claudecode 使用经验编写。

> **免责声明**：本项目致力于知识传播与分享。如原作者认为本仓库侵犯合法权益，请联系 `kscbxxliuxp@linux.do`，将在收到通知后第一时间删除相关内容并致歉。
