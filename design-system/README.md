# MYCC Design System · 2026-06-27 全套重做 SSoT

> **所有页面共享的设计语言**——dashboard / mycc-config / 7 手册 / 营销页都用这一套 token。
> 改色改字改间距：只改 `tokens.css`，全站同步。

## 📐 三层结构

```
design-system/
├── tokens.css       ← 第 1 层: 原子 (颜色/字号/间距/阴影) · 全站 SSoT
├── components.css   ← 第 2 层: 组件 (card/btn/badge/grid) · 跨页通用
└── README.md        ← 本文件: 使用约定 + 命名 + 决策记录
```

## 🎨 设计语言来源

- **唐霜老师原站** `https://claudecode.tangshuang.net/` (5.0 评分 · 10000+ 用户) = 设计标杆
- **Apple HIG** + **Linear** + **Vercel** = 极简 + 高端 + 信息密度
- **Claude Code 官方** = 暖米底 + 黏土橘 (#c15f3c) 品牌色

## 🧱 使用规范

### 必读
- ❌ **禁止**硬编码颜色 (如 `color: #c15f3c`) — 必须 `color: var(--accent)`
- ❌ **禁止**硬编码字号 (如 `font-size: 13px`) — 必须 `font-size: var(--fs-base)`
- ❌ **禁止**硬编码间距 — 必须 `padding: var(--sp-4)`
- ❌ **禁止**硬编码圆角 — 必须 `border-radius: var(--radius-lg)`
- ✅ 唯一例外：极少用的微调 (如 `transform: translateX(2px)`)

### 字号选择决策树

| 用途 | token | 数值 |
|---|---|---|
| Hero / 营销页大标题 | `--fs-4xl` | 56px |
| Page title | `--fs-3xl` | 40px |
| Section title | `--fs-2xl` | 28px |
| Card title | `--fs-xl` | 20px |
| 副标题 | `--fs-lg` | 16px |
| 强调正文 / 列表项 | `--fs-md` | 14px |
| 正文 / 表格 | `--fs-base` | 13px |
| input / badge | `--fs-sm` | 12px |
| 注释 / kbd | `--fs-xs` | 11px |
| 极小 (badge 内文 / copyright) | `--fs-2xs` | 10px |

### 间距选择决策树

| 用途 | token | 数值 |
|---|---|---|
| Hero 区上下空白 | `--sp-9` | 96px |
| Section 之间 | `--sp-7` | 48px |
| Card 之间 | `--sp-5` | 24px |
| Card 内 padding | `--sp-5` | 24px |
| 段落之间 | `--sp-4` | 16px |
| 元素微调 | `--sp-2` | 8px |

## 🔧 组件对照表

| 组件 | 用什么类 |
|---|---|
| 卡片 | `<div class="card">` |
| 主 CTA 按钮 | `<button class="btn btn-primary">` |
| 次要按钮 | `<button class="btn">` |
| 标签 chip | `<span class="badge badge-orange">` |
| 代码引用 | `<kbd>` |

## 📝 决策记录

- **2026-06-27 立**：用户报"网站弱智、没设计感"，C 方案全套重做。本文件为 SSoT。
- **拆 4 pane 并行**：dashboard / mycc-config / 7 手册 / 营销页，各自引用 tokens.css
- **保留兼容**：dashboard.html 旧 var() 名继续可用（已在 tokens.css 加 alias）
- **颜色策略**：暖米底 + 黏土橘 + 4 辅助色（绿/蓝/紫/橙），克制不堆
- **字体策略**：Fraunces 衬线标题 + Inter 无衬线正文 + JetBrains Mono 代码
- **动效策略**：默认 ease-out 200ms，减少动效降级为 0.01ms（a11y）

## ⚠️ 注意

- 改 token 前必先确认影响面（grep `var(--accent)` 全仓计数）
- 新增 token 必须在此 README 加决策记录
- 旧 dashboard.html 内的 `:root` 块**待废弃**，新代码全部走 tokens.css